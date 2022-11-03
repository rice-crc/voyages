from __future__ import absolute_import, division, unicode_literals

import json
import uuid
from builtins import str
from datetime import date
import time
import copy
from django.conf import settings
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse, FileResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from past.utils import old_div
from voyages.apps.common.models import SavedQuery

from voyages.apps.common.views import get_filtered_results
from .models import (AltLanguageGroupName, Enslaved,
                     EnslavedContribution, EnslavedContributionLanguageEntry,
                     EnslavedContributionNameEntry, EnslavedSearch, EnslaverSearch, EnslaverVoyageConnection,
                     LanguageGroup, MultiValueHelper, ModernCountry, EnslavedNameSearchCache,
                     _modern_name_fields, _name_fields)
from voyages.apps.voyage.models import Place,Region
from voyages.apps.past.routes_curves import *
from voyages.apps.past.region_vals_to_port_ids import *
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
def get_language_groups(_):
    countries_list_key = "countries_list"
    alt_names_key = "alt_names_list"
    country_helper = MultiValueHelper(countries_list_key, ModernCountry.languages.through, 'languagegroup_id', country_name='moderncountry__name')
    alt_names_helper = MultiValueHelper(alt_names_key, AltLanguageGroupName, 'language_group_id', alt_name='name')
    q = LanguageGroup.objects.all()
    q = country_helper.adapt_query(q)
    q = alt_names_helper.adapt_query(q)
    items = [country_helper.patch_row(alt_names_helper.patch_row(row)) for row in q.values()]
    return JsonResponse([{ "id": item["id"], "name": item["name"], "lat": item["latitude"], "lng": item["longitude"], "alts": item[alt_names_key], "countries": item[countries_list_key] }
        for item in items], safe=False)


@csrf_exempt
@cache_page(3600)
def get_enumeration(_, model_name):
    from django.apps import apps
    model = apps.get_model(app_label="past", model_name=model_name.replace('-', ''))
    return JsonResponse({x.pk: x.name for x in model.objects.all()})


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


@require_POST
@csrf_exempt
def search_enslaved(request):
    st=time.time()
    # A little bit of Python magic where we pass the dictionary
    # decoded from the JSON body as arguments to the EnslavedSearch
    # constructor.
    data = json.loads(request.body)
    search = EnslavedSearch(**data['search_query'])
    fields=data.get('fields',None)
    output_type = data.get('output', 'resultsTable')
    
    if output_type == 'maps':
#         fields = [
#             'language_group__id',
#             'voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__value',
#             'voyage__voyage_itinerary__imp_principal_port_slave_dis__value',
#             'post_disembark_location__value'
#         ]
        fields = [
            'language_group__id',
            'voyage__voyage_itinerary__imp_principal_region_of_slave_purchase__value',
            'voyage__voyage_itinerary__imp_principal_region_slave_dis__value',
            'post_disembark_location__value'
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
            'voyage_id',
            'voyage__voyage_ship__ship_name',
            'voyage__voyage_dates__first_dis_of_slaves',
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
        print("enslavedsearch response time (table):",time.time()-st)
        return JsonResponse(table)
    elif output_type=='maps':
        
        mapmode=data.get('mapmode', 'points')
        paginator = Paginator(query, len(query))
        page = paginator.page(1)  
        print(time.time()-st)
#         itineraries=[
#             [i[k] for k in 
#             ['language_group__id',
#             'voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__value',
#             'voyage__voyage_itinerary__imp_principal_port_slave_dis__value',
#             'post_disembark_location__value'
#             ]]
#             for i in page
#         ]
        itineraries=[
            [i[k] for k in 
            ['language_group__id',
            'voyage__voyage_itinerary__imp_principal_region_of_slave_purchase__value',
            'voyage__voyage_itinerary__imp_principal_region_slave_dis__value',
            'post_disembark_location__value'
            ]]
            for i in page
        ]        
        
        if mapmode=='points':
            language_group_counts=dict(Counter(i[0] for i in itineraries))
            embarkation_location_counts=dict(Counter(i[1] for i in itineraries))
            disembarkation_location_counts=dict(Counter(i[2] for i in itineraries))
            final_location_counts=dict(Counter(i[3] for i in itineraries))
        
            d=open("voyages/apps/past/routes_points.json","r")
            t=d.read()
            j=json.loads(t)
            routes_points={int(i):j[i] for i in j}
            d.close()
            language_group_ids_offset=1000000
            
#             print(language_group_counts)
            
            points_dict={
                p_id:{
                    'name':routes_points[p_id][1],
                    'coords':[routes_points[p_id][0][1],routes_points[p_id][0][0]],
                    'pk':routes_points[p_id][2],
                    'nodesize':0
                } for p_id in routes_points
            }
            
            for p_id in routes_points:
                for triple in [
                    [language_group_counts,'origin',language_group_ids_offset],
                    [embarkation_location_counts,'embarkation',0],
                    [disembarkation_location_counts,'disembarkation',0],
                    [final_location_counts,'post-disembarkation',0]
                ]:
                    this_dict,tag,offset=triple
                    if p_id-offset in this_dict:
                        weight=this_dict[p_id-offset]
                        if tag in points_dict:
                            points_dict[p_id][tag]+=weight
                        else:
                            points_dict[p_id][tag]=weight
                        points_dict[p_id]['nodesize']+=weight
            
               
            featurecollection=[]
            for point_id in points_dict:
                point=points_dict[point_id]
                coords=point['coords']
                name=point['name']
                nodesize=point['nodesize']
                pk=point['pk']
                if nodesize > 0:
                    popuplines=[]
                    pointtags={}
                    for tag in ['origin','embarkation','disembarkation','post-disembarkation']:
                        if tag in point:
                            ##yes, you guessed it! on post-disembark,
                            ##someone decided to use place names instead of primary keys or spss codes!
                            ##and even better than that, they used spss codes for the parent regions of the ports
                            ##which all appear to be fed into the same endpoint as unique id's, which is not guaranteed
                            ##unless i'm mistaken
                            if tag in ('post-disembarkation','origin'):
                                href_event='<a id="%d" \
                                title="" \
                                href="#" \
                                onclick="linkfilter(%d,\'%s\');\
                                return false;">'\
                                %(int(point_id),int(pk),tag)
                            else:
                                href_event='<a id="%d" \
                                    title="" \
                                    href="#" \
                                    onclick="linkfilter(%d,\'%s\');\
                                    return false;">'\
                                    %(int(point_id),int(point_id),tag)
                            tag_size=point[tag]
                            if tag_size==1:
                                person_or_people="person"
                            else:
                                person_or_people="people"
                            if tag=='origin':
# currently, the language groups are, in the search interface, keyed against an on the fly index of the country (0-15) concatenated with the language group pk
## e.g. 13-160515 for Yoruba, because Nigeria is how Yoruba gets nested and Nigeria is the 13th top-level nest
## this is either a result of trying to keep m2m relations between countries and language groups, or just a trick to keep the nested items tracked
## but either way i can't get my click events to interface with it until it's cleaned up
#                               popupULline="%s%d %s originated here</a>" %(href_event,point[tag],person_or_people)
                                popupULline="%d %s originated here." %(point[tag],person_or_people)
                            elif tag=='embarkation':
                                popupULline="%d %s embarked here. %sFilter</a>" %(point[tag],person_or_people,href_event)
                            elif tag=='disembarkation':
                                popupULline="%d %s disembarked here. %sFilter</a>" %(point[tag],person_or_people,href_event)
                            elif tag=='post-disembarkation':
                                popupULline="%d %s ended up here. %sFilter</a>" %(point[tag],person_or_people,href_event)
                            else:
                                print("??????")
                            popuplines.append(popupULline)
                            
                            pointtags[tag]=point[tag]
                            
                    popupcontent="<strong>%s</strong><ul><li>%s</li></ul>" %(name,"</li><li>".join(popuplines))
                    feature_properties={
                        "name":name,
                        "size":nodesize,
                        "popupcontent":popupcontent,
                        "node_classes":pointtags,
                        "region_spss_code":point_id
                    }
                
                    feature_geometry={
                        "type":"Point",
                        "coordinates":coords
                    }
                
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
                "features": []
            }
            
            for feature in featurecollection:
                result_points['features'].append(feature)
            print("point map time:",time.time()-st)
        
            itinerary_names=["-".join([str(i) for i in itinerary]) for itinerary in itineraries]
            itinerary_names=[i for i in itinerary_names if i in route_curves]
            print(time.time()-st)
        
            leg_weights=Counter([l for i in itinerary_names for l in route_curves[i]])
            itinerary_weights=Counter(itinerary_names).most_common()
            itinerary_weights.reverse()
            #this trickery ensures that the heaviest route determines which sub-leg's geometry gets used
            leg_geometry={l:route_curves[i[0]][l] for i in itinerary_weights for l in route_curves[i[0]]}
        
            result_routes=[
                {
                    'geometry':leg_geometry[l]
                    ,'weight':leg_weights[l]
                } for l in leg_weights
            ]
            
            result={
                'routes':result_routes,
                'points':result_points,
                'region_vals_to_port_ids':region_vals_to_port_ids,
                'total_results_count':len(query)
            }
            
            return JsonResponse(result,safe=False)
            print("line map time:",time.time()-st)
        return JsonResponse(result,safe=False)
        
    return JsonResponse({'error': 'Unsupported'})


@require_POST
@csrf_exempt
def search_enslaver(request):
    data = json.loads(request.body)
    search = EnslaverSearch(**data['search_query'])
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
        for i, lang in enumerate(languages):
            lang_entry = EnslavedContributionLanguageEntry()
            lang_entry.contribution = contrib
            lang_entry.order = i + 1
            lang_group_id = lang.get('lang_group_id', None)
            if lang_group_id is None:
                transaction.rollback()
                return HttpResponseBadRequest(
                    'Invalid language entry in contribution')
            lang_entry.language_group = LanguageGroup.objects.get(
                pk=lang_group_id) if lang_group_id else None
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
