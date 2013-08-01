from django.http import Http404, HttpResponseRedirect
from django.db.models import Max, Min
from django.template import TemplateDoesNotExist, loader, RequestContext
from django.shortcuts import render
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from os import listdir, stat
from stat import ST_SIZE, ST_MTIME
from hurry.filesize import size
from django.core.paginator import Paginator
import time
from .forms import *
from haystack.query import SearchQuerySet

list_text_fields = ['var_ship_name',
                    'var_owner',
                    'var_captain',
                    'var_sources']
list_select_fields = ['var_nationality',
                      'var_imputed_nationality',
                      'var_outcome_voyage',
                      'var_outcome_slaves',
                      'var_outcome_owner',
                      'var_resistance',
                      'var_outcome_ship_captured',
                      ]
list_numeric_fields = ['var_voyage_id',
                       'var_year_of_construction',
                       'var_registered_year',
                       'var_rig_of_vessel',
                       'var_guns_mounted',

                        # Voyage dates variables
                       'var_imp_arrival_at_port_of_dis', # Year arrived with salves
                       'var_imp_length_home_to_disembark',
                       'var_length_middle_passage_days',

                       'var_crew_voyage_outset',
                       'var_crew_first_landing',
                       'var_crew_died_complete_voyage',

                       'var_num_slaves_carried_first_port',
                       'var_num_slaves_carried_second_port',
                       'var_num_slaves_carried_third_port',
                       'var_total_num_slaves_purchased',
                       'var_imp_total_num_slaves_purchased',
                       'var_total_num_slaves_arr_first_port_embark',
                       'var_num_slaves_disembark_first_place',
                       'var_second_place_of_landing',
                       'var_num_slaves_disembark_third_place',
                       'var_imp_total_slaves_disembarked',

                       # Possible change the below to decimal fields
                       'var_tonnage',
                       'var_tonnage_mod',

                       'var_imputed_percentage_men',
                       'var_imputed_percentage_women',
                       'var_imputed_percentage_boys',
                       'var_imputed_percentage_girls',
                       'var_imputed_percentage_female',
                       'var_imputed_percentage_male',
                       'var_imputed_percentage_child',
                       'var_imputed_sterling_cash',
                       'var_imputed_death_middle_passage',
                       'var_imputed_mortality'
                       ]

list_date_fields = ['var_voyage_began',
                    'var_slave_purchase_began',
                    'var_vessel_left_port',
                    'var_first_dis_of_slaves',
                    'var_departure_last_place_of_landing',
                    'var_voyage_completed'
                    ]

list_place_fields = ['var_vessel_construction_place',
                     'var_registered_place',
                     'var_imp_port_voyage_begin',
                     'var_first_place_slave_purchase',
                     'var_second_place_slave_purchase',
                     'var_third_place_slave_purchase',
                     'var_imp_principal_place_of_slave_purchase',
                     'var_port_of_call_before_atl_crossing',
                     'var_first_landing_place',
                     'var_second_landing_place',
                     'var_third_landing_place',
                     'var_principal_port_of_slave_dis',
                     'var_place_voyage_ended',
                     ]

list_boolean_fields = ['var_voyage_in_cd_rom']

list_imputed_nationality_values = ['Spain / Uruguay', 'Portugal / Brazil', 'Great Britain',
                                   'Netherlands', 'U.S.A', 'France', 'Denmark / Baltic',
                                   'Other (specify in note)']

list_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

paginator_range_factors = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
option_results_per_page = [10, 15, 20, 30, 50, 100, 200]

if VoyageDates.objects.count() > 1:
    voyage_span_first_year = VoyageDates.objects.all().aggregate(Min('imp_voyage_began'))['imp_voyage_began__min'][2:]
    voyage_span_last_year = VoyageDates.objects.all().aggregate(Max('imp_voyage_began'))['imp_voyage_began__max'][2:]
else:
    voyage_span_first_year = 1514
    voyage_span_last_year = 1866

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
        uploaded_files_info.append({'name': f, 'size': size(st[ST_SIZE]), 'date_mod': time.asctime(time.localtime(st[ST_MTIME]))})

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
    Currently on renders the initial page
    """
    pagins = None
    paginator_range = None
    no_result = False

    # Get and update form of option results per page if necessary
    form, results_per_page = check_and_save_options_form(request)

    # Get number of requested page
    # if request.POST.get('desired_page') is None:
    #     current_page = 1
    # else:
    #     current_page = request.POST.get('desired_page')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    # Try to retrieve results from session
    try:
        results = request.session['results_voyages']
    except:
        results = SearchQuerySet().models(Voyage).order_by('var_voyage_id')
        request.session['results_voyages'] = results

    if request.method == 'POST':

        submitVal = request.POST.get('submitVal')

        time_span_form = TimeFrameSpanSearchForm(request.POST)
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
                    if tmp_varname in list_text_fields:
                        cur_var['form'] = SimpleTextForm(request.POST, prefix=tmp_varname)

                    elif tmp_varname in list_select_fields:
                        # Select box variables
                        oldChoices = cur_var['form'].fields['choice_field'].choices
                        cur_var['form'] = SimpleSelectSearchForm(oldChoices, request.POST, prefix=tmp_varname)
                    elif tmp_varname in list_numeric_fields:
                        # Numeric variables
                        cur_var['form'] = SimpleNumericSearchForm(request.POST, prefix=tmp_varname)

                    elif tmp_varname in list_date_fields:
                        # Numeric variables
                        cur_var['form'] = SimpleDateSearchForm(auto_id=('id_' + tmp_varname + "_%s"), initial={'options': '1'}, prefix=tmp_varname)

                    elif tmp_varname in list_place_fields:
                        pass

                    elif tmp_varname in list_boolean_fields:
                         # Boolean field
                        cur_var['form'].initial = {'choice_field': request.POST.getlist(tmp_varname + '-choice_field')}
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

            if varname in list_text_fields:
                # Plain text fields
                form = SimpleTextForm(auto_id=('id_' + varname + "_%s"), prefix=varname)
                tmpElemDict['form'] = form
                tmpElemDict['type'] = 'plain_text'

            elif varname in list_select_fields:
                # Select box variables
                choices = getChoices(varname)
                form = SimpleSelectSearchForm(listChoices=choices, auto_id=('id_' + varname + "_%s"), prefix=varname)

                tmpElemDict['form'] = form
                tmpElemDict['type'] = 'select'
                tmpElemDict['varname_wrapper'] = "select_" + varname
                tmpElemDict['choices'] = choices

            elif varname in list_numeric_fields:
                # Numeric variables
                form = SimpleNumericSearchForm(auto_id=('id_' + varname + "_%s"), initial={'options': '4'}, prefix=varname)
                tmpElemDict['form'] = form
                tmpElemDict['type'] = 'numeric'

            elif varname in list_date_fields:
                # Numeric variables
                form = SimpleDateSearchForm(auto_id=('id_' + varname + "_%s"), initial={'options': '1'}, prefix=varname)
                tmpElemDict['form'] = form
                tmpElemDict['type'] = 'date'
                tmpElemDict['list_months'] = list_months

            elif varname in list_place_fields:
                choices = getNestedListPlaces(varname)

                tmpElemDict['type'] = 'select_three_layers'
                tmpElemDict['varname_wrapper'] = "select_" + varname
                tmpElemDict['choices'] = choices
                tmpElemDict['selected_choices'] = varname + "_selected"

            elif varname in list_boolean_fields:
                 # Boolean field
                form = SimpleSelectBooleanForm(auto_id=('id_' + varname + "_%s"), prefix=varname)
                tmpElemDict['form'] = form
                tmpElemDict['type'] = 'boolean'
            else:
                pass
            request.session['existing_form'].append(tmpElemDict)

        elif submitVal == 'reset':
            existing_form = []
            request.session['existing_form'] = existing_form
            results = SearchQuerySet().models(Voyage).order_by('var_voyage_id')
            request.session['results_voyages'] = results

        elif submitVal == 'search':
            list_search_vars = request.POST.getlist('list-input-params')

            new_existing_form = []
            query_dict = {}

            # Time frame search
            query_dict['var_imp_voyage_began__range'] = [request.session['time_span_form'].cleaned_data['frame_from_year'],
                                                             request.session['time_span_form'].cleaned_data['frame_to_year']]

            for tmp_varname in list_search_vars:
                for cur_var in request.session['existing_form']:

                    if tmp_varname == cur_var['varname']:
                        if tmp_varname in list_text_fields:
                            cur_var['form'] = SimpleTextForm(request.POST, prefix=tmp_varname)
                            if cur_var['form'].is_valid():
                                query_dict[tmp_varname + "__contains"] = cur_var['form'].cleaned_data['text_search']

                        elif tmp_varname in list_select_fields:
                            # Select box variables
                            oldChoices = cur_var['form'].fields['choice_field'].choices
                            cur_var['form'] = SimpleSelectSearchForm(oldChoices, request.POST, prefix=tmp_varname)
                            if cur_var['form'].is_valid():
                                query_dict[tmp_varname + "__in"] = cur_var['form'].cleaned_data['choice_field']

                        elif tmp_varname in list_numeric_fields:
                            # Numeric variables
                            cur_var['form'] = SimpleNumericSearchForm(request.POST, prefix=tmp_varname)
                            if cur_var['form'].is_valid():
                                opt = cur_var['form'].cleaned_data['options']
                                if opt == '1': # Between
                                    query_dict[tmp_varname + "__range"] = [cur_var['form'].cleaned_data['lower_bound'],
                                                                           cur_var['form'].cleaned_data['upper_bound']]
                                elif opt == '2': #
                                    query_dict[tmp_varname + "__lte"] = cur_var['form'].cleaned_data['threshold']
                                elif opt == '3':
                                    query_dict[tmp_varname + "__gte"] = cur_var['form'].cleaned_data['threshold']
                                elif opt == '4': # Is equal
                                    query_dict[tmp_varname + "__exact"] = cur_var['form'].cleaned_data['threshold']
                                else:
                                    pass

                        elif tmp_varname in list_date_fields:
                            # Currently in progress
                            # To be updated
                            cur_var['form'] = SimpleDateSearchForm(request.POST, prefix=tmp_varname)

                        elif tmp_varname in list_place_fields:
                            query_dict[tmp_varname + "__in"] = request.POST.getlist(tmp_varname + "_selected")

                        elif tmp_varname in list_boolean_fields:
                             # Boolean field
                            cur_var['form'] = SimpleSelectBooleanForm(request.POST, prefix=tmp_varname)
                            if cur_var['form'].is_valid():
                                query_dict[tmp_varname + "__in"] = cur_var['form'].cleaned_data['choice_field']

                        new_existing_form.append(cur_var)

            request.session['existing_form'] = new_existing_form

            # Initially sort by voyage_id
            results = SearchQuerySet().filter(**query_dict).models(Voyage).order_by('var_voyage_id')
            if results.count() == 0:
                no_result = True
            request.session['results_voyages'] = results
        # else:
        #     results = SearchQuerySet().models(Voyage).order_by('var_voyage_id')


        # paginator = Paginator(results, results_per_page)
        # pagins = paginator.page(int(current_page))

    elif request.method == 'GET':
        # Create a new form
        existing_form = []
        request.session['existing_form'] = existing_form

        # results = SearchQuerySet().models(Voyage).order_by('var_voyage_id')
        # paginator = Paginator(results, results_per_page)
        # pagins = paginator.page(int(current_page))

        # Check if there is any result in session, save if necessary
        # results = SearchQuerySet().models(Voyage).order_by('var_voyage_id')
        # results = SearchQuerySet().models(Voyage).order_by('var_voyage_id')

        request.session['time_span_form'] = TimeFrameSpanSearchForm(
            initial={'frame_from_year': voyage_span_first_year,
                     'frame_to_year': voyage_span_last_year})

    form, results_per_page = check_and_save_options_form(request)

    if results.count() == 0:
        no_result = True

    if request.POST.get('desired_page') is None:
        current_page = 1
    else:
        current_page = request.POST.get('desired_page')

    paginator = Paginator(results, results_per_page)
    pagins = paginator.page(int(current_page))

    form, results_per_page = check_and_save_options_form(request)

    # Prepare paginator ranges
    paginator_range = prepare_paginator_ranges(paginator, current_page, results_per_page)

    return render(request, "voyage/search.html", {
                              'voyage_span_first_year': voyage_span_first_year,
                              'voyage_span_last_year': voyage_span_last_year,
                              'results': pagins,
                              'paginator_range': paginator_range,
                              'no_result': no_result,
                              'options_results_per_page_form': form})


def getChoices(varname):
    """
    Retrieve a list of two-tuple items for select boxes depending on the model
    :param varname variable name:
    :return:
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
            if nation.label in list_imputed_nationality_values:
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


def getNestedListPlaces(varname):
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
                reg_content.append({'id': 'id_' + varname + '_2_' + str(place.pk),
                                    'text': place.place,
                                    'order_num': place.pk})
            area_content.append({'id': 'id_' + varname + '_1_' + str(reg.pk),
                                'text': reg.region,
                                'order_num': reg.pk,
                                'choices': reg_content})
        choices.append({'id': 'id_' + varname + '_0_' + str(area.pk),
                        'text': area.broad_region,
                        'order_num': area.pk,
                        'choices': area_content})
    return choices


def prepare_paginator_ranges(paginator, current_page, results_per_page):
    """
    Function prepares set of paginator links for template.

    :param paginator: Paginator which links are calculating for
    :param current_page: Current page serves on search site
    """

    paginator_range = []
    last_saved_index = 0

    for i in paginator_range_factors:

        # Get last inserted index
        try:
            last = last = paginator_range[-1]
        except IndexError:
            last = 0

        # If page number would be greater than max page number,
        # return, since this is the end of page paginator ranges
        if last_saved_index >= len(paginator.object_list):
            return paginator_range
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

    return paginator_range


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


def getMonth(value):
    return value.split(",")[0]


def getDay(value):
    return value.split(",")[1]


def getYear(value):
    return value.split(",")[2]

