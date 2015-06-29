# Create your views here.
from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.shortcuts import render
from haystack.query import SearchQuerySet
from .models import *
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
    data = {'tab_selected': 'timeline'}
    results = get_estimates_common(request, data)
    # Group estimates by year and sum embarked and disembarked for year.
    # The following dict has keys corresponding to years and entries
    # formed by tuples (embarked_count, disembarked_count)
    timeline = {}
    for result in results:
        item = (0, 0)
        if result.year in timeline:
            item = timeline[result.year]
        timeline[result.year] = (item[0] + result.embarked_slaves, item[1] + result.disembarked_slaves)
    data['timeline'] = timeline
    return render(request, 'assessment/estimates.html', data)

def get_estimates_common(request, data):
    """ Append common page content to the argument data
    :param request:  web request
    :param data: A dict that contains page render data.
    :return: the results of the search query
    """
    post = None
    if request.method == "POST":
        post = request.POST

    query = {}

    def is_checked(prefix, element):
        """
        Helper function that checks post data (if any) to see if
        the checkbox corresponding to the given element is checked.
        :param prefix: the prefix used by the view to identify the
        model of the element.
        :param element: the model object whose check state is needed.
        :return: 1 if the checkbox is checked, 0 otherwise
        """
        if post is not None and prefix + str(element.pk) not in post:
            return 0
        else:
            return 1

    data['nations'] = [[x.name, x.pk, is_checked("checkbox_nation_", x)] for x in Nation.objects.all()]

    export_regions = {}
    areas = ExportArea.objects.all()
    for area in areas:
        regions = ExportRegion.objects.filter(export_area__pk=area.pk)
        children = [[[x.name, x.pk], is_checked("eregion-button-", x)] for x in regions]
        checked = is_checked("earea-button-", area)
        export_regions[(area, checked)] = children

    import_regions = {}
    areas = ImportArea.objects.all()
    for area in areas:
        regions = ImportRegion.objects.filter(import_area__pk=area.pk)
        children = [[[x.name, x.pk], is_checked("dregion-button-", x)] for x in regions]
        checked = is_checked("darea-button-", area)
        import_regions[(area, checked)] = children

    data['export_regions'] = collections.OrderedDict(sorted(export_regions.items(), key=lambda x: x[0][0].name))
    data['import_regions'] = collections.OrderedDict(sorted(import_regions.items(), key=lambda x: x[0][0].name))

    def query_region(query_key, regions_dict):
        """
        Obtain a list of the names of selected regions in the regions_dict
        :param query_key: The key used when inserting this list on the query
        dict
        :param regions_dict: A dictionary with keys given by Area and whose
        values are lists of the regions in that area in the format
        [[name, pk], checked]
        :return:
        """
        from itertools import chain
        # Flatten the regions so that we may generate the corresponding query term.
        flat = chain.from_iterable(regions_dict.values())
        query[query_key] = [region[0][0] for region in flat if region[1] == 1]

    query_region("embarkation_region__in", export_regions)
    query_region("disembarkation_region__in", import_regions)

    year_form = None
    if post is not None:
        year_form = EstimateYearForm(request.POST)
    if year_form is None or not year_form.is_valid():
        year_form = EstimateYearForm(initial={'frame_from_year': globals.default_first_year,
            'frame_to_year': globals.default_last_year})

    data['year_form'] = year_form

    query["year__gte"] = year_form.cleaned_data["frame_from_year"]
    query["year__lte"] = year_form.cleaned_data["frame_to_year"]
    data['query'] = query

    return SearchQuerySet().models(Estimate).filter(**query).load_all()

def get_estimates_table(request):
    first_year = None
    last_year = None
    years_rows = False
    extra_range = None
    nations = None
    query = {}
    search_configuration = {"year": {}}

    # Try to retrieve years
    if "estimate_year_from" in request.session:
        search_configuration["year"]["year_from"] = request.session["estimate_year_from"]
    if "estimate_year_to" in request.session:
        search_configuration["year"]["year_to"] = request.session["estimate_year_to"]

    if "estimate_query" in request.session:
        query = request.session["query"]

    export_regions = {}
    a = SearchQuerySet().models(ExportArea)
    for i in a:
        b = SearchQuerySet().models(ExportRegion).filter(export_area__exact=i.name)
        export_regions[i] = [[x.name, x.pk] for x in b]

    import_regions = {}
    a = SearchQuerySet().models(ImportArea)
    for i in a:
        b = SearchQuerySet().models(ImportRegion).filter(import_area__exact=i.name)
        import_regions[i] = [[x.name, x.pk] for x in b]

    # Default settings for columns and rows
    column_query_set = globals.table_columns[1][2]()
    column_variable_name = globals.table_columns[1][1]
    row_query_set = globals.table_rows[0][2]()
    row_variable_name = globals.table_rows[0][1]
    cell_mode = 1

    column_sums = []
    columns_before_titles = 1
    rows_before_titles = 1
    row_list = []

    if request.method == "POST":
        estimate_selection_form = EstimateSelectionForm(request.POST)
        year_form = EstimateYearForm(request.POST)

        search_configuration["post"] = request.POST

        if "submit_nation" in request.POST and request.POST["submit_nation"] == "Reset to default":
            nations, query["nation__in"] = globals.get_flag_labels(None)
        else:
            nations, query["nation__in"] = globals.get_flag_labels(search_configuration)

        if "submit_regions" in request.POST and request.POST["submit_regions"] == "Reset to default":
            export_regions, query["embarkation_region__in"] = globals.update_regions_labels(export_regions, None,
                                                                   "earea-button-", "eregion-button-")
            import_regions, query["disembarkation_region__in"] = globals.update_regions_labels(import_regions, None,
                                                       "darea-button-", "dregion-button-")
        else:
            export_regions, query["embarkation_region__in"] = globals.update_regions_labels(export_regions, search_configuration,
                                                                   "earea-button-", "eregion-button-")
            import_regions, query["disembarkation_region__in"] = globals.update_regions_labels(import_regions, search_configuration,
                                                       "darea-button-", "dregion-button-")

        if year_form.is_valid():
            query["year__gte"] = year_form.cleaned_data["frame_from_year"]
            query["year__lte"] = year_form.cleaned_data["frame_to_year"]
            search_configuration["year"]["year_from"] = year_form.cleaned_data["frame_from_year"]
            search_configuration["year"]["year_to"] = year_form.cleaned_data["frame_to_year"]

        if "submit_year" in request.POST and request.POST["submit_year"] == "Reset to default":
            print "reseting year"
            query["year__gte"] = globals.default_first_year
            query["year__lte"] = globals.default_last_year
            search_configuration["year"]["year_from"] = globals.default_first_year
            search_configuration["year"]["year_to"] = globals.default_last_year
            year_form = EstimateYearForm(initial={'frame_from_year': globals.default_first_year,
                                                  'frame_to_year': globals.default_last_year})

        # Perform a query
        print "performing query = " + str(query)
        results = SearchQuerySet().models(Estimate).filter(**query)

        # If form is valid, set passed preferences
        if estimate_selection_form.is_valid():
            column_query_set = globals.table_columns[int(estimate_selection_form.cleaned_data['columns'])][2](
                search_configuration, int(estimate_selection_form.cleaned_data['columns'])
            )
            column_variable_name = globals.table_columns[int(estimate_selection_form.cleaned_data['columns'])][1]
            row_query_set = globals.table_rows[int(estimate_selection_form.cleaned_data['rows'])][2](
                search_configuration, int(estimate_selection_form.cleaned_data['rows'])
            )
            row_variable_name = globals.table_rows[int(estimate_selection_form.cleaned_data['rows'])][1]
            cell_mode = int(estimate_selection_form.cleaned_data['cells'])

    else:
        # Prepare data
        nations = [[k.name, k.pk, 1] for k in SearchQuerySet().models(Nation)]

        export_regions, x  = globals.update_regions_labels(export_regions, None,
                                                                   "earea-button-", "eregion-button-")
        import_regions, x = globals.update_regions_labels(import_regions, None,
                                                       "darea-button-", "dregion-button-")

        results = SearchQuerySet().models(Estimate)
        estimate_selection_form = EstimateSelectionForm()
        year_form = EstimateYearForm(initial={'frame_from_year': globals.default_first_year,
                                              'frame_to_year': globals.default_last_year})

    if cell_mode == 0:
        extra_range = range(len(column_query_set[-1])*2)
        rows_before_titles += 1

    # Iterate through columns and collect sums. TODO: Omit if necessary (omit checked).
    # There is -1, since always last item is the item with most granular choices
    # col_query_item is in form of: ('City name', 1), where 1 is number of child (span)
    for col_query_item in column_query_set[-1]:
        query_dict = {column_variable_name: col_query_item[0]}
        column_results = results.filter(**query_dict)
        if cell_mode == 0:
            sum_values_embarked = sum([int(item.embarked_slaves) for item in column_results])
            sum_values_disembarked = sum([int(item.disembarked_slaves) for item in column_results])
            column_sums.append(sum_values_embarked)
            column_sums.append(sum_values_disembarked)
        elif cell_mode == 1:
            sum_values = sum([int(item.embarked_slaves) for item in column_results])
            column_sums.append(sum_values)
        else:
            sum_values = sum([int(item.disembarked_slaves) for item in column_results])
            column_sums.append(sum_values)


    # If row is disembarkation region, it will be spanned
    if row_variable_name == "disembarkation_region__exact":
        area_ranges = create_area_ranges(row_query_set[0])
        columns_before_titles = 2

    # The same for columns
    if column_variable_name == "disembarkation_region__exact":
        rows_before_titles += 1

    # All variables with "__in" are year variables, so they are never spanned (setting for template)
    if row_variable_name.endswith("__in"):
        years_rows = True

    # Counter for counting row total value and counting row number
    if cell_mode == 0:
        row_total = [0, 0]
    else:
        row_total = 0
    row_counter = 1

    # Iterate through rows
    for row_query_item in row_query_set[-1]:
        # if row_query_item[1] != 1:
        #     print "CONTINUE"
        #     continue

        if years_rows:
            # If this is year, include entire list (form: [1501, 1502])
            row_query_dict = {row_variable_name: row_query_item}
        else:
            # Otherwise, include only name
            row_query_dict = {row_variable_name: row_query_item[0]}

        #print "row_query_dict = " + str(row_query_dict)

        row_results = results.filter(**row_query_dict)
        #print "for row = " + str(row_query_item[0])

        row_list_item = []
        row_values_list = []

        # If this is a disembarkation region and first item in area, include area
        if row_variable_name == "disembarkation_region__exact" and row_counter in area_ranges:
            index = area_ranges.index(row_counter)
            row_list_item.append([row_query_set[0][index], row_query_item, ])
        else:
            row_list_item.append([row_query_item, ])

        row_counter += 1

        # Iterate through columns
        for col_query_item in column_query_set[-1]:
            column_query_dict = {column_variable_name: col_query_item[0]}
            column_results = row_results.filter(**column_query_dict)

            if cell_mode == 0:
                row_values_list.append(sum([int(c.embarked_slaves) for c in column_results]))
                row_values_list.append(sum([int(c.disembarked_slaves) for c in column_results]))
            elif cell_mode == 1:
                row_values_list.append(sum([int(c.embarked_slaves) for c in column_results]))
            else:
                row_values_list.append(sum([int(c.disembarked_slaves) for c in column_results]))
            #print "sum for " + str(col_query_item[0]) + " = " + str(sum([int(c.embarked_slaves) for c in b]))

        row_list_item.append(row_values_list)
        if cell_mode == 0:
            row_sum_emb = sum(row_values_list[0::2])
            row_sum_dis = sum(row_values_list[1::2])
            row_sum = [row_sum_emb, row_sum_dis]
            row_total[0] += row_sum_emb
            row_total[1] += row_sum_dis
        else:
            row_sum = sum(row_values_list)
            row_total += row_sum
        row_list_item.append(row_sum)
        row_list.append(row_list_item)

    print "at the end, column query set = " + str(column_query_set)
    if cell_mode == 0:
        column_sums.extend(row_total)
    else:
        column_sums.append(row_total)
    print "row_list = " + str(row_list)
    print "sum = " + str(column_sums)

    return render(request, 'assessment/estimates.html',
        {'first_year': first_year,
         'last_year': last_year,
         'years_rows': years_rows,
         'year_form': year_form,
         'export_regions': collections.OrderedDict(sorted(export_regions.items(), key=lambda x: x[0][0].name)),
         'import_regions': collections.OrderedDict(sorted(import_regions.items(), key=lambda x: x[0][0].name)),
         'nations': nations,
         'col_labels': column_query_set,
         'row_list': row_list,
         'col_sums': column_sums,
         'columns_before_titles': columns_before_titles,
         'rows_before_titles': rows_before_titles,
         'cell_mode': cell_mode,
         'extra_range': extra_range,
         'table_form': estimate_selection_form,
         'tab_selected': 'table'})


def create_area_ranges(areas):
    values = []
    values.append(areas[0][1])
    for i, area in enumerate(areas):
        if i > 0:
            values.append(sum([k[1] for k in areas[0:i]]) + 1)

    print "values = " + str(values)
    return values
