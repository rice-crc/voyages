from django.http import Http404, HttpResponseRedirect
from django.db.models import Max, Min
from django.template import TemplateDoesNotExist, loader, RequestContext
from django.shortcuts import render
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import iri_to_uri
from django.contrib.admin.views.decorators import staff_member_required
from os import listdir, stat
from stat import ST_SIZE, ST_MTIME
from hurry.filesize import size
from django.core.paginator import Paginator
import time
import types
from .forms import *
from haystack.query import SearchQuerySet
from itertools import groupby
import globals


def get_page(request, chapternum, sectionnum, pagenum):
    """
    Voyage Understanding the Database part
    
    Display an html page corresponding to the chapter-section-page passed in
    ** Context **
    ``RequestContext``
    
    ** Basic template that will be rendered **
    :template:`voyage/c01_s02_generic.html`
    
    Further content is rendered using the pagepath parameter 
    """
    # We might want to do some error checking for pagenum here. Even though 404 will be raised if needed
    pagepath = "voyage/c" + chapternum + "_s" + sectionnum + "_p" + pagenum + ".html"
    templatename = "voyage/c" + chapternum + "_s" + sectionnum + "_generic" + ".html"

    try:
        loader.get_template(pagepath)
        loader.get_template(templatename)
        return render(request, templatename, dictionary={"pagepath": pagepath})
    except TemplateDoesNotExist:
        raise Http404


@staff_member_required
def download_file(request):
    """
    This view serves uploading files, which will be in 
    the download section. It uses UploadFileForm to maintain
    information regarding uploaded files and call 
    handle_uploaded_file() to store files on the disk.
    This view is available only for admin users.
    :template:`voyage/upload.html`
    """
    templatename = 'voyage/upload.html'

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['downloadfile'])
            return HttpResponseRedirect('/admin/downloads')
    else:
        form = UploadFileForm()
    uploaded_files = listdir(settings.MEDIA_ROOT + '/download')
    uploaded_files_info =[]
    for f in uploaded_files:
        st = stat(settings.MEDIA_ROOT + '/download/' + f)
        uploaded_files_info.append({'name': f, 'size': size(st[ST_SIZE]),
                                    'date_mod': time.asctime(time.localtime(st[ST_MTIME]))})

    return render(request, templatename, {'form': form, 'uploaded_files': uploaded_files_info})


def handle_uploaded_file(f):
    """
    Function handles uploaded files by saving them
    by chunks in the MEDIA_ROOT/download directory
    """
    with open('%s/%s/%s' % (settings.MEDIA_ROOT, 'download', f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def search(request):
    """
    Handles the Search the Database part
    """
    no_result = False
    url_to_copy = ""
    query_dict = {}
    tab = ""

    # Check if saved url has been used
    if request.GET.values():
        query_dict, date_filters, request.session['existing_form'], voyage_span_first_year, voyage_span_last_year, no_result = decode_from_url(request)
        results = SearchQuerySet().filter(**query_dict).models(Voyage).order_by('var_voyage_id')

        # Check if dates filters have to be used
        if date_filters and no_result is not True:
            results = date_filter_query(date_filters, results)

        if len(results) == 0:
            no_result = True

    # Otherwise, process next
    else:

        date_filters = []

        voyage_span_first_year, voyage_span_last_year = calculate_maxmin_years()

        if not request.session.exists(request.session.session_key):
            request.session.create()

        # Set up the initial column of display
        try:
            if request.session['result_columns']:
                pass
        except KeyError:
            result_columns = []
            for column in globals.default_result_columns:
                for item in globals.var_dict:
                    if item['var_name'] == column:
                        result_columns.append([item['var_name'],
                                               item['var_full_name']])
            request.session['result_columns'] = result_columns


        # Try to retrieve results from session
        try:
            results = request.session['results_voyages']
        except KeyError:
            results = SearchQuerySet().models(Voyage).order_by('var_voyage_id')
            request.session['results_voyages'] = results

        if request.method == 'POST':

            # Handles what list of variables should be collapsed or expanded
            if request.POST.get("basic_list_expanded"):
                request.session["basic_list_contracted"] = True
            else:
                request.session["basic_list_contracted"] = None

            submitVal = request.POST.get('submitVal')

            # Update variable values
            list_search_vars = request.POST.getlist('list-input-params')
            existing_form = request.session['existing_form']
            new_existing_form = []

            # Time frame search
            frame_form = TimeFrameSpanSearchForm(request.POST)
            if frame_form.is_valid():
                request.session['time_span_form'] = frame_form

            for tmp_varname in list_search_vars:
                for cur_var in existing_form:
                    if tmp_varname == cur_var['varname']:
                        if tmp_varname in globals.list_text_fields:
                            cur_var['form'] = SimpleTextForm(request.POST, prefix=tmp_varname)

                        elif tmp_varname in globals.list_select_fields:
                            # Select box variables
                            oldChoices = cur_var['form'].fields['choice_field'].choices
                            cur_var['form'] = SimpleSelectSearchForm(oldChoices, request.POST, prefix=tmp_varname)
                        elif tmp_varname in globals.list_numeric_fields:
                            # Numeric variables
                            cur_var['form'] = SimpleNumericSearchForm(request.POST, prefix=tmp_varname)

                        elif tmp_varname in globals.list_date_fields:
                            # Numeric variables
                            cur_var['form'] = SimpleDateSearchForm(request.POST, prefix=tmp_varname)
                            cur_var['list_deselected'] = request.POST.getlist(tmp_varname + '_deselected_months')

                        elif tmp_varname in globals.list_place_fields:
                            place_selected = request.POST.getlist(tmp_varname + "_selected")
                            region_selected = request.POST.getlist(tmp_varname + "_selected_regs")
                            area_selected = request.POST.getlist(tmp_varname + "_selected_areas")
                            cur_var['choices'] = getNestedListPlaces(tmp_varname,
                                                                     place_selected, region_selected, area_selected)

                        elif tmp_varname in globals.list_boolean_fields:
                             # Boolean field
                            cur_var['form'] = SimpleSelectBooleanForm(request.POST, prefix=tmp_varname)
                        new_existing_form.append(cur_var)

            request.session['existing_form'] = new_existing_form

            if submitVal == 'add_var':

                results = SearchQuerySet().models(Voyage).order_by('var_voyage_id')
                # Add variables
                tmpElemDict = {}
                varname = request.POST.get('new_var_name')
                tmpElemDict['varname'] = request.POST.get('new_var_name')
                tmpElemDict['var_full_name'] = request.POST.get('new_var_fullname')
                tmpElemDict['input_field_name'] = "header_" + varname

                if varname in globals.list_text_fields:
                    # Plain text fields
                    form = SimpleTextForm(auto_id=('id_' + varname + "_%s"), prefix=varname)
                    tmpElemDict['form'] = form
                    tmpElemDict['type'] = 'plain_text'

                elif varname in globals.list_select_fields:
                    # Select box variables
                    choices = getChoices(varname)
                    form = SimpleSelectSearchForm(listChoices=choices,
                                                  auto_id=('id_' + varname + "_%s"), prefix=varname)

                    tmpElemDict['form'] = form
                    tmpElemDict['type'] = 'select'
                    tmpElemDict['varname_wrapper'] = "select_" + varname
                    tmpElemDict['choices'] = choices

                elif varname in globals.list_numeric_fields:
                    # Numeric variables
                    form = SimpleNumericSearchForm(auto_id=('id_' + varname + "_%s"),
                                                   initial={'options': '4'}, prefix=varname)
                    tmpElemDict['form'] = form
                    tmpElemDict['type'] = 'numeric'

                elif varname in globals.list_date_fields:
                    # Numeric variables
                    form = SimpleDateSearchForm(auto_id=('id_' + varname + "_%s"),
                                                initial={'options': '1',
                                                         'from_year': voyage_span_first_year,
                                                         'to_year': voyage_span_last_year},
                                                prefix=varname)
                    tmpElemDict['form'] = form
                    tmpElemDict['type'] = 'date'
                    tmpElemDict['list_months'] = globals.list_months
                    tmpElemDict['deselected_months'] = varname + '_deselected_months'
                    tmpElemDict['list_deselected'] = []

                elif varname in globals.list_place_fields:
                    choices = getNestedListPlaces(varname, [], [], [])

                    tmpElemDict['type'] = 'select_three_layers'
                    tmpElemDict['varname_wrapper'] = "select_" + varname
                    tmpElemDict['choices'] = choices
                    tmpElemDict['selected_choices'] = varname + "_selected"
                    tmpElemDict['selected_regs'] = varname + "_selected_regs"
                    tmpElemDict['selected_areas'] = varname + "_selected_areas"

                elif varname in globals.list_boolean_fields:
                     # Boolean field
                    form = SimpleSelectBooleanForm(auto_id=('id_' + varname + "_%s"), prefix=varname)
                    tmpElemDict['form'] = form
                    tmpElemDict['type'] = 'boolean'
                else:
                    pass
                request.session['existing_form'].append(tmpElemDict)

            elif submitVal == 'reset':
                # Reset the search page
                existing_form = []
                request.session['existing_form'] = existing_form
                results = SearchQuerySet().models(Voyage).order_by('var_voyage_id')
                request.session['results_voyages'] = results

                # Reset time_frame form as well
                voyage_span_first_year, voyage_span_last_year = calculate_maxmin_years()

                # Time frame search
                request.session['time_span_form'] = TimeFrameSpanSearchForm(
                initial={'frame_from_year': voyage_span_first_year,
                         'frame_to_year': voyage_span_last_year})

            elif submitVal == 'configColumn':
                # Configure columns in the result page
                tab = 'config_column'
                pass

            elif submitVal == 'search':
                list_search_vars = request.POST.getlist('list-input-params')

                new_existing_form = []

                # Time frame search
                query_dict['var_imp_voyage_began__range'] = [request.session['time_span_form'].cleaned_data['frame_from_year'],
                                                             request.session['time_span_form'].cleaned_data['frame_to_year']]

                for tmp_varname in list_search_vars:
                    for cur_var in request.session['existing_form']:

                        if tmp_varname == cur_var['varname']:
                            if tmp_varname in globals.list_text_fields:
                                cur_var['form'] = SimpleTextForm(request.POST, prefix=tmp_varname)
                                if cur_var['form'].is_valid():
                                    query_dict[tmp_varname + "__contains"] = cur_var['form'].cleaned_data['text_search']

                            elif tmp_varname in globals.list_select_fields:
                                # Select box variables
                                oldChoices = cur_var['form'].fields['choice_field'].choices
                                cur_var['form'] = SimpleSelectSearchForm(oldChoices, request.POST, prefix=tmp_varname)
                                if cur_var['form'].is_valid():
                                    query_dict[tmp_varname + "__in"] = cur_var['form'].cleaned_data['choice_field']

                            elif tmp_varname in globals.list_numeric_fields:
                                # Numeric variables
                                cur_var['form'] = SimpleNumericSearchForm(request.POST, prefix=tmp_varname)
                                if cur_var['form'].is_valid():
                                    opt = cur_var['form'].cleaned_data['options']
                                    if opt == '1':  # Between
                                        query_dict[tmp_varname + "__range"] = [cur_var['form'].cleaned_data['lower_bound'],
                                                                               cur_var['form'].cleaned_data['upper_bound']]
                                    elif opt == '2':  # Less or equal to
                                        query_dict[tmp_varname + "__lte"] = cur_var['form'].cleaned_data['threshold']
                                    elif opt == '3':  # Greater or equal to
                                        query_dict[tmp_varname + "__gte"] = cur_var['form'].cleaned_data['threshold']
                                    elif opt == '4':  # Is equal
                                        query_dict[tmp_varname + "__exact"] = cur_var['form'].cleaned_data['threshold']
                                    else:
                                        pass

                            elif tmp_varname in globals.list_date_fields:
                            # Currently in progress
                            # To be updated
                                cur_var['form'] = SimpleDateSearchForm(request.POST, prefix=tmp_varname)
                                if cur_var['form'].is_valid():
                                    opt = cur_var['form'].cleaned_data['options']
                                    if opt == '1':  # Between
                                        query_dict[tmp_varname + "__range"] = [
                                            formatDate(cur_var['form'].cleaned_data['from_year'],
                                                       cur_var['form'].cleaned_data['from_month']),
                                            formatDate(cur_var['form'].cleaned_data['to_year'],
                                                       cur_var['form'].cleaned_data['to_month'])]

                                    elif opt == '2':  # Less or equal to
                                        query_dict[tmp_varname + "__lte"] = \
                                            formatDate(cur_var['form'].cleaned_data['threshold_year'],
                                                       cur_var['form'].cleaned_data['threshold_month'])
                                    elif opt == '3':  # Greater or equal to
                                        query_dict[tmp_varname + "__gte"] = \
                                            formatDate(cur_var['form'].cleaned_data['threshold_year'],
                                                       cur_var['form'].cleaned_data['threshold_month'])
                                    elif opt == '4':  # Is equal
                                        query_dict[tmp_varname + "__exact"] = \
                                            formatDate(cur_var['form'].cleaned_data['threshold_year'],
                                                       cur_var['form'].cleaned_data['threshold_month'])
                                    else:
                                        pass

                                    deselected_months = request.POST.getlist(tmp_varname + "_deselected_months")

                                    if 0 < len(deselected_months) < len(globals.list_months):
                                        date_filters.append({'varname': tmp_varname, 'deselected_months': deselected_months})
                                    elif len(deselected_months) == len(globals.list_months):
                                        no_result = True
                                    else:  # user selected all 12 months
                                        pass

                            elif tmp_varname in globals.list_place_fields:
                                a = request.POST.getlist(tmp_varname + "_selected")
                                query_dict[tmp_varname + "__in"] = request.POST.getlist(tmp_varname + "_selected")

                            elif tmp_varname in globals.list_boolean_fields:
                                 # Boolean field
                                cur_var['form'] = SimpleSelectBooleanForm(request.POST, prefix=tmp_varname)
                                if cur_var['form'].is_valid():
                                    query_dict[tmp_varname + "__in"] = cur_var['form'].cleaned_data['choice_field']

                            new_existing_form.append(cur_var)

                request.session['existing_form'] = new_existing_form

                # Initially sort by voyage_id
                results = SearchQuerySet().filter(**query_dict).models(Voyage).order_by('var_voyage_id')

                # Date filters

                results = date_filter_query(date_filters, results)

                if len(results) == 0:
                    no_result = True
                    results = []
                request.session['results_voyages'] = results

        elif request.method == 'GET':
            # Create a new form
            existing_form = []
            request.session['existing_form'] = existing_form

            # Get all results (get means 'reset')
            results = SearchQuerySet().models(Voyage)

            request.session['time_span_form'] = TimeFrameSpanSearchForm(
                initial={'frame_from_year': voyage_span_first_year,
                         'frame_to_year': voyage_span_last_year})



        # Encode url to url_to_copy form (for user)
        url_to_copy = encode_to_url(request, request.session['existing_form'], voyage_span_first_year, voyage_span_last_year, no_result, date_filters,  query_dict)

    form, results_per_page = check_and_save_options_form(request)

    if len(results) == 0:
        no_result = True

    if request.POST.get('desired_page') is None:
        current_page = 1
    else:
        current_page = request.POST.get('desired_page')

    paginator = Paginator(results, results_per_page)
    pagins = paginator.page(int(current_page))

    form, results_per_page = check_and_save_options_form(request)

    # Prepare paginator ranges
    (paginator_range, pages_range) = prepare_paginator_variables(paginator, current_page, results_per_page)

    # Customize result page
    if not request.session.exists(request.session.session_key):
        request.session.create()

    return render(request, "voyage/search.html",
                  {'voyage_span_first_year': voyage_span_first_year,
                   'voyage_span_last_year': voyage_span_last_year,
                   'basic_variables': globals.basic_variables,
                   'general_variables': globals.var_dict,
                   'results': pagins,
                   'paginator_range': paginator_range,
                   'pages_range': pages_range,
                   'no_result': no_result,
                   'url_to_copy': url_to_copy,
                   'tab': tab,
                   'options_results_per_page_form': form})


def getChoices(varname):
    """
    Retrieve a list of two-tuple items for select boxes depending on the model
    :param varname variable name:
    :return: nested list of choices/options for that variable
    """
    choices = []
    if varname in ['var_nationality']:
        for nation in Nationality.objects.all():
            if "/" in nation.label or "Other (specify in note)" in nation.label:
                continue
            choices.append((nation.label, nation.label))
    elif varname in ['var_imputed_nationality']:
        for nation in Nationality.objects.all():
            # imputed flags
            if nation.label in globals.list_imputed_nationality_values:
                choices.append((nation.label, nation.label))
    elif varname in ['var_outcome_voyage']:
        for outcome in ParticularOutcome.objects.all():
            choices.append((outcome.label, outcome.label))
    elif varname in ['var_outcome_slaves']:
        for outcome in SlavesOutcome.objects.all():
            choices.append((outcome.label, outcome.label))
    elif varname in ['var_outcome_owner']:
        for outcome in OwnerOutcome.objects.all():
            choices.append((outcome.label, outcome.label))
    elif varname in ['var_resistance']:
        for outcome in Resistance.objects.all():
            choices.append((outcome.label, outcome.label))
    elif varname in ['var_outcome_ship_captured']:
        for outcome in VesselCapturedOutcome.objects.all():
            choices.append((outcome.label, outcome.label))
    return choices


def getNestedListPlaces(varname, place_selected, region_selected, area_selected):
    """
    Retrieve a nested list of places sorted by broad region (area) and then region
    :param varname:
    :return:
    """
    choices = []
    for area in BroadRegion.objects.all():
        area_content = []
        for reg in Region.objects.filter(broad_region=area):
            reg_content = []
            for place in Place.objects.filter(region=reg):
                if place.place == "???":
                    continue
                if place.place in place_selected:
                    reg_content.append({'id': 'id_' + varname + '_2_' + str(place.pk),
                                        'text': place.place, 'selected': True})

                else:
                    reg_content.append({'id': 'id_' + varname + '_2_' + str(place.pk),
                                        'text': place.place})
            if reg.region in region_selected:
                area_content.append({'id': 'id_' + varname + '_1_' + str(reg.pk),
                                    'text': reg.region,
                                    'choices': reg_content,
                                    'selected': True})
            else:
                area_content.append({'id': 'id_' + varname + '_1_' + str(reg.pk),
                                    'text': reg.region,
                                    'choices': reg_content})
        if area.broad_region in area_selected:
            choices.append({'id': 'id_' + varname + '_0_' + str(area.pk),
                            'text': area.broad_region,
                            'choices': area_content,
                            'selected' : True})
        else:
            choices.append({'id': 'id_' + varname + '_0_' + str(area.pk),
                            'text': area.broad_region,
                            'choices': area_content})
    return choices


def prepare_paginator_variables(paginator, current_page, results_per_page):
    """
    Function prepares set of paginator links for template.

    :param paginator: Paginator which links are calculating for
    :param current_page: Current page serves on search site
    """

    paginator_range = []
    pages_range = []
    last_saved_index = 0

    # Prepare page numbers
    for i in globals.paginator_range_factors:

        # Get last inserted index
        try:
            last = paginator_range[-1]
        except IndexError:
            last = 0

        # If page number would be greater than max page number,
        # return, since this is the end of page paginator ranges
        if last_saved_index >= len(paginator.object_list):
            continue
        # Index can't be less than '1'
        if int(current_page) + i < 1:
            paginator_range.append(last+1)
            last_saved_index = ((last+1) * results_per_page)
        else:
            # Index has to be always +1 from the last one
            # (e.g. current_page is '1')
            if int(current_page) + i <= last:
                paginator_range.append(last+1)
                last_saved_index = ((last+1) * results_per_page)
            # Otherwise, just increment current_page
            else:
                paginator_range.append(int(current_page) + i)
                last_saved_index = ((int(current_page)+i) * results_per_page)

    # Prepare results range
    pages_range.append(int(current_page)*results_per_page - results_per_page + 1)
    if (int(current_page)*results_per_page) > len(paginator.object_list):
        pages_range.append(len(paginator.object_list))
    else:
        pages_range.append(int(current_page)*results_per_page)

    return paginator_range, pages_range


def check_and_save_options_form(request):
    """
    Function checks and replaces if necessary
    form (results per page) form in the session.

    :param request: Request to serve
    """

    # Try to get a form from session
    try:
        form_in_session = request.session['results_per_page_form']
    except KeyError:
        form_in_session = None

    if request.method == "POST":
        form = ResultsPerPageOptionForm(request.POST)

        if form.is_valid():
            results_per_page = form.cleaned_option()
        else:
            form = form_in_session
            if form is not None:
                form.is_valid()
                results_per_page = form.cleaned_option()
            else:
                form = ResultsPerPageOptionForm()
                results_per_page = form.cleaned_option()

        if form_in_session != form:
            request.session['results_per_page_form'] = form
    else:
        if form_in_session is not None:
            form = request.session['results_per_page_form']
            form.is_valid()
            results_per_page = form.cleaned_option()
        else:
            form = ResultsPerPageOptionForm()
            results_per_page = form.cleaned_option()

    return form, results_per_page


def encode_to_url(request, session, voyage_span_first_year, voyage_span_last_year, no_result, date_filters=[], dict={}):
    """
    Function to encode dictionary into url to copy form.

    :param request: request to serve
    :param dict: dict contains search conditions
    If empty, returns default url
    """
    url = request.build_absolute_uri(reverse('voyage:search',)) + "?"
    session_dict = {}

    # If search has not performed, return default url
    if dict == {}:
        url += "var_imp_voyage_began__range=1514|1866"

    else:
        for k, v in dict.iteritems():
            var_name = k.split("__")[0]

            # If this is the __range component.
            if "__range" in k:
                url += str(k) + "=" + str(v[0]) + "|" + str(v[1])
            # If list, split and join with underscores
            elif isinstance(v, types.ListType):
                url += str(k) + "="
                for j in v:
                    url += "_".join(j.split(" ")) + "|"
                url = url[0:-1]
            else:
                url += str(k) + "=" + str(v)

            # If variable is date, try to also store deselected months.
            for i in date_filters:
                # There is deselected months
                if i['varname'] == var_name:
                    url += "|" + ",".join(i['deselected_months'])
            url += "&"

        # At the end, delete the last unnecessary underscore
        url = url[0:-1]
        session_dict['dict'] = dict
        session_dict['existing_form'] = session
        session_dict['date_filters'] = date_filters
        session_dict['no_result'] = no_result
        session_dict['voyage_span_first_year'] = voyage_span_first_year
        session_dict['voyage_span_last_year'] = voyage_span_last_year

    # Store dict in session and return url
    safe_url = url.encode('ascii', 'ignore')
    url_key = iri_to_uri("/" + str("/".join(safe_url.split("/")[3:])))

    request.session[url_key] = session_dict
    return url


def decode_from_url(request):
    """
    Function to decode url to dict and forms.

    :param request: request to serve

    """

    # Check if this path is in session
    try:
        session_dict = request.session[request.get_full_path()]
        return session_dict['dict'], session_dict['date_filters'], \
               session_dict['existing_form'], session_dict['voyage_span_first_year'], \
                session_dict['voyage_span_last_year'], session_dict['no_result']
    except KeyError:
        pass

    dict = {}

    for k, v in request.GET.iteritems():
        # if "__range" in k:
        #     dict[k] = []
        #     dict[k].append(v.split("|")[0])
        #     dict[k].append(v.split("|")[1])
        #
        # elif isinstance(v, types.ListType):
        #     dict[k] = []
        #     for i in v.split("|"):
        #         dict[k].append(i)
        if len(v.split("|")) > 1:
            dict[k] = []
            for i in v.split("|"):
                dict[k].append(i)
        else:
            dict[k] = v

        # Deselected months
        if "__range" in k and len(v.split("|")) == 3:
            dict[k].append(v.split("|")[2])
        elif isinstance(v, types.ListType) and len(v.split("|") == 2):
            dict[k].append(v.split("|")[1])

    date_filters, existing_form, voyage_span_first_year, voyage_span_last_year, no_result = create_menu_forms(dict)
    request.session['time_span_form'] = TimeFrameSpanSearchForm(
                initial={'frame_from_year': voyage_span_first_year,
                         'frame_to_year': voyage_span_last_year})
    return dict, date_filters, existing_form, voyage_span_first_year, voyage_span_last_year, no_result


def create_menu_forms(dict):
    """
    Function to create forms.
    """

    new_existing_form = []
    date_filters = []
    no_result = False

    for k, v in dict.iteritems():
        elem_dict = {}

        # e.g.: k = var_imp_voyage_began__range
        # var_name = var_imp_voyage_began

        var_name = k.split("__")[0]

        if var_name == "var_imp_voyage_began":
            voyage_span_first_year = v[0]
            voyage_span_last_year = v[1]
            continue

        var = search_var_dict(var_name)
        var_type = var['var_type']

        elem_dict['varname'] = var['var_name']
        elem_dict['type'] = var['var_type']
        elem_dict['input_field_name'] = "header_" + var_name
        elem_dict['var_full_name'] = var['var_full_name']

        if var_type == "plain_text":
            # Plain text fields
            form = SimpleTextForm(auto_id=('id_' + var_name + "_%s"), initial={'text_search': v}, prefix=var_name)
            elem_dict['form'] = form

        elif var_type == "select":
            # Select box variables
            choices_list = []
            choices = getChoices(var_name)
            for select_field in v.split("|"):
                choices_list.append(" ".join(select_field.split("_")))

            form = SimpleSelectSearchForm(listChoices=choices,
                                          auto_id=('id_' + var_name + "_%s"),
                                          initial={'choice_field': choices_list},
                                          prefix=var_name)

            elem_dict['form'] = form
            elem_dict['varname_wrapper'] = "select_" + var_name
            elem_dict['choices'] = choices

        elif var_type == "numeric":
            # Numeric variables
            word_option = var_name = k.split("__")[1]
            if word_option == "range":
                option = 1
                lower_bound = v[0]
                upper_bound = v[1]
            elif word_option == "lte":
                option = 2
            elif word_option == "gte":
                option = 3
            elif word_option == "exact":
                option = 4

            if option == 1:
                form = SimpleNumericSearchForm(auto_id=('id_' + var_name + "_%s"),
                                               initial={'options': option,
                                                        'lower_bound': lower_bound,
                                                        'upper_bound': upper_bound},
                                               prefix=var_name)
            else:
                form = SimpleNumericSearchForm(auto_id=('id_' + var_name + "_%s"),
                                               initial={'options': option,
                                                        'threshold': v},
                                               prefix=var_name)
            elem_dict['form'] = form

        elif var_type == "date":
            # Date variables

            deselected_months = []
            word_option = k.split("__")[1]
            if word_option == "range":
                option = 1
                from_month = v[0].split(",")[1]
                from_year = v[0].split(",")[0]
                to_month = v[1].split(",")[1]
                to_year = v[1].split(",")[0]
                if len(v) == 3:
                    for month in v[2].split(","):
                        deselected_months.append(month)

            else:
                if len(v) == 1:
                    threshold_month = v.split(",")[1]
                    threshold_year = v.split(",")[0]
                else:
                    threshold_month = v[0].split(",")[1]
                    threshold_year = v[0].split(",")[0]
                    for month in v[1].split(","):
                        deselected_months.append(month)

                if word_option == "lte":
                    option = 2
                elif word_option == "gte":
                    option = 3
                elif word_option == "exact":
                    option = 4

            if word_option == "range":
                form = SimpleDateSearchForm(auto_id=('id_' + var_name + "_%s"),
                                               initial={'options': option,
                                               'from_month': from_month,
                                               'from_year': from_year,
                                               'to_month': to_month,
                                               'to_year': to_year},
                                               prefix=var_name)
            else:
                form = SimpleDateSearchForm(auto_id=('id_' + var_name + "_%s"),
                                               initial={'options': option,
                                                        'threshold_month': threshold_month,
                                                        'threshold_year': threshold_year},
                                               prefix=var_name)

            elem_dict['list_months'] = globals.list_months
            elem_dict['form'] = form

            elem_dict['list_deselected'] = deselected_months
            elem_dict['deselected_months'] = var_name + '_deselected_months'

            if 0 < len(deselected_months) < len(globals.list_months):
                date_filters.append({'varname': var_name, 'deselected_months': deselected_months})
            elif len(deselected_months) == len(globals.list_months):
                no_result = True

        elif var_type in "select_three_layers":
            # Get places

            choices = getNestedListPlaces(var_name, v, [], [])

            elem_dict['varname_wrapper'] = "select_" + var_name
            elem_dict['choices'] = choices
            elem_dict['selected_choices'] = var_name + "_selected"
            elem_dict['selected_regs'] = var_name + "_selected_regs"
            elem_dict['selected_areas'] = var_name + "_selected_areas"

        elif var_type == "boolean":
             # Boolean field

            [k for k, v in enumerate(SimpleSelectBooleanForm.BOOLEAN_CHOICES) if v[0] == v]
            form = SimpleSelectBooleanForm(auto_id=('id_' + var_name + "_%s"),
                                           initial={'choice_field': SimpleSelectBooleanForm.BOOLEAN_CHOICES[k]},
                                           prefix=var_name)
            elem_dict['form'] = form

        else:
            pass

        new_existing_form.append(elem_dict)

    return date_filters, new_existing_form, voyage_span_first_year, voyage_span_last_year, no_result


def search_var_dict(var_name):
    for i in globals.var_dict:
        if i['var_name'] == var_name:
            return i


def date_filter_query(date_filters, results):
    if date_filters:
        for var_filter in date_filters:
            l_months = []
            tmp_query = dict()
            for month in var_filter['deselected_months']:
                l_months.append("-" + month + "-")

            tmp_query[var_filter['varname'] + "__in"] = l_months
            results = results.exclude(**tmp_query)

    return results


def calculate_maxmin_years():
    if VoyageDates.objects.count() > 1:
        voyage_span_first_year = VoyageDates.objects.all().aggregate(Min('imp_voyage_began'))['imp_voyage_began__min'][2:]
        voyage_span_last_year = VoyageDates.objects.all().aggregate(Max('imp_voyage_began'))['imp_voyage_began__max'][2:]
    else:
        voyage_span_first_year = 1514
        voyage_span_last_year = 1866

    return voyage_span_first_year, voyage_span_last_year


def getMonth(value):
    return value.split(",")[0]


def getDay(value):
    return value.split(",")[1]


def getYear(value):
    return value.split(",")[2]


def formatDate(year, month):
    """
    Format the passed year month to a YYYY,MM string
    :param year:
    :param month:
    :return:
    """
    return "%s,%s" % (str(year).zfill(4), str(month).zfill(2))


def variable_list(request):
    """
    renders a list of variables and their statistics into Variable List web page
    :param request:
    :return:
    """
    var_list_stats = []

    grouped_list_vars = groupby(globals.var_dict, lambda x: x['var_category'])

    for key, group in grouped_list_vars:
        tmpGroup = []

        for elem in group:
            query = {}

            var_name = elem['var_name']
            if var_name == 'var_voyage_in_cd_rom':
                query[var_name + "__exact"] = True

            ### TO BE DELETED (after updating solr schema)
            elif var_name == "var_num_slaves_intended_first_port" or var_name == "var_num_slaves_disembark_second_place":
                continue

            elif elem['var_type'] == 'numeric':
                query[var_name + "__gte"] = -1
            else:
                query[var_name + "__gte"] = ""

            elem['num_voyages'] = SearchQuerySet().models(Voyage).filter(**query).count()
            tmpGroup.append(elem)

        var_list_stats.append({"var_category": key, "variables": tmpGroup})

    return render(request, "voyage/variable_list.html", {'var_list_stats': var_list_stats })
