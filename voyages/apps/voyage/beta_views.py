from cache import VoyageCache, CachedGeo
from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from graphs import *
from haystack.query import SearchQuerySet
from search_indexes import VoyageIndex
from voyages.apps.common.export import download_xls
from voyages.apps.common.models import get_pks_from_haystack_results
from voyages.apps.voyage.models import *
import json

class SearchOperator():
    def __init__(self, front_end_op_str, back_end_op_str, list_type):
        self.front_end_op_str = front_end_op_str
        self.back_end_op_str = back_end_op_str
        self.list_type = list_type

# A list of operators used with Solr/Haystack to perform searches.
_operators_list = [
    SearchOperator('equals', 'exact', False),
    SearchOperator('is at most', 'lte', False),
    SearchOperator('is at least', 'gte', False), 
    SearchOperator('is between', 'range', True),
    SearchOperator('contains', 'contains', False),
    SearchOperator('is one of', 'in', True),
]
_operators_dict = {op.front_end_op_str: op for op in _operators_list}

index = VoyageIndex()
plain_text_suffix = '_plaintext'
plain_text_suffix_list = [f[:-len(plain_text_suffix)] for f in index.fields.keys() if f.endswith(plain_text_suffix)]
translate_suffix = '_lang_en'
translated_field_list = [f[:-len(translate_suffix)] for f in index.fields.keys() if f.endswith(translate_suffix)]

def perform_search(search, lang):
    items = search['items']
    search_terms = {}
    for item in items:
        term = item['searchTerm']
        operator = _operators_dict[item['op']]
        is_list = isinstance(term, list)
        if is_list and not operator.list_type:
            term = term[0]
        search_terms[u'var_' + unicode(item['varName']) + u'__' + unicode(operator.back_end_op_str)] = term
    result = SearchQuerySet().models(Voyage).filter(**search_terms)
    order_fields = search.get('orderBy')
    if order_fields:
        remaped_fields = []
        for field in order_fields:
            # Remap field names if they are plain text or language dependent.
            order_by_field = u'var_' + unicode(field['name'])
            if order_by_field in translated_field_list:
                order_by_field += '_lang_' + lang + '_exact'
            elif order_by_field in plain_text_suffix_list:
                order_by_field += '_plaintext_exact'
            if field['direction'] == 'desc':
                order_by_field = '-' + order_by_field
            remaped_fields.append(order_by_field)
        result = result.order_by(*remaped_fields)
    return result

# Construct a dict with all X-axes
_all_x_axes = {a.var_name: a for a in (graphs_x_axes + other_graphs_x_axes)}
_all_y_axes = {a.var_name: a for a in graphs_y_axes}
def get_results_graph(results, post):
    """
    post['graphData']: contains a single X axis and one or more Y axes.
    """
    graphData = post.get('graphData')
    if graphData is None:
        return HttpResponseBadRequest('Missing graph data')
    x_axis = graphData.get('xAxis', '')
    y_axes = graphData.get('yAxes', [])
    if not x_axis in _all_x_axes:
        return HttpResponseBadRequest('X axis is invalid: ' + str(x_axis) + '. Available: ' + str(_all_x_axes.keys()))
    if len(y_axes) == 0:
        return HttpResponseBadRequest('No Y axis specified')
    missing_y_axes = [y for y in y_axes if y not in _all_y_axes]
    if len(missing_y_axes) > 0:
        return HttpResponseBadRequest('Missing Y axes: ' + str(missing_y_axes) + '. Available: ' + str(_all_y_axes.keys()))
    output = get_graph_data(results, _all_x_axes[x_axis], [_all_y_axes[y] for y in y_axes])
    return JsonResponse({str(_(k)): [{'x': v[0], 'value': v[1]} for v in lst] for k, lst in output.items()})

def get_results_map_animation(results):
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
                yield {
                    "voyage_id": str(voyage.voyage_id),
                    "source_name": unicode(source[0].name),
                    "source_lat": str(source[0].lat),
                    "source_lng": str(source[0].lng),
                    "destination_name": unicode(destination[0].name),
                    "destination_lat": str(destination[0].lat),
                    "destination_lng": str(destination[0].lng),
                    "embarked": str(voyage.embarked),
                    "disembarked": str(voyage.disembarked),
                    "year": str(voyage.year),
                    "ship_ton": str(voyage.ship_ton) if voyage.ship_ton is not None else '0',
                    "ship_nationality_id": str(voyage.ship_nat_pk) if voyage.ship_nat_pk is not None else '0',
                    "ship_nationality_name": unicode(flag),
                    "ship_name": unicode(voyage.ship_name) if voyage.ship_name is not None else '',
                    "route": route
                }
    return JsonResponse(list(animation_response()), safe=False)

def get_results_map_flow(request, results):
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
    return render(
        request,
        "voyage/search_maps.datatemplate",
        {
            'map_ports': map_ports,
            'map_flows': map_flows
        },
        content_type='text/javascript')

def get_results_table(results, post):
    # Here we output a data set page.
    table_params = post['tableParams']
    rows_per_page = int(table_params['length'])
    current_page_num = 1 + int(table_params['start']) / rows_per_page
    paginator = Paginator(results, rows_per_page)
    page = paginator.page(current_page_num)
    reponse_data = {}
    total_results = results.count()
    reponse_data['recordsTotal'] = total_results
    reponse_data['recordsFiltered'] = total_results
    reponse_data['draw'] = int(table_params['draw'])
    reponse_data['data'] = [{k: v if v != '[]' else '' for k, v in x.get_stored_fields().items()} for x in page]
    return JsonResponse(reponse_data)

@require_POST
@csrf_exempt
def ajax_search(request):
    data = json.loads(request.body)
    search = data['searchData']
    lang = request.LANGUAGE_CODE
    results = perform_search(search, lang)
    # The output now depends on which type of
    # result the caller expects.
    output_type = data.get('output')
    if output_type == 'resultsTable':
        return get_results_table(results, data)
    elif output_type == 'mapAnimation':
        return get_results_map_animation(results)
    elif output_type == 'mapFlow':
        return get_results_map_flow(request, results)
    elif output_type == 'graph':
        return get_results_graph(results, data)
    return HttpResponseBadRequest('Unkown type of output.')

@require_POST
def ajax_download(request):
    data = json.loads(request.POST['data'])
    search = data['searchData']
    lang = request.LANGUAGE_CODE
    results = perform_search(search, lang)
    columns = data['cols']
    return download_xls(
        [[(col, 1) for col in columns]],
        [[item[col] for col in columns] for item in [x.get_stored_fields() for x in results]])

def search_view(request):
    return render(request, 'voyage/beta_search_main.html')