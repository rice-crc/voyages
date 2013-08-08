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
                       'var_imp_arrival_at_port_of_dis',  # Year arrived with salves
                       'var_imp_length_home_to_disembark',
                       'var_length_middle_passage_days',

                       'var_crew_voyage_outset',
                       'var_crew_first_landing',
                       'var_crew_died_complete_voyage',
                       'var_num_slaves_intended_first_port',
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

list_months = [('Jan', '01'), ('Feb', '02'), ('Mar', '03'), ('Apr', '04'), ('May', '05'), ('Jun', '06'),
               ('Jul', '07'), ('Aug', '08'), ('Sep', '09'), ('Oct', '10'), ('Nov', '11'), ('Dec', '12')]

var_dict = {
            # Ship, Nation, Owners
            'var_voyage_id':
                {'var_full_name': 'Voyage identification number',
                 'var_type': 'numeric',
                 'var_category': 'Ship, nation, owners'},
            'var_voyage_in_cd_rom':
                {'var_full_name': 'Voyage in 1999 CD-ROM',
                 'var_type': 'boolean',
                 'var_category': 'Ship, nation, owners'},
            'var_ship_name':
                {'var_full_name': 'Vessel name',
                 'var_type': 'plain_text',
                 'var_category': 'Ship, nation, owners'},
            'var_nationality':
                {'var_full_name': 'Flag',
                 'var_type': 'select',
                 'var_category': 'Ship, nation, owners'},
            'var_imputed_nationality':
                {'var_full_name': 'Flag' + "*",
                 'var_type': 'select',
                 'var_category': 'Ship, nation, owners'},
            'var_vessel_construction_place':
                {'var_full_name': 'Place constructed',
                 'var_type': 'select_three_layers',
                 'var_category': 'Ship, nation, owners'},
            'var_year_of_construction':
                {'var_full_name': 'Year constructed',
                 'var_type': 'numeric',
                 'var_category': 'Ship, nation, owners'},
            'var_registered_place':
                {'var_full_name': 'Place registered',
                 'var_type': 'select_three_layers',
                 'var_category': 'Ship, nation, owners'},
            'var_rig_of_vessel':
                {'var_full_name': 'Rig',
                 'var_type': 'numeric',
                 'var_category': 'Ship, nation, owners'},
            'var_tonnage':
                {'var_full_name': 'Tonnage',
                 'var_type': 'numeric',
                 'var_category': 'Ship, nation, owners'},
            'var_tonnage_mod':
                {'var_full_name': 'Standardized tonnage',
                 'var_type': 'numeric',
                 'var_category': 'Ship, nation, owners'},
            'var_guns_mounted':
                {'var_full_name': 'Guns mounted',
                 'var_type': 'numeric',
                 'var_category': 'Ship, nation, owners'},
            'var_owner':
                {'var_full_name': 'Vessel owners',
                 'var_type': 'plain_text',
                 'var_category': 'Ship, nation, owners'},

            # Voyage outcome
            'var_outcome_voyage':
                {'var_full_name': 'Particular outcome of voyage',
                 'var_type': 'select',
                 'var_category': 'Voyage Outcome'},
            'var_outcome_slaves':
                {'var_full_name': 'Outcome of voyage for slaves',
                 'var_type': 'select',
                 'var_category': 'Voyage Outcome'},
            'var_outcome_ship_captured':
                {'var_full_name': 'Outcome of voyage if ship captured',
                 'var_type': 'select',
                 'var_category': 'Voyage Outcome'},
            'var_outcome_owner':
                {'var_full_name': 'Outcome of voyage for owner',
                 'var_type': 'select',
                 'var_category': 'Voyage Outcome'},
            'var_resistance':
                {'var_full_name': 'African resistance',
                 'var_type': 'select',
                 'var_category': 'Voyage Outcome'},

            # Voyage Itinerary
            'var_imp_port_voyage_begin':
                {'var_full_name': 'Place where voyage began',
                 'var_type': 'select_three_layers',
                 'var_category': 'Voyage Itinerary'},
            'var_first_place_slave_purchase':
                {'var_full_name': 'First place of slave purchase',
                 'var_type': 'select_three_layers',
                 'var_category': 'Voyage Itinerary'},
            'var_second_place_slave_purchase':
                {'var_full_name': 'Second place of slave purchase',
                 'var_type': 'select_three_layers',
                 'var_category': 'Voyage Itinerary'},
            'var_third_place_slave_purchase':
                {'var_full_name': 'Third place of slave purchase',
                 'var_type': 'select_three_layers',
                 'var_category': 'Voyage Itinerary'},
            'var_imp_principal_place_of_slave_purchase':
                {'var_full_name': 'Principal place of slave purchase',
                 'var_type': 'select_three_layers',
                 'var_category': 'Voyage Itinerary'},
            'var_port_of_call_before_atl_crossing':
                {'var_full_name': 'Places of call before Atlantic crossing',
                 'var_type': 'select_three_layers',
                 'var_category': 'Voyage Itinerary'},
            'var_first_landing_place':
                {'var_full_name': 'First place of slave landing',
                 'var_type': 'select_three_layers',
                 'var_category': 'Voyage Itinerary'},
            'var_second_landing_place':
                {'var_full_name': 'Second place of slave landing',
                 'var_type': 'select_three_layers',
                 'var_category': 'Voyage Itinerary'},
            'var_third_landing_place':
                {'var_full_name': 'Third place of slave landing',
                 'var_type': 'select_three_layers',
                 'var_category': 'Voyage Itinerary'},
            'var_imp_principal_port_of_slave_dis':
                {'var_full_name': 'Principal place of slave landing',
                 'var_type': 'select_three_layers',
                 'var_category': 'Voyage Itinerary'},
            'var_place_voyage_ended':
                {'var_full_name': 'Place where voyage ended',
                 'var_type': 'select_three_layers',
                 'var_category': 'Voyage Itinerary'},

            # Voyage Dates
            'var_imp_arrival_at_port_of_dis':
                {'var_full_name': 'Year arrived with slaves',
                 'var_type': 'numeric',
                 'var_category': 'Voyage Dates'},
            'var_voyage_began':
                {'var_full_name': 'Date voyage began',
                 'var_type': 'date',
                 'var_category': 'Voyage Dates'},
            'var_slave_purchase_began':
                {'var_full_name': 'Date trade began in Africa',
                 'var_type': 'date',
                 'var_category': 'Voyage Dates'},
            'var_vessel_left_port':
                {'var_full_name': 'Date vessel departed Africa',
                 'var_type': 'date',
                 'var_category': 'Voyage Dates'},
            'var_first_dis_of_slaves':
                {'var_full_name': 'Date vessel arrived with slaves',
                 'var_type': 'date',
                 'var_category': 'Voyage Dates'},
            'var_departure_last_place_of_landing':
                {'var_full_name': 'Date vessel departed for homeport',
                 'var_type': 'date',
                 'var_category': 'Voyage Dates'},
            'var_voyage_completed':
                {'var_full_name': 'Date voyage completed',
                 'var_type': 'date',
                 'var_category': 'Voyage Dates'},
            'var_imp_length_home_to_disembark':
                {'var_full_name': 'Voyage length, homeport to slaves landing (days)',
                 'var_type': 'numeric',
                 'var_category': 'Voyage Dates'},
            'var_length_middle_passage_days':
                {'var_full_name': 'Middle passage (days)',
                 'var_type': 'numeric',
                 'var_category': 'Voyage Dates'},

            # Captain and Crew
            'var_captain':
                {'var_full_name': 'Captain\'s name',
                 'var_type': 'plain_text',
                 'var_category': 'Captain and Crew'},
            'var_crew_voyage_outset':
                {'var_full_name': 'Crew at voyage outset',
                 'var_type': 'numeric',
                 'var_category': 'Captain and Crew'},
            'var_crew_first_landing':
                {'var_full_name': 'Crew at first landing of slaves',
                 'var_type': 'numeric',
                 'var_category': 'Captain and Crew'},
            'var_crew_died_complete_voyage':
                {'var_full_name': 'Crew deaths during voyage',
                 'var_type': 'numeric',
                 'var_category': 'Captain and Crew'},

            # Slaves (numbers)
            'var_num_slaves_intended_first_port':
                {'var_full_name': 'Number of slaves intended at first place of purchase',
                 'var_type': 'numeric',
                 'var_category': 'Slave (numbers)'},
            'var_num_slaves_carried_first_port':
                {'var_full_name': 'Slaves carried from first port of purchase',
                 'var_type': 'numeric',
                 'var_category': 'Slave (numbers)'},
            'var_num_slaves_carried_second_port':
                {'var_full_name': 'Slaves carried from second port of purchase',
                 'var_type': 'numeric',
                 'var_category': 'Slave (numbers)'},
            'var_num_slaves_carried_third_port':
                {'var_full_name': 'Slaves carried from third port of purchase',
                 'var_type': 'numeric',
                 'var_category': 'Slave (numbers)'},
            'var_total_num_slaves_purchased':
                {'var_full_name': 'Total slaves embarked',
                 'var_type': 'numeric',
                 'var_category': 'Slave (numbers)'},
            'var_imp_total_num_slaves_purchased':
                {'var_full_name': 'Total slaves embarked',
                 'var_type': 'numeric',
                 'var_category': 'Slave (numbers)'},
            'var_total_num_slaves_arr_first_port_embark':
                {'var_full_name': 'Number of slaves arriving at first place of landing',
                 'var_type': 'numeric',
                 'var_category': 'Slave (numbers)'},
            'var_num_slaves_disembark_first_place':
                {'var_full_name': 'Number of slaves disembarked at first place of landing',
                 'var_type': 'numeric',
                 'var_category': 'Slave (numbers)'},
            'var_second_place_of_landing':
                {'var_full_name': 'Number of slaves disembarked at second place of landing',
                 'var_type': 'numeric',
                 'var_category': 'Slave (numbers)'},
            'var_num_slaves_disembark_third_place':
                {'var_full_name': 'Number of slaves disembarked at third place of landing',
                 'var_type': 'numeric',
                 'var_category': 'Slave (numbers)'},
            'var_imp_total_slaves_disembarked':
                {'var_full_name': 'Total slaves disembarked',
                 'var_type': 'numeric',
                 'var_category': 'Slave (numbers)'},

            # Slaves (characteristics)
            'var_imputed_percentage_men':
                {'var_full_name': 'Percentage men',
                 'var_type': 'numeric',
                 'var_category': 'Slave (characteristics)'},
            'var_imputed_percentage_women':
                {'var_full_name': 'Percentage women',
                 'var_type': 'numeric',
                 'var_category': 'Slave (characteristics)'},
            'var_imputed_percentage_boys':
                {'var_full_name': 'Percentage boys',
                 'var_type': 'numeric',
                 'var_category': 'Slave (characteristics)'},
            'var_imputed_percentage_girls':
                {'var_full_name': 'Percentage girls',
                 'var_type': 'numeric',
                 'var_category': 'Slave (characteristics)'},
            'var_imputed_percentage_female':
                {'var_full_name': 'Percentage female',
                 'var_type': 'numeric',
                 'var_category': 'Slave (characteristics)'},
            'var_imputed_percentage_male':
                {'var_full_name': 'Percentage male',
                 'var_type': 'numeric',
                 'var_category': 'Slave (characteristics)'},
            'var_imputed_percentage_child':
                {'var_full_name': 'Percentage children',
                 'var_type': 'numeric',
                 'var_category': 'Slave (characteristics)'},
            'var_imputed_sterling_cash':
                {'var_full_name': 'Sterling cash price in Jamaica',
                 'var_type': 'numeric',
                 'var_category': 'Slave (characteristics)'},
            'var_imputed_death_middle_passage':
                {'var_full_name': 'Slave deaths during middle passage',
                 'var_type': 'numeric',
                 'var_category': 'Slave (characteristics)'},
            'var_imputed_mortality':
                {'var_full_name': 'Mortality rate',
                 'var_type': '',
                 'var_category': 'Slave (characteristics)'},

            # Source
            'var_sources':
                {'var_full_name': 'Sources',
                 'var_type': 'plain_text',
                 'var_category': 'Source'}
}

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

    # Check if saved url has been used
    if request.GET.values():
        query_dict, request.session['existing_form'] = decode_from_url(request)
        results = SearchQuerySet().filter(**query_dict).models(Voyage).order_by('var_voyage_id')

        if results.count() == 0:
            no_result = True

        request.session['results_voyages'] = results

    # Otherwise, process next
    else:

        if not request.session.exists(request.session.session_key):
            request.session.create()

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
                            cur_var['form'] = SimpleDateSearchForm(request.POST, prefix=tmp_varname)
                            cur_var['list_deselected'] = request.POST.getlist(tmp_varname + '_deselected_months')
                            print cur_var['list_deselected']

                        elif tmp_varname in list_place_fields:
                            place_selected = request.POST.getlist(tmp_varname + "_selected")
                            region_selected = request.POST.getlist(tmp_varname + "_selected_regs")
                            area_selected = request.POST.getlist(tmp_varname + "_selected_areas")
                            cur_var['choices'] = getNestedListPlaces(tmp_varname,
                                                                     place_selected, region_selected, area_selected)

                        elif tmp_varname in list_boolean_fields:
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

                if varname in list_text_fields:
                    # Plain text fields
                    form = SimpleTextForm(auto_id=('id_' + varname + "_%s"), prefix=varname)
                    tmpElemDict['form'] = form
                    tmpElemDict['type'] = 'plain_text'

                elif varname in list_select_fields:
                    # Select box variables
                    choices = getChoices(varname)
                    form = SimpleSelectSearchForm(listChoices=choices,
                                                  auto_id=('id_' + varname + "_%s"), prefix=varname)

                    tmpElemDict['form'] = form
                    tmpElemDict['type'] = 'select'
                    tmpElemDict['varname_wrapper'] = "select_" + varname
                    tmpElemDict['choices'] = choices

                elif varname in list_numeric_fields:
                    # Numeric variables
                    form = SimpleNumericSearchForm(auto_id=('id_' + varname + "_%s"),
                                                   initial={'options': '4'}, prefix=varname)
                    tmpElemDict['form'] = form
                    tmpElemDict['type'] = 'numeric'

                elif varname in list_date_fields:
                    # Numeric variables
                    form = SimpleDateSearchForm(auto_id=('id_' + varname + "_%s"),
                                                initial={'options': '1',
                                                         'from_year': voyage_span_first_year,
                                                         'to_year': voyage_span_last_year},
                                                prefix=varname)
                    tmpElemDict['form'] = form
                    tmpElemDict['type'] = 'date'
                    tmpElemDict['list_months'] = list_months
                    tmpElemDict['deselected_months'] = varname + '_deselected_months'
                    tmpElemDict['list_deselected'] = []

                elif varname in list_place_fields:
                    choices = getNestedListPlaces(varname, [], [], [])

                    tmpElemDict['type'] = 'select_three_layers'
                    tmpElemDict['varname_wrapper'] = "select_" + varname
                    tmpElemDict['choices'] = choices
                    tmpElemDict['selected_choices'] = varname + "_selected"
                    tmpElemDict['selected_regs'] = varname + "_selected_regs"
                    tmpElemDict['selected_areas'] = varname + "_selected_areas"

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

                # Time frame search
                query_dict['var_imp_voyage_began__range'] = [request.session['time_span_form'].cleaned_data['frame_from_year'],
                                                             request.session['time_span_form'].cleaned_data['frame_to_year']]
                date_filters = []

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

                            elif tmp_varname in list_date_fields:
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

                                    if 0 < len(deselected_months) < len(list_months):
                                        date_filters.append({'varname': tmp_varname,
                                                             'deselected_months': deselected_months})
                                    elif len(deselected_months) == len(list_months):
                                        no_result = True
                                    else:  # user selected all 12 months
                                        pass

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

                # Date filters
                if date_filters:
                    for var_filter in date_filters:
                        l_months = []
                        tmp_query = dict()
                        for month in var_filter['deselected_months']:
                            l_months.append("-" + month + "-")

                        tmp_query[tmp_varname + "__in"] = l_months
                        results = results.exclude(**tmp_query)

                if results.count() == 0:
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
        url_to_copy = encode_to_url(request, request.session['existing_form'], query_dict)

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
    (paginator_range, pages_range) = prepare_paginator_variables(paginator, current_page, results_per_page)

    return render(request, "voyage/search.html",
                  {'voyage_span_first_year': voyage_span_first_year,
                   'voyage_span_last_year': voyage_span_last_year,
                   'results': pagins,
                   'paginator_range': paginator_range,
                   'pages_range': pages_range,
                   'no_result': no_result,
                   'url_to_copy': url_to_copy,
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
    for i in paginator_range_factors:

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


def encode_to_url(request, session, dict={}):
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

            url += "&"

        # At the end, delete the last unnecessary underscore
        url = url[0:-1]
        session_dict['dict'] = dict
        session_dict['existing_form'] = session

    # Store dict in session and return url
    url_key = iri_to_uri("/" + str("/".join(url.split("/")[3:])))

    request.session[url_key] = session_dict
    return url


def decode_from_url(request):
    """
    Function to decode url to dict and forms.

    :param request: request to serve

    """
    #FIXME: existing_form is not saved out of session.

    # Check if this path is in session
    # try:
    #     session_dict = request.session[request.get_full_path()]
    #     return session_dict['dict'], session_dict['existing_form']
    # except KeyError:
    #     pass

    dict = {}

    for k, v in request.GET.iteritems():
        if "__range" in k:
            dict[k] = []
            dict[k].append(v.split("|")[0])
            dict[k].append(v.split("|")[1])

        elif isinstance(v, types.ListType):
            dict[k] = []
            for i in v.split("|"):
                dict[k].append(i)
        else:
            dict[k] = v

    create_menu_forms(dict)
    return dict, 1


def create_menu_forms(dict):
    """
    Function to create forms.
    """

    for k, v in dict.iteritems():
        # Get var_name
        var_name = k.split("__")[0]


        3/0
        pass

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
