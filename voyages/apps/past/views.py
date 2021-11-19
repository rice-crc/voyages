from __future__ import absolute_import, division, unicode_literals

import itertools
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
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from past.utils import old_div

from .models import (AltLanguageGroupName, Enslaved,
                     EnslavedContribution, EnslavedContributionLanguageEntry,
                     EnslavedContributionNameEntry, EnslavedSearch,
                     LanguageGroup, ModernCountry, NameSearchCache,
                     _modern_name_fields, _name_fields, extract_sources)


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
    qlg = LanguageGroup.objects.prefetch_related('alt_names')
    qmc = ModernCountry.objects.prefetch_related(Prefetch('languages', queryset=qlg)).filter(languages__name__isnull=False).order_by('name', 'languages__name')
    flat = qmc.values('name', 'languages__id', "languages__latitude", "languages__longitude", 'languages__name', 'languages__alt_names__name')
    grouped = {k: list(g) for k, g in itertools.groupby(flat, key=lambda value: (value['name'], value['languages__name']))}
    data = { g[0]['languages__id']: { "country": k[0], "name": k[1], "latitude": float(g[0]["languages__latitude"]), "longitude": float(g[0]["languages__longitude"]), "alts": [alt for alt in [x['languages__alt_names__name'] for x in g] if alt and alt != k[1]]} for k, g in grouped.items() }
    return JsonResponse(data)


def restore_permalink(_, link_id):
    """Redirect the page with a URL param"""
    return redirect("/past/database#searchId=" + link_id)

_SOURCES_FIELD = 'sources_list'

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
            'enslaved_id', 'age', 'gender', 'height',
            'language_group__name',
            'register_country', 'sources_list',
            'voyage__id', 'voyage__voyage_ship__ship_name',
            'voyage__voyage_dates__first_dis_of_slaves',
            'voyage__voyage_itinerary__int_first_port_dis__place',
            'voyage__voyage_itinerary__imp_principal_place_of_slave_purchase_'
            '_place',
            'voyage__voyage_itinerary__imp_principal_place_of_slave_purchase_'
            '_latitude',
            'voyage__voyage_itinerary__imp_principal_place_of_slave_purchase_'
            '_longitude',
            'voyage__voyage_itinerary__imp_principal_port_slave_dis__place',
            _SOURCES_FIELD
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
                # Our ORM query returns all source data as a single string. Here
                # we extract structured source data (e.g. an array of dicts)
                # so that the API consumer has a better experience.
                if _SOURCES_FIELD in row:
                    row[_SOURCES_FIELD] = list(extract_sources(row[_SOURCES_FIELD]))
            return page

        table = _generate_table(query, data.get('tableParams', {}), adapter)
        page = table.get('data', [])
        NameSearchCache.load()
        for entry in page:
            entry['recordings'] = NameSearchCache.get_recordings(
                [entry[f] for f in _name_fields if f in entry])
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
