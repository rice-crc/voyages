# -*- coding: utf-8 -*-
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
import xlwt
from openpyxl import Workbook
import urllib
import unidecode
from itertools import groupby
from django.views.decorators.gzip import gzip_page
from datetime import date

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

def create_query_forms():
    """
    Uses the list of variables in globals.py and creates a form
    for each of them that is either a basic or a general variable
    Returns a list of dictionaries containing the var_name, var_full_name, form
    """
    voyage_span_first_year, voyage_span_last_year = calculate_maxmin_years()
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
            print "WARNING: variable not in any form type lists: %s" % varname
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
            print "WARNING: variable not in any form type lists: %s" % varname
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
        mangle_method = globals.search_mangle_methods.get(varname, globals.no_mangle)
        if varname == 'var_sources':
            query_dict[varname + "__startswith"] = mangle_method(var_list[varname + '_text_search'])
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
        output.append(('Time frame:', unicode(varlist['time_span_from_year']) + ' - ' + unicode(varlist['time_span_to_year'])))
    for kvar, vvar in qdict.items():
        varname = kvar.split('__')[0]
        is_real_var = False
        fullname = ''
        for var in globals.var_dict:
            if varname == var['var_name']:
                fullname = var['var_full_name']
                is_real_var = True
                break
            elif varname[-6:] == '_idnum' and varname[:-6] == var['var_name']:
                fullname = var['var_full_name']
                is_real_var = True
                break
        if not is_real_var:
            # it is a month variable
            varn = varname[:-7]
            for var in globals.var_dict:
                if varn == var['var_name']:
                    fullname = var['var_full_name']
                    break
            month_dict = {}
            for monnum, monval in globals.list_months:
                month_dict[int(monnum)] = monval
            output.append((fullname + " month:", ', '.join([month_dict[int(i)] for i in vvar])))
            continue
        unmangle_method = globals.parameter_unmangle_methods.get(varname, globals.no_mangle)
        tvar = unmangle_method(vvar)
        value = unicode(tvar)
        if isinstance(tvar, (list, tuple)):
            value = unicode(u', '.join(map(unicode, tvar)))
        prefix = ''
        if (varname + '_options') in varlist:
            opt = varlist[varname + '_options']
            if opt == '1' and len(vvar) >= 2:
                if varname == 'var_imp_arrival_at_port_of_dis':
                    value = 'between ' + unicode(tvar[0]) + ' and ' + unicode(tvar[1])
                elif varname in globals.list_date_fields:
                    tod = None
                    if vvar[1].month == 1:
                        tod = date(vvar[1].year - 1, 12, vvar[1].day)
                    else:
                        tod = date(vvar[1].year, vvar[1].month - 1, vvar[1].day)
                    value = 'between ' + unicode(unmangle_method(vvar[0])) + ' and ' + unicode(unmangle_method(tod))
                else:
                    value = 'between ' + unicode(tvar[0]) + ' and ' + unicode(tvar[1])
            elif opt == '4':
                if isinstance(vvar, (list, tuple)):
                    value = 'in ' + unicode(unmangle_method(vvar[0]))
                else:
                    value = 'equal to ' + unicode(tvar)
            elif isinstance(vvar, (list, tuple)):
                continue
            elif opt == '2':
                if varname == 'var_imp_arrival_at_port_of_dis':
                    value = 'before ' + unicode(tvar)
                elif varname in globals.list_date_fields:
                    tod = None
                    if vvar.month == 1:
                        tod = date(vvar.year - 1, 12, vvar.day)
                    else:
                        tod = date(vvar.year, vvar.month - 1, vvar.day)
                    value = 'before ' + unicode(unmangle_method(tod))
                else:
                    value = 'at most ' + unicode(tvar)
            elif opt == '3':
                if varname == 'var_imp_arrival_at_port_of_dis':
                    value = 'after ' + unicode(tvar)
                elif varname in globals.list_date_fields:
                    value = 'after ' + unicode(tvar)
                else:
                    value = 'at least ' + unicode(tvar)
        # Prevent display of 'Year arrived with slaves*' when it is just the time frame
        if not (isinstance(vvar, (list, tuple)) and varname in globals.list_numeric_fields and not ((varname + '_options') in varlist)):
            output.append((fullname + ":", (prefix + value)))
    return output

def voyage_map(request, voyage_id):
    """
    Displays the map for a voyage
    """
    voyage = SearchQuerySet().models(Voyage).filter(var_voyage_id=int(voyage_id))[0]
    return render(request, "voyage/voyage_info.html",
                  {'tab': 'map',
                   'voyage_id': voyage_id,
                   'voyage': voyage})

def voyage_images(request, voyage_id):
    """
    Displays the images for a voyage
    """
    voyage = SearchQuerySet().models(Voyage).filter(var_voyage_id=int(voyage_id))[0]
    return render(request, "voyage/voyage_info.html",
                  {'tab': 'images',
                   'voyage_id': voyage_id,
                   'voyage': voyage})
    
def voyage_variables(request, voyage_id):
    """
    Displays all the variables for a single voyage
    """
    voyagenum = int(voyage_id)
    voyage = SearchQuerySet().models(Voyage).filter(var_voyage_id=voyagenum)[0]
    # Apply the matching method (if there is one) in the display_method_details dict for each variable value in the voyage and return a dict of varname: varvalue
    voyagevariables = {}
    for vname, vvalue in voyage.get_stored_fields().items():
        voyagevariables[vname] = globals.display_methods_details.get(vname, globals.no_mangle)(vvalue, voyagenum)
    allvargroups = groupby(globals.var_dict, key=lambda x: x['var_category'])
    allvars = []
    for i in allvargroups:
        group = i[0]
        gvalues = i[1]
        glist = list(gvalues)
        for idx,j in enumerate(glist):
            val = unicode("")
            if voyagevariables[j['var_name']]:
                mangle_method = globals.display_unmangle_methods.get(j['var_name'], globals.no_mangle)
                val = unicode(mangle_method(voyagevariables[j['var_name']]))
            if idx == 0:
                # For the first variable, give the number of variables in the group, and give the name of the group as a tuple in the first entry of the triple for the row
                allvars.append(((len(glist),unicode(group)),unicode(j['var_full_name']),val))
            else:
                allvars.append(((None,None,),unicode(j['var_full_name']),val))

    return render(request, "voyage/voyage_info.html",
                  {'voyage_variables': allvars,
                   'voyage': voyage,
                   'tab': 'variables',
                   'voyage_id': voyage_id})

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
    voyage_span_first_year, voyage_span_last_year = calculate_maxmin_years()
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
    graphs_xy_select_form = None
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
        time_frame_form = TimeFrameSpanSearchForm(initial={'frame_from_year': var_list['time_span_from_year'],
                                                           'frame_to_year': var_list['time_span_to_year']})
        query_dict = create_query_dict(var_list)
        results = perform_search(query_dict, None)
        search_url = request.build_absolute_uri(reverse('voyage:search',)) + "?" + urllib.urlencode(var_list)
        
    elif request.method == "GET" or request.POST.get('submitVal') == 'reset':
        # A new search is being performed
        results_per_page_form = ResultsPerPageOptionForm()
        form_list = create_query_forms()
        results = SearchQuerySet().models(Voyage).order_by('var_voyage_id')
        time_frame_form = TimeFrameSpanSearchForm(initial={'frame_from_year': voyage_span_first_year,
                                                           'frame_to_year': voyage_span_last_year})
        results = SearchQuerySet().models(Voyage).order_by('var_voyage_id')
        if request.POST.get('submitVal') == 'reset':
            request.session['result_columns'] = get_new_visible_attrs(globals.default_result_columns)
    elif request.method == "POST":
        
        # A normal search is being performed, or it is on another tab, or it is downloading a file
        results_per_page_form = ResultsPerPageOptionForm(request.POST)
        if results_per_page_form.is_valid():
            results_per_page = results_per_page_form.cleaned_option()
            request.session['results_per_page_choice'] = results_per_page_form.cleaned_data['option']
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
        results = perform_search(query_dict, None)
        
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
        elif submitVal == 'tab_tables' or submitVal == 'xls_download_table':
            # row_cell_values is what is displayed in the cells in the table, it is a list of triples which contain the row_label, the cell values, then the row total
            # rowlabels is a list of lists of row label tuples (e.g. there is the region and the port). Typically these will just be a list of lists with one entry that is the label tuple for that row/
            # column labels is similar, but it is a list of column label lists, and will typically be a list of one element that is a list of the column label tuples
            #  entries in the rowlabels/collabels matrix are tuples that contain the label and then the row/column span of that cell. Most of the time the row/column span will just be 1.
            xls_table = []
            tab = 'tables'
            pst = {x: y for x,y in request.POST.items()}
            # Force the initial value
            if 'columns' not in pst:
                pst['columns'] = '1'
            if 'cells' not in request.POST:
                pst['cells'] = '1'
            if 'rows' not in request.POST:
                pst['rows'] = '12'
            table_stats_form = TableSelectionForm(pst)
            table_row_query_def = globals.table_rows[12]
            table_col_query_def = globals.table_columns[1]
            display_function = globals.table_functions[1][1]
            display_fun_name = globals.table_functions[1][0]
            omit_empty = False
            if table_stats_form.is_valid():
                table_row_query_def = globals.table_rows[int(table_stats_form.cleaned_data['rows'])]
                table_col_query_def = globals.table_columns[int(table_stats_form.cleaned_data['columns'])]
                display_function = globals.table_functions[int(table_stats_form.cleaned_data['cells'])][1]
                display_fun_name = globals.table_functions[int(table_stats_form.cleaned_data['cells'])][0]
                omit_empty = table_stats_form.cleaned_data.get('omit_empty', False)
            extra_cols = table_row_query_def[2]
            cell_values = []
            used_col_query_sets = []
            collabels = [[j for j in i] for i in table_col_query_def[2]]
            num_col_labels_total = len(collabels)
            num_row_labels = extra_cols + 1
            remove_cols = []
            if display_fun_name in globals.double_functions:
                is_double_fun = True

            for idx, colquery in enumerate(table_col_query_def[1]):
                colqueryset = results.filter(**colquery)
                if omit_empty and colqueryset.count() == 0:
                    # Find column label that matches, then find the parent labels that match
                    # Generate the list of subcolumns for the parent column label
                    remove_cols.insert(0, idx)
                else:
                    if is_double_fun:
                        display_col_total = display_function(colqueryset, None, colqueryset, results)
                        col_totals.append(display_col_total[0])
                        col_totals.append(display_col_total[1])
                    else:
                        col_totals.append(display_function(colqueryset, None, colqueryset, results))
                    used_col_query_sets.append((colquery, colqueryset))
            for col in remove_cols:
                for idt, collbllist in enumerate(collabels):
                    idy=0
                    for idc, colstuff in enumerate(collbllist):
                        if col >= idy and col < idy + colstuff[1]:
                            collabels[idt][idc] = (colstuff[0], colstuff[1] - 1)
                        idy += colstuff[1]
            remove_rows = []
            if is_double_fun:
                collabels = [[(j, k*2) for j, k in i] for i in collabels]
                lastcol = []
                for i in collabels[-1]:
                    lastcol.append(('Embarked', i[1]/2))
                    lastcol.append(('Disembarked', i[1]/2))
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
                rowqueryset = results.filter(**rowquery)
                if omit_empty and rowqueryset.count() == 0:
                    remove_rows.insert(0, idx)
                row_cell_values = []
                # Iterate through column labels to make the labels for the xls download
                for colquery, colqueryset in used_col_query_sets:
                    cell_queryset = rowqueryset
                    if rowqueryset.count() > 0:
                        cell_queryset = rowqueryset.filter(**colquery)
                    if is_double_fun:
                        display_result = display_function(cell_queryset, rowqueryset, colqueryset, results)
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
                        display_result = display_function(cell_queryset, rowqueryset, colqueryset, results)
                        row_cell_values.append(display_result)
                        if display_result != None:
                            xls_row.append(display_result)
                        else:
                            xls_row.append('')
                cell_values.append(row_cell_values)
                row_total = display_function(rowqueryset, rowqueryset, None, results)
                row_list.append(([(i[0], i[1]) for i in rowlabels], row_cell_values, row_total,))
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
#            print(list(enumerate(xls_table)))
#            print(remove_rows)
            for rownum in remove_rows:
                xls_table.pop(rownum + num_col_labels_before)
                row_counters = [0,0,0]
                count1 = 0
                count2 = 0
                row_list[rownum] = ([(i[0], i[1] - 1) for i in row_list[rownum][0]], row_list[rownum][1], row_list[rownum][2])
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
                grand_total_value = display_function(results, None, None, results)
                col_totals.append(grand_total_value[0])
                col_totals.append(grand_total_value[1])
            else:
                col_totals.append(display_function(results, None, None, results))
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
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
                wb = Workbook()
                ws = wb.active
                for idx, i in enumerate(xls_table):
                    for idy, j in enumerate(i):
                        ws.cell(row=idx,column=idy).value = unicode(j).encode('utf-8')
                wb.save(response)
                return response
        elif submitVal == 'tab_graphs':
            tab = 'graphs'
            graphs_xy_select_form = GraphXYSelectionForm(request.POST)
        elif  submitVal == 'tab_timeline':
            tab = 'timeline'
        elif submitVal == 'tab_maps':
            tab = 'maps'
        elif submitVal == 'download_xls_current_page':
            pageNum = request.POST.get('pageNum')
            if not pageNum:
                pageNum = 1
                print "Warning: unable to get page number from post"
            return download_xls_page(results, int(pageNum), results_per_page, display_columns, var_list, query_dict)
        elif submitVal == 'delete_prev_query':
            prev_query_num = int(request.POST.get('prev_query_num'))
            prevqs = request.session['previous_queries']
            prevqs.remove(prevqs[prev_query_num])
            request.session['previous_queries'] = prevqs
            prev_queries_open = True
            
    if len(results) == 0:
        no_result = True

    # Paginate results to pages
    paginator = Paginator(results, results_per_page)
    pagins = paginator.page(int(current_page))
    request.session['current_page'] = current_page
    # Prepare paginator ranges
    (paginator_range, pages_range) = prepare_paginator_variables(paginator, current_page, results_per_page)
    # Customize result page
    if not request.session.exists(request.session.session_key):
        request.session.create()

    # Set up the initial column of display
    if not 'result_columns' in request.session:
        request.session['result_columns'] = get_new_visible_attrs(globals.default_result_columns)
    if len(request.session.get('previous_queries', [])) > 10:
        request.session['previous_queries'] = request.session['previous_queries'][:5]

    previous_queries = enumerate(map(prettify_var_list, request.session.get('previous_queries', [])))
    result_display = prettify_results(pagins, globals.display_methods)
    result_display = prettify_results(pagins, globals.display_methods)

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
                   'graphs_xy_select_form': graphs_xy_select_form})

def prettify_results(results, lookup_table):
    """
    Returns a list of dictionaries keyed by variable name, prettifies the value so that it displays properly
    Uses the lookup_table which has the methods to prettify the variable based on the value and the voyage id
    The lookup_table is gotten from the globals file, either from the display_methods or the display_methods_xls
    """
    mangled = []
    for i in results:
        idict = {}
        voyageid = int(i.get_stored_fields()['var_voyage_id'])
        for varname, varvalue in i.get_stored_fields().items():
            if varvalue:
                if varname in lookup_table:
                    idict[varname] = lookup_table[varname](varvalue, voyageid)
                else:
                    idict[varname] = varvalue
            else:
                idict[varname] = None
        mangled.append(idict)
    return mangled

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
            choices.append((nation.value, nation.label))
    elif varname in ['var_imputed_nationality']:
        for nation in Nationality.objects.all():
            # imputed flags
            if nation.label in globals.list_imputed_nationality_values:
                choices.append((nation.value, nation.label))
    elif varname in ['var_outcome_voyage']:
        for outcome in ParticularOutcome.objects.all():
            choices.append((outcome.value, outcome.label))
    elif varname in ['var_outcome_slaves']:
        for outcome in SlavesOutcome.objects.all():
            choices.append((outcome.value, outcome.label))
    elif varname in ['var_outcome_owner']:
        for outcome in OwnerOutcome.objects.all():
            choices.append((outcome.value, outcome.label))
    elif varname in ['var_resistance']:
        for outcome in Resistance.objects.all():
            choices.append((outcome.value, outcome.label))
    elif varname in ['var_outcome_ship_captured']:
        for outcome in VesselCapturedOutcome.objects.all():
            choices.append((outcome.value, outcome.label))
    elif varname == 'var_rig_of_vessel':
        for rig in RigOfVessel.objects.all():
            choices.append((rig.value, rig.label))
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

def shorten_search_url(request):
    response_data = {}
    url = shorten_url(request.GET['long_url'])
    response_data['url'] = url
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def shorten_url(long_url):
    """
    Function to shorten url using google url shortening service.
    :param long_url: Long url to shorten
    If google doesn't provide url or the google url doesn't work, then it will just return the long_url
    """
    url = long_url
    try:
        payload = json.dumps({'longUrl': long_url})
        headers = {'Content-Type': 'application/json'}
        result = requests.post('https://www.googleapis.com/urlshortener/v1/url', headers=headers, data=payload)
        url = result.json().get('id', long_url)
    except:
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
    # TODO: change this to have Voyage before filter
    results = SearchQuerySet().filter(**query_dict).models(Voyage).order_by('var_voyage_id')
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


def download_xls_page(results, current_page, results_per_page, columns, var_list, query_dict):
    # Download only current page
    res = results
    if current_page != -1:
        paginator = Paginator(results, results_per_page)
        curpage = paginator.page(current_page)
        res = curpage.object_list
    res = prettify_results(res, globals.display_methods_xls)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="data.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("data")
    #TODO: add query to download
    if len(var_list.get('used_variable_names', [])) > 0:
        ws.write(0,0,label=extract_query_for_download(query_dict, []))
    else:
        ws.write(0,0,label='All Records')
    for idx, column in enumerate(columns):
        ws.write(1,idx,label=get_spss_name(column[0]))

    for idx, item in enumerate(res):
        #stored_fields = item.get_stored_fields()
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
