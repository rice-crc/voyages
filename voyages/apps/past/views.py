from __future__ import absolute_import, division, unicode_literals

import json
import uuid
from builtins import str
from datetime import date
import time
import copy
from django.conf import settings
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse, Http404
from django.http.response import HttpResponseBadRequest
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect, render,HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from past.utils import old_div
from voyages.apps.common.models import SavedQuery

from voyages.apps.common.views import get_filtered_results
from .models import (AltLanguageGroupName, Enslaved,
                     EnslavedContribution, EnslavedContributionLanguageEntry,
                     EnslavedContributionNameEntry, EnslavedContributionStatus, EnslavedInRelation, EnslavedSearch, EnslavementRelation, EnslaverContribution, EnslaverInRelation, EnslaverRole, EnslaverSearch, EnslaverVoyageConnection,
                     LanguageGroup, MultiValueHelper, ModernCountry, EnslavedNameSearchCache, PivotTableDefinition,
                     _modern_name_fields, _name_fields)
from voyages.apps.voyage.models import Place,Region
from collections import Counter



ENSLAVED_DATASETS = ['african-origins', 'oceans-of-kinfolk']

def _generate_table(query, table_params, data_adapter=None):
    try:
        rows_per_page = int(table_params.get('length', 10))
        current_page_num = 1 + \
            old_div(int(table_params.get('start', 0)), rows_per_page)
        paginator = Paginator(query, rows_per_page)
        page = paginator.page(current_page_num)
    except Exception as e:
        print(f"Failed query pagination: {e}")
        page = query
    response_data = {}
    try:
        total_results = paginator.count
    except Exception:
        total_results = len(query)
    response_data['recordsTotal'] = total_results
    response_data['recordsFiltered'] = total_results
    response_data['draw'] = int(table_params.get('draw', 0))
    if data_adapter:
        changed = data_adapter(page)
        if changed:
            page = changed
    response_data['data'] = list(page)
    return response_data

def enslaved_database(request, dataset=None):
    if dataset is not None:
        try:
            dataset = ENSLAVED_DATASETS.index(dataset)
        except:
            dataset = None
    return render(
        request,
        'past/database.html',
        { 'dataset': str(dataset) if dataset is not None else None })

@csrf_exempt
@require_POST
def get_enslaver_filtered_places(request):
    data = json.loads(request.body)
    var_name = data.get('var_name')
    if var_name is None:
        return JsonResponse({ "error": "var_name must be set" })
    cache_key = f"_filtered_places_ENSLAVER_{var_name}"
    var_name = f"voyage__voyage_itinerary__{var_name}"
    qs = EnslaverVoyageConnection.objects \
        .select_related(var_name) \
        .values_list(var_name, flat=True) \
        .distinct()
    filtered = get_filtered_results(cache_key, qs)
    filtered['filtered_var_name'] = var_name
    return JsonResponse(filtered)

@csrf_exempt
@require_POST
def get_enslaved_filtered_places(request):
    """
    Obtains a list of places and corresponding regions/broad regions that are
    present in a given field of VoyageItinerary when filtered to the enslaved of
    the given dataset.
    """
    data = json.loads(request.body)
    var_name = data.get('var_name')
    dataset = data.get('dataset')
    if var_name is None or dataset is None:
        return JsonResponse({ "error": "Both dataset and var_name must be set" })
    cache_key = f"_filtered_places_ENSLAVED_{str(dataset)}_{var_name}"
    # Most location variables come from VoyageItinerary, but
    # post_disembarkation_location is only present in the Enslaved model
    # directly.
    if var_name != 'post_disembark_location_id':
        var_name = f"voyage__voyage_itinerary__{var_name}"
    qs = Enslaved.objects.filter(dataset=dataset) \
        .select_related(var_name) \
        .values_list(var_name, flat=True) \
        .distinct()
    filtered = get_filtered_results(cache_key, qs)
    filtered['filtered_var_name'] = var_name
    filtered['dataset'] = dataset
    return JsonResponse(filtered)


@csrf_exempt
@cache_page(3600)
def get_modern_countries(_):
    mcs = {
        mc.id: {
            'name': mc.name,
            'longitude': mc.longitude,
            'latitude': mc.latitude
        } for mc in ModernCountry.objects.all()
    }
    return JsonResponse(mcs)


@csrf_exempt
@cache_page(3600)
def get_language_groups(request):
    #we need a switch between used and unused language groups (search should only have used, contribute should have all)
    active_only = True
    try:
        active_only = json.loads(request.body).get('active_only', active_only)
    except:
        pass
    countries_list_key = "countries_list"
    alt_names_key = "alt_names_list"
    country_helper = MultiValueHelper(countries_list_key, ModernCountry.languages.through, 'languagegroup_id', modern_country_id='moderncountry__pk', country_name='moderncountry__name')
    alt_names_helper = MultiValueHelper(alt_names_key, AltLanguageGroupName, 'language_group_id', alt_name='name')
    q = LanguageGroup.objects.all()
    q = country_helper.adapt_query(q)
    q = alt_names_helper.adapt_query(q)
    items = [country_helper.patch_row(alt_names_helper.patch_row(row)) for row in q.values()]
    if active_only:
        enslaved=Enslaved.objects.all().filter(enslaved_id__lte=500000)
        used_lgids=list(set([i[0] for i in list(enslaved.values_list('language_group_id')) if i[0] is not None]))
    
        return JsonResponse([{ "id": item["id"], "name": item["name"], "lat": item["latitude"], "lng": item["longitude"], "alts": item[alt_names_key], "countries": item[countries_list_key] }
            for item in items if item["id"] in used_lgids], safe=False)
    else:
        return JsonResponse([{ "id": item["id"], "name": item["name"], "lat": item["latitude"], "lng": item["longitude"], "alts": item[alt_names_key], "countries": item[countries_list_key] }
            for item in items], safe=False)


@csrf_exempt
@cache_page(3600)
def get_enslaver_roles(request):
    return JsonResponse([{"id": r.id, "label": r.name} for r in EnslaverRole.objects.all()], safe=False)

@csrf_exempt
@cache_page(3600)
def get_enumeration(_, model_name):
    from django.apps import apps
    model = apps.get_model(app_label="past", model_name=model_name.replace('-', ''))
    return JsonResponse({int(x.pk): x.name for x in model.objects.all()})


def restore_enslaved_permalink(_, link_id):
    """Redirect the page with a URL param"""
    q = SavedQuery.objects.get(pk=link_id)
    query = json.loads(q.query)
    # Detect the dataset of the query.
    dataset = query.get('items', {}).get('enslaved_dataset')
    ds_name = ''
    try:
        ds_name = '/' + ENSLAVED_DATASETS[int(dataset)]
    except:
        pass
    return redirect("/past/database" + ds_name + "#searchId=" + link_id)


def restore_enslaver_permalink(_, link_id):
    return redirect(f"/past/enslavers#searchId={link_id}")


def is_valid_name(name):
    return name is not None and name.strip() != ""

_voyage_related_fields_default = [
    'voyage__voyage_ship__ship_name',
    'voyage__voyage_dates__first_dis_of_slaves',
    'voyage__voyage_itinerary__int_first_port_dis__place',
    'voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__place',
    'voyage__voyage_itinerary__imp_principal_port_slave_dis__place',
    'voyage__voyage_name_outcome__vessel_captured_outcome__label'
]



place_routes_points={}
region_routes_points={}
place_edge_ids={}
region_edge_ids={}
place_route_curves={}
region_route_curves={}
region_vals_to_port_ids={}

def refresh_maps_cache(request):
    try:
        from voyages.localsettings import STATIC_ROOT
        import os
        d=open(os.path.join(STATIC_ROOT,"pastmaps/place_routes_points.json"),"r")
        t=d.read()
        j=json.loads(t)
        global place_routes_points
        place_routes_points={int(i):j[i] for i in j}
        d.close()
    
        d=open(os.path.join(STATIC_ROOT,"pastmaps/region_routes_points.json"),"r")
        t=d.read()
        j=json.loads(t)
        global region_routes_points
        region_routes_points={int(i):j[i] for i in j}
        d.close()
    
        d=open(os.path.join(STATIC_ROOT,"pastmaps/place_edge_ids.json"),"r")
        t=d.read()
        j=json.loads(t)
        global place_edge_ids
        place_edge_ids={int(i):j[i] for i in j}
        d.close()
    
        d=open(os.path.join(STATIC_ROOT,"pastmaps/region_edge_ids.json"),"r")
        t=d.read()
        j=json.loads(t)
        global region_edge_ids
        region_edge_ids={int(i):j[i] for i in j}
        d.close()
    
        import sys
        sys.path.insert(1,os.path.join(STATIC_ROOT,"pastmaps/"))
        from place_routes_curves import place_route_curves as prc
        from region_routes_curves import region_route_curves as rrc
        from region_vals_to_port_ids import region_vals_to_port_ids as rvpi
        global place_route_curves
        place_route_curves=prc
        global region_route_curves
        region_route_curves=rrc
        global region_vals_to_port_ids
        region_vals_to_port_ids=rvpi
        msg="successfully loaded maps cache data"
    except:
        msg="------>  warning. missing essential mapping static files. individual enslaved itinerary maps will not run"
    
    print(msg)
    return HttpResponse("<html><body>"+msg+"</body></html>")


refresh_maps_cache(None)

def process_search_query_post(user_query):
    # Initially we started with a simple approach that does not include the
    # operators on variables and thus can be immediately passed to the
    # EnslavedSearch constructor. However, that decision causes pain for the
    # saved query feature since the UI should know which operator was used for
    # the query in order to properly reproduce it. We are therefore handling
    # both situations here by simply removing what we don't need at the backend
    # and allowing the saved query to follow the same format as before.
    if 'items' in user_query:
        # This is the newer format with the operation encoded.
        user_query = {item['varName']: item['searchTerm'] for item in user_query['items']}
    return user_query

# TODO: Summary tables have fixed column structures so we pre-generate their
# definitions to simplify the API for clients.
from django.db.models.expressions import RawSQL, Func, Value

_pivot_year_field = F('voyage__voyage_dates__imp_arrival_at_port_of_dis')

class CoalesceFunc(Func):
    function = 'COALESCE'
    arity = 2
    arg_joiner = ','
    template = 'COALESCE(%(expressions)s)'

class LessThanFunc(Func):
    function = '<'
    arity = 2
    arg_joiner = '<'
    template = '%(expressions)s'

class RightFunc(Func):
    function = 'RIGHT'
    arity = 2
    arg_joiner = ','
    template = 'RIGHT(%(expressions)s)'

class DivFunc(Func):
    function = 'DIV'
    arity = 2
    arg_joiner = ' DIV '
    template = '%(expressions)s'

_pivot_fields = {
    'language': 'language_group__name',
    'gender_code': 'gender',
    # Separate (age < 16) vs (age >= 16 OR age IS NULL).
    'age_group': LessThanFunc(CoalesceFunc(F('age'), Value(100)), Value(16)),
    'year': _pivot_year_field,
    # The year is given in ",,{year}" string format, so we first get the 4 right
    # most values, then subtract 1 and do an integer division by 5. The
    # subtraction is so that the year ranges are of the form [xxx1, xxx5],
    # [xxx6, xxx0].
    'year_5': DivFunc(RightFunc(_pivot_year_field, Value(4)) - Value(1), Value(5))
}

_pivot_summaries = {
    'enslaved_gender': PivotTableDefinition({ 'gender_code': 'gender' }, 'enslaved_id'),
    'enslaved_lang_captives': PivotTableDefinition({ 'language': 'language_group__name' }, 'enslaved_id'),
    'enslaved_lang_voyages': PivotTableDefinition({ 'language': 'language_group__name' }, 'voyage_id')
}

@require_POST
@csrf_exempt
def search_enslaved(request):
    st=time.time()
    # A little bit of Python magic where we pass the dictionary
    # decoded from the JSON body as arguments to the EnslavedSearch
    # constructor.
    data = json.loads(request.body)
    user_query = process_search_query_post(data['search_query'])
    output_type = data.get('output', 'resultsTable')
    if output_type == 'summary':
        selection = data.get('summary_selection', _pivot_summaries.keys())
        results = {}
        for sel in selection:
            pivot = _pivot_summaries.get(sel)
            if pivot is None:
                return JsonResponse({ 'error': f"Invalid request: summary selection {sel} not found" })
            user_query['pivot_table'] = pivot
            q = EnslavedSearch(**user_query)
            results[sel] = list(q.execute([]))
        print("SUMMARY enslavedsearch response time:",time.time() - st)
        return JsonResponse(results)
    
    if output_type == 'pivot':
        pivot_fields = data.get('pivot_fields')
        if not pivot_fields:
            return JsonResponse({ "error": f"No pivot fields specified: {pivot_fields}" })
        pivot_fields = {k: _pivot_fields.get(k, k) for k in pivot_fields}
        pivot = PivotTableDefinition(pivot_fields, 'enslaved_id')
        user_query['pivot_table'] = pivot
        res = list(EnslavedSearch(**user_query).execute([]))
        print("PIVOT enslavedsearch response time:",time.time() - st)
        # Compute margin aggregates (e.g. for each field, a dict: field val => sum of cells).
        margins = {}
        for item in res:
            cell = item['cell']
            for k, v in item.items():
                if k == 'cell':
                    continue
                margin = margins.setdefault(k, {})
                margin[v] = margin.get(v, 0) + cell
        margins = {k: sorted(v.items(), key=lambda x: -x[1]) for k, v in margins.items()}
        return JsonResponse({ 'results': res, 'margins': margins })

    search = EnslavedSearch(**user_query)
    fields = data.get('fields',None)
    
    if output_type == 'maps':
        fields = [
            'language_group__id',
            'voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__value',
            'voyage__voyage_itinerary__imp_principal_port_slave_dis__value',
            'voyage__voyage_itinerary__imp_principal_region_of_slave_purchase__value',
            'voyage__voyage_itinerary__imp_principal_region_slave_dis__value',
            'post_disembark_location__value',
            'post_disembark_location__region__value'
        ]

    if fields is None:
        fields = [
            'enslaved_id',
            'age',
            'gender',
            'height',
            'skin_color',
            'language_group__name',
            'register_country__name',
            'notes',
            'voyage_id',
            'voyage__voyage_ship__ship_name',
            'voyage__voyage_dates__first_dis_of_slaves',
            'voyage__voyage_dates__date_departed_africa',
            'voyage__voyage_itinerary__int_first_port_dis__place',
            'voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__place',
            'voyage__voyage_itinerary__imp_principal_port_slave_dis__place',
            'voyage__voyage_name_outcome__vessel_captured_outcome__label',
            'captive_fate__name', 'post_disembark_location__place'
        ] + _name_fields + _modern_name_fields + \
        [helper.projected_name for helper in EnslavedSearch.all_helpers]
        
    query = search.execute(fields)
    
    # For now we only support outputing the results to DataTables.
    if output_type == 'resultsTable':

        def adapter(page):
            for row in page:
                all_names = list({
                    row[name_field]
                    for name_field in _name_fields
                    if is_valid_name(row.get(name_field))
                })
                all_names.sort(
                    reverse=(search.get_order_for_field('names') == 'desc'))
                all_modern_names = list({
                    row[name_field]
                    for name_field in _modern_name_fields
                    if is_valid_name(row.get(name_field))
                })
                all_modern_names.sort(reverse=(
                    search.get_order_for_field('modern_names') == 'desc'))
                row['names'] = all_names
                row['modern_names'] = all_modern_names
                keys = list(row.keys())
                for k in keys:
                    if k.startswith('_'):
                        row.pop(k)
                # Patch the rows so that special fields (e.g. sources_list)
                # are converted to a list of dicts.
                EnslavedSearch.patch_row(row)
            return page

        table = _generate_table(query, data.get('tableParams', {}), adapter)
        page = table.get('data', [])
        EnslavedNameSearchCache.load()
        for entry in page:
            entry['recordings'] = EnslavedNameSearchCache.get_recordings(
                [entry[f] for f in _name_fields if f in entry])
        print("TABLE enslavedsearch response time:",time.time()-st)
        return JsonResponse(table)
    
    if output_type == 'maps':
        
        mapmode=data.get('mapmode', 'points')
        paginator = Paginator(query, len(query))
        page = paginator.page(1)
        
        place_itineraries=[
            [i[k] for k in 
            ['language_group__id',
            'voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__value',
            'voyage__voyage_itinerary__imp_principal_port_slave_dis__value',
            'post_disembark_location__value'
            ]]
            for i in page
        ]
        region_itineraries=[
            [i[k] for k in 
            ['language_group__id',
            'voyage__voyage_itinerary__imp_principal_region_of_slave_purchase__value',
            'voyage__voyage_itinerary__imp_principal_region_slave_dis__value',
            'post_disembark_location__region__value'
            ]]
            for i in page
        ]
        
        final_result={}
        
        itinerary_groups=[
            ['region',region_itineraries,region_routes_points,region_route_curves,region_edge_ids],
            ['place',place_itineraries,place_routes_points,place_route_curves,place_edge_ids],        
        ]
        
        for itinerary_group in itinerary_groups:
            itinerary_group_name,itineraries,routes_points,route_curves,edge_ids_visibility=itinerary_group
            language_group_counts=dict(Counter(i[0] for i in itineraries))
            embarkation_location_counts=dict(Counter(i[1] for i in itineraries))
            disembarkation_location_counts=dict(Counter(i[2] for i in itineraries))
            final_location_counts=dict(Counter(i[3] for i in itineraries))
            language_group_ids_offset=1000000
        
            points_dict={
                p_id:{
                    'name':routes_points[p_id][1],
                    'coords':[routes_points[p_id][0][1],routes_points[p_id][0][0]],
                    'pk':routes_points[p_id][2],
                    'hidden_edges':routes_points[p_id][3],
                    'nodesize':0
                } for p_id in routes_points
            }
        
            for p_id in routes_points:
                for triple in [
                    [language_group_counts,'origin',language_group_ids_offset],
                    [embarkation_location_counts,'embarkation',0],
                    [disembarkation_location_counts,'disembarkation',0],
                    [final_location_counts,'post-disembarkation',0],
                ]:
                    this_dict,tag,offset=triple
                    if p_id-offset in this_dict:
                        weight=this_dict[p_id-offset]
                        if tag in points_dict[p_id]:
                            points_dict[p_id][tag]+=weight
                        else:
                            points_dict[p_id][tag]=weight
                        points_dict[p_id]['nodesize']+=weight
            
            featurecollection=[]
            
            nodes_hidden_edges={}
            
            for point_id in points_dict:
                
                point=points_dict[point_id]
                coords=point['coords']
                name=point['name']
                
                addfeature=False
                
                if name=="oceanic_waypoint":
                    feature_properties={
                            "name":name,
                            "size":0,
                            "node_classes":{"oceanic_waypoint":0},
                            "point_id":point_id,
                            "hidden_edges":points_dict[point_id]['hidden_edges']
                        }
                    addfeature=True
                else:
                    nodesize=point['nodesize']
                    pk=point['pk']
                    hidden_edges=point['hidden_edges']
                    if nodesize > 0:
                        addfeature=True
                        popuplines=[]
                        live_tags=['origin','embarkation','disembarkation','post-disembarkation']
                        if itinerary_group_name=='region':
                            pointtags={tag:{"count":point[tag],"key": int(pk) if tag in ('origin') else int(point_id)}
                                for tag in live_tags if tag in point
                            }
                        elif itinerary_group_name=='place':
                            pointtags={tag:{"count":point[tag],"key": int(pk)}
                                for tag in live_tags if tag in point
                            }
                        feature_properties={
                            "name":name,
                            "size":nodesize,
                            "node_classes":pointtags,
                            "point_id":point_id,
                            "hidden_edges":points_dict[point_id]['hidden_edges']
                        }
                if addfeature:
                
                    feature={
                        "type":"Feature",
                        "properties":feature_properties,
                        "geometry":{
                            "type":"Point",
                            "coordinates":coords
                        }
                    }
                    featurecollection.append(feature)
            
            result_points={
                "type": "FeatureCollection",
                "features": featurecollection
            }
            itinerary_names=["-".join([str(i) for i in itinerary]) for itinerary in itineraries]
            itinerary_names=[i for i in itinerary_names if i in route_curves]
            leg_weights=Counter([l for i in itinerary_names for l in route_curves[i]])
            itinerary_weights=Counter(itinerary_names).most_common()
            itinerary_weights.reverse()
            leg_data={l:route_curves[i[0]][l] for i in itinerary_weights for l in route_curves[i[0]]}
            result_routes=[
                {
                    'geometry':leg_data[l][0],
                    'source_target':leg_data[l][1],
                    'leg_type':leg_data[l][2],
                    'weight':leg_weights[l],
                    'id':l,
                    'visible':edge_ids_visibility[l]
                } for l in leg_data
            ]
        
            result={
                'routes':result_routes,
                'points':result_points,
                'region_vals_to_port_ids':region_vals_to_port_ids,
                'total_results_count':len(query)
            }
            
            final_result[itinerary_group_name]=result
        print("MAP enslavedsearch response time:",time.time()-st)    
        return JsonResponse(final_result,safe=False)

    return JsonResponse({'error': 'Unsupported'})


@require_POST
@csrf_exempt
def search_enslaver(request):
    data = json.loads(request.body)
    user_query = process_search_query_post(data['search_query'])
    search = EnslaverSearch(**user_query)
    fields = data.get('fields')
    if fields is None:
        fields = [
            'id',
            'principal_alias',
            'birth_year', 'birth_month', 'birth_day',
            'death_year', 'death_month', 'death_day',
            'cached_properties__enslaved_count',
            EnslaverSearch.ALIASES_LIST,
            EnslaverSearch.VOYAGES_LIST,
            EnslaverSearch.SOURCES_LIST,
            EnslaverSearch.RELATIONS_LIST
        ]
    query = search.execute(fields)
    output_type = data.get('output', 'resultsTable')
    # For now we only support outputing the results to DataTables.
    if output_type == 'resultsTable':

        def adapter(page):
            for row in page:
                EnslaverSearch.patch_row(row)
            return page

        table = _generate_table(query, data.get('tableParams', {}), adapter)
        return JsonResponse(table)
    return JsonResponse({'error': 'Unsupported'})

@require_POST
@csrf_exempt
def enslaved_contribution(request):
    """
    Create a contribution for an enslaved name.
    """
    data = json.loads(request.body)
    enslaved_id = data.get('enslaved_id')
    enslaved = Enslaved.objects.get(pk=enslaved_id) if enslaved_id else None
    if enslaved is None:
        return HttpResponseBadRequest('A valid enslaved id is required')
    names = data.get('contrib_names', [])
    languages = data.get('contrib_languages', [])
    # TODO: Check if this is enough validation.
    if len(names) == 0 and len(languages) == 0:
        return HttpResponseBadRequest(
            'Contribution must specify at least a name or a language')
    token = uuid.uuid4().hex
    contrib = EnslavedContribution()
    contrib.date = date.today()
    contrib.enslaved = enslaved
    contrib.notes = str(data.get('notes', ''))  # Optional notes
    contrib.contributor = request.user if request.user.is_authenticated(
    ) else None
    contrib.is_multilingual = bool(data.get('is_multilingual', False))
    contrib.token = token
    contrib.status = 0
    result = {}
    with transaction.atomic():
        contrib.save()
        result['contrib_id'] = contrib.pk
        name_ids = []
        for i, item in enumerate(names):
            name_entry = EnslavedContributionNameEntry()
            name_entry.contribution = contrib
            name_entry.order = i + 1
            contrib_name = item['name'].strip()
            if len(contrib_name) < 2:
                transaction.rollback()
                return HttpResponseBadRequest('Invalid name in contribution')
            name_entry.name = contrib_name
            name_entry.notes = item.get('notes', '')
            name_entry.save()
            name_ids.append(name_entry.pk)
        result['name_ids'] = name_ids
        language_ids = []
#         for i, lang in enumerate(languages):
        for i in languages:
            lang_entry = EnslavedContributionLanguageEntry()
            lang_entry.contribution = contrib
            lang_entry.order = i + 1
            lang_group_id = i
            lang_entry.language_group = LanguageGroup.objects.get(
                pk=lang_group_id) if lang_group_id else None
            if lang_entry.language_group is None:
                transaction.rollback()
                return HttpResponseBadRequest(
                    'Invalid language entry in contribution')
            lang_entry.save()
            language_ids.append(lang_entry.pk)
        result['language_ids'] = language_ids
    # The audio token is used so that the client can upload audio files for
    # storage. The token is used to avoid overwriting any files by accident and
    # to prevent malicious players from storing arbitrary data in our servers.
    result['audio_token'] = token
    return JsonResponse(result)

def _get_audio_filename(contrib_pk, name_pk, full_path=True, check_exists=False):
    filename = f"audio/{contrib_pk}_{name_pk}.webm"
    fullname = f"{settings.MEDIA_ROOT}{filename}"
    if full_path:
        filename = fullname
    if check_exists:
        from os.path import exists
        if not exists(fullname):
            return None
    return filename

@require_POST
@csrf_exempt
def store_audio(request, contrib_pk, name_pk, token):
    if len(request.body) > 1000000:
        return HttpResponseBadRequest('Audio file is too large')
    contrib_pk = int(contrib_pk)
    contrib = EnslavedContribution.objects.get(pk=contrib_pk)
    if contrib is None or contrib.token != token:
        return HttpResponseBadRequest('Contribution not found')
    name_pk = int(name_pk)
    file_name = _get_audio_filename(contrib_pk, name_pk)
    with open(file_name, 'wb+') as destination:
        destination.write(request.body)
    return JsonResponse({'len': len(request.body)})

def _get_login_url(next_url):
    return f"{reverse('account_login')}?next={next_url}"

def _enslaver_contrib_action(request, data):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(_get_login_url(request.build_absolute_uri()))
    return render(request, 'past/enslavers_contribute.html', data)

def enslaver_contrib_delete(request, id):
    return _enslaver_contrib_action(request, { "mode": "delete", "id": id })

def enslaver_contrib_edit(request, id):
    return _enslaver_contrib_action(request, { "mode": "edit", "id": id })

def enslaver_contrib_merge(request, merge_a, merge_b):
    return _enslaver_contrib_action(request, { "mode": "merge", "id": f"{merge_a},{merge_b}" })

def enslaver_contrib_split(request, id):
    return _enslaver_contrib_action(request, { "mode": "split", "id": id })

def enslaver_contrib_new(request):
    return _enslaver_contrib_action(request, { "mode": "new", "id": "" })

def get_enslavement_relation_info(request, relation_pk):
    relation = EnslavementRelation.objects \
        .filter(pk=relation_pk) \
        .select_related(*_voyage_related_fields_default) \
        .values('id', 'date', 'amount', 'text_ref', 'voyage_id', \
            location=F('place__place'), type=F('relation_type__name'), *_voyage_related_fields_default)
    relation = list(relation)
    if len(relation) != 1:
        raise Http404
    relation = relation[0]
    relation['enslavers'] = list(EnslaverInRelation.objects.filter(relation_id=relation_pk) \
        .values(alias=F('enslaver_alias__alias'), role_name=F('role__name')))
    relation['enslaved'] = list(EnslavedInRelation.objects.filter(relation_id=relation_pk) \
        .values(name=F('enslaved__documented_name')))
    return JsonResponse(relation)

def enslaver_contrib_editorial_review(request, pk):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(_get_login_url(request.build_absolute_uri()))
    contrib = get_object_or_404(EnslaverContribution, pk=pk)
    if contrib.status == EnslavedContributionStatus.ACCEPTED:
        raise Http404("This contribution has already been accepted")
    # Parsing makes sure that we have valid JSON data.
    interim = json.loads(contrib.data)
    return render(request, 'past/enslavers_contribute.html', {
        'mode': interim['type'],
        'interim': contrib.data,
        'editorialMode': True,
        'contrib_pk': pk
    })
