from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from voyages.apps.past.models import *
from name_search import NameSearchCache
import itertools
import json

def _generate_table(query, table_params):
    try:
        rows_per_page = int(table_params.get('length', 10))
        current_page_num = 1 + int(table_params.get('start', 0)) / rows_per_page
        paginator = Paginator(query, rows_per_page)
        page = paginator.page(current_page_num)
    except:
        page = query
    response_data = {}
    try:
        total_results = query.count()
    except:
        total_results = len(query)
    response_data['recordsTotal'] = total_results
    response_data['recordsFiltered'] = total_results
    response_data['draw'] = int(table_params.get('draw', 0))
    response_data['data'] = list(page)
    return response_data

def _get_alt_named(altModel, parent_fk, parent_map):
    key_fn = lambda x: getattr(x, parent_fk + '_id')
    res = {}
    for k, g in itertools.groupby(sorted(altModel.all(), key=key_fn), key=key_fn):
        alts = list(g)
        parent = getattr(alts[0], parent_fk)
        item = parent_map(parent)
        item['alts'] = sorted([a.name for a in alts])
        res[k] = item
    return res

@csrf_exempt
@cache_page(3600)
def get_modern_countries(request):
    mcs = {mc.id: mc.name for mc in ModernCountry.objects.all()}
    return JsonResponse(mcs)

@csrf_exempt
@cache_page(3600)
def get_ethnicities(request):
    parent_map = lambda e: {'name': e.name, 'language_group_id': e.language_group_id }
    models = AltEthnicityName.objects.prefetch_related('ethnicity')
    return JsonResponse(_get_alt_named(models, 'ethnicity', parent_map))

@csrf_exempt
@cache_page(3600)
def get_language_groups(request):
    parent_map = lambda lg: {'name': lg.name, 'lat': lg.latitude, 'lng': lg.longitude, 'country': lg.modern_country.name}
    models = AltLanguageGroupName.objects.prefetch_related(Prefetch('language_group', queryset=LanguageGroup.objects.select_related('modern_country')))
    return JsonResponse(_get_alt_named(models, 'language_group', parent_map))

@require_POST
@csrf_exempt
def search_enslaved(request):
    # A little bit of Python magic where we pass the dictionary
    # decoded from the JSON body as arguments to the EnslavedSearch
    # constructor.
    data = json.loads(request.body)
    search = EnslavedSearch(**data['search_query'])
    _name_fields = ['documented_name', 'name_first', 'name_second', 'name_third']
    _fields = ['enslaved_id',
        'age', 'gender', 'height', 'ethnicity__name', 'language_group__name', 'language_group__modern_country__name',
        'voyage__id', 'voyage__voyage_ship__ship_name', 'voyage__voyage_dates__first_dis_of_slaves',
        'voyage__voyage_itinerary__int_first_port_dis__place',
        'voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__place',
        'voyage__voyage_itinerary__imp_principal_port_slave_dis__place'] + _name_fields
    query = search.execute(_fields)
    output_type = data.get('output', 'resultsTable')
    # For now we only support outputing the results to DataTables.
    if output_type == 'resultsTable':
        table = _generate_table(query, data.get('tableParams', {}))
        page = table.get('data', [])
        NameSearchCache.load()
        for x in page:
            x['recordings'] = NameSearchCache.get_recordings([x[f] for f in _name_fields if f in x])
        return JsonResponse(table)
    return JsonResponse({'error': 'Unsupported'})