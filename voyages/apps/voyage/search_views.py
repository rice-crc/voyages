from cache import VoyageCache, CachedGeo
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import get_language
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from graphs import *
from globals import voyage_timeline_variables, table_columns, table_rows, table_functions
from haystack.query import SearchQuerySet
from search_indexes import VoyageIndex
from voyages.apps.common.export import download_xls
from voyages.apps.common.models import get_pks_from_haystack_results, SavedQuery
from voyages.apps.common.views import get_ordered_places
from voyages.apps.common.views import get_datatable_json_result as get_results_table
from voyages.apps.voyage.models import *
from voyages.apps.voyage.search_indexes import VoyageIndex
from voyages.apps.voyage.tables import *
import csv
import itertools
import json
import re
import unicodecsv

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
    search_terms[u'var_intra_american_voyage__exact'] = json.loads(search_terms.get(u'var_intra_american_voyage__exact', 'false'))
    result = SearchQuerySet().models(Voyage).filter(**search_terms)
    order_fields = search.get('orderBy')
    if order_fields:
        remaped_fields = []
        for field in order_fields:
            # Remap field names if they are plain text or language dependent.
            order_by_field = u'var_' + unicode(field['name'])
            if order_by_field.endswith('_lang'):
                order_by_field += '_' + lang + '_exact'
            elif order_by_field in translated_field_list:
                order_by_field += '_lang_' + lang + '_exact'
            elif order_by_field in plain_text_suffix_list:
                order_by_field += '_plaintext_exact'
            if field['direction'] == 'desc':
                order_by_field = '-' + order_by_field
            remaped_fields.append(order_by_field)
        result = result.order_by(*remaped_fields)
    return result

def get_results_pivot_table(results, post):
    row_field = post.get('row_field')
    col_field = post.get('col_field')
    pivot_functions = post.get('pivot_functions')
    if row_field is None or col_field is None or pivot_functions is None:
        return HttpResponseBadRequest('Post data must contain row_field, col_field, and pivot_functions')
    row_data = get_pivot_table_advanced(results, row_field, col_field, pivot_functions, post.get('range'))
    VoyageCache.load()

    def grouping(seq):
        return [(_(g[0]), sum([1 for __ in g[1]])) for g in itertools.groupby(seq)]

    def region_extra_header_map(port_ids):
        regions = [VoyageCache.regions[VoyageCache.ports_by_value[x].parent].name for x in port_ids]
        return grouping(regions)

    def broad_region_from_port_extra_header_map(port_ids):
        broad_regions = [VoyageCache.broad_regions[VoyageCache.regions[VoyageCache.ports_by_value[x].parent].parent].name for x in port_ids]
        return grouping(broad_regions)

    def broad_region_extra_header_map(region_ids):
        broad_regions = [VoyageCache.broad_regions[VoyageCache.regions_by_value[x].parent].name for x in region_ids]
        return grouping(broad_regions)

    def get_header_map(header):
        if '_idnum' in header:
            if 'place' in header or 'port' in header:
                return lambda x: _(VoyageCache.ports_by_value[x].name), [broad_region_from_port_extra_header_map, region_extra_header_map]
            if 'broad_region' in header:
                return lambda x: _(VoyageCache.broad_regions_by_value[x].name), None
            if 'region' in header:
                return lambda x: _(VoyageCache.regions_by_value[x].name), [broad_region_extra_header_map]
            if 'nation' in header:
                return lambda x: _(VoyageCache.nations_by_value[x]), None
        return lambda x: x, None

    col_map, col_extra_headers = get_header_map(col_field)
    row_map, row_extra_headers = get_header_map(row_field)
    pivot_table = PivotTable(row_data, col_map, row_map, post.get('omit_empty', '').lower() == 'true')
    pivot_dict = pivot_table.to_dict()
    # Add extra column or row headers.
    if col_extra_headers:
        pivot_dict['col_extra_headers'] = [f(pivot_table.original_columns) for f in col_extra_headers]
    if row_extra_headers:
        pivot_dict['row_extra_headers'] = [f(pivot_table.original_rows) for f in row_extra_headers]
    return JsonResponse(pivot_dict)

# Construct a dict with Timeline variables.
_all_timeline_vars = {t[0] + t[3]: {'var_name': t[3], 'time_line_func': t[2], 'var_description': t[1]} for t in voyage_timeline_variables}
def get_results_timeline(results, post):
    """
    post['timelineVariable']: the timeline variable that will be the source of the data.
    """
    timeline_var_name = post.get('timelineVariable')
    timeline_var = _all_timeline_vars.get(timeline_var_name)
    if not timeline_var:
        return HttpResponseBadRequest('Timeline variable is invalid ' + str(timeline_var_name) + '. Available: ' + str(_all_timeline_vars.keys()))
    timeline_var_name = timeline_var['var_name']
    timeline_data = sorted(timeline_var['time_line_func'](results, timeline_var_name), key=lambda t: t[0])
    return JsonResponse({'var_name': timeline_var_name, 'data': [{'year': t[0], 'value': t[1]} for t in timeline_data]})

# Construct a dict with all X/Y-axes
_all_x_axes = {a.id(): a for a in (graphs_x_axes + other_graphs_x_axes)}
_all_y_axes = {a.id() + '_' + a.mode: a for a in graphs_y_axes} # MODES: avg, freq, count, sum 
def get_results_graph(results, post):
    """
    post['graphData']: contains a single X axis (xAxis key) and one or more Y axes (yAxes key).
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
    x_axis_info = _all_x_axes[x_axis]
    output = get_graph_data(results, x_axis_info, [_all_y_axes[y] for y in y_axes])
    data_format = post.get('data_format', 'json')
    if data_format == 'json':
        return JsonResponse({unicode(_(k)): [{'x': v[0], 'value': v[1]} for v in lst] for k, lst in output.items()})
    if data_format == 'csv':
        # Here we need to build a tabular data format. The output
        # is a collection of series, each correspond to a column in
        # the export. It is not necessary that they have the same row
        # sets, so we first build a row index to account for "blank"
        # cells in the output.
        all_series = output.values()
        row_index = sorted(set(sum([[v[0] for v in lst] for lst in all_series], [])))
        columns = [{v[0]: v[1] for v in lst} for lst in all_series]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="graph.csv"'
        writer = csv.writer(response)
        writer.writerow([x_axis_info.description or ''] + output.keys())
        for index in row_index:
            writer.writerow([index] + [col.get(index, '') for col in columns])
        return response
    return JsonResponse({'error': 'Invalid format in request ' + str(data_format)})

def get_results_map_animation(results):
    VoyageCache.load()
    all_voyages = VoyageCache.voyages
    from voyages.apps.voyage.maps import VoyageRoutesCache
    all_routes = VoyageRoutesCache.load()

    keys = get_pks_from_haystack_results(results)
    items = []
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
            items.append({
                "voyage_id": str(voyage.voyage_id),
                "src": voyage.emb_pk,
                "dst": voyage.dis_pk,
                "embarked": str(voyage.embarked),
                "disembarked": str(voyage.disembarked),
                "year": str(voyage.year),
                "month": str(voyage.month),
                "ship_ton": str(voyage.ship_ton) if voyage.ship_ton is not None else '0',
                "nat_id": str(voyage.ship_nat_pk) if voyage.ship_nat_pk is not None else '0',
                "ship_name": unicode(voyage.ship_name) if voyage.ship_name is not None else '',
            })
    return JsonResponse(items, safe=False)

def get_results_map_flow(request, results):
    map_ports = {}
    map_flows = {}

    def add_port(geo):
        result = geo is not None and len(geo) == 3 and geo[0].show and geo[1].show and geo[2].show and \
            geo[0].lat and geo[0].lng and geo[1].lat and geo[1].lng and geo[2].lat and geo[2].lng
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
        "search_maps.datatemplate",
        {
            'map_ports': map_ports,
            'map_flows': map_flows
        },
        content_type='text/javascript')

def get_results_summary_stats(results):
    from voyages.apps.voyage.views import retrieve_summary_stats
    summary = retrieve_summary_stats(results)
    return JsonResponse({'data': summary})

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
        target_lang = 'lang_' + lang
        requested_fields = [x['data'] for x in data['tableParams']['columns']]
        requested_fields = set([f + '_' + lang if f.endswith('lang') else f for f in requested_fields])
        return get_results_table(results, data, 
            field_filter=lambda field_name: field_name in requested_fields,
            key_adapter=lambda key_val: key_val[0].replace(target_lang, 'lang'))
    elif output_type == 'mapAnimation':
        return get_results_map_animation(results)
    elif output_type == 'mapFlow':
        return get_results_map_flow(request, results)
    elif output_type == 'graph':
        return get_results_graph(results, data)
    elif output_type == 'timeline':
        return get_results_timeline(results, data)
    elif output_type == 'pivotTable':
        return get_results_pivot_table(results, data)
    elif output_type == 'summaryStats':
        return get_results_summary_stats(results)
    return HttpResponseBadRequest('Unkown type of output.')

download_header_map = {}

def get_download_header(var_name):
    """
    Here we use a bit of magic to follow relationships in Django models
    specified on the model_attr of indexed fields.
    """
    def follow_field(model, name_to_follow):
        split = name_to_follow.find('__')
        current = name_to_follow[:split] if split > 0 else name_to_follow
        try:
            f = model._meta.get_field(current)
        except:
            f = None
        result = f.verbose_name if f else ''
        if split > 0 and f:
            result += ' ' + follow_field(f.remote_field.model, name_to_follow[split + 2:])
        return result
    def smart(h):
        # Clean up name.
        h = h.lower()
        words = h.split(' ')
        for w in words:
            pos = h.find(w) + len(w)
            h = h[:pos] + h[pos:].replace(w, '')
        h = re.sub(r'\s+', ' ', h)
        return h[:1].upper() + h[1:]
    def smart_var_name():
        s = var_name.lower()
        s = s.replace('var_', '')
        s = s.replace('_', ' ')
        s = s.replace('imp ', 'imputed ')
        s = s.replace('plaintext', '')
        return s[:1].upper() + s[1:]
    header = download_header_map.get(var_name)
    if header is None:
        if hasattr(VoyageIndex, var_name):
            index = getattr(VoyageIndex, var_name)
            if index and hasattr(index, 'model_attr') and index.model_attr:
                model = index.related_model if hasattr(index, 'related_model') else Voyage
                header = smart(follow_field(model, index.model_attr))
            download_header_map[var_name] = header
    return header if (not header is None and header != '') else smart_var_name()

@require_POST
@csrf_exempt
def ajax_download(request):
    """
    API to download results in tabular format (Excel or CSV).
    The parameter 'data' of the request should contain a JSON
    encoded object.
    
    The member 'cols' is an array of columns which correspond
    to Solr indexed variables. If this array is empty, all
    columns are exported.

    The default export mode is Excel. To export as a CSV, set
    'excel_mode' to False.
    """
    data = json.loads(request.POST['data'])
    search = data['searchData']
    lang = request.LANGUAGE_CODE
    results = perform_search(search, lang)
    columns = data['cols']
    excel_mode = data.get('excel_mode', True)
    if len(columns) == 0:
        # Get all columns.
        lang_version = 'lang_' + lang
        columns = [col for col in results[0].get_stored_fields().keys() if 'lang' not in col or lang_version in col]
        # Remove columns which have a name matching a prefix of another column.
        copy = list(columns)
        columns = [col for col in copy if len([x for x in copy if len(x) > len(col) and col in x]) == 0]
    else:
        columns = [col if 'lang' not in col or 'lang_' in col else col + '_' + lang for col in columns]
    if excel_mode:
        return download_xls(
            [[(_(get_download_header(col)), 1) for col in columns]],
            [[item[col] for col in columns] for item in [x.get_stored_fields() for x in results]])
    else:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'
        writer = unicodecsv.DictWriter(response, fieldnames=columns)
        #writer.writeheader()
        writer.writerow({col: _(get_download_header(col)) for col in columns})
        for x in results:
            item = x.get_stored_fields()
            writer.writerow({col: item[col] for col in columns})
        return response

_options_model = {
    'var_outcome_voyage': ParticularOutcome.objects,
    'var_outcome_slaves': SlavesOutcome.objects,
    'var_outcome_ship_captured': VesselCapturedOutcome.objects,
    'var_outcome_owner': OwnerOutcome.objects,
    'var_resistance': Resistance.objects,
    'var_nationality': Nationality.objects,
    'var_rig_of_vessel': RigOfVessel.objects,
    'var_tonnage': TonType.objects,
    # Imputed nationality is currently restricted to a subset of code-values.
    'var_imputed_nationality': Nationality.objects.filter(value__in=[3, 6, 7, 8, 9, 10, 15, 30]),
}

@csrf_exempt
def get_var_options(request):
    """
    This API fetches the values allowed for a given variable on
    the database. For efficiency, we will cache these values since
    they do not change frequently.
    The caller must specify which variable is needed in the request.
    """
    data = json.loads(request.body)
    var_name = data.get('var_name', '(blank)')
    options_model = _options_model.get(var_name)
    if not options_model:
        return HttpResponseBadRequest('Caller passed: "' + var_name + '". Must specify some var_name in ' + str(_options_model.keys()))
    # Check if we have the results cached to avoid a db hit.
    cache_key = '_options_' + var_name
    response_data = cache.get(cache_key)
    is_cached = response_data is not None
    if not is_cached:
        response_data = [{'label': x.label, 'value': x.value, 'pk': x.pk} for x in options_model.all()]
        # Cache the data for 24h.
        cache.set(cache_key, response_data, 24 * 60 * 60)
    for d in response_data:
        d['label'] = _(d['label'])
    return JsonResponse({'var_name': var_name, 'is_cached': is_cached, 'data': response_data})

@csrf_exempt
def get_filtered_places(request):
    """
    Obtains a list of places and corresponding regions/broad regions
    that are present in a given field of VoyageItinerary.
    """
    data = json.loads(request.body)
    blank = '|blank|'
    var_name = data.get('var_name', blank)
    cache_key = '_filtered_places_' + var_name
    result = cache.get(cache_key)
    is_cached = result is not None
    if not is_cached:
        place_query = None
        if var_name != blank:
            pks = list(VoyageItinerary.objects.values_list(var_name, flat=True).distinct())
            place_query = Place.objects.filter(pk__in=pks)
        result = get_ordered_places(place_query, False)
        # Cache the data for 24h.
        cache.set(cache_key, result, 24 * 60 * 60)
    for d in result:
        # Translate the corresponding entry.
        geo_type = d['type']
        d[geo_type] = _(d[geo_type])
    return JsonResponse({
        'filtered_var_name': var_name if var_name != blank else 'None',
        'is_cached': is_cached,
        'data': result
    })

@csrf_exempt
@require_POST
def get_all_sources(request):
    data = json.loads(request.body)
    order_by = None
    results = SearchQuerySet().models(VoyageSources)
    try:
        # Process data table filter.
        table_params = data['tableParams']
        search = table_params['search']['value']
        results = results.filter(text__contains=search)
    except: pass
    try:
        # Process data table sorting.
        table_params = data['tableParams']
        order_info = table_params['order'][0]
        order_by = table_params['columns'][int(order_info['column'])]['data']
        if order_info['dir'] == 'desc':
            order_by = '-' + order_by
        results = results.order_by(order_by)
    except: pass
    output_fields = ['group_name', 'short_ref', 'full_ref']
    return get_results_table(results, data, field_filter=lambda f: f in output_fields)

@csrf_exempt
@require_POST
def save_query(request):
    saved_query = SavedQuery()
    saved_query.query = request.body
    saved_query.is_legacy = False
    saved_query.save()
    return JsonResponse({'saved_query_id': saved_query.pk})

def get_saved_query(request, query_id):
    q = SavedQuery.objects.get(pk=query_id)
    return HttpResponse(q.query, content_type='application/json')
