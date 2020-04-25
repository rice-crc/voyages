# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.db.models import Max, Min
from django.template import TemplateDoesNotExist, loader
from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache
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
import globals
import bitly_api
import requests
import json
import xlwt
from openpyxl import Workbook
import urllib
import unidecode
from itertools import groupby
from django.views.decorators.gzip import gzip_page
from datetime import date
from voyages.apps.assessment.globals import get_map_year
from voyages.apps.common.export import download_xls
from voyages.apps.resources.models import Image
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from cache import VoyageCache, CachedGeo
from voyages.apps.common.models import get_pks_from_haystack_results
from graphs import *
from django.shortcuts import redirect


# Here we enumerate all fields that should be cleared
# from the session if a reset is required.
reset_fields = ['voyages_tables_columns', 'voyages_tables_rows',
               'voyages_tables_cells', 'voyages_tables_omit',
               'voyage_timeline_form_option', 'selected_graphs_tab',
               'tab_graphs_bar_defs', 'tab_graphs_lin_defs', 'tab_graphs_pie_defs',
               'tab_graphs_bar_defs_x_ind', 'tab_graphs_bar_defs_y_ind',
               'tab_graphs_lin_defs_x_ind', 'tab_graphs_lin_defs_y_ind',
               'tab_graphs_pie_defs_x_ind', 'tab_graphs_pie_defs_y_ind',]

def get_voyages_search_query_set():
    return SearchQuerySet().models(Voyage).filter(var_dataset=0)

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


def understanding_page(request, name='guide'):
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
        dictionary['page'] = 'variable-list.html'
    else:
        dictionary['page'] = name + ".html"
        dictionary['title'] = 'Guide'
    dictionary['title'] = _(dictionary['title'])

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
    templatename = 'upload.html'

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

def download_flatpage(request):
    from django.contrib.flatpages.models import FlatPage
    page_title = 'Downloads'
    lang = get_language()
    flatpage = None
    if lang != 'en':
        try:
            flatpage = FlatPage.objects.get(title=page_title + '_' + lang)
        except:
            pass
    if flatpage is None:
        flatpage = FlatPage.objects.get(title=page_title)
    from datetime import date
    return render(request,
                  'flatpages/download.html',
                  {'flatpage': flatpage, 'num_voyages': Voyage.objects.count(), 'year': str(date.today().year)})

def handle_uploaded_file(f):
    """
    Function handles uploaded files by saving them
    by chunks in the MEDIA_ROOT/download directory
    """
    with open('%s/%s/%s' % (settings.MEDIA_ROOT, 'download', f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def create_query_forms():
    """
    Uses the list of variables in globals.py and creates a form
    for each of them that is either a basic or a general variable
    Returns a list of dictionaries containing the var_name, var_full_name, form
    """
    voyage_span_first_year, voyage_span_last_year = globals.calculate_maxmin_years()
    form_list = []
    # for all basic and/or general variables
    for var in [x for x in globals.var_dict if x['is_general'] or x['is_basic']]:
        varname = var['var_name']
        tmpElem = {'var_name': varname,
                   'var_full_name': var['var_full_name']}
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
            nestedChoices, flatChoices = getNestedListPlaces(varname, var['choices'])
            form = SimplePlaceSearchForm(prefix=varname)
            form.fields['choice_field'].choices = flatChoices
            tmpElem['nested_choices'] = nestedChoices
            tmpElem['selected_choices'] = []
        elif varname in globals.list_boolean_fields:
            form = SimpleSelectBooleanForm(prefix=varname)
        else:
            pass
        form.fields['var_name_field'].initial = varname
        tmpElem['form'] = form
        form_list.append(tmpElem)
    return form_list

def retrieve_post_search_forms(post):
    """
    Retrieves the forms in the post and returns a list of dictionaries with var_name, var_full_name, and form
    """
    form_list = []
    # for all basic and/or general variables
    for var in [x for x in globals.var_dict if x['is_general'] or x['is_basic']]:
        varname = var['var_name']
        tmpElem = {'var_name': varname,
                   'var_full_name': var['var_full_name']}
        form = None
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
            nestedChoices, flatChoices = getNestedListPlaces(varname, var['choices'])
            form.fields['choice_field'].choices = flatChoices
            selected_choices = []
            if form.is_valid():
                selected_choices = [int(i) for i in form.cleaned_data['choice_field']]
            # Get the nested list places again to fill out the selected regions and areas. Needed to get the flat choices and set the choice field to that before form would validate.
            nestedChoices, flatChoices = getNestedListPlaces(varname, var['choices'], selected_choices)
            tmpElem['nested_choices'] = nestedChoices
            tmpElem['selected_choices'] = selected_choices

        tmpElem['form'] = form
        form_list.append(tmpElem)
    return form_list

# This won't work since some places have the same name
def get_place_from_ascii(ascii_name, flat_place_list):
    for place in flat_place_list:
        if ascii_name == unidecode.unidecode(place[0]):
            return place[0]

def create_forms_from_var_list(var_list):
    """
    Creates filled out forms based on a var_list
    """
    form_list = []
    vl = var_list.get('used_variable_names', '')
    vs = []
    if len(vl) > 0:
        vs = vl.split(';');
    for idx, varname in enumerate(vs):
        var = search_var_dict(varname)
        tmpElem = {'var_name': varname,
                   'var_full_name': var['var_full_name']}
        if varname in globals.list_text_fields:
            form = SimpleTextForm(prefix=varname)
            form.fields['text_search'].initial = var_list[varname + '_text_search']
        elif varname in globals.list_select_fields:
            choices = getChoices(varname)
            form = SimpleSelectSearchForm(prefix=varname)
            form.fields['choice_field'].choices = choices
            form.fields['choice_field'].initial = var_list[varname + '_choice_field'].split(';')
        elif varname in globals.list_numeric_fields:
            form = SimpleNumericSearchForm(prefix=varname)
            opt = var_list[varname + '_options']
            form.fields['options'].initial = opt
            if opt == '1': # Between
                form.fields['lower_bound'].initial = var_list[varname + '_lower_bound']
                form.fields['upper_bound'].initial = var_list[varname + '_upper_bound']
            elif opt == '2': # Less than or equal to
                form.fields['threshold'].initial = var_list[varname + '_threshold']
            elif opt == '3': # Greater than or equal to
                form.fields['threshold'].initial = var_list[varname + '_threshold']
            elif opt == '4': # Equal to
                form.fields['threshold'].initial = var_list[varname + '_threshold']
        elif varname in globals.list_date_fields:
            form = SimpleDateSearchForm(prefix=varname)
            mdict = dict([(int(choice[0]), choice) for choice in globals.list_months])
            form.fields['months'].initial = map(lambda x: str(x).zfill(2), var_list[varname + '_months'].split(','))
            
            opt = var_list[varname + '_options']
            form.fields['options'].initial = opt
            if opt == '1': # Between
                form.fields['from_year'].initial = var_list[varname + '_from_year']
                form.fields['from_month'].initial = var_list[varname + '_from_month']
                form.fields['to_year'].initial = var_list[varname + '_to_year']
                form.fields['to_month'].initial = var_list[varname + '_to_month']
            elif opt == '2': # Less than or equal to
                form.fields['threshold_year'].initial = var_list[varname + '_threshold_year']
                form.fields['threshold_month'].initial = var_list[varname + '_threshold_month']
            elif opt == '3': # Greater than or equal to
                form.fields['threshold_year'].initial = var_list[varname + '_threshold_year']
                form.fields['threshold_month'].initial = var_list[varname + '_threshold_month']
            elif opt == '4': # Equal to
                form.fields['threshold_year'].initial = var_list[varname + '_threshold_year']
                form.fields['threshold_month'].initial = var_list[varname + '_threshold_month']
        elif varname in globals.list_place_fields:
            selected_choices = [int(i) for i in var_list[varname + '_choice_field'].split(';')]
            form = SimplePlaceSearchForm(prefix=varname)
            nestedChoices, flatChoices = getNestedListPlaces(varname, var['choices'], selected_choices)
            form.fields['choice_field'].choices = flatChoices
            tmpElem['nested_choices'] = nestedChoices
            tmpElem['selected_choices'] = selected_choices
            form.fields['choice_field'].initial = selected_choices
        elif varname in globals.list_boolean_fields:
            form = SimpleSelectBooleanForm(prefix=varname)
            form.fields['choice_field'].initial = var_list[varname + '_choice_field'].split(';')
        else:
            pass
        form.fields['var_name_field'].initial = varname
        form.fields['is_shown_field'].initial = str(idx)
        tmpElem['form'] = form
        form_list.append(tmpElem)
    return form_list


def create_var_dict(query_forms, time_frame_form):
    """
    query_forms: list of dictionaries with var_name and value (also probably var_full_name, but I don't think I need to count on that)
    returns a dictionary of var names and values for that var
    """
    # Creates a query dict based on all the restrictions the user has made
    var_list = {}
    used_variables = []
    # Year Time Frame Search
    if time_frame_form.is_valid():
        var_list['time_span_from_year'] = time_frame_form.cleaned_data['frame_from_year']
        var_list['time_span_to_year'] = time_frame_form.cleaned_data['frame_to_year']
    for qryform in [x for x in query_forms if x['form'].is_valid() and x['form'].is_form_shown()]:
        #qform = next((l for l in query_forms if l['varname'] == search_var), None)
        varname = qryform['var_name']
        used_variables.append(varname)
        form = qryform['form']
        if varname in globals.list_text_fields:
            var_list[varname + '_text_search'] = unidecode.unidecode(form.cleaned_data['text_search'])
        elif varname in globals.list_select_fields:
            # I don't think I need to unidecode this for the url
            var_list[varname + '_choice_field'] = ';'.join(form.cleaned_data['choice_field'])
        elif varname in globals.list_numeric_fields:
            opt = form.cleaned_data['options']
            var_list[varname + '_options'] = opt
            mangle_method = globals.no_mangle
            if opt == '1': # Between
                var_list[varname + '_lower_bound'] = form.cleaned_data['lower_bound']
                var_list[varname + '_upper_bound'] = form.cleaned_data['upper_bound']
            elif opt == '2': # Less than or equal to
                var_list[varname + '_threshold'] = form.cleaned_data['threshold']
            elif opt == '3': # Greater than or equal to
                var_list[varname + '_threshold'] = form.cleaned_data['threshold']
            elif opt == '4': # Equal to
                var_list[varname + '_threshold'] = form.cleaned_data['threshold']
        elif varname in globals.list_date_fields:
            var_list[varname + '_months'] = ','.join(form.cleaned_data['months'])
            opt = form.cleaned_data['options']
            var_list[varname + '_options'] = opt
            if opt == '1': # Between
                var_list[varname + '_from_year'] = form.cleaned_data['from_year']
                var_list[varname + '_from_month'] = form.cleaned_data['from_month']
                var_list[varname + '_to_year'] = form.cleaned_data['to_year']
                var_list[varname + '_to_month'] = form.cleaned_data['to_month']
            elif opt == '2': # Less than or equal to
                var_list[varname + '_threshold_year'] = form.cleaned_data['threshold_year']
                var_list[varname + '_threshold_month'] = form.cleaned_data['threshold_month']
            elif opt == '3': # Greater than or equal to
                var_list[varname + '_threshold_year'] = form.cleaned_data['threshold_year']
                var_list[varname + '_threshold_month'] = form.cleaned_data['threshold_month']
            elif opt == '4': # Equal to
                var_list[varname + '_threshold_year'] = form.cleaned_data['threshold_year']
                var_list[varname + '_threshold_month'] = form.cleaned_data['threshold_month']
        elif varname in globals.list_place_fields:
            var_list[varname + '_choice_field'] = unidecode.unidecode(';'.join(form.cleaned_data['choice_field']))
        elif varname in globals.list_boolean_fields:
            var_list[varname + '_choice_field'] = ';'.join(form.cleaned_data['choice_field'])

    if len(used_variables) > 0:
        var_list['used_variable_names'] = ';'.join(used_variables)
    #for var in var_list:
    #    var_list[var] = unidecode.unidecode(unicode(var_list[var]))
    
    return var_list

def create_query_dict(var_list):
    """
    query_forms: list of dictionaries with var_name and form (also probably var_full_name, but I don't think I need to count on that)
    returns a tuple of query dict and a dictionary of variable names with the value(s) it has
    """
    # Creates a query dict based on all the restrictions the user has made
    query_dict = {}
    # Year Time Frame Search
    #if time_span_name in var_list:
    if 'time_span_from_year' in var_list and 'time_span_to_year' in var_list:
        query_dict['var_imp_arrival_at_port_of_dis__range'] = [var_list['time_span_from_year'],
                                                               var_list['time_span_to_year']]
    vl = var_list.get('used_variable_names', '')
    vs = []
    if len(vl) > 0:
        vs = vl.split(';');
    for varname in vs:
        try:
            mangle_method = globals.search_mangle_methods.get(varname, globals.no_mangle)
            if varname == 'var_sources':
                query_dict["var_sources_plaintext_search__contains"] = mangle_method(var_list[varname + '_text_search'])
            elif varname in globals.list_text_fields:
                query_dict[varname + "__contains"] = mangle_method(var_list[varname + '_text_search'])
            elif varname in globals.list_select_fields:
                query_dict[varname + "_idnum" + "__in"] = [int(i) for i in mangle_method(var_list[varname + '_choice_field']).split(';') if i != '']
            elif varname in globals.list_numeric_fields:
                opt = var_list[varname + '_options']
                if opt == '1': # Between
                    query_dict[varname + "__range"] = [mangle_method(var_list[varname + '_lower_bound']),
                                                    mangle_method(var_list[varname + '_upper_bound'])]
                elif opt == '2': # Less than or equal to
                    query_dict[varname + "__lte"] = mangle_method(var_list[varname + '_threshold'])
                elif opt == '3': # Greater than or equal to
                    query_dict[varname + "__gte"] = mangle_method(var_list[varname + '_threshold'])
                elif opt == '4': # Equal to
                    query_dict[varname + "__exact"] = mangle_method(var_list[varname + '_threshold'])
            elif varname in globals.list_date_fields:
                if varname + '_months' in var_list:
                    months = map(lambda x: int(x), var_list[varname + '_months'].split(','))
                    # Only filter by months if not all the months are included
                    if len(months) < 12:
                        query_dict[varname + '_month' + '__in'] = map(lambda x: int(x), months)
                opt = var_list[varname + '_options']
                if opt == '1': # Between
                    to_date = None
                    if int(var_list[varname + '_to_month']) == 12:
                        to_date = formatDate(int(mangle_method(var_list[varname + '_to_year'])) + 1, 1)
                    else:
                        to_date = formatDate(int(mangle_method(var_list[varname + '_to_year'])), int(mangle_method(var_list[varname + '_to_month'])) + 1)
                    query_dict[varname + "__range"] = [
                        formatDate(mangle_method(var_list[varname + '_from_year']),
                                mangle_method(var_list[varname + '_from_month'])),
                        to_date]
                elif opt == '2': # Less than or equal to
                    to_date = None
                    if int(var_list[varname + '_threshold_month']) == 12:
                        to_date = formatDate(int(mangle_method(var_list[varname + '_threshold_year'])) + 1, 1)
                    else:
                        to_date = formatDate(int(mangle_method(var_list[varname + '_threshold_year'])), int(mangle_method(var_list[varname + '_threshold_month'])) + 1)
                    query_dict[varname + "__lte"] = to_date
                elif opt == '3': # Greater than or equal to
                    query_dict[varname + "__gte"] = \
                        formatDate(mangle_method(var_list[varname + '_threshold_year']),
                                mangle_method(var_list[varname + '_threshold_month']))
                elif opt == '4': # In
                    to_date = None
                    if int(var_list[varname + '_threshold_month']) == 12:
                        to_date = formatDate(int(mangle_method(var_list[varname + '_threshold_year'])) + 1, 1)
                    else:
                        to_date = formatDate(int(mangle_method(var_list[varname + '_threshold_year'])), int(mangle_method(var_list[varname + '_threshold_month'])) + 1)
                    query_dict[varname + "__range"] = [
                        formatDate(mangle_method(var_list[varname + '_threshold_year']),
                                mangle_method(var_list[varname + '_threshold_month'])),
                        to_date]
            elif varname in globals.list_place_fields:
                query_dict[varname + "_idnum" + "__in"] = [int(i) for i in mangle_method(var_list[varname + '_choice_field']).split(';') if i != '']
            elif varname in globals.list_boolean_fields:
                query_dict[varname + "__in"] = mangle_method(var_list[varname + '_choice_field']).split(';')
        except:
            print("Failure when mangling variable " + varname + ". It will be removed from the search.")
            import traceback
            traceback.print_exc()
    return query_dict

def create_var_list_from_url(get):
    """
    Takes a request.GET and returns a var_list with the search parameters
    """
    var_list = {}
    for i in get:
        var_list[i] = get.get(i)
    return var_list

# Takes a var list and then gives tuples of strings that describe the query in a nice way
# Used for formatting the display of previous_queries
def prettify_var_list(varlist):
    output = []
    qdict = create_query_dict(varlist)
    # For some reason, when time_span is set, it also shows "Year arrived with slaves*"
    if 'time_span_from_year' in varlist and 'time_span_to_year' in varlist:
        output.append((_('Time frame:'), unicode(varlist['time_span_from_year']) + ' - ' + unicode(varlist['time_span_to_year'])))
    for kvar, vvar in qdict.items():
        varname = kvar.split('__')[0]
        is_real_var = False
        fullname = ''
        accepted_suffixes = varname.endswith(('_idnum', '_plaintext_search'))
        for var in globals.var_dict:
            if varname == var['var_name'] or (accepted_suffixes and varname.startswith(var['var_name'])):
                fullname = var['var_full_name']
                is_real_var = True
                break
        if not is_real_var:
            # it is a month variable
            varn = varname[:-6]
            for var in globals.var_dict:
                if varn == var['var_name']:
                    fullname = var['var_full_name']
                    break
            month_dict = {}
            for monnum, monval in globals.list_months:
                month_dict[int(monnum)] = monval
            output.append((fullname + _(" month:"), ', '.join([month_dict[int(i)] for i in vvar])))
            continue
        unmangle_method = globals.parameter_unmangle_methods.get(varname, globals.default_prettifier(varname))
        tvar = unmangle_method(vvar)
        if isinstance(tvar, (list, tuple)):
            value = unicode(u', '.join(map(unicode, tvar)))
        else:
            value = tvar
        prefix = ''
        if (varname + '_options') in varlist:
            opt = varlist[varname + '_options']
            if opt == '1' and len(vvar) >= 2:
                if varname == 'var_imp_arrival_at_port_of_dis':
                    value = _('between ') + unicode(tvar[0]) + _(' and ') + unicode(tvar[1])
                elif varname in globals.list_date_fields:
                    tod = None
                    if vvar[1].month == 1:
                        tod = date(vvar[1].year - 1, 12, vvar[1].day)
                    else:
                        tod = date(vvar[1].year, vvar[1].month - 1, vvar[1].day)
                    value = _('between ') + unicode(unmangle_method(vvar[0])) + _(' and ') + unicode(unmangle_method(tod))
                else:
                    value = _('between ') + unicode(tvar[0]) + _(' and ') + unicode(tvar[1])
            elif opt == '4':
                if isinstance(vvar, (list, tuple)):
                    value = _('in ') + unicode(unmangle_method(vvar[0]))
                else:
                    value = _('equal to ') + unicode(tvar)
            elif isinstance(vvar, (list, tuple)):
                continue
            elif opt == '2':
                if varname == 'var_imp_arrival_at_port_of_dis':
                    value = _('before ') + unicode(tvar)
                elif varname in globals.list_date_fields:
                    tod = None
                    if vvar.month == 1:
                        tod = date(vvar.year - 1, 12, vvar.day)
                    else:
                        tod = date(vvar.year, vvar.month - 1, vvar.day)
                    value = _('before ') + unicode(unmangle_method(tod))
                else:
                    value = _('at most ') + unicode(tvar)
            elif opt == '3':
                if varname == 'var_imp_arrival_at_port_of_dis':
                    value = _('after ') + unicode(tvar)
                elif varname in globals.list_date_fields:
                    value = _('after ') + unicode(tvar)
                else:
                    value = _('at least ') + unicode(tvar)
        # Prevent display of 'Year arrived with slaves*' when it is just the time frame
        if not (isinstance(vvar, (list, tuple)) and varname in globals.list_numeric_fields and not ((varname + '_options') in varlist)):
            output.append((fullname + ":", (prefix + value)))
    return output

def first_match(items):
    return items[0] if len(items) > 0 else None

def voyage_map(request, voyage_id):
    """
    Displays the map for a voyage
    """
    voyage = first_match(get_voyages_search_query_set().filter(var_voyage_id=int(voyage_id)))
    if voyage:
        year_completed = int(voyage.var_imp_voyage_began) if voyage.var_imp_voyage_began else 0
        map_year = get_map_year(year_completed, year_completed)
    else:
        map_year = None
    return render(request, "voyage_info.html",
                  {'tab': 'map',
                   'map_year': map_year,
                   'voyage_id': voyage_id,
                   'voyage': voyage})

def voyage_images(request, voyage_id):
    """
    Displays the images for a voyage
    """
    voyage = first_match(get_voyages_search_query_set().filter(var_voyage_id=int(voyage_id)))
    images = []
    if voyage:
        images = list(Image.objects.filter(voyage=int(voyage_id)))
    return render(request, "voyage_info.html",
                  {'tab': 'images',
                   'voyage_id': voyage_id,
                   'voyage': voyage,
                   'images': images})

def voyage_variables_data(voyage_id, show_imputed=True):
    voyagenum = int(voyage_id)
    voyage = first_match(get_voyages_search_query_set().filter(var_voyage_id=voyagenum))
    if voyage is None:
        return None, []
    # Apply the matching method (if there is one) in the display_method_details dict for each variable value in the voyage and return a dict of varname: varvalue
    voyagevariables = voyage.get_stored_fields()
    #for vname, vvalue in voyage.get_stored_fields().items():
    #    voyagevariables[vname] = globals.display_methods_details.get(vname, globals.no_mangle)(vvalue, voyagenum)
    allvargroups = groupby(globals.var_dict, key=lambda x: x['var_category'])
    allvars = []
    for i in allvargroups:
        group = i[0]
        glist = list([x for x in i[1] if show_imputed or not x['var_full_name'].endswith('*')])
        for idx,j in enumerate(glist):
            val = unicode("")
            if voyagevariables[j['var_name']]:
                mangle_method = globals.display_unmangle_methods.get(j['var_name'], globals.default_prettifier(j['var_name']))
                val = unicode(mangle_method(voyagevariables[j['var_name']], voyagenum))
            if val == u'[]': val = u''
            if idx == 0:
                # For the first variable, give the number of variables in the group, and give the name of the group as a tuple in the first entry of the triple for the row
                allvars.append(((len(glist), unicode(group)), unicode(j['var_full_name']), val, j['var_name']))
            else:
                allvars.append(((None, None), unicode(j['var_full_name']), val, j['var_name']))
    return voyage, allvars

def voyage_variables(request, voyage_id):
    """
    Displays all the variables for a single voyage
    """
    (voyage, allvars) = voyage_variables_data(voyage_id)

    return render(request, "voyage_info.html",
                  {'voyage_variables': allvars,
                   'voyage': voyage,
                   'tab': 'variables',
                   'voyage_id': voyage_id})

def reload_cache(request):
    VoyageCache.load(True)
    return HttpResponse("Voyages cache reloaded")

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@gzip_page
def search(request):
    """
    Handles the Search the Database part
    """
    no_result = False
    to_reset_form = False
    query_dict = {}
    result_data = {}
    search_forms = []
    tab = 'result'
    result_data['summary_statistics_columns'] = globals.summary_statistics_columns
    form_list = []
    voyage_span_first_year, voyage_span_last_year = globals.calculate_maxmin_years()
    search_url = None
    results = None
    time_frame_form = None
    results_per_page_form = None
    results_per_page = 10
    basic_list_contracted = False
    previous_queries = {}
    collabels = []
    prev_queries_open = False
    row_list = []
    table_stats_form = None

    col_totals = []
    extra_cols = 0
    num_col_labels_before = 1
    num_col_labels_total = 1
    num_row_labels = 1
    is_double_fun = False
    graphs_select_form = None
    graph_data = None
    graph_xfun_index = None
    graphs_tab = None
    graph_remove_plots_form = None
    inline_graph_png = None

    # Timeline
    timeline_data = []
    timeline_form = None
    timeline_chart_settings = {}

    order_by_field = request.session.get('voyages_order_by_field', 'var_voyage_id')
    sort_direction = request.session.get('voyages_sort_direction', 'asc')

    # Map
    map_year = '1750'

    # Check if we are restoring POST data from session,
    # which is what would happen when accessing a permalink.
    if 'voyages_post_data' in request.session:
        request.method = 'POST'
        request.POST = request.session.pop('voyages_post_data')

    # If there is no requested page number, serve 1
    current_page = 1
    desired_page = request.POST.get('desired_page')
    if desired_page:
        current_page = desired_page

    submitVal = request.POST.get('submitVal')

    if 'submit_val' in request.GET:
        submitVal = request.GET['submit_val']

    # If session has expired (no search activity for the last globals.session_expire_minutes time) then clear the previous queries
    old_time = request.session.get('last_access_time', 0.0)
    if old_time < (time.time() - (globals.session_expire_minutes * 60.0)):
        #request.session.clear()
        request.session['previous_queries'] = []

    request.session['last_access_time'] = time.time()

    # if used_variable_names or the pair of time_span_from_year and time_span_to_year keys are in request.GET,
    # then that means that it is a query url and we should get the query from it.
    # or if it is restore_prev_query, then restore it from the session.
    if ((request.method == "GET"
         and ('used_variable_names' in request.GET
              or ('time_span_from_year' in request.GET
                  and 'time_span_to_year' in request.GET)))
        or submitVal == 'restore_prev_query'):
        # Search parameters were specified in the url
        var_list = {}
        results_per_page_form = ResultsPerPageOptionForm()
        if submitVal == 'restore_prev_query':
            qnum = int(request.POST.get('prev_query_num', request.GET.get('prev_query_num')))
            if 'prev_query_num' in request.GET:
                current_page = request.session.get('current_page', 0)
                results_per_page_form.fields['option'].initial = request.session.get('results_per_page_choice', '1')
                results_per_page = dict(results_per_page_form.fields['option'].choices)[request.session.get('results_per_page_choice', '1')]
            qprev = request.session.get('previous_queries', [])
            if 0 <= qnum < len(qprev):
                var_list = qprev[qnum]
                qprev.remove(qprev[qnum])
            request.session['previous_queries'] = qprev
            prev_queries_open = True
        else:
            var_list = create_var_list_from_url(request.GET)
        if 'previous_queries' not in request.session:
            request.session['previous_queries'] = []
        request.session['previous_queries'] = [var_list] + request.session['previous_queries']
        form_list = create_query_forms()
        var_name_indexes = {}
        for idx, form in enumerate(form_list):
            var_name_indexes[form['var_name']] = idx
        filled_form_list = create_forms_from_var_list(var_list)
        to_remove_numbers = []
        for form in filled_form_list:
            to_remove_numbers.append(var_name_indexes[form['var_name']])
            form_list.append(form)
        for idx in sorted(to_remove_numbers, reverse=True):
            del form_list[idx]
        time_frame_form = TimeFrameSpanSearchForm(initial={'frame_from_year': var_list.get('time_span_from_year', voyage_span_first_year),
                                                           'frame_to_year': var_list.get('time_span_to_year', voyage_span_last_year)})
        query_dict = create_query_dict(var_list)
        results = perform_search(query_dict, None, order_by_field, sort_direction, request.LANGUAGE_CODE)
        search_url = request.build_absolute_uri(reverse('voyage:search',)) + "?" + urllib.urlencode(var_list)
        
    elif request.method == "GET" or request.POST.get('submitVal') == 'reset':
        # A new search is being performed
        # Clear session keys.
        for key in reset_fields:
            request.session.pop(key, None)
        results_per_page_form = ResultsPerPageOptionForm()
        form_list = create_query_forms()
        time_frame_form = TimeFrameSpanSearchForm(initial={'frame_from_year': voyage_span_first_year,
                                                           'frame_to_year': voyage_span_last_year})
        results = get_voyages_search_query_set().order_by('var_voyage_id')
        if request.POST.get('submitVal') == 'reset':
            request.session['result_columns'] = get_new_visible_attrs(globals.default_result_columns)
    elif request.method == "POST":
        
        # A normal search is being performed, or it is on another tab, or it is downloading a file
        results_per_page_form = ResultsPerPageOptionForm(request.POST)
        if results_per_page_form.is_valid():
            results_per_page = results_per_page_form.cleaned_option()
            request.session['results_per_page_choice'] = results_per_page_form.cleaned_data['option']
            request.session['results_per_page'] = results_per_page
        elif 'results_per_page' in request.session and 'results_per_page_choice' in request.session:
            results_per_page = request.session['results_per_page']
            results_per_page_form.fields['option'].initial = request.session['results_per_page_choice']
            results_per_page_form = ResultsPerPageOptionForm({u'option': request.session['results_per_page_choice']})
        display_columns = get_new_visible_attrs(globals.default_result_columns)
        if 'result_columns' in request.session:
            display_columns = request.session['result_columns']
        
        ble = request.POST.get('basic_list_expanded')
        basic_list_contracted = not ble

        form_list = retrieve_post_search_forms(request.POST)
        time_frame_form = TimeFrameSpanSearchForm(request.POST)
        var_list = create_var_dict(form_list, time_frame_form)
        if 'previous_queries' not in request.session:
            request.session['previous_queries'] = []
        if submitVal != 'delete_prev_query':
            if len(request.session['previous_queries']) < 1 or not request.session['previous_queries'][0] == var_list:
                request.session['previous_queries'] = [var_list] + request.session['previous_queries']
        search_url = request.build_absolute_uri(reverse('voyage:search',)) + "?" + urllib.urlencode(var_list)
        query_dict = create_query_dict(var_list)

        order_by_field = request.POST.get('order_by_field', order_by_field)
        sort_direction = request.POST.get('sort_direction', sort_direction)
        request.session['voyages_order_by_field'] = order_by_field
        request.session['voyages_sort_direction'] = sort_direction
        results = perform_search(query_dict, None, order_by_field, sort_direction, request.LANGUAGE_CODE)
        
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
        elif (submitVal is not None and submitVal.startswith("tab_tables")) or submitVal == 'xls_download_table':
            # row_cell_values is what is displayed in the cells in the table,
            # it is a list of triples which contain the row_label, the cell values, then the row total
            # rowlabels is a list of lists of row label tuples (e.g. there is the region and the port).
            # Typically these will just be a list of lists with one entry that is the label tuple for that row/
            # column labels is similar, but it is a list of column label lists,
            # and will typically be a list of one element that is a list of the column label tuples
            # entries in the rowlabels/collabels matrix are tuples
            # that contain the label and then the row/column span of that cell.
            # Most of the time the row/column span will just be 1.
            xls_table = []
            tab = 'tables'
            pst = {x: y for x, y in request.POST.items()}

            # Try to retrieve sessions values
            tables_columns = request.session.get('voyages_tables_columns')
            tables_rows = request.session.get('voyages_tables_rows')
            tables_cells = request.session.get('voyages_tables_cells')
            omit_empty = request.session.get('voyages_tables_omit')

            # Collect settings (if possible retrieve from the session)
            if 'columns' not in pst and tables_columns:
                # Stored in session, retrieve
                pst['columns'] = tables_columns
            elif 'columns' not in pst:
                # Not in session, set default
                pst['columns'] = '7'

            if 'rows' not in pst and tables_rows:
                pst['rows'] = tables_rows
            elif 'rows' not in pst:
                pst['rows'] = '12'

            if 'cells' not in pst and tables_cells:
                pst['cells'] = tables_cells
            elif 'cells' not in pst:
                pst['cells'] = '1'

            if submitVal == "tab_tables_in":
                if omit_empty is True and 'omit_empty' not in pst:
                    omit_empty = False
                elif not omit_empty and 'omit_empty' in pst:
                    omit_empty = True
            else:
                if omit_empty is None:
                    omit_empty = True

            pst['omit_empty'] = omit_empty
            request.session['voyages_tables_omit'] = omit_empty

            # Update sessions with updated values
            request.session['voyages_tables_columns'] = pst['columns']
            request.session['voyages_tables_rows'] = pst['rows']
            request.session['voyages_tables_cells'] = pst['cells']

            table_stats_form = TableSelectionForm(pst)
            table_row_query_def = globals.table_rows[12]
            table_col_query_def = globals.table_columns[7]
            display_function = globals.table_functions[1][1]
            display_fun_name = globals.table_functions[1][0]
            if table_stats_form.is_valid():
                # If form is valid, collect all necessary settings: column, row and cell variables
                table_row_query_def = globals.table_rows[int(table_stats_form.cleaned_data['rows'])]
                table_col_query_def = globals.table_columns[int(table_stats_form.cleaned_data['columns'])]
                display_function = globals.table_functions[int(table_stats_form.cleaned_data['cells'])][1]
                display_fun_name = globals.table_functions[int(table_stats_form.cleaned_data['cells'])][0]
                table_stats_form.omit_empty = omit_empty

            restrict_query = {}
            # Get the variable name of the variable used to filter the rows
            # so we can constrain the column totals to voyages with the row variable defined
            table_row_var_name = ''
            if len(table_row_query_def[1]) > 0:
                # The query def is a triple with the 2nd element being a list
                # that list is a list of tuples with the label and the query dict
                # the query dict is a dictionary with 1 element which the key is the var name with a '__'
                # and then the query type (e.g. "__exact")
                table_row_var_name = table_row_query_def[1][0][1].keys()[0].split('__')[0]
            table_row_var = search_var_dict(table_row_var_name)
            if not table_row_var:
                for var in globals.additional_var_dict:
                    if var['var_name'] == table_row_var_name:
                        table_row_var = var
            if table_row_var:
                if table_row_var['var_type'] == 'numeric':
                    restrict_query[table_row_var_name + "__gte"] = -1
                elif table_row_var['var_type'] == 'date':
                    restrict_query[table_row_var_name + "__gte"] = date(1 , 1, 1)
                else:
                    restrict_query[table_row_var_name + "__gte"] = ""
            elif table_row_var_name.endswith('_idnum'):
                restrict_query[table_row_var_name + "__gte"] = "-1"
            elif table_row_var_name != '':
                restrict_query[table_row_var_name + "__gte"] = ""

            # Get the variable name for the column
            table_col_var_name = ''
            if len(table_col_query_def[1]) > 0:
                table_col_var_name = table_col_query_def[1][0].keys()[0].split('__')[0]
            table_col_var = search_var_dict(table_col_var_name)
            if not table_col_var:
                for var in globals.additional_var_dict:
                    if var['var_name'] == table_col_var_name:
                        table_col_var = var
            if table_col_var:
                if table_col_var['var_type'] == 'numeric':
                    restrict_query[table_col_var_name + "__gte"] = -1
                elif table_col_var['var_type'] == 'date':
                    restrict_query[table_col_var_name + "__gte"] = date(1,1,1)
                else:
                    restrict_query[table_col_var_name + "__gte"] = ""
            elif table_col_var_name.endswith('_idnum'):
                restrict_query[table_col_var_name + "__gte"] = "-1"
            elif table_col_var_name != '':
                restrict_query[table_col_var_name  + "__gte"] = ""

            tableresults = results.filter(**restrict_query)

            extra_cols = table_row_query_def[2]
            cell_values = []
            used_col_query_sets = []

            # Transform tuples to lists
            listed_cols = [map(list, k) for k in table_col_query_def[2]]

            # Create column labels
            collabels = [[j for j in i] for i in listed_cols]

            num_col_labels_total = len(collabels)
            num_row_labels = extra_cols + 1
            remove_cols = []
            if display_fun_name in globals.double_functions:
                is_double_fun = True

            for idx, colquery in enumerate(table_col_query_def[1]):
                colqueryset = tableresults.filter(**colquery)
                if omit_empty and colqueryset.count() == 0:

                    # Find column label that matches, then find the parent labels that match
                    # Generate the list of subcolumns for the parent column label
                    remove_cols.insert(0, idx)
                else:
                    if is_double_fun:
                        display_col_total = display_function(colqueryset, None, colqueryset, tableresults)
                        col_totals.append(display_col_total[0])
                        col_totals.append(display_col_total[1])
                    else:
                        col_totals.append(display_function(colqueryset, None, colqueryset, tableresults))
                    used_col_query_sets.append((colquery, colqueryset))
            for col in remove_cols:
                for idt, collbllist in enumerate(collabels):
                    idy=0
                    for idc, colstuff in enumerate(collbllist):
                        if col >= idy and col < idy + colstuff[1]:
                            collabels[idt][idc] = [colstuff[0], colstuff[1] - 1]
                        idy += colstuff[1]
            remove_rows = []
            if is_double_fun:
                collabels = [[[j, k*2] for j, k in i] for i in collabels]
                lastcol = []
                for i in collabels[-1]:
                    lastcol.append(['Embarked', i[1]/2])
                    lastcol.append(['Disembarked', i[1]/2])
                collabels.append(lastcol)
            num_col_labels_before = len(collabels)
            xls_row = []
            for idx, i in enumerate(collabels):
                xls_row = []
                for j in range(num_row_labels):
                    xls_row.append('')
                for lbl, num in i:
                    if num > 0:
                        xls_row.append(lbl)
                        for j in range(num - 1):
                            xls_row.append('')
                xls_table.append(xls_row)
                if idx == 0:
                    if is_double_fun:
                        xls_row.append('Total Embarked')
                        xls_row.append('Total Disembarked')
                    else:
                        xls_row.append('Totals')

            for idx, rowstuff in enumerate(table_row_query_def[1]):
                xls_row = []
                rowlabels = rowstuff[0]
                rowquery = rowstuff[1]
                rowqueryset = tableresults.filter(**rowquery)
                if omit_empty and rowqueryset.count() == 0:
                    remove_rows.insert(0, idx)
                row_cell_values = []
                # Iterate through column labels to make the labels for the xls download
                for colquery, colqueryset in used_col_query_sets:
                    cell_queryset = rowqueryset
                    if rowqueryset.count() > 0:
                        cell_queryset = rowqueryset.filter(**colquery)

                    if is_double_fun:
                        display_result = display_function(cell_queryset, rowqueryset, colqueryset, tableresults)
                        row_cell_values.append(display_result[0])
                        row_cell_values.append(display_result[1])
                        if display_result[0] != None:
                            xls_row.append(display_result[0])
                        else:
                            xls_row.append('')
                        if display_result[1] != None:
                            xls_row.append(display_result[1])
                        else:
                            xls_row.append('')
                    else:
                        display_result = display_function(cell_queryset, rowqueryset, colqueryset, tableresults)
                        row_cell_values.append(display_result)
                        if display_result != None:
                            xls_row.append(display_result)
                        else:
                            xls_row.append('')
                cell_values.append(row_cell_values)
                row_total = display_function(rowqueryset, rowqueryset, None, tableresults)
                row_list.append([[(i[0], i[1]) for i in rowlabels], row_cell_values, row_total,])
                if is_double_fun:
                    if row_total[0] != None:
                        xls_row.append(row_total[0])
                    else:
                        xls_row.append('')
                    if row_total[1] != None:
                        xls_row.append(row_total[1])
                    else:
                        xls_row.append('')
                else:
                    if row_total != None:
                        xls_row.append(row_total)
                    else:
                        xls_row.append('')
                xls_table.append(xls_row)
                #cell_displays.append((rowlbl, row_cell_displays, row_total))
            for rownum in remove_rows:
                xls_table.pop(rownum + num_col_labels_before)
                row_counters = [0,0,0]
                count1 = 0
                count2 = 0
                row_list[rownum] = ([(i[0], i[1] - 1) for i in row_list[rownum][0]],
                                    row_list[rownum][1], row_list[rownum][2])
                # Now find the rows with the headers for it and reduce those header counts by 1
                for idx, rl in enumerate(row_list):
                    rowlbl = [i for i in rl[0]]
                    for idy, i in enumerate(rowlbl):
                        # Don't handle the case for the rownum, since that has already been decremented
                        if idx < rownum and idx + i[1] > rownum:
                            row_list[idx][0][idy] = (row_list[idx][0][idy][0], row_list[idx][0][idy][1] - 1)
                # Now handle the case when this row we are removing has headers of its own
                rowlbl = [i for i in row_list[rownum][0]]
                rowlbl.reverse()
                for lbl, num in rowlbl:
                    if num > 0:
                        row_list[rownum+1][0].insert(0, (lbl, num))
                row_list.pop(rownum)
            for idx, row in enumerate(row_list):
                rowlbl = [i for i in row[0]]
                for i in range(num_row_labels - len(rowlbl)):
                    xls_table[idx+num_col_labels_before].insert(0, '')
                rowlbl.reverse()
                for i in rowlbl:
                    xls_table[idx+num_col_labels_before].insert(num_row_labels - len(rowlbl), i[0])
            if is_double_fun:
                grand_total_value = display_function(tableresults, None, None, tableresults)
                col_totals.append(grand_total_value[0])
                col_totals.append(grand_total_value[1])
            else:
                col_totals.append(display_function(tableresults, None, None, tableresults))
            xls_row = []
            for i in range(num_row_labels):
                if i == 0:
                    xls_row.append('Totals')
                else:
                    xls_row.append('')
            for i in col_totals:
                if i != None:
                    xls_row.append(i)
                else:
                    xls_row.append('')
            xls_table.append(xls_row)
            if 'xls_download_table' == submitVal:
                response = HttpResponse(
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
                wb = Workbook()
                ws = wb.active
                for idx, i in enumerate(xls_table):
                    for idy, j in enumerate(i):
                        ws.cell(row=idx+1,column=idy+1).value = j
                wb.save(response)
                return response

            # If empty, check if any columns need to be removed
            # TODO: Temporarily commented (waiting for David's response.
            #if omit_empty:
            #    remove_empty_columns(0, row_list, collabels, col_totals)

        elif submitVal and submitVal.startswith('tab_graphs'):
            tab = 'graphs'
            # Each tab name is encoded by 3 characters (lin, bar, pie)
            # representing the types of graphs supported.
            graphs_tab = submitVal[:len('tab_graphs_???')]
            if graphs_tab not in ['tab_graphs_lin', 'tab_graphs_bar', 'tab_graphs_pie']:
                graphs_tab = request.session.get('selected_graphs_tab', 'tab_graphs_lin')
            request.session['selected_graphs_tab'] = graphs_tab
            session_defs_key = graphs_tab + '_defs'
            # Default value for x-axis or session stored value (if any).
            xind = request.session.get(session_defs_key + '_x_ind', 0)
            yind = request.session.get(session_defs_key + '_y_ind', 0)
            # Handle adding a y-function or simply changing the x-function.
            xfuns = graphs.graphs_x_axes if graphs_tab == 'tab_graphs_lin' else \
                graphs.other_graphs_x_axes
            graphs_form_params = {'data': request.POST, 'prefix': graphs_tab, 'xfunctions': xfuns}
            if graphs_tab == 'tab_graphs_pie':
                graphs_form_params['xfield_label'] = 'Sectors'
                graphs_form_params['yfield_label'] = 'Values'
            graphs_select_form = GraphSelectionForm(**graphs_form_params)
            if graphs_select_form.is_valid():
                # Form is valid and we should use the xy-axes specified by it.
                xind = int(graphs_select_form.cleaned_data['xselect'])
                yind = int(graphs_select_form.cleaned_data['yselect'])
            else:
                graphs_form_params.pop('data', None)
                graphs_form_params['initial'] = {'xselect': xind, 'yselect': yind}
                graphs_select_form = GraphSelectionForm(**graphs_form_params)
            # Recall y-axes stored in session (if any).
            y_axes = set(request.session.get(session_defs_key, [yind]))
            if submitVal.endswith('_add') and yind not in y_axes:
                y_axes.add(yind)
            if (submitVal.endswith('_show') and len(y_axes) == 0) or graphs_tab == 'tab_graphs_pie':
                y_axes = set([yind])

            # Create form allowing the user to remove selected y-functions.
            remove_plots_list = []
            for yid in y_axes:
                remove_plots_list.append((graphs.graphs_y_axes[yid].description, yid))
            graph_remove_plots_form = GraphRemovePlotForm(remove_plots_list, request.POST)

            # Handle removing a y-function.
            if submitVal.endswith('_remove'):
                for yid in graph_remove_plots_form.get_to_del():
                    y_axes.remove(yid)
                    graph_remove_plots_form.fields.pop(str(yid))
            request.session[session_defs_key] = y_axes
            request.session[session_defs_key + '_x_ind'] = xind
            request.session[session_defs_key + '_y_ind'] = yind

            # Fetch graph data and pass it to the View template.
            graph_xfun_index = xind
            graph_data = get_graph_data(results, xfuns[xind], [graphs_y_axes[yind] for yind in y_axes])
        elif submitVal == 'tab_timeline':
            tab = 'timeline'

            timeline_form = TimelineVariableForm(request.POST)
            try:
                timeline_form_in_session = request.session['voyage_timeline_form_option']
            except:
                timeline_form_in_session = None

            if timeline_form.is_valid():
                # If any choice passed, get chosen index and get selected tuple
                timeline_selected_var_index = int(timeline_form.cleaned_data['variable_select'])
                timeline_selected_tuple = globals.voyage_timeline_variables[timeline_selected_var_index]
            elif timeline_form_in_session is not None and timeline_form_in_session.is_valid():
                # If option is stored in the session
                timeline_form = timeline_form_in_session
                timeline_selected_var_index = int(timeline_form.cleaned_data['variable_select'])
                timeline_selected_tuple = globals.voyage_timeline_variables[timeline_selected_var_index]
            else:
                # Otherwise, it's the first time when timeline is loaded
                timeline_form = TimelineVariableForm(initial={'variable_select': '15'})
                timeline_selected_tuple = globals.voyage_timeline_variables[15]

            request.session['voyage_timeline_form_option'] = timeline_form

            # Get set based on choice
            timeline_data = timeline_selected_tuple[2](results,
                                                       timeline_selected_tuple[3])

            if request.POST is not None and "download" in request.POST:
                return download_xls([[("Year", 1), (timeline_selected_tuple[1], 1)]], timeline_data)

            timeline_chart_settings['name'] = timeline_selected_tuple[1]
            if len(timeline_selected_tuple) > 4:
                # Include extra dict if exists
                timeline_chart_settings = dict(timeline_chart_settings.items() + timeline_selected_tuple[4].items())

        elif submitVal == 'tab_maps' or submitVal == 'tab_animation':
            tab = submitVal[4:]
            frame_from_year = int(request.POST.get('frame_from_year', voyage_span_first_year))
            frame_to_year = int(request.POST.get('frame_to_year', voyage_span_last_year))
            map_year = get_map_year(frame_from_year, frame_to_year)
        elif submitVal == 'map_ajax':
            map_ports = {}
            map_flows = {}

            def add_port(geo):
                result = geo is not None and geo[0].show and geo[1].show and geo[2].show
                if result and not geo[0].pk in map_ports:
                    map_ports[geo[0].pk] = geo
                return result

            def add_flow(source, destination, embarked, disembarked):
                result = embarked is not None and disembarked is not None and add_port(source) and add_port(destination)
                if result:
                    flow_key = long(source[0].pk) * 2147483647 + long(destination[0].pk)
                    current = map_flows.get(flow_key)
                    if current is not None:
                        embarked += current[2]
                        disembarked += current[3]
                    map_flows[flow_key] = (source[0].name, destination[0].name, embarked, disembarked)
                return result

            # Ensure cache is loaded.
            VoyageCache.load()
            all_voyages = VoyageCache.voyages
            missed_embarked = 0
            missed_disembarked = 0
            # Set up an unspecified source that will be used if the appropriate setting is enabled
            geo_unspecified = CachedGeo(-1, -1, _('Africa, port unspecified'), 0.05, 9.34, True, None)
            source_unspecified = (geo_unspecified, geo_unspecified, geo_unspecified)
            keys = get_pks_from_haystack_results(results)
            for pk in keys:
                voyage = all_voyages.get(pk)
                if voyage is None:
                    continue
                source = CachedGeo.get_hierarchy(voyage.emb_pk)
                if source is None and settings.MAP_MISSING_SOURCE_ENABLED:
                    source = source_unspecified
                destination = CachedGeo.get_hierarchy(voyage.dis_pk)
                add_flow(
                    source,
                    destination,
                    voyage.embarked,
                    voyage.disembarked)
            if missed_embarked > 0 or missed_disembarked > 0:
                import logging
                logging.getLogger('voyages').info('Missing flow: (' + str(missed_embarked) +
                                                  ', ' + str(missed_disembarked) + ')')
            return render(request, "voyage/search_maps.datatemplate",
                          {
                              'map_ports': map_ports,
                              'map_flows': map_flows
                          }, content_type='text/javascript')
        elif submitVal == 'animation_ajax':
            VoyageCache.load()
            all_voyages = VoyageCache.voyages
            from voyages.apps.voyage.maps import VoyageRoutesCache
            all_routes = VoyageRoutesCache.load()

            def animation_response():
                keys = get_pks_from_haystack_results(results)
                for pk in keys:
                    voyage = all_voyages.get(pk)
                    if voyage is None:
                        continue
                    route = all_routes.get(pk, ([],))[0]
                    source = CachedGeo.get_hierarchy(voyage.emb_pk)
                    destination = CachedGeo.get_hierarchy(voyage.dis_pk)
                    if source is not None and destination is not None and source[0].show and \
                            destination[0].show and voyage.year is not None and \
                            voyage.embarked is not None and voyage.embarked > 0 and voyage.disembarked is not None:
                        flag = VoyageCache.nations.get(voyage.ship_nat_pk)
                        if flag is None:
                            flag = ''
                        yield '{ "voyage_id": ' + str(voyage.voyage_id) + \
                              ', "source_name": "' + _(source[0].name) + '"' + \
                              ', "source_lat": ' + str(source[0].lat) + \
                              ', "source_lng": ' + str(source[0].lng) + \
                              ', "destination_name": "' + _(destination[0].name) + '"' + \
                              ', "destination_lat": ' + str(destination[0].lat) + \
                              ', "destination_lng": ' + str(destination[0].lng) + \
                              ', "embarked": ' + str(voyage.embarked) + \
                              ', "disembarked": ' + str(voyage.disembarked) + \
                              ', "year": ' + str(voyage.year) + \
                              ', "ship_ton": ' + \
                              (str(voyage.ship_ton) if voyage.ship_ton is not None else '0') + \
                              ', "nat_id": ' + \
                              (str(voyage.ship_nat_pk) if voyage.ship_nat_pk is not None else '0') + \
                              ', "ship_nationality_name": "' + _(flag) + '"' \
                              ', "ship_name": "' + \
                              (unicode(voyage.ship_name) if voyage.ship_name is not None else '') + '"' + \
                              ', "route": ' + json.dumps(route) +\
                              ' }'
            return HttpResponse('[' + ',\n'.join(animation_response()) + ']', 'application/json')
        elif submitVal == 'download_xls_current_page':
            pageNum = request.POST.get('pageNum')
            if not pageNum:
                pageNum = 1
            return download_xls_page(results, int(pageNum), results_per_page, display_columns, var_list)
        elif submitVal == 'delete_prev_query':
            prev_query_num = int(request.POST.get('prev_query_num'))
            prevqs = request.session['previous_queries']
            prevqs.remove(prevqs[prev_query_num])
            request.session['previous_queries'] = prevqs
            prev_queries_open = True
            
    if len(results) == 0:
        no_result = True

    # Paginate results to pages
    if tab == 'result':
        paginator = Paginator(results, results_per_page)
        pagins = paginator.page(int(current_page))
        request.session['current_page'] = current_page
        # Prepare paginator ranges
        (paginator_range, pages_range) = prepare_paginator_variables(paginator, current_page, results_per_page)
        result_display = prettify_results(map(lambda x: x.get_stored_fields(), pagins), globals.display_methods)
    else:
        pagins = None
        (paginator_range, pages_range) = (None, None)
        result_display = None
    # Customize result page
    if not request.session.exists(request.session.session_key):
        request.session.create()

    # Set up the initial column of display
    if not 'result_columns' in request.session:
        request.session['result_columns'] = get_new_visible_attrs(globals.default_result_columns)
    if len(request.session.get('previous_queries', [])) > 10:
        request.session['previous_queries'] = request.session['previous_queries'][:5]

    previous_queries = enumerate(map(prettify_var_list, request.session.get('previous_queries', [])))

    return render(request, "voyage/search.html",
                  {'voyage_span_first_year': voyage_span_first_year,
                   'voyage_span_last_year': voyage_span_last_year,
                   'basic_variables': globals.basic_variables,
                   'general_variables': globals.general_variables,
                   'all_var_list': globals.var_dict,
                   'results': pagins,
                   'result_data': result_data,
                   'order_by_field': order_by_field,
                   'sort_direction': sort_direction,
                   'paginator_range': paginator_range,
                   'pages_range': pages_range,
                   'curpage': pagins,
                   'no_result': no_result,
                   'url_to_copy': search_url,
                   'tab': tab,
                   'options_results_per_page_form': results_per_page_form,
                   'form_list': form_list,
                   'time_frame_search_form': time_frame_form,
                   'result_display': result_display,
                   'basic_list_contracted': basic_list_contracted,
                   'previous_queries': previous_queries,
                   'prev_queries_open': prev_queries_open,
                   'col_labels_list': collabels,
                   'row_list': row_list,
                   'table_stats_form': table_stats_form,
                   'col_totals': col_totals,
                   'extra_cols': range(extra_cols),
                   'num_col_labels_before': num_col_labels_before, 
                   'num_col_labels_total': num_col_labels_total, 
                   'num_row_labels': num_row_labels,
                   'is_double_fun': is_double_fun,
                   'inline_graph_png': inline_graph_png,
                   'graph_remove_plots_form': graph_remove_plots_form,
                   'graph_xfun_index': graph_xfun_index,
                   'graphs_tab': graphs_tab,
                   'graphs_select_form': graphs_select_form,
                   'graph_data': graph_data,
                   'timeline_data': timeline_data,
                   'timeline_form': timeline_form,
                   'timeline_chart_settings': timeline_chart_settings,
                   'map_year': map_year
                  })

def prettify_results(results, lookup_table):
    """
    Returns a list of dictionaries keyed by variable name, prettifies the value so that it displays properly
    Uses the lookup_table which has the methods to prettify the variable based on the value and the voyage id
    The lookup_table is gotten from the globals file, either from the display_methods or the display_methods_xls
    """
    # Results must be a list of dictionaries of variable name and value
    for i in results:
        idict = {}
        voyageid = int(i['var_voyage_id'])
        for varname, varvalue in i.items():
            if varvalue:
                prettify_varvalue = lookup_table.get(varname, globals.default_prettifier(varname))
                if varvalue == u'[]': varvalue = u''
                idict[varname] = prettify_varvalue(varvalue, voyageid)
            else:
                idict[varname] = None
        yield idict

def _get_all(model):
    try:
        return list(model.objects.all())
    except:
        return []

class ChoicesCache:
    nations = _get_all(Nationality)
    particular_outcomes = _get_all(ParticularOutcome)
    slaves_outcomes = _get_all(SlavesOutcome)
    owner_outcomes = _get_all(OwnerOutcome)
    resistances = _get_all(Resistance)
    captured_outcomes = _get_all(VesselCapturedOutcome)
    rigs = _get_all(RigOfVessel)

def getChoices(varname):
    """
    Retrieve a list of two-tuple items for select boxes depending on the model
    :param varname variable name:
    :return: nested list of choices/options for that variable
    """
    choices = []
    if varname in ['var_nationality']:
        for nation in ChoicesCache.nations:
            if "/" in nation.label or "Other (specify in note)" in nation.label:
                continue
            choices.append((nation.value, _(nation.label)))
    elif varname in ['var_imputed_nationality']:
        for nation in ChoicesCache.nations:
            # imputed flags
            if nation.label in globals.list_imputed_nationality_values:
                choices.append((nation.value, _(nation.label)))
    elif varname in ['var_outcome_voyage']:
        for outcome in ChoicesCache.particular_outcomes:
            choices.append((outcome.value, _(outcome.label)))
    elif varname in ['var_outcome_slaves']:
        for outcome in ChoicesCache.slaves_outcomes:
            choices.append((outcome.value, _(outcome.label)))
    elif varname in ['var_outcome_owner']:
        for outcome in ChoicesCache.owner_outcomes:
            choices.append((outcome.value, _(outcome.label)))
    elif varname in ['var_resistance']:
        for outcome in ChoicesCache.resistances:
            choices.append((outcome.value, _(outcome.label)))
    elif varname in ['var_outcome_ship_captured']:
        for outcome in ChoicesCache.captured_outcomes:
            choices.append((outcome.value, _(outcome.label)))
    elif varname == 'var_rig_of_vessel':
        for rig in ChoicesCache.rigs:
            choices.append((rig.value, _(rig.label)))
    return choices

def putOtherLast(lst):
    others = filter(lambda x: 'other' in x['text'].lower() or 'unspecified' in x['text'].lower() or '???' in x['text'], lst)
    for rem in others:
        lst.remove(rem)
        lst.append(rem)
    return lst

def getNestedListPlaces(varname, nested_places, selected_places=[]):#, place_visible=[], region_visible=[], area_visible=[], place_selected=[], region_selected=[], area_selected=[]):
    """
    Retrieve a nested list of places sorted by broad region (area) and then region
    :param varname:
    returns a tuple of the nested choices and the choices
    """
    nestedChoices = []
    flatChoices = []

    select = [int(i) for i in selected_places]

    for area, regs in nested_places.items():
        area_content = []
        is_area_selected = True
        for reg, places in regs.items():
            reg_content = []
            is_selected = True
            for place in places:
                if place.value not in select:
                    is_selected = False
                    is_area_selected = False
                    # Why did I have this here?
#                if place.place == "???":
#                    continue
                # Selected does not need to be part of this, since the form dict will have a list of places selected that the template checks
                reg_content.append({'id': 'id_' + varname + '_2_' + str(place.pk),
                                    'text': place.place,
                                    'value': place.value})
                flatChoices.append((place.value, place.place))
            reg_content = putOtherLast(reg_content)
            area_content.append({'id': 'id_' + varname + '_1_' + str(reg.pk),
                                 'text': reg.region,
                                 'choices': reg_content,
                                 'is_selected': is_selected,
                                 'value': reg.value})
        area_content = putOtherLast(area_content)
        nestedChoices.append({'id': 'id_' + varname + '_0_' + str(area.pk),
                              'text': area.broad_region,
                              'choices': area_content,
                              'is_selected': is_area_selected,
                              'value': area.value})
    nestedChoices = putOtherLast(nestedChoices)
    
    # Check if visible parameters have been passed, if so filter
    return nestedChoices, flatChoices


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

def search_var_dict(var_name):
    for i in globals.var_dict:
        if i['var_name'] == var_name:
            return i
    return None

# Automatically fetch fields that should be sorted differently, either
# by using a translated version or a plain text version of tokenized fields.
from search_indexes import VoyageIndex
index = VoyageIndex()
plain_text_suffix = '_plaintext'
plain_text_suffix_list = [f[:-len(plain_text_suffix)] for f in index.fields.keys() if f.endswith(plain_text_suffix)]
translate_suffix = '_lang_en'
translated_field_list = [f[:-len(translate_suffix)] for f in index.fields.keys() if f.endswith(translate_suffix)]

def perform_search(query_dict, date_filters, order_by_field='var_voyage_id', sort_direction='asc', lang='en'):
    """
    Perform the actual query towards SOLR
    :param query_dict:
    :param date_filters:
    :return:
    """
    if order_by_field in plain_text_suffix_list:
        order_by_field += '_plaintext_exact'
    elif order_by_field in translated_field_list:
        order_by_field += '_lang_' + lang + '_exact'
    if sort_direction == 'desc':
        order_by_field = '-' + order_by_field
    results = get_voyages_search_query_set().filter(**query_dict).order_by(order_by_field)
    # Date filters
    return date_filter_query(date_filters, results)

# TODO: remove this function
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

def formatDate(year, month):
    """
    Format the passed year month to a YYYY,MM string
    :param year:
    :param month:
    :return:
    """
    if month == "":
        month = 1
    return date(int(year), int(month), 1)
    #return "%s,%s" % (str(year).zfill(4), str(month).zfill(2))


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
            elif elem['var_type'] == 'date':
                query[var_name + "__gte"] = date(1,1,1)
            else:
                query[var_name + "__gte"] = ""

            elem['num_voyages'] = get_voyages_search_query_set().filter(**query).count()
            tmpGroup.append(elem)

        var_list_stats.append({"var_category": key, "variables": tmpGroup})

    return var_list_stats

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


def download_xls_page(results, current_page, results_per_page, columns, var_list):
    # Download only current page
    if current_page != -1:
        paginator = Paginator(results, results_per_page)
        curpage = paginator.page(current_page)
        res = map(lambda x: x.get_stored_fields(), curpage.object_list)
    else:
        res = list(results.values(*[x[0] for x in columns]).all())
    pres = prettify_results(res, globals.display_methods_xls)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="data.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("data")
    #TODO: add query to download
    if len(var_list.get('used_variable_names', [])) > 0:
        vartxt = "; ".join([i[0] + " " + i[1] for i in prettify_var_list(var_list)])
        ws.write(0,0,label=vartxt)
    elif current_page == -1:
        ws.write(0,0,label='All Records')
    else:
        ws.write(0,0,label='Current Page')
    for idx, column in enumerate(columns):
        ws.write(1,idx,label=get_spss_name(column[0]))

    for idx, item in enumerate(pres):
        for idy, column in enumerate(columns):
            data = item[column[0]]
            if data is None:
                ws.write(idx+2,idy,label="")
            elif isinstance(data, (int, long, float)):
                ws.write(idx+2,idy,label=data)
            else:
                ws.write(idx+2,idy,label=data.encode("utf-8"))

    wb.save(response)

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

        results = perform_search(query_dict, date_filters, lang=request.LANGUAGE_CODE)

        if len(results) == 0:
            no_result = True
            results = []
    else:
        results = get_voyages_search_query_set().order_by('var_voyage_id')

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
        stats = results.stats(item['var_name']).stats_results().get(item['var_name'])

        if item['has_total'] and stats:
            tmp_row.append(int(stats['sum']))
        else:
            tmp_row.append("")

        # Number of voyages
        count = 0
        if stats:
            count = int(stats['count'])
            tmp_row.append(count)
        else:
            tmp_row.append("")

        if stats and count > 0:
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


def remove_empty_columns(index, row_list, collabels, col_totals):
    finish = True

    # Check if any has to be removed
    for i in range(index, len(col_totals)-1):
        if col_totals[i] == 0:
            index = i
            finish = False
            break

    # If not, finish
    if finish:
        return

    # Remove column in row_list (values)
    for i in row_list:
        del i[1][index]

    # Remove total column
    del col_totals[index]

    # Remove port and any parents if needed
    # Port
    current_index = 1
    for ind, value in enumerate(collabels[-1]):
        if value[1] == 1 and current_index == index+1:
            del collabels[-1][ind]
            break
        elif value[1] == 1:
            current_index += 1

    # If there is more (parents), check then and remove if necessary
    # Start from first parent and go to grandparents if necessary
    depth = len(collabels) - 2

    # As long as parent exists
    while depth > -1:
        current_list = collabels[depth]

        # val - keep adding values of parents
        # count_items - counting how many items (parents) already checked
        val = 1
        count_items = 0

        for i, value in enumerate(current_list):
            # Check only items that are displayed (>1)
            if value[1] > 0:
                # Increment counter of items
                count_items += 1

                # If wanted index is in between of the current val and less than val+next, found
                if current_index >= val and current_index < val + value[1]:

                    # Decrement current parent value
                    value[1] -= 1

                    # If 0, remove it
                    if value[1] == 0:
                        del collabels[depth][i]
                        depth -= 1
                    else:
                        depth -= 1

                    # Go to the next parents if needed
                    break
                else:
                    val += value[1]

    remove_empty_columns(index+1, row_list, collabels, col_totals)

def get_permanent_link(request):
    """
    Obtain a permanent link for the current search query.
    :param request: The request containing the search quer
    :param request: The request containing the search query.
    :return: A permanent URL link for that exact query.
    """
    from voyages.apps.common.models import SavedQuery
    saved_query = SavedQuery()
    return saved_query.get_link(request, 'restore_v_permalink')

def restore_permalink(request, link_id):
    """
    Fetch the query corresponding to the link id and redirect to the
    search results of that query.
    :param request: web request
    :param link_id: the id of the permanent link
    :return: a Redirect to the Voyages search page after setting the session POST data to match the permalink
    or an Http404 error if the link is not found.
    """
    # from voyages.apps.common.models import SavedQuery
    # return SavedQuery.restore_link(link_id, request.session, 'voyages_post_data', 'voyage:search')
    return redirect("/voyage/database#searchId=" + link_id)

def debug_permalink(request, link_id):
    from voyages.apps.common.models import SavedQuery
    from django.shortcuts import get_object_or_404
    from django.http import HttpResponse
    permalink = get_object_or_404(SavedQuery, pk=link_id)
    return HttpResponse(permalink.query, content_type='text/plain')
