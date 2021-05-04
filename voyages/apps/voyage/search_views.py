from __future__ import absolute_import, print_function, unicode_literals

import csv
import itertools
import json
import logging
import os
import re
from builtins import str

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from haystack.inputs import Raw
from haystack.query import SearchQuerySet
import unicodecsv

from voyages.apps.common.export import download_xls
from voyages.apps.common.models import (SavedQuery,
                                        get_pks_from_haystack_results)
from voyages.apps.common.views import \
    get_datatable_json_result as get_results_table
from voyages.apps.common.views import get_ordered_places
from voyages.apps.voyage.models import (Nationality, OwnerOutcome,
                                        ParticularOutcome, Place, Resistance,
                                        RigOfVessel, SlavesOutcome, TonType,
                                        VesselCapturedOutcome, Voyage,
                                        VoyageDataset, VoyageItinerary,
                                        VoyageSources)
from voyages.apps.voyage.views import retrieve_summary_stats

from .cache import CachedGeo, VoyageCache
from .globals import voyage_timeline_variables
from .graphs import (get_graph_data, graphs_x_axes, graphs_y_axes,
                     other_graphs_x_axes)
from .search_indexes import ok_to_show_animation, VoyageIndex
from .tables import PivotTable, get_pivot_table_advanced


class SearchOperator:

    def __init__(self, front_end_op_str, back_end_op_str, list_type):
        self.front_end_op_str = front_end_op_str
        self.back_end_op_str = back_end_op_str
        self.list_type = list_type


_op_eq = SearchOperator('equals', 'exact', False)
_op_at_most = SearchOperator('is at most', 'lte', False)
_op_at_least = SearchOperator('is at least', 'gte', False)
_op_between = SearchOperator('is between', 'range', True)
_op_contains = SearchOperator('contains', 'contains', False)
_op_one_of = SearchOperator('is one of', 'in', True)
# A list of operators used with Solr/Haystack to perform searches.
_operators_list = [
    _op_eq, _op_at_most, _op_at_least, _op_between, _op_contains, _op_one_of
]
_operators_dict = {op.front_end_op_str: op for op in _operators_list}

index = VoyageIndex()
plain_text_suffix = '_plaintext'
plain_text_suffix_list = [
    f[:-len(plain_text_suffix)]
    for f in list(index.fields.keys())
    if f.endswith(plain_text_suffix)
]
translate_suffix = '_lang_en'
translated_field_list = [
    f[:-len(translate_suffix)]
    for f in list(index.fields.keys())
    if f.endswith(translate_suffix)
]


def perform_search(search, lang):
    items = search['items']
    search_terms = {}
    custom_terms = []
    sqs = SearchQuerySet()
    for item in items:
        term = item['searchTerm']
        operator = _operators_dict[item['op']]
        is_list = isinstance(term, list)
        if is_list and not operator.list_type:
            term = term[0]
        skip = False
        if operator.front_end_op_str == _op_contains.front_end_op_str:
            m = re.match(r'^\s*["\u201c](\*?)([^\*]*)(\*?)["\u201d]\s*$', term)
            if m:
                # Change to exact match and remove quotes.
                # Make sure we sanitize the input.
                term = sqs.query.clean(m.group(2))
                operator = _op_eq
                # Here we are using Solr's format, which is not very portable,
                # but at this stage this project is very dependent on Solr
                # anyway. If the search is really for a full exact match, then
                # we search on the plaintext_exact variant of the field. If it
                # is a "contains" the exact search terms, then we use the
                # plaintext variant instead.
                xt = '_exact' if len(m.group(1)) + len(m.group(3)) == 0 else ''
                custom_terms.append(
                    f'var_{item["varName"]}_plaintext{xt}:("{term}")')
                skip = True
        if not skip:
            search_terms[f'var_{item["varName"]}__'
                         f'{operator.back_end_op_str}'] = term
    dataset = search_terms.pop(u'var_dataset__exact', None)
    if dataset is None:
        # Map I-Am searches to the appropriate dataset.
        dataset = VoyageDataset.Transatlantic
        try:
            if json.loads(
                    search_terms.get(u'var_intra_american_voyage__exact',
                                     'false')):
                dataset = VoyageDataset.IntraAmerican
            rem_keys = [
                k for k in list(search_terms.keys())
                if k.startswith(u'var_intra_american_voyage')
            ]
            for k in rem_keys:
                search_terms.pop(k)
        except Exception:
            pass
    else:
        try:
            dataset = int(dataset)
        except Exception:
            dataset = VoyageDataset.Transatlantic
    if dataset >= 0:
        search_terms[u'var_dataset__exact'] = dataset
    result = sqs.models(Voyage).filter(**search_terms)
    for ct in custom_terms:
        result = result.filter(content=Raw(ct, clean=True))
    order_fields = search.get('orderBy')
    if order_fields:
        remaped_fields = []
        for field in order_fields:
            # Remap field names if they are plain text or language dependent.
            order_by_field = u'var_' + str(field['name'])
            if order_by_field.endswith('_partial'):
                # Partial dates are encoded in a way that is terrible for
                # sorting MM,DD,YYYY. Therefore we use the original Date value
                # (which defaults month, day to 1).
                order_by_field = order_by_field[0:-8]
            if order_by_field.endswith('_lang'):
                order_by_field += '_' + lang + '_exact'
            elif order_by_field in translated_field_list:
                order_by_field += '_lang_' + lang + '_exact'
            elif order_by_field in plain_text_suffix_list:
                order_by_field += '_plaintext_exact'
            if field['direction'] == 'desc':
                order_by_field = '-' + order_by_field
            elif order_by_field.endswith('_exact'):
                remaped_fields.append('eq(' + order_by_field + ', \' \')')
            remaped_fields.append(order_by_field)
        result = result.order_by(*remaped_fields)
    return result


def get_results_pivot_table(results, post):
    row_field = post.get('row_field')
    col_field = post.get('col_field')
    pivot_functions = post.get('pivot_functions')
    if row_field is None or col_field is None or pivot_functions is None:
        return HttpResponseBadRequest(
            'Post data must contain row_field, col_field, and pivot_functions')
    row_data = get_pivot_table_advanced(results, row_field, col_field,
                                        pivot_functions, post.get('range'))
    VoyageCache.load()

    def grouping(seq):
        return [(_(g[0]), sum([1 for __ in g[1]]))
                for g in itertools.groupby(seq)]

    def region_extra_header_map(port_ids):
        regions = [
            VoyageCache.regions[VoyageCache.ports_by_value[x].parent].name
            for x in port_ids
        ]
        return grouping(regions)

    def broad_region_from_port_extra_header_map(port_ids):
        broad_regions = [
            VoyageCache.broad_regions[VoyageCache.regions[
                VoyageCache.ports_by_value[x].parent].parent].name
            for x in port_ids
        ]
        return grouping(broad_regions)

    def broad_region_extra_header_map(region_ids):
        broad_regions = [VoyageCache.broad_regions[
            VoyageCache.regions_by_value[x].parent
        ].name for x in region_ids]
        return grouping(broad_regions)

    def get_header_map(header):
        if '_idnum' not in header:
            return lambda x: x, None
        if 'place' in header or 'port' in header:
            return lambda x: _(VoyageCache.ports_by_value[
                x].name), [
                    broad_region_from_port_extra_header_map,
                    region_extra_header_map]
        if 'broad_region' in header:
            return lambda x: _(VoyageCache.broad_regions_by_value[
                x].name), None
        if 'region' in header:
            return lambda x: _(VoyageCache.regions_by_value[
                x].name), [broad_region_extra_header_map]
        if 'nation' in header:
            return lambda x: _(VoyageCache.nations_by_value[
                x]), None
        return lambda x: x, None

    col_map, col_extra_headers = get_header_map(col_field)
    row_map, row_extra_headers = get_header_map(row_field)
    pivot_table = PivotTable(row_data, col_map, row_map,
                             post.get('omit_empty', '').lower() == 'true')
    pivot_dict = pivot_table.to_dict()
    # Add extra column or row headers.
    if col_extra_headers:
        pivot_dict['col_extra_headers'] = [
            f(pivot_table.original_columns) for f in col_extra_headers
        ]
    if row_extra_headers:
        pivot_dict['row_extra_headers'] = [
            f(pivot_table.original_rows) for f in row_extra_headers
        ]
    return JsonResponse(pivot_dict)


# Construct a dict with Timeline variables.
_all_timeline_vars = {
    t[0] + t[3]: {
        'var_name': t[3],
        'time_line_func': t[2],
        'var_description': t[1]
    } for t in voyage_timeline_variables
}


def get_results_timeline(results, post):
    """
    post['timelineVariable']: the timeline variable that will be the source of
    the data.
    """
    timeline_var_name = post.get('timelineVariable')
    timeline_var = _all_timeline_vars.get(timeline_var_name)
    if not timeline_var:
        return HttpResponseBadRequest(
            f'Timeline variable is invalid {timeline_var_name}. '
            f'Available: {list(_all_timeline_vars.keys())}')
    timeline_var_name = timeline_var['var_name']
    timeline_data = sorted(timeline_var['time_line_func'](results,
                                                          timeline_var_name),
                           key=lambda t: t[0])
    return JsonResponse({
        'var_name': timeline_var_name,
        'data': [{
            'year': t[0],
            'value': t[1]
        } for t in timeline_data]
    })


# Construct a dict with all X/Y-axes
_all_x_axes = {a.id(): a for a in graphs_x_axes + other_graphs_x_axes}
# MODES: avg, freq, count, sum
_all_y_axes = {a.id() + '_' + a.mode: a for a in graphs_y_axes}


def get_results_graph(results, post):
    """
    post['graphData']: contains a single X axis (xAxis key) and one or more Y
    axes (yAxes key).
    """
    graph_data = post.get('graphData')
    if graph_data is None:
        return HttpResponseBadRequest('Missing graph data')
    x_axis = graph_data.get('xAxis', '')
    y_axes = graph_data.get('yAxes', [])
    if x_axis not in _all_x_axes:
        return HttpResponseBadRequest(f'X axis is invalid: {x_axis}. '
                                      f'Available: {list(_all_x_axes.keys())}')
    if len(y_axes) == 0:
        return HttpResponseBadRequest('No Y axis specified')
    missing_y_axes = [y for y in y_axes if y not in _all_y_axes]
    if len(missing_y_axes) > 0:
        return HttpResponseBadRequest(f'Missing Y axes: {missing_y_axes}. '
                                      f'Available: {list(_all_y_axes.keys())}')
    x_axis_info = _all_x_axes[x_axis]
    output = get_graph_data(results, x_axis_info,
                            [_all_y_axes[y] for y in y_axes])
    data_format = post.get('data_format', 'json')
    if data_format == 'json':
        return JsonResponse({
            str(_(k)): [{'x': v[0], 'value': v[1]} for v in lst]
            for k, lst in list(output.items())})
    if data_format == 'csv':
        # Here we need to build a tabular data format. The output
        # is a collection of series, each correspond to a column in
        # the export. It is not necessary that they have the same row
        # sets, so we first build a row index to account for "blank"
        # cells in the output.
        all_series = list(output.values())
        row_index = sorted(
            set(sum([[v[0] for v in lst] for lst in all_series], [])))
        columns = [{v[0]: v[1] for v in lst} for lst in all_series]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="graph.csv"'
        writer = csv.writer(response)
        writer.writerow([x_axis_info.description or ''] + list(output.keys()))
        for index in row_index:
            writer.writerow([index] + [col.get(index, '') for col in columns])
        return response
    return JsonResponse(
        {'error': 'Invalid format in request ' + str(data_format)})


def get_results_map_animation(results, allow_no_numbers=False):
    VoyageCache.load()
    all_voyages = VoyageCache.voyages

    keys = get_pks_from_haystack_results(results)
    items = []
    for pk in keys:
        voyage = all_voyages.get(pk)
        if voyage is None:
            print("Missing voyage with PK" + str(pk))
            continue

        def can_show(ph):
            return ph is not None and (ph[0].show or ph[1].show)

        if ok_to_show_animation(voyage, can_show, allow_no_numbers):
            # flag = VoyageCache.nations.get(voyage.ship_nat_pk) or ''
            source = CachedGeo.get_hierarchy(voyage.emb_pk)
            destination = CachedGeo.get_hierarchy(voyage.dis_pk)
            items.append({
                "voyage_id": voyage.voyage_id,
                "src": voyage.emb_pk,
                "dst": voyage.dis_pk,
                "regsrc": source[1].pk,
                "bregsrc": source[2].pk,
                "bregdst": destination[2].pk,
                "embarked": voyage.embarked or 0,
                "disembarked": voyage.disembarked or 0,
                "year": voyage.year,
                "month": voyage.month,
                "ship_ton": voyage.ship_ton or 0,
                "nat_id": voyage.ship_nat_pk or 0,
                "ship_name": str(voyage.ship_name or ''),
            })
    return JsonResponse(items, safe=False)


@cache_page(3600)
def get_compiled_routes(request):
    network_name = request.GET.get('networkName')
    route_type = request.GET.get('routeType')
    names = ['trans', 'intra']
    if network_name is None or network_name not in names:
        return JsonResponse({
            "error":
                "Value of 'networkName' parameter should be in " + str(names)
        })
    route_types = ['port', 'regional']
    if route_type is None or route_type not in route_types:
        return JsonResponse({
            "error":
                f"Value of 'routeType' parameter should be in {route_types}"
        })
    fpath = os.path.join(settings.STATIC_ROOT, "maps/js", network_name,
                         route_type + "_routes.json")
    return HttpResponse(content=open(fpath, 'rb'),
                        content_type='application/json')


@cache_page(3600)
def get_timelapse_port_regions(_):
    # Generate a simple JSON that reports the broad regions.
    VoyageCache.load()
    regions = {
        'src': {
            pk: {
                'value': r.value,
                'name': r.name
            } for pk, r in list(VoyageCache.regions.items()) if r.parent == 1
        },
        'dst': {
            pk: {
                'value': r.value,
                'name': r.name
            } for pk, r in list(VoyageCache.broad_regions.items())
        }
    }
    return JsonResponse(regions)


def get_results_map_flow(request, results):
    map_ports = {}
    map_flows = {}

    def check_geo(geo):
        return geo.show and geo.lat and geo.lng

    def add_port(geo):
        result = geo and len(geo) == 3 and all([check_geo(g) for g in geo])
        if result and not geo[0].pk in map_ports:
            map_ports[geo[0].pk] = geo
        return result

    def add_flow(source, destination, embarked, disembarked):
        result = embarked is not None and disembarked is not None and add_port(
            source) and add_port(destination)
        if result:
            flow_key = int(source[0].pk) * 2147483647 + int(destination[0].pk)
            current = map_flows.get(flow_key)
            if current is not None:
                embarked += current[2]
                disembarked += current[3]
            map_flows[flow_key] = (source[0].name, destination[0].name,
                                   embarked, disembarked)
        return result

    # Ensure cache is loaded.
    VoyageCache.load()
    all_voyages = VoyageCache.voyages
    missed_embarked = 0
    missed_disembarked = 0
    # Set up an unspecified source that will be used if the appropriate setting
    # is enabled
    geo_unspecified = CachedGeo(-1, -1, _('Africa, port unspecified'),
                                0.05, 9.34, True, None)
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
        add_flow(source, destination, voyage.embarked, voyage.disembarked)
    if missed_embarked > 0 or missed_disembarked > 0:
        logging.getLogger('voyages').info(
            'Missing flow: (%d, %d)', missed_embarked, missed_disembarked)
    return render(request,
                  "search_maps.datatemplate", {
                      'map_ports': map_ports,
                      'map_flows': map_flows
                  },
                  content_type='text/javascript')


def get_results_summary_stats(results):
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
        requested_fields = {
            f + '_' + lang if f.endswith('lang') else f
            for f in requested_fields
        }
        return get_results_table(
            results,
            data,
            field_filter=lambda field_name: field_name in requested_fields,
            key_adapter=lambda keyval: keyval[0].replace(target_lang, 'lang'))
    if output_type == 'mapAnimation':
        return get_results_map_animation(results)
    if output_type == 'mapFlow':
        return get_results_map_flow(request, results)
    if output_type == 'graph':
        return get_results_graph(results, data)
    if output_type == 'timeline':
        return get_results_timeline(results, data)
    if output_type == 'pivotTable':
        return get_results_pivot_table(results, data)
    if output_type == 'summaryStats':
        return get_results_summary_stats(results)
    return HttpResponseBadRequest('Unkown type of output.')


download_header_map = {
    "var_captain":
        "Captain's name",
    "var_crew_died_complete_voyage":
        "Crew deaths during voyage",
    "var_crew_first_landing":
        "Crew at first landing of slaves",
    "var_crew_voyage_outset":
        "Crew at voyage outset",
    "var_date_departed_africa":
        "Date vessel departed Africa",
    "var_departure_last_place_of_landing":
        "Date vessel departed for homeport",
    "var_display_settings":
        "Display in compact mode",
    "var_first_dis_of_slaves":
        "Date vessel arrived with slaves",
    "var_first_landing_place_id":
        "1st place of slave landing",
    "var_first_place_slave_purchase_id":
        "1st place of slave purchase",
    "var_guns_mounted":
        "Guns mounted",
    "var_imp_arrival_at_port_of_dis":
        "Year of arrival at port of disembarkation",
    "var_imp_length_home_to_disembark":
        "Voyage length, homeport to disembarkation",
    "var_imp_port_voyage_begin_id":
        "Place where voyage began",
    "var_imp_principal_place_of_slave_purchase_id":
        "Principal place of slave purchase",
    "var_imp_principal_port_slave_dis_id":
        "Principal place of slave landing",
    "var_imp_total_num_slaves_purchased":
        "Total embarked",
    "var_imp_total_slaves_disembarked":
        "Total disembarked",
    "var_imputed_death_middle_passage":
        "Slaves died during middle passage",
    "var_imputed_mortality":
        "Mortality rate",
    "var_imputed_nationality":
        "Flag (imputed)",
    "var_imputed_percentage_boys":
        "Percent boys",
    "var_imputed_percentage_child":
        "Percent children",
    "var_imputed_percentage_girls":
        "Percent girls",
    "var_imputed_percentage_male":
        "Percent males",
    "var_imputed_percentage_men":
        "Percent men",
    "var_imputed_percentage_women":
        "Percent women",
    "var_imputed_sterling_cash":
        "Sterling cash price in Jamaica",
    "var_length_middle_passage_days":
        "Middle passage",
    "var_nationality":
        "Flag",
    "var_num_slaves_carried_first_port":
        "Slaves carried from 1st port",
    "var_num_slaves_carried_second_port":
        "Slaves carried from 2nd port",
    "var_num_slaves_carried_third_port":
        "Slaves carried from 3rd port",
    "var_num_slaves_disembark_first_place":
        "Slaves landed at 1st port",
    "var_num_slaves_disembark_second_place":
        "Slaves landed at 2nd port",
    "var_num_slaves_disembark_third_place":
        "Slaves landed at 3rd port",
    "var_num_slaves_intended_first_port":
        "Slaves intended at 1st place",
    "var_outcome_owner":
        "Outcome of voyage for owner",
    "var_outcome_ship_captured":
        "Outcome of voyage if ship captured",
    "var_outcome_slaves":
        "Outcome of voyage for slaves",
    "var_outcome_voyage":
        "Particular outcome of voyage",
    "var_owner":
        "Vessel owner",
    "var_place_voyage_ended_id":
        "Place where voyage ended",
    "var_port_of_call_before_atl_crossing_id":
        "Places of call before Atlantic crossing",
    "var_registered_place_idnum":
        "Place registered",
    "var_registered_year":
        "Year registered",
    "var_resistance":
        "African resistance",
    "var_rig_of_vessel":
        "Rig of vessel",
    "var_search_settings":
        "Show advanced variables in search filters",
    "var_second_landing_place_id":
        "2nd place of slave landing",
    "var_second_place_slave_purchase_id":
        "2nd place of slave purchase",
    "var_ship_name":
        "Vessel name",
    "var_slave_purchase_began":
        "Date trade began in Africa",
    "var_sources_plaintext":
        "Source of data",
    "var_third_landing_place_id":
        "3rd place of slave landing",
    "var_third_place_slave_purchase_id":
        "3rd place of slave purchase",
    "var_tonnage":
        "Tonnage",
    "var_tonnage_mod":
        "Standardized tonnage",
    "var_total_num_slaves_arr_first_port_embark":
        "Slaves arrived at 1st port",
    "var_total_num_slaves_purchased":
        "Total embarked",
    "var_vessel_construction_place_idnum":
        "Place constructed",
    "var_voyage_began":
        "Date that voyage began",
    "var_voyage_completed":
        "Date voyage completed",
    "var_voyage_id":
        "Voyage ID",
    "var_year_of_construction":
        "Year constructed",
}


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
        except Exception:
            f = None
        result = f.verbose_name if f else ''
        if split > 0 and f:
            result += ' ' + \
                follow_field(f.remote_field.model, name_to_follow[split + 2:])
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
                model = index.related_model if hasattr(
                    index, 'related_model') else Voyage
                header = smart(follow_field(model, index.model_attr))
            download_header_map[var_name] = header
    return header if (header and header != '') else smart_var_name()


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
        columns = [
            col for col in list(results[0].get_stored_fields().keys())
            if 'lang' not in col or lang_version in col
        ]
        # Remove columns which have a name matching a prefix of another column.
        copy = list(columns)
        columns = [
            col for col in copy
            if len([x for x in copy if len(x) > len(col) and col in x]) == 0
        ]
    else:
        columns = [
            col if 'lang' not in col or 'lang_' in col else col + '_' + lang
            for col in columns
        ]
    if excel_mode:
        return download_xls(
            [[(_(get_download_header(col)), 1) for col in columns]],
            [[item[col] for col in columns]
             for item in [x.get_stored_fields() for x in results]])
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    writer = unicodecsv.DictWriter(response, fieldnames=columns)
    # writer.writeheader()
    writer.writerow({col: _(get_download_header(col)) for col in columns})
    for x in results:
        item = x.get_stored_fields()
        writer.writerow({col: item[col] for col in columns})
    return response


_options_model = {
    'var_outcome_voyage':
        ParticularOutcome.objects,
    'var_outcome_slaves':
        SlavesOutcome.objects,
    'var_outcome_ship_captured':
        VesselCapturedOutcome.objects,
    'var_outcome_owner':
        OwnerOutcome.objects,
    'var_resistance':
        Resistance.objects,
    'var_nationality':
        Nationality.objects,
    'var_rig_of_vessel':
        RigOfVessel.objects,
    'var_tonnage':
        TonType.objects,
    # Imputed nationality is currently restricted to a subset of code-values.
    'var_imputed_nationality':
        Nationality.objects.filter(value__in=[3, 6, 7, 8, 9, 10, 15, 30]),
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
        return HttpResponseBadRequest(
            f'Caller passed: "{var_name}". '
            f'Must specify some var_name in ' + list(_options_model.keys()))
    # Check if we have the results cached to avoid a db hit.
    cache_key = '_options_' + var_name
    response_data = cache.get(cache_key)
    is_cached = response_data is not None
    if not is_cached:
        response_data = [{
            'label': x.label,
            'value': x.value,
            'pk': x.pk
        } for x in options_model.all()]
        # Cache the data for 24h.
        cache.set(cache_key, response_data, 24 * 60 * 60)
    for d in response_data:
        d['label'] = _(d['label'])
    return JsonResponse({
        'var_name': var_name,
        'is_cached': is_cached,
        'data': response_data
    })


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
            pks = list(
                VoyageItinerary.objects.values_list(var_name,
                                                    flat=True).distinct())
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
    except Exception:
        pass
    try:
        # Process data table sorting.
        table_params = data['tableParams']
        order_info = table_params['order'][0]
        order_by = table_params['columns'][int(order_info['column'])]['data']
        if order_info['dir'] == 'desc':
            order_by = '-' + order_by
        results = results.order_by(order_by)
    except Exception:
        pass
    output_fields = ['group_name', 'short_ref', 'full_ref']
    return get_results_table(results,
                             data,
                             field_filter=lambda f: f in output_fields)


@csrf_exempt
@require_POST
def save_query(request):
    saved_query = SavedQuery()
    saved_query.query = request.body
    saved_query.is_legacy = False
    saved_query.save()
    return JsonResponse({'saved_query_id': saved_query.pk})


def get_saved_query(_, query_id):
    q = SavedQuery.objects.get(pk=query_id)
    return HttpResponse(q.query, content_type='application/json')
