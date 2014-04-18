# -*- coding: utf-8 -*-
# List of basic variables
from django.utils.datastructures import SortedDict
import models
import lxml.html
import re
from datetime import date

session_expire_minutes = 60

list_imputed_nationality_values = ['Spain / Uruguay', 'Portugal / Brazil', 'Great Britain',
                                   'Netherlands', 'U.S.A.', 'France', 'Denmark / Baltic',
                                   'Other (specify in note)']

list_months = [('01', 'Jan'), ('02', 'Feb'), ('03', 'Mar'), ('04', 'Apr'), ('05', 'May'), ('06', 'Jun'),
               ('07', 'Jul'), ('08', 'Aug'), ('09', 'Sep'), ('10', 'Oct'), ('11', 'Nov'), ('12', 'Dec')]

def structure_places(place_list):
    """
    Takes a list of places and then returns a tree of the places structured by region and broad region.
    Returns a dictionary(key=broad_region, value=dictionary(key=region, value=list of places))
    """
    # Dict keyed by region, value is a list of places
    # Distinct for foreign key returns a list (sort of) of tuples with the django id of the place.
    # I think it will only ever have one place in each tuple, though it would probably be best to just iterate through the tuple
    region_list = {}
    for tup in place_list:
        for idx in tup:
            if idx:
                place = models.Place.objects.get(id=idx)
                reg = place.region
                if reg not in region_list:
                    region_list[reg] = []
                region_list[reg].append(place)
    broad_region_list = {}
    for region, list_of_places in region_list.items():
        broad_reg = region.broad_region
        if broad_reg not in broad_region_list:
            broad_region_list[broad_reg] = {}
        broad_region_list[broad_reg][region] = list_of_places
    return broad_region_list

def structure_places_all(place_list):
    """
    Takes a list of places and then returns a tree of the places structured by region and broad region.
    Returns a dictionary(key=broad_region, value=dictionary(key=region, value=list of places))
    """
    # Dict keyed by region, value is a list of places
    # Distinct for foreign key returns a list (sort of) of tuples with the django id of the place.
    # I think it will only ever have one place in each tuple, though it would probably be best to just iterate through the tuple
    region_list = {}
    for place in place_list:
        reg = place.region
        if reg not in region_list:
            region_list[reg] = []
        region_list[reg].append(place)
    broad_region_list = {}
    for region, list_of_places in region_list.items():
        broad_reg = region.broad_region
        if broad_reg not in broad_region_list:
            broad_region_list[broad_reg] = {}
        broad_region_list[broad_reg][region] = list_of_places
    return broad_region_list
            
def display_percent(value, voyageid):
    return str(round(value*100, 1)) + "%"
def display_sterling_price(value, voyageid):
    return "£" + str(round(value, 2))
def display_sterling_price_nopound(value, voyageid):
    return str(round(value, 2))
def display_xls_multiple_names(value, voyageid):
    return value.replace('<br/>', ';').replace('<br>', ';')
# Returns a list of the short form sources split by semicolons
def display_xls_sources(value, voyageid):
    if not value:
        return value
    srcs = []
    for i in value:
        split = i.split('<>')
        if split and len(split) > 0 and split[0] != '':
            srcs.append(split[0])
    return '; '.join(srcs)
def detail_display_sources(value, voyageid):
    if not value:
        return value
    srcs = []
    for i in value:
        parts = i.split('<>')
        if len(parts) > 1:
            parts[1] = '<span class="detail-data-rollover"> ' + parts[1] + " </span>\n"
            srcs.append(': '.join(parts))
    return ' <br/>'.join(srcs)
# Converts a text percentage to a decimal between 0 and 1
def mangle_percent(value, voyageid=None):
    return float(str(value).replace('%', '')) / 100.0
def mangle_source(value, voyageid=None):
    return re.sub(r'[,\s]', '', value)
def unmangle_percent(value, voyageid=None):
    if isinstance(value, (str, int, float)):
        return str(round(float(value) * 100, 1)) + "%"
    else:
        return str(value * 100) + "%"
def unmangle_date(value, voyageid=None):
    if isinstance(value, date):
        return unicode(value.month) + u'/' + unicode(value.day) + u'/' + unicode(value.year)
    splitstr = str(value).split(',')
    splitstr.reverse()
    return '/'.join(splitstr)
def unmangle_datem(value, voyageid=None):
    if isinstance(value, date):
        return unicode(value.month) + u'/' + unicode(value.year)
    splitstr = str(value).split(',')
    splitstr.reverse()
    return '/'.join(splitstr)
def unmangle_truncate(value, voyageid=None):
    val = float(value)
    return int(round(val))
def no_mangle(value, voyageid=None):
    return value

# Run against solr field values when displaying in results table
display_methods = {'var_imputed_percentage_men': display_percent,
                   'var_imputed_percentage_women': display_percent,
                   'var_imputed_percentage_boys': display_percent,
                   'var_imputed_percentage_girls': display_percent,
                   'var_imputed_percentage_male': display_percent,
                   'var_imputed_percentage_child': display_percent,
                   'var_imputed_mortality': display_percent,
                   'var_imputed_sterling_cash': display_sterling_price,
                   'var_tonnage': unmangle_truncate,
                   'var_tonnage_mod': unmangle_truncate,
                   'var_voyage_began': unmangle_date,
                   'var_slave_purchase_began': unmangle_date,
                   'var_date_departed_africa': unmangle_date,
                   'var_first_dis_of_slaves': unmangle_date,
                   'var_departure_last_place_of_landing': unmangle_date,
                   'var_voyage_completed': unmangle_date}
# Run against solr field values when creating an xls file
display_methods_xls = {'var_imputed_percentage_men': display_percent,
                       'var_imputed_percentage_women': display_percent,
                       'var_imputed_percentage_boys': display_percent,
                       'var_imputed_percentage_girls': display_percent,
                       'var_imputed_percentage_male': display_percent,
                       'var_imputed_percentage_child': display_percent,
                       'var_imputed_mortality': display_percent,
                       'var_imputed_sterling_cash': display_sterling_price_nopound,
                       'var_captain': display_xls_multiple_names,
                       'var_owner': display_xls_multiple_names,
                       'var_sources': display_xls_sources,
                       'var_voyage_began': unmangle_date,
                       'var_slave_purchase_began': unmangle_date,
                       'var_date_departed_africa': unmangle_date,
                       'var_first_dis_of_slaves': unmangle_date,
                       'var_departure_last_place_of_landing': unmangle_date,
                       'var_voyage_completed': unmangle_date}
# Run against solr field values when displaying values for a single voyage
display_methods_details = {'var_sources': detail_display_sources}
# Used to convert a form value to a proper value for searching with
search_mangle_methods = {'var_imputed_percentage_men': mangle_percent,
                         'var_imputed_percentage_women': mangle_percent,
                         'var_imputed_percentage_boys': mangle_percent,
                         'var_imputed_percentage_girls': mangle_percent,
                         'var_imputed_percentage_male': mangle_percent,
                         'var_imputed_percentage_child': mangle_percent,
                         'var_imputed_mortality': mangle_percent,
                         'var_sources': mangle_source}
# Used for display of previous queries
parameter_unmangle_methods = {'var_imputed_percentage_men': unmangle_percent,
                              'var_imputed_percentage_women': unmangle_percent,
                              'var_imputed_percentage_boys': unmangle_percent,
                              'var_imputed_percentage_girls': unmangle_percent,
                              'var_imputed_percentage_male': unmangle_percent,
                              'var_imputed_percentage_child': unmangle_percent,
                              'var_imputed_mortality': unmangle_percent,
                              'var_voyage_began': unmangle_datem,
                              'var_slave_purchase_began': unmangle_datem,
                              'var_date_departed_africa': unmangle_datem,
                              'var_first_dis_of_slaves': unmangle_datem,
                              'var_departure_last_place_of_landing': unmangle_datem,
                              'var_voyage_completed': unmangle_datem,
                              'var_tonnage': unmangle_truncate,
                              'var_tonnage_mod': unmangle_truncate}
# Run against solr field values when displaying values for a single voyage
display_unmangle_methods = {'var_imputed_percentage_men': unmangle_percent,
                            'var_imputed_percentage_women': unmangle_percent,
                            'var_imputed_percentage_boys': unmangle_percent,
                            'var_imputed_percentage_girls': unmangle_percent,
                            'var_imputed_percentage_male': unmangle_percent,
                            'var_imputed_percentage_child': unmangle_percent,
                            'var_imputed_mortality': unmangle_percent,
                            'var_voyage_began': unmangle_date,
                            'var_slave_purchase_began': unmangle_date,
                            'var_date_departed_africa': unmangle_date,
                            'var_first_dis_of_slaves': unmangle_date,
                            'var_departure_last_place_of_landing': unmangle_date,
                            'var_voyage_completed': unmangle_date,
                            'var_tonnage': unmangle_truncate,
                            'var_tonnage_mod': unmangle_truncate}


#all_place_list = structure_places_all(models.Place.objects.all())

var_dict = [
    # Ship, Nation, Owners
    {'var_name': 'var_voyage_id',
     'spss_name': 'voyageid',
     'var_full_name': 'Voyage identification number',
     'var_type': 'numeric',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True},
    {'var_name': 'var_voyage_in_cd_rom',
     'spss_name': 'evgreen',
     'var_full_name': 'Voyage in 1999 CD-ROM',
     'var_type': 'boolean',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_ship_name',
     'spss_name': 'shipname',
     'var_full_name': 'Vessel name',
     'var_type': 'plain_text',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True},
    {'var_name': 'var_nationality',
     'spss_name': 'national',
     'var_full_name': 'Flag',
     'var_type': 'select',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_imputed_nationality',
     'spss_name': 'natinimp',
     'var_full_name': 'Flag' + "*",
     'var_type': 'select',
     'var_category': 'Ship, nation, owners',
     "is_estimate": True,
     "is_basic": True,
     "is_general": True,
     "note" : "Flag regrouped into seven major national carriers"},
    {'var_name': 'var_vessel_construction_place',
     'spss_name': 'placcons',
     'var_full_name': 'Place constructed',
     'var_type': 'select_three_layers',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageShip.objects.values_list('vessel_construction_place').distinct())},
#     'choices': all_place_list},
    {'var_name': 'var_year_of_construction',
     'spss_name': 'yrcons',
     'var_full_name': 'Year constructed',
     'var_type': 'numeric',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_registered_place',
     'spss_name': 'placreg',
     'var_full_name': 'Place registered',
     'var_type': 'select_three_layers',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageShip.objects.values_list('registered_place').distinct())},
#     'choices': all_place_list},
    {'var_name': 'var_registered_year',
     'spss_name': 'yrreg',
     'var_full_name': 'Year registered',
     'var_type': 'numeric',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_rig_of_vessel',
     'spss_name': 'rig',
     'var_full_name': 'Rig',
     'var_type': 'select',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_tonnage',
     'spss_name': 'tonnage',
     'var_full_name': 'Tonnage',
     'var_type': 'numeric',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_tonnage_mod',
     'spss_name': 'tonmod',
     'var_full_name': 'Standardized tonnage*',
     'var_type': 'numeric',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     "note": "Converted to pre-1786 British registered tons"},
    {'var_name': 'var_guns_mounted',
     'spss_name': 'guns',
     'var_full_name': 'Guns mounted',
     'var_type': 'numeric',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_owner',
     'spss_name': 'owner',
     'var_full_name': 'Vessel owners',
     'var_type': 'plain_text',
     'var_category': 'Ship, nation, owners',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True},

    # Voyage outcome
    {'var_name': 'var_outcome_voyage',
     'spss_name': 'fate',
     'var_full_name': 'Particular outcome of voyage',
     'var_type': 'select',
     'var_category': 'Voyage Outcome',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_outcome_slaves',
     'spss_name': 'fate2',
     'var_full_name': 'Outcome of voyage for slaves*',
     'var_type': 'select',
     'var_category': 'Voyage Outcome',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note": "Derived from particular outcome"},
    {'var_name': 'var_outcome_ship_captured',
     'spss_name': 'fate3',
     'var_full_name': 'Outcome of voyage if ship captured*',
     'var_type': 'select',
     'var_category': 'Voyage Outcome',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     "note": "Derived from particular outcome"},
    {'var_name': 'var_outcome_owner',
     'spss_name': 'fate4',
     'var_full_name': 'Outcome of voyage for owner*',
     'var_type': 'select',
     'var_category': 'Voyage Outcome',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note": "Derived from particular outcome"},
    {'var_name': 'var_resistance',
     'spss_name': 'resistance',
     'var_full_name': 'African resistance',
     'var_type': 'select',
     'var_category': 'Voyage Outcome',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True},

    # Voyage Itinerary
    {'var_name': 'var_imp_port_voyage_begin',
     'spss_name': 'ptdepimp',
     'var_full_name': 'Place where voyage began*',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('imp_port_voyage_begin').distinct()),
#     'choices': all_place_list,
     "note": "Same as data variable in most cases, but derived from "
             "port of return for certain Brazilian voyages"},

    {'var_name': 'var_first_place_slave_purchase',
     'spss_name': 'plac1tra',
     'var_full_name': 'First place of slave purchase',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('first_place_slave_purchase').distinct())},
#     'choices': all_place_list},

    {'var_name': 'var_second_place_slave_purchase',
     'spss_name': 'plac2tra',
     'var_full_name': 'Second place of slave purchase',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('second_place_slave_purchase').distinct())},
#     'choices': all_place_list},

    {'var_name': 'var_third_place_slave_purchase',
     'spss_name': 'plac3tra',
     'var_full_name': 'Third place of slave purchase',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('third_place_slave_purchase').distinct())},
#     'choices': all_place_list},

    {'var_name': 'var_imp_principal_place_of_slave_purchase',
     'spss_name': 'mjbyptimp',
     'var_full_name': 'Principal place of slave purchase*',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": True,
     "is_basic": True,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('imp_principal_place_of_slave_purchase').distinct()),
#     'choices': all_place_list,
     "note": "Place where largest number of captives embarked"},

    {'var_name': 'var_port_of_call_before_atl_crossing',
     'spss_name': 'npafttra',
     'var_full_name': 'Places of call before Atlantic crossing',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('port_of_call_before_atl_crossing').distinct())},
#     'choices': all_place_list},

    {'var_name': 'var_first_landing_place',
     'spss_name': 'sla1port',
     'var_full_name': 'First place of slave landing',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('first_landing_place').distinct())},
#     'choices': all_place_list},

    {'var_name': 'var_second_landing_place',
     'spss_name': 'adpsale1',
     'var_full_name': 'Second place of slave landing',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('second_landing_place').distinct())},
#     'choices': all_place_list},

    {'var_name': 'var_third_landing_place',
     'spss_name': 'adpsale2',
     'var_full_name': 'Third place of slave landing',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('third_landing_place').distinct())},
#     'choices': all_place_list},

    {'var_name': 'var_imp_principal_port_slave_dis',
     'spss_name': 'mjslptimp',
     'var_full_name': 'Principal place of slave landing*',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": True,
     "is_basic": True,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('imp_principal_port_slave_dis').distinct()),
#     'choices': all_place_list,
     "note": "Place where largest number of captives embarked"},

    {'var_name': 'var_place_voyage_ended',
     'spss_name': 'portret',
     'var_full_name': 'Place where voyage ended',
     'var_type': 'select_three_layers',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     'choices': structure_places(models.VoyageItinerary.objects.values_list('place_voyage_ended').distinct())},
#     'choices': all_place_list},

    # Itinerary - region variables
    {'var_name': 'var_imp_region_voyage_begin',
     'spss_name': 'deptregimp',
     'var_full_name': 'Region where voyage began*',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    {'var_name': 'var_first_region_slave_emb',
     'spss_name': 'regem1',
     'var_full_name': 'First region of slave purchase',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},


    {'var_name': 'var_second_region_slave_emb',
     'spss_name': 'regem2',
     'var_full_name': 'Second region of slave purchase',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    {'var_name': 'var_third_region_slave_emb',
     'spss_name': 'regem3',
     'var_full_name': 'Third region of slave purchase',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    {'var_name': 'var_imp_principal_region_of_slave_purchase',
     'spss_name': 'majbyimp',
     'var_full_name': 'Principal region of slave purchase*',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    {'var_name': 'var_first_landing_region',
     'spss_name': 'regdis1',
     'var_full_name': 'First region of slave landing',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    {'var_name': 'var_second_landing_region',
     'spss_name': 'regdis2',
     'var_full_name': 'Second region of slave landing',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    {'var_name': 'var_third_landing_region',
     'spss_name': 'regdis3',
     'var_full_name': 'Third region of slave landing',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    {'var_name': 'var_imp_principal_region_slave_dis',
     'spss_name': 'mjselimp',
     'var_full_name': 'Principal region of slave landing*',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    {'var_name': 'var_region_voyage_ended',
     'spss_name': 'retrnreg',
     'var_full_name': 'Region where voyage ended',
     'var_category': 'Voyage Itinerary',
     "is_estimate": False,
     "is_basic": False,
     "is_general": False},

    # Voyage Dates
    {'var_name': 'var_imp_arrival_at_port_of_dis',
     'spss_name': 'yearam',
     'var_full_name': 'Year arrived with slaves*',
     'var_type': 'numeric',
     'var_category': 'Voyage Dates',
     "is_estimate": True,
     "is_basic": True,
     "is_general": True,
     "note": "Standard variable for classification by year of voyage"},
    {'var_name': 'var_voyage_began',
     'spss_name': 'date_dep',
     'var_full_name': 'Date voyage began',
     'var_type': 'date',
     'var_category': 'Voyage Dates',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_slave_purchase_began',
     'spss_name': 'date_buy',
     'var_full_name': 'Date trade began in Africa',
     'var_type': 'date',
     'var_category': 'Voyage Dates',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_date_departed_africa',
     'spss_name': 'date_leftAfr',
     'var_full_name': 'Date vessel departed Africa',
     'var_type': 'date',
     'var_category': 'Voyage Dates',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_first_dis_of_slaves',
     'spss_name': 'date_land1',
     'var_full_name': 'Date vessel arrived with slaves',
     'var_type': 'date',
     'var_category': 'Voyage Dates',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_departure_last_place_of_landing',
     'spss_name': 'date_depam',
     'var_full_name': 'Date vessel departed for homeport',
     'var_type': 'date',
     'var_category': 'Voyage Dates',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_voyage_completed',
     'spss_name': 'date_end',
     'var_full_name': 'Date voyage completed',
     'var_type': 'date',
     'var_category': 'Voyage Dates',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_imp_length_home_to_disembark',
     'spss_name': 'voy1imp',
     'var_full_name': 'Voyage length, homeport to slaves landing (days)*',
     'var_type': 'numeric',
     'var_category': 'Voyage Dates',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     "note": "Difference between date voyage began and date vessel "
             "arrived with slaves"},
    {'var_name': 'var_length_middle_passage_days',
     'spss_name': 'voy2imp',
     'var_full_name': 'Middle passage (days)*',
     'var_type': 'numeric',
     'var_category': 'Voyage Dates',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     "note": "Difference between date vessel left Africa "
             "and date it arrived with slaves"},
    # Captain and Crew
    {'var_name': 'var_captain',
     'spss_name': 'captain',
     'var_full_name': 'Captain\'s name',
     'var_type': 'plain_text',
     'var_category': 'Captain and Crew',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True},
    {'var_name': 'var_crew_voyage_outset',
     'spss_name': 'crew1',
     'var_full_name': 'Crew at voyage outset',
     'var_type': 'numeric',
     'var_category': 'Captain and Crew',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True},
    {'var_name': 'var_crew_first_landing',
     'spss_name': 'crew3',
     'var_full_name': 'Crew at first landing of slaves',
     'var_type': 'numeric',
     'var_category': 'Captain and Crew',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_crew_died_complete_voyage',
     'spss_name': 'crewdied',
     'var_full_name': 'Crew deaths during voyage',
     'var_type': 'numeric',
     'var_category': 'Captain and Crew',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True},

    # Slaves (numbers)
    {'var_name': 'var_num_slaves_intended_first_port',
     'spss_name': 'slintend',
     'var_full_name': 'Number of slaves intended at first place of purchase',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_num_slaves_carried_first_port',
     'spss_name': 'ncar13',
     'var_full_name': 'Slaves carried from first port of purchase',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_num_slaves_carried_second_port',
     'spss_name': 'ncar15',
     'var_full_name': 'Slaves carried from second port of purchase',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_num_slaves_carried_third_port',
     'spss_name': 'ncar17',
     'var_full_name': 'Slaves carried from third port of purchase',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_total_num_slaves_purchased',
     'spss_name': 'tslavesd',
     'var_full_name': 'Total slaves embarked',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_imp_total_num_slaves_purchased',
     'spss_name': 'slaximp',
     'var_full_name': 'Total slaves embarked*',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": True,
     "is_basic": True,
     "is_general": True,
     "note": "Estimated embarkations"},
    {'var_name': 'var_total_num_slaves_arr_first_port_embark',
     'spss_name': 'slaarriv',
     'var_full_name': 'Number of slaves arriving at first place of landing',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_num_slaves_disembark_first_place',
     'spss_name': 'slas32',
     'var_full_name': 'Number of slaves disembarked at first place of landing',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_num_slaves_disembark_second_place',
     'spss_name': 'slas36',
     'var_full_name': 'Number of slaves disembarked at second place of landing',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_num_slaves_disembark_third_place',
     'spss_name': 'slas39',
     'var_full_name': 'Number of slaves disembarked at third place of landing',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_imp_total_slaves_disembarked',
     'spss_name': 'slamimp',
     'var_full_name': 'Total slaves disembarked*',
     'var_type': 'numeric',
     'var_category': 'Slave (numbers)',
     "is_estimate": True,
     "is_basic": True,
     "is_general": True,
     "note": "Estimated embarkations"},

    # Slaves (characteristics)
    {'var_name': 'var_imputed_percentage_men',
     'spss_name': 'menrat7',
     'var_full_name': 'Percentage men*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note" : "Captives identified by age and gender"},
    {'var_name': 'var_imputed_percentage_women',
     'spss_name': 'womrat7',
     'var_full_name': 'Percentage women*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note" : "Captives identified by age and gender"},
    {'var_name': 'var_imputed_percentage_boys',
     'spss_name': 'boyrat7',
     'var_full_name': 'Percentage boys*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note" : "Captives identified by age and gender"},
    {'var_name': 'var_imputed_percentage_girls',
     'spss_name': 'girlrat7',
     'var_full_name': 'Percentage girls*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note" : "Captives identified by age and gender"},
    {'var_name': 'var_imputed_percentage_male',
     'spss_name': 'malrat7',
     'var_full_name': 'Percentage male*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note" : "Captives identified by gender (males/females)"},
    {'var_name': 'var_imputed_percentage_child',
     'spss_name': 'chilrat7',
     'var_full_name': 'Percentage children*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note" : "Captives identified by age group (adults/children)"},
    {'var_name': 'var_imputed_sterling_cash',
     'spss_name': 'jamcaspr',
     'var_full_name': 'Sterling cash price in Jamaica*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True},
    {'var_name': 'var_imputed_death_middle_passage',
     'spss_name': 'vymrtimp',
     'var_full_name': 'Slave deaths during middle passage*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": False,
     "is_general": True,
     "note": "Documented or difference between embarked "
             "and disembarked captives (data variables)"},
    {'var_name': 'var_imputed_mortality',
     'spss_name': 'vymrtrat',
     'var_full_name': 'Mortality rate*',
     'var_type': 'numeric',
     'var_category': 'Slave (characteristics)',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True,
     "note": "Slave deaths during Middle Passage divided by number of "
             "captives leaving Africa"},

    # Source
    {'var_name': 'var_sources',
     'spss_name': 'source',
     'var_full_name': 'Sources',
     'var_type': 'plain_text',
     'var_category': 'Source',
     "is_estimate": False,
     "is_basic": True,
     "is_general": True}
]

# This variable has only these field visible
var_imp_principal_place_of_slave_purchase_fields = ["Africa", "Other"]

paginator_range_factors = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
option_results_per_page = [10, 15, 20, 30, 50, 100, 200]

basic_variables = []
for item in var_dict:
    if item['is_basic']:
        basic_variables.append(item)

general_variables = []
for item in var_dict:
    if item['is_general']:
        general_variables.append(item)

list_text_fields = []
for item in var_dict:
    if 'var_type' in item and item['var_type'] == 'plain_text':
        list_text_fields.append(item['var_name'])

list_select_fields = []
for item in var_dict:
    if 'var_type' in item and item['var_type'] == 'select':
        list_select_fields.append(item['var_name'])

list_numeric_fields = []
for item in var_dict:
    if 'var_type' in item and item['var_type'] == 'numeric':
        list_numeric_fields.append(item['var_name'])

list_date_fields = []
for item in var_dict:
    if 'var_type' in item and item['var_type'] == 'date':
        list_date_fields.append(item['var_name'])

list_place_fields = []
for item in var_dict:
    if 'var_type' in item and item['var_type'] == 'select_three_layers':
        list_place_fields.append(item['var_name'])

list_boolean_fields = []
for item in var_dict:
    if 'var_type' in item and item['var_type'] == 'boolean':
        list_boolean_fields.append(item['var_name'])

# List of default result columns
default_result_columns = [
    'var_voyage_id',
    'var_ship_name',
    'var_captain',
    'var_imp_arrival_at_port_of_dis',
    'var_imp_principal_region_of_slave_purchase',
    'var_imp_principal_region_slave_dis',
]

# Dictionary of sources
sources_id = {
    'documentary': 0,
    'newspapers': 1,
    'published_sources': 2,
    'unpublished_secondary_sources': 3,
    'private_notes_and_collections': 4
}


# Source types sorted by letters
letters_sorted_source_types = [
    "published_sources"
]

summary_statistics_columns = [
    '',
    'Total slaves',
    'Total voyages',
    'Average',
    'Standard deviation'
]

summary_statistics = [
    {'display_name' : 'Slaves embarked *', 'var_name': 'var_imp_total_num_slaves_purchased',
     'has_total': True, 'is_percentage' : False},
    {'display_name' : 'Slaves disembarked *', 'var_name': 'var_imp_total_slaves_disembarked',
     'has_total' : True, 'is_percentage' : False},
    {'display_name' : 'Percentage of slaves embarked who died during voyage *',
     'var_name': 'var_imputed_mortality', 'has_total' : False, 'is_percentage' : True},
    {'display_name' : 'Length of Middle Passage (in days) *',
     'var_name': 'var_length_middle_passage_days',
     'has_total' : False, 'is_percentage' : False},
    {'display_name' : 'Percentage male *', 'var_name': 'var_imputed_percentage_male',
     'has_total' : False, 'is_percentage' : True},
    {'display_name' : 'Percentage children*', 'var_name': 'var_imputed_percentage_child',
     'has_total' : False, 'is_percentage' : True},
    {'display_name' : 'Tonnage of vessel', 'var_name': 'var_tonnage',
     'has_total' : False, 'is_percentage' : False},
]

methodology_items = SortedDict()
methodology_items = [
    {'number': 1,
     'name': "Introduction",
     'page': "methodology-1"},
    {'number': 2,
     'name': "Coverage of the Slave Trade",
     'page': "methodology-2"},
    {'number': 3,
     'name': "Nature of Sources",
     'page': "methodology-3"},
    {'number': 4,
     'name': "Cases and Variables",
     'page': "methodology-4"},
    {'number': 5,
     'name': "Data Variables",
     'page': "methodology-5"},
    {'number': 6,
     'name': "Age Categories",
     'page': "methodology-6"},
    {'number': 7,
     'name': "Dates",
     'page': "methodology-7"},
    {'number': 8,
     'name': "Names",
     'page': "methodology-8"},
    {'number': 9,
     'name': "Imputed Variables",
     'page': "methodology-9"},
    {'number': 10,
     'name': "Geographic Data",
     'page': "methodology-10"},
    {'number': 11,
     'name': "Imputed Voyage Dates",
     'page': "methodology-11"},
    {'number': 12,
     'name': "Classification as a Trans-Atlantic Slavic Voyage",
     'page': "methodology-12"},
    {'number': 13,
     'name': "Voyage Outcomes",
     'page': "methodology-13"},
    {'number': 14,
     'name': "Inferring Places of Trade",
     'page': "methodology-14"},
    {'number': 15,
     'name': "Imputed Numbers of Slaves",
     'page': "methodology-15"},
    {'number': 16,
     'name': "Regions of Embarkation and Disembarkation",
     'page': "methodology-16"},
    {'number': 17,
     'name': "Age and Gender Ratios",
     'page': "methodology-17"},
    {'number': 18,
     'name': "National Carriers",
     'page': "methodology-18"},
    {'number': 19,
     'name': "Tonnage",
     'page': "methodology-19"},
    {'number': 20,
     'name': "Resistance and Price of Slaves",
     'page': "methodology-20"},
    {'number': 21,
     'name': "Appendix",
     'page': "methodology-21"},
    {'number': 22,
     'name': "Notes",
     'page': "methodology-22"},
]
