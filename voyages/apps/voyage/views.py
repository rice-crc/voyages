from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.db.models import Max, Min
from django.template import TemplateDoesNotExist, loader
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
import csv
import re
from .forms import *
from haystack.query import SearchQuerySet
from itertools import groupby
import globals
import bitly_api
import requests
import json

def get_page(request, chapternum, sectionnum, pagenum):
    """
    Voyage Understanding the Database part
    
    Display an html page corresponding to the chapter-section-page
    
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


def understanding_page(request, name):
    dictionary = {}

    if "methodology" in name:
        dictionary['pagepath'] = "voyage/" + name + ".html"
        dictionary['pagename'] = name
        dictionary['page'] = "voyage/methodology-generic.html"
        dictionary['title'] = "Methodology"
        m = re.match(r'[a-zA-Z]+-([0-9]+)', name)

        dictionary['right'] = ""
        for num, index in enumerate(globals.methodology_items):
            if index['number'] == int(m.group(1)):
                if num > 0:
                    dictionary['left'] = globals.methodology_items[num-1]
                else:
                    dictionary['left'] = ""
                if num != len(globals.methodology_items)-1:
                    dictionary['right'] = globals.methodology_items[num+1]
                else:
                    dictionary['right'] = ""
                break
    elif "variable-list" in name:
        dictionary['title'] = "Variable List"
        dictionary['var_list_stats'] = variable_list()
        dictionary['page'] = 'voyage/variable-list.html'
    else:
        page = "voyage/" + name + ".html"
        dictionary['page'] = 'voyage/' + name + ".html"
        dictionary['title'] = 'Guide'

    return render(request, 'voyage/understanding_base.html', dictionary)


@staff_member_required
def download_file(request):
    """
    This view serves uploading files, which will be in 
    the download section. It uses UploadFileForm to maintain
    information regarding uploaded files and call 
    handle_uploaded_file() to store files on the disk.
    This view is available only for admin users.
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

def create_query_dict(query):
    query_dict = {}
    return query_dict

def create_query_from_url(request):
    return request

def create_form_from_query(query):
    return query

def create_query_from_request(request):
#    search_vars = request.POST.getlist('list-input-params')
#    query = create_query_dict(request, search_vars)
#    query['list-input-params'] = search_vars
#    query['to_year'] = request.POST.get('frame_to_year')
#    query['from_year'] = request.POST.get('frame_from_year')
    
    
    #print to_year
    #print from_year
    #print search_vars
    return None

def create_query_forms():
    """
    Uses the list of variables in globals.py and creates a form
    for each of them that is either a basic or a general variable
    Returns a list of dictionaries containing the var_name, var_full_name, form
    """
    print "Creating Query Forms"
    voyage_span_first_year, voyage_span_last_year = calculate_maxmin_years()
    form_list = []
    # for all basic and/or general variables
    for var in [x for x in globals.var_dict if x['is_general'] or x['is_basic']]:
        varname = var['var_name']
        if varname in globals.list_text_fields:
            form = SimpleTextForm(prefix=varname)
        elif varname in globals.list_select_fields:
            choices = getChoices(varname)
            form = SimpleSelectSearchForm(prefix=varname)
            form.fields['choice_field'].choices = choices
        elif varname in globals.list_numeric_fields:
            form = SimpleNumericSearchForm(initial={'options': '4'}, prefix=varname)
        elif varname in globals.list_date_fields:
            form = SimpleDateSearchForm(initial={'options': '1',
                                                 'from_year': voyage_span_first_year,
                                                 'to_year': voyage_span_last_year},
                                        prefix=varname)
        elif varname in globals.list_place_fields:
            choices = getNestedListPlaces(varname, var['choices'])
            form = SimplePlaceSearchForm(prefix=varname)
            form.fields['choice_field'].choices = choices
        elif varname in globals.list_boolean_fields:
            form = SimpleSelectBooleanForm(prefix=varname)
        else:
            print "WARNING: variable not in any form type lists: %s" % varname
            pass
        form.fields['var_name_field'].initial = varname
        elem = {}
        elem['var_name'] = varname
        elem['var_full_name'] = var['var_full_name']
        elem['form'] = form
        form_list.append(elem)
    return form_list

def retrieve_post_search_forms(post):
    """
    Retrieves the forms in the post and returns a list of dictionaries with var_name, var_full_name, and form
    """
    print "Retrieving Query Forms from POST"
    form_list = []
    # for all basic and/or general variables
    for var in [x for x in globals.var_dict if x['is_general'] or x['is_basic']]:
        varname = var['var_name']
        if varname in globals.list_text_fields:
            form = SimpleTextForm(post, prefix=varname)
        elif varname in globals.list_select_fields:
            form = SimpleSelectSearchForm(data=post, prefix=varname)
            form.fields['choice_field'].choices = getChoices(varname)
        elif varname in globals.list_numeric_fields:
            form = SimpleNumericSearchForm(post, prefix=varname)
        elif varname in globals.list_date_fields:
            form = SimpleDateSearchForm(post, prefix=varname)
        elif varname in globals.list_boolean_fields:
            form = SimpleSelectBooleanForm(post, prefix=varname)
        elif varname in globals.list_place_fields:
            form = SimplePlaceSearchForm(post, prefix=varname)
            choices = getNestedListPlaces(varname, var['choices'])
            form.fields['choice_field'].choices = choices
            print ""

        form_list.append({'var_name': varname,
                          'var_full_name': var['var_full_name'],
                          'form': form})
    return form_list


def create_var_dict(query_forms, time_frame_form):
    """
    query_forms: list of dictionaries with var_name and form (also probably var_full_name, but I don't think I need to count on that)
    returns a dictionary of var names and values for that var
    """
    # Creates a query dict based on all the restrictions the user has made
    var_list = {}
    # Year Time Frame Search
    if time_frame_form.is_valid():
        var_list['time_span_var_imp_arrival_at_port_of_dis'] = {'frame_from_year': time_frame_form.cleaned_data['frame_from_year'],
                                                                'frame_to_year': time_frame_form.cleaned_data['frame_to_year']}
    for qryform in [x for x in query_forms if x['form'].is_valid() and x['form'].is_form_shown()]:
        #qform = next((l for l in query_forms if l['varname'] == search_var), None)
        varname = qryform['var_name']
        form = qryform['form']
        if varname in globals.list_text_fields:
            var_list[varname] = {'text_search': form.cleaned_data['text_search']}
        elif varname in globals.list_select_fields:
            # TODO: make sure this works. This is supposed to be a list
            var_list[varname] = {'choice_field': form.cleaned_data['choice_field']}
        elif varname in globals.list_numeric_fields:
            opt = form.cleaned_data['options']
            var_list[varname] = {'options': opt}
            if opt == '1': # Between
                var_list[varname]['lower_bound'] = form.cleaned_data['lower_bound']
                var_list[varname]['upper_bound'] = form.cleaned_data['upper_bound']
            elif opt == '2': # Less than or equal to
                var_list[varname]['threshold'] = form.cleaned_data['threshold']
            elif opt == '3': # Greater than or equal to
                var_list[varname]['threshold'] = form.cleaned_data['threshold']
            elif opt == '4': # Equal to
                var_list[varname]['threshold'] = form.cleaned_data['threshold']
        elif varname in globals.list_date_fields:
            opt = form.cleaned_data['options']
            var_list[varname] = {'option': opt}
            if opt == '1': # Between
                var_list[varname]['from_year'] = form.cleaned_data['from_year']
                var_list[varname]['from_month'] = form.cleaned_data['from_month']
                var_list[varname]['to_year'] = form.cleaned_data['to_year']
                var_list[varname]['to_month'] = form.cleaned_data['to_month']
            elif opt == '2': # Less than or equal to
                var_list[varname]['threshold_year'] = form.cleaned_data['threshold_year']
                var_list[varname]['threshold_month'] = form.cleaned_data['threshold_month']
            elif opt == '3': # Greater than or equal to
                var_list[varname]['threshold_year'] = form.cleaned_data['threshold_year']
                var_list[varname]['threshold_month'] = form.cleaned_data['threshold_month']
            elif opt == '4': # Equal to
                var_list[varname]['threshold_year'] = form.cleaned_data['threshold_year']
                var_list[varname]['threshold_month'] = form.cleaned_data['threshold_month']
        elif varname in globals.list_place_fields:
            # TODO: figure out how to coalesce the list when the region or broadregion is selected
            #places = request.POST.getlist(search_var + "_selected")
            var_list[varname] = {'choice_field': form.cleaned_data['choice_field']}
        elif varname in globals.list_boolean_fields:
            var_list[varname] = {'choice_field': form.cleaned_data['choice_field']}
    return var_list

def create_query_dict(var_list):
    """
    query_forms: list of dictionaries with var_name and form (also probably var_full_name, but I don't think I need to count on that)
    returns a tuple of query dict and a dictionary of variable names with the value(s) it has
    """
    # Creates a query dict based on all the restrictions the user has made
    query_dict = {}
    time_span_name = 'time_span_var_imp_arrival_at_port_of_dis'
    # Year Time Frame Search
    if time_span_name in var_list:
        query_dict['var_imp_arrival_at_port_of_dis__range'] = [var_list[time_span_name]['frame_from_year'],
                                                               var_list[time_span_name]['frame_to_year']]
    for varname in var_list:
        if varname in globals.list_text_fields:
            query_dict[varname + "__contains"] = var_list[varname]['text_search']
        elif varname in globals.list_select_fields:
            # TODO: this probably needs to be fixed
            query_dict[varname + "__in"] = var_list[varname]['choice_field']
        elif varname in globals.list_numeric_fields:
            opt = form.cleaned_data['options']
            if opt == '1': # Between
                query_dict[varname + "__range"] = [var_list[varname]['lower_bound'],
                                                   var_list[varname]['upper_bound']]
            elif opt == '2': # Less than or equal to
                query_dict[varname + "__lte"] = var_list[varname]['threshold']
            elif opt == '3': # Greater than or equal to
                query_dict[varname + "__gte"] = var_list[varname]['threshold']
            elif opt == '4': # Equal to
                query_dict[varname + "__exact"] = var_list[varname]['threshold']
        elif varname in globals.list_date_fields:
            opt = var_list[varname]['options']
            if opt == '1': # Between
                query_dict[varname + "__range"] = [
                    formatDate(var_list[varname]['from_year'],
                               var_list[varname]['from_month']),
                    formatDate(var_list[varname]['to_year'],
                               var_list[varname]['to_month'])]
            elif opt == '2': # Less than or equal to
                query_dict[varname + "__lte"] = \
                    formatDate(var_list[varname]['threshold_year'],
                               var_list[varname]['theshold_month'])
            elif opt == '3': # Greater than or equal to
                query_dict[varname + "__gte"] = \
                    formatDate(var_list[varname]['threshold_year'],
                               var_list[varname]['theshold_month'])
            elif opt == '4': # Equal to
                query_dict[varname + "__exact"] = \
                    formatDate(var_list[varname]['threshold_year'],
                               var_list[varname]['theshold_month'])
        elif varname in globals.list_place_fields:
            # TODO: figure out how to coalesce the list when the region or broadregion is selected
            #places = request.POST.getlist(search_var + "_selected")
            query_dict[varname + "__in"] = var_list[varname]['choice_field']
        elif varname in globals.list_boolean_fields:
            query_dict[varname + "__in"] = var_list[varname]['choice_field']
    return query_dict

def search(request):
    """
    Handles the Search the Database part
    """
    no_result = False
    to_reset_form = False
    url_to_copy = ""
    query_dict = {}
    result_data = {}
    search_forms = []
    tab = 'result'
    result_data['summary_statistics_columns'] = globals.summary_statistics_columns
    form_list = []
    voyage_span_first_year, voyage_span_last_year = calculate_maxmin_years()
    results = None
    time_frame_form = None
    results_per_page_form = None
    

    if request.method == "GET" or request.POST.get('submitVal') == 'reset':
        results_per_page_form = ResultsPerPageOptionForm()
        form_list = create_query_forms()
        results = SearchQuerySet().models(Voyage).order_by('var_voyage_id')
        time_frame_form = TimeFrameSpanSearchForm(initial={'frame_from_year': voyage_span_first_year,
                                                      'frame_to_year': voyage_span_last_year})
        results = SearchQuerySet().models(Voyage).order_by('var_voyage_id')
    elif request.method == "POST":
        results_per_page_form = ResultsPerPageOptionForm(request.POST)
        form_list = retrieve_post_search_forms(request.POST)
        time_frame_form = TimeFrameSpanSearchForm(request.POST)
        var_list = create_var_dict(form_list, time_frame_form)
        query_dict = create_query_dict(var_list)
        results = perform_search(query_dict, None)
        submitVal = request.POST.get('submitVal')
        if submitVal == 'configColumn':
            tab = 'config_column'
        elif submitVal == 'applyConfig':
            request.session['result_columns'] = get_new_visible_attrs(request.POST.getlist('configure_visibleAttributes'))
            tab = 'result'
        elif submitVal == 'cancelConfig':
            tab = 'result'
        elif submitVal == 'restoreConfig':
            request.session['result_columns'] = get_new_visible_attrs(globals.default_result_columns)
            tab = 'config_column'
        elif submitVal == 'tab_results':
            tab = 'result'
        elif submitVal == 'tab_statistics':
            tab = 'statistics'
            result_data['summary_statistics'] = retrieve_summary_stats(results)
        elif submitVal == 'tab_tables':
            tab = 'tables'
        elif submitVal == 'tab_graphs':
            tab = 'graphs'
        elif  submitVal == 'tab_timeline':
            tab = 'timeline'
        elif submitVal == 'tab_maps':
            tab = 'maps'

    if len(results) == 0:
        no_result = True
    # If there is no requested page number, serve 1
    if request.POST.get('desired_page') is None:
        current_page = 1
    else:
        current_page = request.POST.get('desired_page')
    results_per_page = 10
    if results_per_page_form.is_valid():
        results_per_page = results_per_page_form.cleaned_option()

    #TODO: refactor pagination
    # Paginate results to pages
    paginator = Paginator(results, results_per_page)
    pagins = paginator.page(int(current_page))

    # Prepare paginator ranges
    (paginator_range, pages_range) = prepare_paginator_variables(paginator, current_page, results_per_page)

    # Customize result page
    if not request.session.exists(request.session.session_key):
        request.session.create()

    # Set up the initial column of display
    if not 'result_columns' in request.session:
        request.session['result_columns'] = get_new_visible_attrs(globals.default_result_columns)

    return render(request, "voyage/search.html",
                  {'voyage_span_first_year': voyage_span_first_year,
                   'voyage_span_last_year': voyage_span_last_year,
                   'basic_variables': globals.basic_variables,
                   'general_variables': globals.general_variables,
                   'all_var_list': globals.var_dict,
                   'results': pagins,
                   'result_data': result_data,
                   'paginator_range': paginator_range,
                   'pages_range': pages_range,
                   'no_result': no_result,
                   'url_to_copy': url_to_copy,
                   'tab': tab,
                   'options_results_per_page_form': results_per_page_form,
                   'form_list': form_list,
                   'time_frame_search_form': time_frame_form})


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
    elif varname == 'var_rig_of_vessel':
        for rig in RigOfVessel.objects.all():
            choices.append((rig.label, rig.label))
    return choices


def getNestedListPlaces(varname, nested_places):#, place_visible=[], region_visible=[], area_visible=[], place_selected=[], region_selected=[], area_selected=[]):
    """
    Retrieve a nested list of places sorted by broad region (area) and then region
    :param varname:
    :return:
    """
    choices = []

    for area, regs in nested_places.items():
        area_content = []
        for reg, places in regs.items():
            reg_content = []
            for place in places:
                if place.place == "???":
                    continue
                # I don't think I need the selected logic here, but double check
                reg_content.append({'id': 'id_' + varname + '_2_' + str(place.pk),
                                    'text': place.place})
            area_content.append({'id': 'id_' + varname + '_1_' + str(reg.pk),
                                 'text': reg.region,
                                 'choices': reg_content})
        choices.append({'id': 'id_' + varname + '_0_' + str(area.pk),
                        'text': area.broad_region,
                        'choices': area_content})
    
    # Check if visible parameters have been passed, if so filter
    """if not place_visible:
        place_visible = Place.objects.all()
    else:
        place_visible = Place.objects.filter(place__in=place_visible)

    if not region_visible:
        region_visible = Region.objects.all()
    else:
        region_visible = Region.objects.filter(region__in=region_visible)

    if not area_visible:
        area_visible = BroadRegion.objects.all()
    else:
        area_visible = BroadRegion.objects.filter(broad_region__in=area_visible)
        

    for area in area_visible:
        area_content = []
        for reg in region_visible.filter(broad_region=area):
            reg_content = []
            for place in place_visible.filter(region=reg):
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
                            'choices': area_content})"""
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


def check_and_save_options_form(request, to_reset_form):
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


    # Reset form if necessary
    if to_reset_form:
        form = ResultsPerPageOptionForm()
        results_per_page = form.cleaned_option()
    else:
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

def shorten_search_url(request):
    response_data = {}
    url = shorten_url(request.GET['long_url'])
    response_data['url'] = url
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def shorten_url(long_url):
    """
    Function to shorten url using bitly service.

    :param long_url: Long url to shorten

    If bitly doesn't provide url or the bitly url doesn't work, then it will just return the long_url
    """
    try:
        con = bitly_api.Connection(access_token=settings.BITLY_OAUTH_TOKEN)
        url = con.shorten(long_url)['url'].encode('utf-8')
    except bitly_api.BitlyError:
        url = long_url
    else:
        try:
            # Python can't handle the redirect to the testvoyages url
            req = requests.get(url, allow_redirects=False)
            if not req.ok:
                url = long_url
        except:
            url = long_url
    return url

def encode_to_url(request, voyage_span_first_year, voyage_span_last_year, no_result, date_filters=[], qdict={}):
    """
    Function to encode dictionary into url to copy form.

    :param request: request to serve
    :param dict: dict contains search conditions
    
    If empty, returns default url
    """
    url = request.build_absolute_uri(reverse('voyage:search',)) + "?"
    session_dict = {}

    # If search has not performed, return default url
    if qdict == {}:
        url += "var_imp_voyage_began__range=1514|1866"

    else:
        for k, v in qdict.iteritems():
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
                if isinstance(v, (int, float)):
                    url += str(k) + "=" + str(v)
                else:
                    url += str(k) + "=" + str(v.encode('ascii', 'ignore'))

            # If variable is date, try to also store deselected months.
            """for i in date_filters:
                # There is deselected months
                if i['varname'] == var_name:
                    url += "|" + ",".join(i['deselected_months'])"""
            url += "&"

        # At the end, delete the last unnecessary underscore
        url = url[0:-1]
        session_dict['dict'] = qdict
        #session_dict['existing_form'] = session
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

    # Rebuild dictionary from GET data
    for k, v in request.GET.iteritems():
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

    # Rebuild left menu
    #date_filters, existing_form, voyage_span_first_year, voyage_span_last_year, no_result = create_menu_forms(dict)
    #request.session['time_span_form'] = TimeFrameSpanSearchForm(
    #            initial={'frame_from_year': voyage_span_first_year,
    #                     'frame_to_year': voyage_span_last_year})
    return dict, date_filters, existing_form, voyage_span_first_year, voyage_span_last_year, no_result


def create_menu_forms(dict):
    """
    Function to create forms.

    :param dict: dictionary with search options
    """
    """
    print "I SHOULDN'T GET HERE!!!!!"
    new_existing_form = []
    date_filters = []
    no_result = False

    for k, v in dict.iteritems():
        elem_dict = {}

        # e.g.: k = var_imp_voyage_began__range
        # var_name = var_imp_voyage_began

        var_name = k.split("__")[0]

        # imputed voyage began is special case
        if var_name == "var_imp_voyage_began":
            voyage_span_first_year = v[0]
            voyage_span_last_year = v[1]
            continue
        else:
            voyage_span_first_year, voyage_span_last_year = calculate_maxmin_years()

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
            # Get selected fields
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

            if var_name != "var_imp_principal_place_of_slave_purchase":
                choices = getNestedListPlaces(var_name, place_selected=v)
            else:
                choices = getNestedListPlaces(var_name, area_visible=globals.var_imp_principal_place_of_slave_purchase_fields, place_selected=v)

            elem_dict['varname_wrapper'] = "select_" + var_name
            elem_dict['choices'] = choices
            elem_dict['selected_choices'] = var_name + "_selected"
            elem_dict['selected_regs'] = var_name + "_selected_regs"
            elem_dict['selected_areas'] = var_name + "_selected_areas"

        elif var_type == "boolean":
             # Boolean field
            print "THIS IS VERY BAD!!!"
            [k for k, v in enumerate(SimpleSelectBooleanForm.BOOLEAN_CHOICES) if v[0] == v]
            form = SimpleSelectBooleanForm(auto_id=('id_' + var_name + "_%s"),
                                           initial={'choice_field': SimpleSelectBooleanForm.BOOLEAN_CHOICES[k]},
                                           prefix=var_name)
            elem_dict['form'] = form

        else:
            pass

        new_existing_form.append(elem_dict)

    return date_filters, new_existing_form, voyage_span_first_year, voyage_span_last_year, no_result
    """
    return None


def search_var_dict(var_name):
    for i in globals.var_dict:
        if i['var_name'] == var_name:
            return i


def perform_search(query_dict, date_filters):
    """
    Perform the actual query towards SOLR
    :param query_dict:
    :param date_filters:
    :return:
    """
    # Initially sort by voyage_id
    results = SearchQuerySet().filter(**query_dict).models(Voyage).order_by('var_voyage_id')
    # Date filters
    return date_filter_query(date_filters, results)


def date_filter_query(date_filters, results):
    """
    Further filter the results passed in by excluding those that have months in date_filtered list (deselected)
    :param date_filters:
    :param results:
    :return:
    """
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


def formatDate(year, month):
    """
    Format the passed year month to a YYYY,MM string
    :param year:
    :param month:
    :return:
    """
    return "%s,%s" % (str(year).zfill(4), str(month).zfill(2))


def get_new_visible_attrs(list_column_varnames):
    """
    :param list_column_varnames: a list of variable names (short_name)
    :return: a list of tuples containing short names and full names of variables from the passed parameter
    """
    result_columns = []
    for column in list_column_varnames:
        for item in globals.var_dict:
            if item['var_name'] == column:
                result_columns.append([item['var_name'], item['var_full_name']])
    return result_columns


def variable_list():
    """
    renders a list of variables and their statistics into Variable List web page
    :param request:
    :return:
    """
    var_list_stats = []

    grouped_list_vars = groupby(globals.general_variables, lambda x: x['var_category'])

    for key, group in grouped_list_vars:
        tmpGroup = []

        for elem in group:
            query = {}

            var_name = elem['var_name']
            if var_name == 'var_voyage_in_cd_rom':
                query[var_name + "__exact"] = True

            elif elem['var_type'] == 'numeric':
                query[var_name + "__gte"] = -1
            else:
                query[var_name + "__gte"] = ""

            elem['num_voyages'] = SearchQuerySet().models(Voyage).filter(**query).count()
            tmpGroup.append(elem)

        var_list_stats.append({"var_category": key, "variables": tmpGroup})

    return var_list_stats


def sources_list(request, category="documentary_sources", sort="short_ref"):
    """
    Creates list of sources of required category, sorted by 'sort'
    method.
    :param request: request to serve
    :param category: category of source list
    :param sort: sort type
    :return: render object
    """

    category_search = " ".join(category.split("_"))
    sources = SearchQuerySet().models(VoyageSources).filter(group_name__exact=category_search)
    divided_groups = []
    sorted_letters = False

    # Create dictionary with sources
    for i in sources:
        insert_source(divided_groups, category, i)

    # Additional sorting is needed for documentary_sources (by cities and countries)
    if category == "documentary_sources":
        # Count sources in each city (needed in template)
        for v in divided_groups:
            for city in v["cities_list"]:
                city_rows = 0
                for j in city["city_groups_dict"]:
                    city_rows += int(len(j['sources']) + 1)
                city["number_of_rows"] = city_rows

        # Sort dictionary and set even and odd marks in dictionary
        sorted_dict = sort_documentary_sources_dict(divided_groups, sort)
        set_even_odd_sources_dict(sorted_dict)

    else:
        # Another sorting by first letter is needed for some categories.
        if category in globals.letters_sorted_source_types:
            sorted_letters = True
            sorted_dict = sort_by_first_letter(divided_groups, sort)
        else:
            sorted_dict = sorted(divided_groups, key=lambda k: k[sort])

    return render(request, "voyage/voyage_sources.html",
                  {'results': sorted_dict,
                   'sort_method': sort,
                   'sorted_letters': sorted_letters,
                   'category': category})


def insert_source(dict, category, source):
    """
    Inserts source in appropriate place in dictionary
    :param dict: dictionary to place source in
    :param category: category of inserting source
    :param source: inserting source
    :return:
    """

    # If category is documentary_sources, full_ref has to be parsed
    # to get information about city, country and text of source
    # Otherwise, just append new item to directory
    if category == "documentary_sources":
        m = re.match(r"(<i>[^<]*</i>)[\s]{1}(\([^\)]*\))[\s]?([^\n]*)", source.full_ref)
    else:
        new_dict_item = {}
        new_dict_item["short_ref"] = source.short_ref
        new_dict_item["full_ref"] = source.full_ref
        dict.append(new_dict_item)
        return

    # If string has been parsed, get information,
    # Otherwise, it will be uncategorized item
    if m is not None:
        if category == "documentary_sources":
            group_name = m.group(1)
            (city, country) = extract_places(m.group(2))
            text = m.group(3)
        else:
            group_name = m.group(1)
    else:
        group_name = source.full_ref
        city = "uncategorized"
        country = "uncategorized"
        text = source.full_ref

    # Get cities in country
    cities_list = None
    for i in dict:
        if i["country"] == country:
            cities_list = i

    # If country item doesn't exist, create new one.
    if cities_list is None:
        cities_list = {}
        cities_list["country"] = country
        cities_list["cities_list"] = []
        dict.append(cities_list)

    # Try to find city in a list
    city_dict = None
    for i in cities_list["cities_list"]:
        if i["city_name"] == city:
            city_dict = i
            break

    # If nothing found, create a city in country item
    if city_dict is None:
        city_dict = {}
        city_dict["city_name"] = city
        city_dict["city_groups_dict"] = []
        cities_list["cities_list"].append(city_dict)

    # Try to find a group
    source_list = None
    for i in city_dict["city_groups_dict"]:
        if i["group_name"] == group_name:
            source_list = i["sources"]
            group_dict = i
            break

    # If nothing found, create new group
    if source_list is None:
        group_dict = {}
        group_dict["group_name"] = group_name
        group_dict["short_ref"] = source.short_ref
        group_dict["sources"] = []
        city_dict["city_groups_dict"].append(group_dict)
        source_list = group_dict["sources"]

    # If contains text, put on the list
    if text != "":
        # If city is uncategorized, it's been already created
        if city != "uncategorized":
            new_source = {}
            new_source["short_ref"] = source.short_ref
            new_source["full_ref"] = text
            if new_source["short_ref"] == group_dict["short_ref"]:
                group_dict["short_ref"] = ""
            source_list.append(new_source)


def sort_documentary_sources_dict(dict, sort):
    for country in dict:
        for city_dict in country["cities_list"]:
            for city_group_dict in city_dict["city_groups_dict"]:
                # print "Source = " + str(city_group_dict["sources"])
                if sort == "short_ref":
                    city_group_dict["sources"] = sorted(city_group_dict["sources"], key=lambda k: k['short_ref'])
                else:
                    city_group_dict["sources"] = sorted(city_group_dict["sources"], key=lambda k: k['full_ref'])

            city_dict["city_groups_dict"] = sorted(city_dict["city_groups_dict"], key=lambda k: k['group_name'])

        country["cities_list"] = sorted(country["cities_list"], key=lambda k: k['city_name'])

    sorted_dict = sorted(dict, key=lambda k: k['country'])
    return sorted_dict


def set_even_odd_sources_dict(dict):
    """
    Sets even and odd marks for template
    :param dict: dict with sources
    :return:
    """

    for country in dict:
        # Counter is reset every country
        counter = 0
        for city_dict in country["cities_list"]:
            for city_group_dict in city_dict["city_groups_dict"]:
                # Set mark for city_group
                if counter%2 == 0:
                    city_group_dict["mark"] = 0
                else:
                    city_group_dict["mark"] = 1
                counter += 1
                # Set mark for sources in group sources
                for source in city_group_dict["sources"]:
                    if counter%2 == 0:
                        source["mark"] = 0
                    else:
                        source["mark"] = 1
                    counter += 1


def sort_by_first_letter(dict, sort_method):
    """
    Sorts dictionary by first letter of source
    (ref type (short or full) depends on sort_method)
    :param dict: dict with sources
    :param sort_method: sort method
    :return: sorted dictionary by first letter
    """

    new_dict = []
    letters = []

    for i in dict:
        # Get first letter from source ref
        first_letter = get_first_letter (i[sort_method])

        # If there is no entry with this first_letter,
        # Create a new one
        if first_letter not in letters:
            letters.append(first_letter)
            new_item = {}
            new_item["letter"] = first_letter
            new_item["items"] = []
            new_dict.append(new_item)

        # Insert entry to dictionary
        for j in new_dict:
            if j["letter"] == first_letter:
                j["items"].append(i)
                break

    # Sort all items in letter element list
    for i in new_dict:
        i["items"] = sorted(i["items"], key=lambda k: k[sort_method])

    # Return sorted dict by letter
    return sorted(new_dict, key= lambda k: k["letter"])


def get_first_letter(string):
    """
    Gets first letter from string (a-zA-Z)
    :param string: string to get from
    :return: first letter from string
    """

    for j in string:
            if (j >= 'a' and j <= 'z') or (j>= 'A' and j <= 'Z'):
                return j.capitalize()


def extract_places(string):
    # Delete parentheses
    string = string[1:-1]

    places_list = string.split(", ")

    # Get city (and state eventually)
    if len(places_list) == 2:
        return places_list[0], places_list[1]
    else:
        return places_list[0] + ", " + places_list[1], places_list[2]


def download_results(request, page):
    """
    Renders a downloadable csv file
    page indicates the current page the user is on
    page = -1 indicates download all results
    :param request:
    :param page:
    :return:
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    try:
        query_dict = request.session['voyage_last_query']
        display_columns = request.session['result_columns']
    except KeyError:
        query_dict = None
        display_columns = get_new_visible_attrs(globals.default_result_columns)

    #writer = UnicodeWriter(response, quoting=csv.QUOTE_ALL, encoding="utf-8-sig")
    writer = csv.writer(response)

    if page == "-1":
        # Download all results
        if 'voyage_last_query' in request.session and request.session['voyage_last_query'] is not None\
                and request.session['voyage_last_query']:
            query_dict = request.session['voyage_last_query']
            if 'voyage_last_query_date_filters' in request.session\
                    and request.session['voyage_last_query_date_filters'] is not None:
                date_filters = request.session['voyage_last_query_date_filters']
            else:
                date_filters = []

            results = perform_search(query_dict, date_filters)

            if len(results) == 0:
                no_result = True
                results = []
        else:
            results = SearchQuerySet().models(Voyage).order_by('var_voyage_id')

    else:
        # Download current view
        results = request.session['voyage_current_result_page']

    # Writing query
    if query_dict is None:
    #    results = SearchQuerySet().models(Voyage).order_by('var_voyage_id')
        writer.writerow(['All records', ])
    else:
    #    results = SearchQuerySet().models(Voyage).filter(**query_dict)
    #    if request.session['voyage_last_query_date_filters']:
    #        results = date_filter_query(request.session['voyage_last_query_date_filters'], results)
        writer.writerow([extract_query_for_download(query_dict, []), ])

    tmpRow = []
    for column in globals.general_variables:
        tmpRow.append(column['spss_name'])
    writer.writerow(tmpRow)

    for item in results:
        tmpRow = []
        stored_fields = item.get_stored_fields()
        for column in [x['var_name'] for x in globals.general_variables]:
            data = stored_fields[column]
            if data is None:
                tmpRow.append("")
            elif isinstance(data, (int, long, float)):
                tmpRow.append(str(data))
            else:
                tmpRow.append(data.encode("utf-8"))
        writer.writerow(tmpRow)

    writer.writerow(["The number of total records: " + str(len(results))])

    return response


def csv_stats_download(request):
    """
    Renders a downloadable csv file of summary statistics
    :param request:
    :param page:
    :return:
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)
    if 'voyage_last_query' in request.session and request.session['voyage_last_query'] is not None\
            and request.session['voyage_last_query']:
        query_dict = request.session['voyage_last_query']
        if 'voyage_last_query_date_filters' in request.session\
                and request.session['voyage_last_query_date_filters'] is not None:
            date_filters = request.session['voyage_last_query_date_filters']
        else:
            date_filters = []

        results = perform_search(query_dict, date_filters)

        if len(results) == 0:
            no_result = True
            results = []
    else:
        results = SearchQuerySet().models(Voyage).order_by('var_voyage_id')

    # Write headers
    tmpRow = []
    for columnname in globals.summary_statistics_columns:
        tmpRow.append(columnname)
    writer.writerow(tmpRow)

    for tmpRow in retrieve_summary_stats(results):
        writer.writerow(tmpRow)
    return response

def get_spss_name(var_short_name):
    """
    Retrieves a variable spss name based on its django name
    :param var_short_name:
    :return:
    """
    for var in globals.var_dict:
        if var['var_name'] == var_short_name:
            return var['spss_name']
    return None


def retrieve_summary_stats(results):
    """
    Return a list of summary statistics
    :param results:
    :return:
    """
    tmp_list = []
    for item in globals.summary_statistics:
        tmp_row = [item['display_name'],]
        stats = results.stats(item['var_name']).stats_results()[item['var_name']]

        if item['has_total'] and stats:
            tmp_row.append(int(stats['sum']))
        else:
            tmp_row.append("")

        # Number of voyages
        if stats:
            tmp_row.append(stats['count'])
        else:
            tmp_row.append("")

        if stats:
            if item['is_percentage']:
                # Average
                tmp_row.append(str(round(stats['mean']*100, 1)) + "%")
                # Standard deviation
                tmp_row.append(str(round(stats['stddev']*100, 1)) + "%")
            else:
                tmp_row.append(round(stats['mean'], 1))
                tmp_row.append(round(stats['stddev'], 1))
        else:
            tmp_row.append("")
            tmp_row.append("")

        tmp_list.append(tmp_row)
    return tmp_list

def extract_query_for_download(query_dict, date_filter):
    """
    Return a more user-friendly format of the query string from query dictionary
    :param query_dict:
    :param date_filter:
    :return:
    """
    query_arr = []
    for key in query_dict.keys():
        query_str = ""
        split_arr = key.split('__')
        var_name_indexed = split_arr[0]
        query_str += get_spss_name(var_name_indexed)
        if split_arr[1] == 'lte':
            query_str += " <= "
        elif split_arr[1] == 'gte':
            query_str += " <= "
        elif split_arr[1] == 'contains':
            query_str += " contains "
        elif split_arr[1] == 'in':
            query_str += " in "
        elif split_arr[1] == 'range':
            query_str += " in range "

        if isinstance(query_dict[key], (int, float)):
            query_str += str(query_dict[key])
        elif isinstance(query_dict[key], (list, tuple)):
            for elem in query_dict[key]:
                if isinstance(elem, (int, float)):
                    typeElem = 'number'
                    break
                else:
                    typeElem = 'text'
                    break

            if typeElem == 'number':
                query_str += "(" + " to ".join(map(str, query_dict[key])) + ")"
            else:
                tmp_arr = []
                for elem in query_dict[key]:
                    tmp_arr.append(elem.encode('ascii', 'ignore'))
                query_str += "(" + " , ".join(tmp_arr) + ")"

            # Encode to sign
        else:
            query_str += str(query_dict[key].encode('ascii', 'ignore'))

        query_arr.append(query_str)

    return " AND ".join(query_arr)
