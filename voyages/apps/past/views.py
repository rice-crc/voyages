from __future__ import absolute_import, division, unicode_literals

import json
import uuid
from builtins import str
from datetime import date

from django.conf import settings
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Prefetch
from django.http import JsonResponse
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
                     EnslavedContributionNameEntry, EnslavedSearch, EnslaverRole, EnslaverSearch,
                     LanguageGroup, MultiValueHelper, ModernCountry, EnslavedNameSearchCache,
                     _modern_name_fields, _name_fields)

ENSLAVED_DATASETS = ['african-origins', 'oceans-of-kinfolk']

def _generate_table(query, table_params, data_adapter=None):
    try:
        rows_per_page = int(table_params.get('length', 10))
        current_page_num = 1 + \
            old_div(int(table_params.get('start', 0)), rows_per_page)
        paginator = Paginator(query, rows_per_page)
        page = paginator.page(current_page_num)
    except Exception:
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
    cache_key = '_filtered_places_ENSLAVED_' + str(dataset) + "_" + var_name
    # Most location variables come from VoyageItinerary, but
    # post_disembarkation_location is only present in the Enslaved model
    # directly.
    if var_name != 'post_disembark_location_id':
        var_name = 'voyage__voyage_itinerary__' + var_name
    qs = Enslaved.objects.filter(dataset=dataset). \
        select_related(var_name). \
        values_list(var_name, flat=True). \
        distinct()
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


def is_valid_name(name):
    return name is not None and name.strip() != ""


@require_POST
@csrf_exempt
def search_enslaved(request):
    # A little bit of Python magic where we pass the dictionary
    # decoded from the JSON body as arguments to the EnslavedSearch
    # constructor.
    data = json.loads(request.body)
    search = EnslavedSearch(**data['search_query'])
    fields = data.get('fields')
    if fields is None:
        fields = [
            'enslaved_id', 'age', 'gender', 'height', 'skin_color',
            'language_group__name',
            'register_country__name',
            'voyage_id', 'voyage__voyage_ship__ship_name',
            'voyage__voyage_dates__first_dis_of_slaves',
            'voyage__voyage_itinerary__int_first_port_dis__place',
            'voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__place',
            'voyage__voyage_itinerary__imp_principal_port_slave_dis__place',
            'captive_fate__name', 'post_disembark_location__place',
            EnslavedSearch.SOURCES_LIST, EnslavedSearch.ENSLAVERS_LIST
        ] + _name_fields + _modern_name_fields
    query = search.execute(fields)
    output_type = data.get('output', 'resultsTable')
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
        return JsonResponse(table)
    return JsonResponse({'error': 'Unsupported'})


@require_POST
@csrf_exempt
def search_enslaver(request):
    data = json.loads(request.body)
    search = EnslaverSearch(**data['search_query'])
    fields = data.get('fields')
    if fields is None:
        fields = [
            'principal_alias',
            'birth_year', 'birth_month', 'birth_day',
            'death_year', 'death_month', 'death_day',
            EnslavedSearch.SOURCES_LIST
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
    # TODO: Do we require the user to be authenticated in order to contribute?
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
            lang_entry.notes = lang.get('notes', '')
            lang_entry.save()
            language_ids.append(lang_entry.pk)
        result['language_ids'] = language_ids
    # The audio token is used so that the client can upload audio files for
    # storage. The token is used to avoid overwriting any files by accident and
    # to prevent malicious players from storing arbitrary data in our servers.
    result['audio_token'] = token
    return JsonResponse(result)


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
    file_name = str(contrib_pk) + "_" + str(name_pk) + ".webm"
    with open('%s/%s/%s' % (settings.MEDIA_ROOT, 'audio', file_name),
              'wb+') as destination:
        destination.write(request.body)
    return JsonResponse({'len': len(request.body)})
