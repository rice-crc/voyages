# Create your views here.
from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.shortcuts import render
from haystack.query import SearchQuerySet
from .forms import *
import collections

                              
def get_page(request, chapternum, sectionnum, pagenum):
    """
    Essay subsection of the Assessment secton
    
    Display an html page corresponding to the chapter-section-page

    The remaining content is rendered using the pagepath parameter
    """
    # We might want to do some error checking for pagenum here. Even though 404 will be raised if needed
    pagepath = "assessment/c" + chapternum + "_s" + sectionnum + "_p" + pagenum + ".html"
    templatename = "assessment/c" + chapternum + "_s" + sectionnum + "_generic" + ".html"
    try:
        loader.get_template(pagepath)
        loader.get_template(templatename)
        return render(request, templatename, {"pagepath" : pagepath})
    except TemplateDoesNotExist:
        raise Http404

def get_estimates(request):
    tab = None
    if request.method == "POST" and "selected_tab" in request.POST:
        tab = request.POST["selected_tab"]
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
    data['map_year'] = globals.get_map_year(data['query']["year__gte"], data['query']["year__lte"])
    # Group estimates by embarkation and disembarkation geocodes.
    regions = {}
    flows = {}
    cache = EstimateManager.cache()
    for result in results:
        result = cache[result.pk]
        dregion = result.disembarkation_region.name
        eregion = result.embarkation_region.name
        regions[dregion] = (result.disembarkation_region.latitude, result.disembarkation_region.longitude)
        regions[eregion] = (result.embarkation_region.latitude, result.embarkation_region.longitude)
        key = eregion + "_" + dregion
        item = (eregion, dregion,  0, 0)
        if key in flows:
            item = flows[key]
        flows[key] = (eregion, dregion, item[2] + result.embarked_slaves, item[3] + result.disembarked_slaves)
    data['regions'] = regions
    data['flows'] = flows
    return render(request, 'assessment/estimates.html', data)

def get_estimates_timeline(request):
    """
    Generates a Time-line page with total traffic volume per year.
    :param request: The web request that specifies search criteria.
    :return: The web page.
    """
    data = {'tab_selected': 'timeline'}
    results = get_estimates_common(request, data)
    # Group estimates by year and sum embarked and disembarked for year.
    # The following dict has keys corresponding to years and entries
    # formed by tuples (embarked_count, disembarked_count)
    timeline = {}
    cache = EstimateManager.cache()
    for result in results:
        result = cache[result.pk]
        item = (0, 0)
        if result.year in timeline:
            item = timeline[result.year]
        timeline[result.year] = (item[0] + result.embarked_slaves, item[1] + result.disembarked_slaves)
    data['timeline'] = timeline

    post = data['post']
    if post is None or "download" not in post:
        return render(request, 'assessment/estimates.html', data)
    else:
        return download_xls([[('Year', 1), ('Embarked Slaves', 1), ('Disembarked Slaves', 1)]],
                            [[k, t[0], t[1]] for k, t in timeline.iteritems()])

def get_estimates_table(request):
    """
    Generate tabular data summarizing the estimates.
    :param request: The web request containing search data and tabular layout
    :return: The rendered page.
    """
    data = {'tab_selected': 'table'}
    results = get_estimates_common(request, data)

    # Helper function that groups years according to a given modulus.
    # For instance, year_mod(1501, 5) = year_mod(1502, 5) = ... = year_mod(1505, 5).
    def year_mod(year, mod):
        year -= 1
        return mod, (year - (year % mod)) / mod

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

    # Select key functions based on post data.
    row_key_index = '7'
    col_key_index = '0'
    cell_key_index = '1'
    estimate_selection_form = None
    post = data['post']

    # Fetch EstimateSelectionForm either from Post (if any), from Session (if any) or a default form.
    if post is not None:
        estimate_selection_form = EstimateSelectionForm(post)
    if (estimate_selection_form is None or not estimate_selection_form.is_valid()) \
            and "estimate_selection_form" in request.session:
        estimate_selection_form = request.session["estimate_selection_form"]
    if estimate_selection_form is not None and estimate_selection_form.is_valid():
        cell_key_index = estimate_selection_form.cleaned_data["cells"]
        col_key_index = estimate_selection_form.cleaned_data["columns"]
        row_key_index = estimate_selection_form.cleaned_data["rows"]
    else:
        estimate_selection_form = EstimateSelectionForm(initial={
            'rows': row_key_index,
            'columns': col_key_index,
            'cells': cell_key_index})
    row_key_function = key_functions[row_key_index]
    col_key_function = key_functions[col_key_index]
    data['table_form'] = estimate_selection_form
    # Save form to session so that if the user navigates elsewhere and then returns, the form is unchanged.
    request.session["estimate_selection_form"] = estimate_selection_form

    # Aggregate results according to the row and column keys.
    # Each result is a pair (tuple) containing total embarked and total disembarked.
    table_dict = {}
    cache = EstimateManager.cache()
    for result in results:
        result = cache[result.pk]
        key = (row_key_function(result), col_key_function(result))
        cell = (0, 0)
        if key in table_dict:
            cell = table_dict[key]
        cell = (cell[0] + result.embarked_slaves, cell[1] + result.disembarked_slaves)
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
    row_set = sorted(set([k[0] for k in table_dict.keys()]), key=row_header_function)
    column_set = set([k[1] for k in table_dict.keys()])
    if col_key_index == '0':
        column_set = list(column_set)
    else:
        column_set = sorted(column_set, key=col_header_function)

    # How many cells a single piece of data spans
    # (1 for either embarked or disembarked only and 2 for both).
    cell_span = 2 if cell_key_index == '0' else 1

    # Header rows are encoded as an array of pairs (tuples), where each
    # pair consists of the header's label and column span.
    header_rows = []
    if col_key_index == '3':
        # Reorder columns by disembarkation area and then group by so that we create a new
        # header row which groups disembarkation regions by their major area.
        keyfunc = lambda region: region.import_area.name
        column_set = sorted(column_set, key=keyfunc)
        from itertools import groupby
        header_rows.append([(k, cell_span * sum(1 for x in g)) for k, g in groupby(column_set, keyfunc)])

    header_rows.append([(col_header_function(x), cell_span) for x in column_set])

    cell_display_list = []
    if cell_key_index == '0':
        # Use list comprehensions to repeat the pair of cells
        # Embarked, Disembarked for each column in column_set.
        helper = ['Embarked', 'Disembarked']
        header_rows.append([(s, 1) for i in range(1 + len(column_set)) for s in helper])
        cell_display_list = [0, 1]
    elif cell_key_index == '1':
        cell_display_list = [0]
    elif cell_key_index == '2':
        cell_display_list = [1]

    data['header_rows'] = header_rows
    data['header_rows_len'] = len(header_rows)
    data['totals_header_rows_len'] = len(header_rows) - (1 if cell_key_index == '0' else 0)
    data['totals_header_cols_span'] = len(cell_display_list)

    # Generate tabular data from table_dict filling any missing entries with (0, 0).
    # At this point each entry of the table is a pair (embarked_count, disembarked_count).
    full_data_set = [[table_dict[(r, c)] if (r, c) in table_dict else (0, 0) for c in column_set]
                     for r in row_set]
    # Round numbers to integers.
    full_data_set = [[tuple(int(round(pair[i])) for i in range(2)) for pair in r] for r in full_data_set]
    # Append row totals (last column).
    full_data_set = [r + [tuple(sum([x[i] for x in r]) for i in range(2))] for r in full_data_set]
    # Append column totals (last row).
    full_data_set.append([tuple(sum([full_data_set[i][j][k] for i in range(len(row_set))]) for k in range(2))
                         for j in range(1 + len(column_set))])
    # Transform pairs(embarked_count, disembarked_count) by projecting their values
    # into single integers using the cell_display_list to determine which numbers
    # (embarked, disembarked, or both) should appear in the final table.
    full_data_set = [[pair[i] for pair in r for i in cell_display_list]
                     for r in full_data_set]
    # Append row headers (AKA first column).
    row_headers = [row_header_function(r) for r in row_set] + ['Totals']
    full_data_set = [[row_headers[i]] + full_data_set[i] for i in range(len(full_data_set))]

    data['rows'] = full_data_set

    if post is None or "download" not in post:
        return render(request, 'assessment/estimates.html', data)
    else:
        header_rows[-1].append(("Totals", 1))
        return download_xls(header_rows, full_data_set, 1)

def download_xls(header_rows, data_set, header_col_offset=0):
    """
    Generates an XLS file with the given data.
    :param header_rows: The header rows, specified as an array of pairs (header label, column span)
    :param data_set: Tabular data in the format [[r_1c_1, r_1c_2, ..., r_1c_N], ..., [r_Mc_1, r_Mc_2, ..., r_Mc_N]]
    :return: An HttpResponse containing the XLS file.
    """
    import xlwt
    from django.http import HttpResponse
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=data.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Data")

    header_style = xlwt.XFStyle()
    number_style = xlwt.XFStyle()
    number_style.alignment.horz = number_style.alignment.HORZ_RIGHT

    # Write headers.
    row_index = 0
    for row in header_rows:
        col_index = header_col_offset
        for pair in row:
            ws.write(row_index, col_index, pair[0], header_style)
            if pair[1] > 1:
                ws.merge(row_index, row_index, col_index, col_index + pair[1] - 1)
            col_index += pair[1]
        row_index += 1

    # Write tabular data.
    for row in data_set:
        col_index = 0
        for cell in row:
            ws.write(row_index, col_index, cell, number_style if col_index > 0 else header_style)
            col_index += 1
        row_index += 1

    wb.save(response)
    return response

def get_estimates_common(request, data):
    """ Append common page content to the argument data
    :param request:  web request
    :param data: A dict that contains page render data.
    :return: the results of the search query
    """
    post = None
    if request.method == "POST":
        post = request.POST
    elif request.GET.get("act_as_post") is not None:
        post = request.GET

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
        else:
            return 1

    # Check which Flags (nations) are selected and include the selection in the query.
    nations = [[x.name, x.pk, is_checked("checkbox_nation_", x, "submit_nation")] for x in Nation.objects.all()]
    data['nations'] = nations
    query["nation__in"] = [nation[0] for nation in nations if nation[2] == 1]
    data['all_nations_selected'] = len(nations) == len(query["nation__in"])

    export_regions = {}
    areas = ExportArea.objects.all()
    for area in areas:
        regions = ExportRegion.objects.filter(export_area__pk=area.pk)
        children = [[[x.name, x.pk], is_checked("eregion-button-", x, "submit_regions")] for x in regions]
        checked = is_checked("earea-button-", area, "submit_regions")
        if len(regions) == 1:
            children[0][1] = checked
        export_regions[(area, checked)] = children

    import_regions = {}
    areas = ImportArea.objects.all()
    for area in areas:
        regions = ImportRegion.objects.filter(import_area__pk=area.pk)
        children = [[[x.name, x.pk], is_checked("dregion-button-", x, "submit_regions")] for x in regions]
        checked = is_checked("darea-button-", area, "submit_regions")
        if len(regions) == 1:
            children[0][1] = checked
        import_regions[(area, checked)] = children

    data['export_regions'] = collections.OrderedDict(sorted(export_regions.items(), key=lambda x: x[0][0].name))
    data['import_regions'] = collections.OrderedDict(sorted(import_regions.items(), key=lambda x: x[0][0].name))

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
        from itertools import chain
        # Flatten the regions so that we may generate the corresponding query term.
        flat = list(chain.from_iterable(regions_dict.values()))
        query[query_key] = [region[0][0] for region in flat if region[1] == 1]
        data[all_selected_key] = len(flat) == len(query[query_key])

    query_region("embarkation_region__in", export_regions, "all_embarkations_selected")
    query_region("disembarkation_region__in", import_regions, "all_disembarkations_selected")

    year_form = None
    # Ensure that GET requests or Reset POST requests yield a fresh copy of the form with default values.
    if post is not None and not post.get("submit_year") == "Reset to default":
        year_form = EstimateYearForm(post)

    if year_form is not None and year_form.is_valid():
        query["year__gte"] = year_form.cleaned_data["frame_from_year"]
        query["year__lte"] = year_form.cleaned_data["frame_to_year"]
    else:
        year_form = EstimateYearForm(initial={'frame_from_year': globals.default_first_year,
            'frame_to_year': globals.default_last_year})
        query["year__gte"] = globals.default_first_year
        query["year__lte"] = globals.default_last_year

    data['year_form'] = year_form
    data['query'] = query
    data['post'] = post

    return SearchQuerySet().models(Estimate).filter(**query).load_all()
