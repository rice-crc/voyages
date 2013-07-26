from django.http import Http404, HttpResponseRedirect
from django.template import TemplateDoesNotExist, loader, RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from os import listdir, stat
from stat import ST_SIZE, ST_MTIME
from hurry.filesize import size
import time
from .forms import *
from .models import *

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
                       'var_imp_arrival_at_port_of_dis',
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
                       'var_second place of landing',
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
                       '"var_imputed_mortality'
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
                     'var_port_of_departure',
                     'var_first_place_slave_purchase',
                     'var_second_place_slave_purchase',
                     'var_third_place_slave_purchase',
                     'var_principal_place_of_slave_purchase',
                     'var_port_of_call_before_atl_crossing',
                     'var_first_landing_place',
                     'var_second_landing_place',
                     'var_third_landing_place',
                     'var_principal_port_of_slave_dis',
                     'var_place_voyage_ended',
                     'var_imp_port_voyage_begin',
                     'var_imp_principal_place_of_slave_purchase',
                     'var_imp_principal_port_slave_dis',
                     ]

list_boolean_fields = ['var_voyage_in_cd_rom',]

list_imputed_nationality_values = ['Spain / Uruguay', 'Portugal / Brazil', 'Great Britain',
                                   'Netherlands', 'U.S.A', 'France', 'Denmark / Baltic',
                                   'Other (specify in note)']

list_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

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
        return render_to_response(templatename, {},
                              context_instance=RequestContext(request, {"pagepath" : pagepath}))
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

    return render_to_response(templatename, {'form': form, 'uploaded_files': uploaded_files_info},
                context_instance=RequestContext(request))


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
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
    return render_to_response("voyage/search.html", {},
                context_instance=RequestContext(request))


def search(request, added_field):
    if request.method == 'POST':
        if not request.GET('form:attr_selected') is None:
            pass
    elif request.method == 'GET':
        pass
    return render_to_response("voyage/search.html", {},
                context_instance=RequestContext(request))


def get_var_box(request, varname):

    # Return/construct a box with information about the variables:
    input_field_name = "header_" + varname

    if varname in list_text_fields:
        # Plain text fields
        form = SimpleTextForm(auto_id=('id_' + varname + "_%s"))
        return render_to_response("voyage/search_box_plain_text.html",
            {'varname': varname, 'input_field_name': input_field_name, 'form': form,},
            context_instance=RequestContext(request))

    elif varname in list_select_fields:
        # Select box variables
        choices = getChoices(varname)
        form = SimpleSelectSearchForm(listChoices=choices, auto_id=('id_' + varname + "_%s"))
        varname_wrapper = "select_" + varname
        return render_to_response("voyage/search_box_select.html",
            {'varname': varname, 'choices': choices,
                'input_field_name': input_field_name,
                'varname_wrapper' : varname_wrapper, 'form': form},
            context_instance=RequestContext(request))

    elif varname in list_numeric_fields:
        # Numeric variables
        form = SimpleNumericSearchForm(auto_id=('id_' + varname + "_%s"), initial={'options': '4'})
        return render_to_response("voyage/search_box_numeric.html",
            {'varname': varname,
                'input_field_name': input_field_name, 'form': form},
            context_instance=RequestContext(request))
    elif varname in list_date_fields:
        # Numeric variables
        form = SimpleDateSearchForm(auto_id=('id_' + varname + "_%s"), initial={'options': '1'})
        return render_to_response("voyage/search_box_date.html",
            {'varname': varname, 'list_months': list_months,
                'input_field_name': input_field_name, 'form': form},
            context_instance=RequestContext(request))
    elif varname in list_place_fields:
        choices = getNestedListPlaces(varname)
        varname_wrapper = "select_" + varname
        return render_to_response("voyage/search_box_select_three_layers.html",
            {'varname': varname, 'choices': choices,
                'input_field_name': input_field_name,
                'varname_wrapper': varname_wrapper},
            context_instance=RequestContext(request))

    elif varname in list_boolean_fields:
         # Boolean field
        choices=(('1', 'Yes'), ('2', 'No'))
        form = SimpleSelectSearchForm(listChoices=choices, auto_id=('id_' + varname + "_%s"))
        return render_to_response("voyage/search_box_plain_text.html",
            {'varname': varname, 'input_field_name': input_field_name, 'form': form,},
            context_instance=RequestContext(request))
    else:
        pass


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
            choices.append((nation.pk, nation.label))
    elif varname in ['var_imputed_nationality']:
        for nation in Nationality.objects.all():
            # imputed flags
            if nation.label in list_imputed_nationality_values:
                choices.append((nation.pk, nation.label))
    elif varname in ['var_outcome_voyage']:
        for outcome in ParticularOutcome.objects.all():
            choices.append((outcome.pk, outcome.label))
    elif varname in ['var_outcome_slaves']:
        for outcome in SlavesOutcome.objects.all():
            choices.append((outcome.pk, outcome.label))
    elif varname in ['var_outcome_owner']:
        for outcome in OwnerOutcome.objects.all():
            choices.append((outcome.pk, outcome.label))
    elif varname in ['var_resistance']:
        for outcome in Resistance.objects.all():
            choices.append((outcome.pk, outcome.label))
    elif varname in ['var_outcome_ship_captured']:
        for outcome in VesselCapturedOutcome.objects.all():
            choices.append((outcome.pk, outcome.label))
    return choices


def getNestedListPlaces(varname):
    """
    Retrieve a nested list of places sorted by broad region (area) and then region
    :param varname:
    :return:
    """
    choices = []
    print "got here"
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


def getMonth(value):
    return value.split(",")[0]


def getDay(value):
    return value.split(",")[1]


def getYear(value):
    return value.split(",")[2]