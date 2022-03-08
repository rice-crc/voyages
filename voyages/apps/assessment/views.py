from __future__ import division, unicode_literals

import collections
import logging
import time
# Create your views here.
from builtins import range, str
from itertools import chain, groupby

from django.http import Http404
from django.shortcuts import render
from django.template import TemplateDoesNotExist, loader
from past.utils import old_div
from haystack.query import SearchQuerySet

from voyages.apps.common.export import download_xls
from voyages.apps.common.models import (SavedQuery,
                                        get_pks_from_haystack_results,
                                        restore_link)

from .forms import EstimateSelectionForm, EstimateYearForm
from .globals import default_first_year, default_last_year, get_map_year
from .models import Estimate, EstimateManager


def get_page(request, chapternum, sectionnum, pagenum):
    """
    Essay subsection of the Assessment secton

    Display an html page corresponding to the chapter-section-page

    The remaining content is rendered using the pagepath parameter
    """
    # We might want to do some error checking for pagenum here. Even though 404
    # will be raised if needed
    pagepath = "assessment/c" + chapternum + \
        "_s" + sectionnum + "_p" + pagenum + ".html"
    templatename = "assessment/c" + chapternum + \
        "_s" + sectionnum + "_generic" + ".html"
    try:
        loader.get_template(pagepath)
        loader.get_template(templatename)
        return render(request, templatename, {"pagepath": pagepath})
    except TemplateDoesNotExist:
        raise Http404


def get_estimates(request):
    tab = None
    if request.method == "POST":
        tab = request.POST.get("selected_tab")
    if request.method == "GET":
        tab = request.GET.get("selected_tab")
    if tab == "map":
        return get_estimates_map(request)
    if tab == "timeline":
        return get_estimates_timeline(request)
    return get_estimates_table(request)


def get_estimates_map(request):
    """
    Generates a Map page containing the routes and traffic flow.
    :param request: The web request that specifies search criteria.
    :return: The web page.
    """
    data = {'tab_selected': 'map'}
    results = get_estimates_common(request, data)
    data['map_year'] = get_map_year(data['query']["year__gte"],
                                    data['query']["year__lte"])
    # Group estimates by embarkation and disembarkation geocodes.
    regions = {}
    flows = {}
    cache = EstimateManager.cache()
    for pk in get_pks_from_haystack_results(results):
        result = cache[int(pk)]
        dregion = result.disembarkation_region.name
        eregion = result.embarkation_region.name
        regions[dregion] = (result.disembarkation_region.latitude,
                            result.disembarkation_region.longitude,
                            result.disembarkation_region.import_area)
        regions[eregion] = (result.embarkation_region.latitude,
                            result.embarkation_region.longitude,
                            result.embarkation_region.export_area)
        key = eregion + "_" + dregion
        item = flows.get(key, (eregion, dregion, 0, 0))
        flows[key] = (eregion, dregion, item[2] + result.embarked_slaves,
                      item[3] + result.disembarked_slaves)
    data['regions'] = regions
    data['flows'] = flows
    return render(request, 'assessment/estimates.html', data)


def get_estimates_timeline(request):
    """
    Generates a Time-line page with total traffic volume per year.
    :param request: The web request that specifies search criteria.
    :return: The web page or an XLS spreadsheet with timeline data.
    """
    data = {'tab_selected': 'timeline'}
    results = get_estimates_common(request, data)
    data['show_events'] = all([
        data[x]
        for x in ['all_nations_selected',
                  'all_embarkations_selected',
                  'all_disembarkations_selected']])
    # Group estimates by year and sum embarked and disembarked for year.
    # The following dict has keys corresponding to years and entries
    # formed by tuples (embarked_count, disembarked_count)
    timeline = {}
    cache = EstimateManager.cache()
    for pk in get_pks_from_haystack_results(results):
        result = cache[pk]
        item = (0, 0)
        if result.year in timeline:
            item = timeline[result.year]
        timeline[result.year] = (item[0] + result.embarked_slaves,
                                 item[1] + result.disembarked_slaves)

    query = data['query']
    data['min_year'] = max(query['year__gte'], default_first_year)
    data['max_year'] = min(query['year__lte'], default_last_year)
    data['timeline'] = timeline
    data['min_year'] -= 1
    data['max_year'] += 1

    post = data['post']
    if post is None or "download" not in post:
        return render(request, 'assessment/estimates.html', data)
    rows = [[k, int(round(t[0])), int(round(t[1]))]
            for k, t in timeline.items()]
    rows = sorted(rows, key=lambda a: a[0])
    return download_xls([[('Year', 1), ('Embarked Slaves', 1),
                          ('Disembarked Slaves', 1)]], rows)


def get_estimates_table(request):
    """
    Generate tabular data summarizing the estimates.
    :param request: The web request containing search data and tabular layout
    :return: The rendered page or an XLS spreadsheet containing table data.
    """
    data = {'tab_selected': 'table'}
    results = get_estimates_common(request, data)

    def year_mod(year, mod):
        """
        Helper function that groups years according to a given modulus.
        For instance, year_mod(1501, 5) = year_mod(1502, 5) = ... =
        year_mod(1505, 5).
        :param year: The year.
        :param mod: The length of each year interval.
        :return: A pair (mod, index of year interval).
        """
        year -= 1
        return mod, old_div((year - (year % mod)), mod)

    # key_functions dictionary specifies grouping functions.
    key_functions = {
        '0': lambda e: e.nation,
        '1': lambda e: e.embarkation_region,
        '2': lambda e: e.disembarkation_region.import_area,
        '3': lambda e: e.disembarkation_region,
        '4': lambda e: e.year,
        '5': lambda e: year_mod(e.year, 5),
        '6': lambda e: year_mod(e.year, 10),
        '7': lambda e: year_mod(e.year, 25),
        '8': lambda e: year_mod(e.year, 50),
        '9': lambda e: year_mod(e.year, 100),
    }

    # Fetch EstimateSelectionForm either from Post (if any), from Session (if
    # any) or a default form.
    post = data['post']
    estimate_selection_form = None
    if post is not None:
        estimate_selection_form = EstimateSelectionForm(post)
    if ((estimate_selection_form is None or
         not estimate_selection_form.is_valid()) and
            "estimate_selection_form" in request.session):
        estimate_selection_form = EstimateSelectionForm(
            request.session["estimate_selection_form"])
    if post is not None and post.get("table_options") == "Reset to default":
        estimate_selection_form = None
    if estimate_selection_form is not None and \
            estimate_selection_form.is_valid():
        cell_key_index = estimate_selection_form.cleaned_data["cells"]
        col_key_index = estimate_selection_form.cleaned_data["columns"]
        row_key_index = estimate_selection_form.cleaned_data["rows"]
        include_empty = estimate_selection_form.cleaned_data["include_empty"]
    else:
        # Select key functions based on post data or use default values if this
        # is the initial GET request.
        row_key_index = '7'
        col_key_index = '0'
        cell_key_index = '1'
        include_empty = False
        estimate_selection_form = EstimateSelectionForm(
            initial={
                'rows': row_key_index,
                'columns': col_key_index,
                'cells': cell_key_index
            })
    row_key_function = key_functions[row_key_index]
    col_key_function = key_functions[col_key_index]
    data['table_form'] = estimate_selection_form
    # Save form to session so that if the user navigates elsewhere and then
    # returns, the form is unchanged.
    if estimate_selection_form.is_valid():
        request.session[
            "estimate_selection_form"] = estimate_selection_form.cleaned_data

    # Aggregate results according to the row and column keys. Each result is a
    # pair (tuple) containing total embarked and total disembarked.
    table_dict = {}
    cache = EstimateManager.cache()
    if include_empty:
        # Force loading entire rows or columns which have zero value. This is
        # done by projecting the entire set of data on each key function and
        # forming the Cartesian product of the two.
        query = data['query']

        def year_filter(e):
            return query['year__gte'] <= e.year <= query['year__lte']

        filter_functions = {
            '0':
                lambda e: e.nation.name in query['nation__in'],
            '1':
                lambda e: e.embarkation_region.name in query[
                    'embarkation_region__in'],
            '2':
                lambda e: e.disembarkation_region.name in query[
                    'disembarkation_region__in'],
            '3':
                lambda e: e.disembarkation_region.name in query[
                    'disembarkation_region__in'],
            '4':
                year_filter,
            '5':
                year_filter,
            '6':
                year_filter,
            '7':
                year_filter,
            '8':
                year_filter,
            '9':
                year_filter,
        }
        row_filter = filter_functions[row_key_index]
        col_filter = filter_functions[col_key_index]
        estimates = list(cache.values())
        all_row_keys = {
            row_key_function(e) for e in estimates if row_filter(e)}
        all_col_keys = {
            col_key_function(e) for e in estimates if col_filter(e)}
        table_dict = {(rk, ck): (0, 0) for rk in all_row_keys
                      for ck in all_col_keys}

    for pk in get_pks_from_haystack_results(results):
        result = cache.get(pk)
        if result is not None:
            key = (row_key_function(result), col_key_function(result))
            cell = (0, 0)
            if key in table_dict:
                cell = table_dict[key]
            cell = (cell[0] + result.embarked_slaves,
                    cell[1] + result.disembarked_slaves)
            table_dict[key] = cell

    def header_with_name(x):
        return x.name

    def header_year_range(x):
        return str(x[0] * x[1] + 1) + '-' + str(x[0] * (1 + x[1]))

    # header_functions specifies how the row/column headers are generated.
    header_functions = {
        '0': header_with_name,
        '1': header_with_name,
        '2': header_with_name,
        '3': header_with_name,
        '4': lambda x: x,
        '5': header_year_range,
        '6': header_year_range,
        '7': header_year_range,
        '8': header_year_range,
        '9': header_year_range
    }

    row_header_function = header_functions[row_key_index]
    col_header_function = header_functions[col_key_index]

    # Order columns and rows by their respective headers.
    def default_sort_fun(x):
        return x.order_num

    row_sort_fun = default_sort_fun if int(
        row_key_index) < 4 else row_header_function
    row_set = sorted({k[0] for k in list(table_dict.keys())},
                     key=row_sort_fun)
    column_set = sorted({k[1] for k in list(table_dict.keys())},
                        key=default_sort_fun)

    # How many cells a single piece of data spans
    # (1 for either embarked or disembarked only and 2 for both).
    cell_span = 2 if cell_key_index == '0' else 1

    def specific_region_grouping(original_set, header_list, span_multiplier=1):
        """
        Helper function that allows grouping column or row headers when the
        headers are composed of Area and Region.
        :param original_set - the original set of columns or rows.
        :param header_list - the list of (row or column) headers that will be
        appended by area headers.
        :param span_multiplier - a multiplicity factor for the columnspan or
        rowspan of each cell.
        :return: original_set sorted according to area.
        """

        def key_map(region):
            return region.import_area.name

        modified_set = sorted(original_set,
                              key=lambda region: region.import_area.order_num)
        header_list.append([(k, span_multiplier * sum(1
                                                      for x in g))
                            for k, g in groupby(modified_set, key_map)])
        return modified_set

    # Header rows are encoded as an array of pairs (tuples), where each
    # pair consists of the header's label and column span.
    header_rows = []
    if col_key_index == '3':
        column_set = specific_region_grouping(column_set, header_rows,
                                              cell_span)
        header_rows[0].append(('', cell_span))
    header_rows.append([(col_header_function(x), cell_span) for x in column_set
                        ])
    header_rows[-1].append(('Totals', cell_span))

    # Generate row headers (left-most columns).
    row_headers = []
    if row_key_index == '3':
        row_set = specific_region_grouping(row_set, row_headers)
        row_headers[0].append(('', 1))
    row_headers.append([(row_header_function(r), 1)
                        for r in row_set] + [('Totals', 1)])

    cell_display_list = []
    if cell_key_index == '0':
        # Use list comprehensions to repeat the pair of cells
        # Embarked, Disembarked for each column in column_set.
        helper = ['Embarked', 'Disembarked']
        header_rows.append([
            (s, 1) for i in range(1 + len(column_set)) for s in helper
        ])
        cell_display_list = [0, 1]
    elif cell_key_index == '1':
        cell_display_list = [0]
    elif cell_key_index == '2':
        cell_display_list = [1]

    data['header_rows'] = header_rows
    data['header_rows_len'] = len(header_rows)
    data['totals_header_rows_len'] = len(header_rows) - \
        (1 if cell_key_index == '0' else 0)
    data['totals_header_cols_span'] = len(cell_display_list)

    # Generate tabular data from table_dict filling any missing entries with
    # (0, 0). At this point each entry of the table is a pair (embarked_count,
    # disembarked_count).
    full_data_set = [[
        table_dict[(r, c)] if (r, c) in table_dict else (0, 0)
        for c in column_set
    ] for r in row_set]
    # Round numbers to integers.
    full_data_set = [[
        tuple(int(round(pair[i])) for i in range(2)) for pair in r
    ] for r in full_data_set]
    # Append row totals (last column).
    full_data_set = [
        r + [tuple(sum([x[i]
                        for x in r])
                   for i in range(2))]
        for r in full_data_set
    ]
    # Append column totals (last row).
    full_data_set.append([
        tuple(
            sum([full_data_set[i][j][k]
                 for i in range(len(row_set))])
            for k in range(2))
        for j in range(1 + len(column_set))
    ])
    # Transform pairs(embarked_count, disembarked_count) by projecting their
    # values into single integers using the cell_display_list to determine
    # which numbers (embarked, disembarked, or both) should appear in the final
    # table.
    full_data_set = [[pair[i]
                      for pair in r
                      for i in cell_display_list]
                     for r in full_data_set]

    data['rows'] = full_data_set

    if post is None or "download" not in post:
        # Alter row_headers so that it is simpler to use in the template.
        tmp = [[None for x in row_headers] for r in full_data_set]
        col_number = 0
        for row_header_col in row_headers:
            row_number = 0
            for cell in row_header_col:
                tmp[row_number][col_number] = cell
                row_number += cell[1]
            col_number += 1
        data['row_headers'] = tmp
        data['row_headers_count'] = len(row_headers)
        return render(request, 'assessment/estimates.html', data)
    return download_xls(header_rows, full_data_set, row_headers)


def get_permanent_link(request):
    """
    Obtain a permanent link for the current search query.
    :param request: The request containing the search query.
    :return: A permanent URL link for that exact query.
    """
    saved_query = SavedQuery()
    return saved_query.get_link(request, 'restore_e_permalink')


def restore_permalink(request, link_id):
    """
    Fetch the query corresponding to the link id and redirect to the
    search results of that query.
    :param request: web request
    :param link_id: the id of the permanent link
    :return: a Redirect to the Estimates page after setting the session POST
    data to match the permalink or an Http404 error if the link is not found.
    """
    return restore_link(link_id, request.session, 'estimates_post_data',
                        'assessment:estimates')


def get_estimates_common(request, data):
    """ Append common page content to the argument data
    :param request:  web request
    :param data: A dict that contains page render data.
    :return: the results of the search query
    """
    post = None
    if request.method == "POST":
        post = request.POST

    # Ensure timeout for session manually.
    # We could have used set_expiry but then we do not get sessions
    # to automatically expire when browser closes.
    last_access = request.session.get('estimates_last_access_time', 0.0)
    current_time = time.time()
    if last_access < (current_time - (20 * 60.0)):
        request.session.pop("estimates_post_data", None)
    request.session['estimates_last_access_time'] = current_time

    # Get post from session if this is not a POST request.
    if post is None:
        # If the user had made queries before during this session, recover the
        # state here.
        post = request.session.get("estimates_post_data")
    else:
        # Store the POST data for possible use later in this session.
        request.session["estimates_post_data"] = post

    query = {}

    def is_checked(prefix, element, reset):
        """
        Helper function that checks post data (if any) to see if
        the checkbox corresponding to the given element is checked.
        :param prefix: the prefix used by the view to identify the
        model of the element.
        :param element: the model object whose check state is needed.
        :param reset: the POST parameter name that may flag a full reset of the
        checkboxes. If this parameter is set to a "Reset to default" value,
        then the result of this function will be 1.
        :return: 1 if the checkbox is checked, 0 otherwise
        """
        if post is not None and prefix + str(element.pk) not in post and \
                post.get(reset) != "Reset to default":
            return 0
        return 1

    EstimateManager.cache()
    # Check which Flags (nations) are selected and include the selection in the
    # query.
    nations = [[
        x.name, x.pk,
        is_checked("checkbox_nation_", x, "submit_nation")
    ] for x in list(EstimateManager.nations.values())]
    data['nations'] = nations
    query["nation__in"] = [nation[0] for nation in nations if nation[2] == 1]
    data['all_nations_selected'] = len(nations) == len(query["nation__in"])

    export_regions = {}
    for area, regions in EstimateManager.export_hierarchy.items():
        children = [[[x.name, x.pk],
                     is_checked("eregion-button-", x, "submit_regions")]
                    for x in regions]
        checked = is_checked("earea-button-", area, "submit_regions")
        if len(regions) == 1:
            children[0][1] = checked
        export_regions[(area, checked)] = children

    import_regions = {}
    for area, regions in EstimateManager.import_hierarchy.items():
        children = [[[x.name, x.pk],
                     is_checked("dregion-button-", x, "submit_regions")]
                    for x in regions]
        checked = is_checked("darea-button-", area, "submit_regions")
        if len(regions) == 1:
            children[0][1] = checked
        import_regions[(area, checked)] = children

    data['export_regions'] = collections.OrderedDict(
        sorted(list(export_regions.items()), key=lambda x: x[0][0].name))
    data['import_regions'] = collections.OrderedDict(
        sorted(list(import_regions.items()), key=lambda x: x[0][0].name))

    def query_region(query_key, regions_dict, all_selected_key):
        """
        Obtain a list of the names of selected regions in the regions_dict
        :param query_key: The key used when inserting this list on the query
        dict
        :param regions_dict: A dictionary with keys given by Area and whose
        values are lists of the regions in that area in the format
        [[name, pk], checked]
        :param all_selected_key: The key to set a boolean value which indicates
        whether all regions are selected.
        :return:
        """
        # Flatten the regions so that we may generate the corresponding query
        # term.
        flat = list(chain.from_iterable(list(regions_dict.values())))
        query[query_key] = [region[0][0] for region in flat if region[1] == 1]
        data[all_selected_key] = len(flat) == len(query[query_key])

    query_region("embarkation_region__in", export_regions,
                 "all_embarkations_selected")
    query_region("disembarkation_region__in", import_regions,
                 "all_disembarkations_selected")

    year_form = None
    # Ensure that GET requests or Reset POST requests yield a fresh copy of the
    # form with default values.
    if post is not None and not post.get("submit_year") == "Reset to default":
        year_form = EstimateYearForm(post)

    if year_form is not None and year_form.is_valid():
        query["year__gte"] = year_form.cleaned_data["frame_from_year"]
        query["year__lte"] = year_form.cleaned_data["frame_to_year"]
    else:
        if year_form is not None:
            logging.getLogger('voyages').error(year_form.errors)
        year_form = EstimateYearForm(
            initial={
                'frame_from_year': default_first_year,
                'frame_to_year': default_last_year
            })
        query["year__gte"] = default_first_year
        query["year__lte"] = default_last_year

    data['year_form'] = year_form
    data['query'] = query
    data['post'] = post

    return SearchQuerySet().models(Estimate).filter(**query).load_all()
