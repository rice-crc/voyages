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

    first_year = None
    last_year = None

    # Try to retrieve years

    export_regions = {}
    a = SearchQuerySet().models(ExportArea)
    for i in a:
        b = SearchQuerySet().models(ExportRegion).filter(export_area__exact=i.name)
        export_regions[i] = [[a.name, a.pk] for a in b]

    import_regions = {}
    a = SearchQuerySet().models(ImportArea)
    for i in a:
        b = SearchQuerySet().models(ImportRegion).filter(import_area__exact=i.name)
        import_regions[i] = [[a.name, a.pk] for a in b]

    if request.method == "POST":
        form = EstimateSelectionForm(request.POST)
        year_form = EstimateYearForm(request.POST)
    else:
        form = EstimateSelectionForm()
        year_form = EstimateYearForm(initial={'frame_from_year': globals.first_year,
                                              'frame_to_year': globals.last_year})

    results = SearchQuerySet().models(Estimate)
    column_query_set = globals.table_columns[0][2]
    column_variable_name = globals.table_columns[0][1]
    column_sums = []

    print "column_query_set = " + str(column_query_set)

    row_query_set = globals.table_rows[2][2]
    row_variable_name = globals.table_rows[2][1]
    rows_sums = []

    print "row_query_set = " + str(row_query_set)

    columns_before_titles = 1
    row_list = []

    # Perform query
    # Iterate through columns and collect sums. Omit if necessary (omit checked).
    for col_query_item in column_query_set[-1]:
        print "query dict = " + column_variable_name + "__exact"
        print "query value = " + str(col_query_item[0])
        query_dict = {column_variable_name + "__exact": col_query_item[0]}
        a = results.filter(**query_dict)
        print "a = " + str(a)
        sum_values = sum([int(b.embarked_slaves) for b in a])
        column_sums.append(sum_values)

    if row_variable_name == "disembarkation_region":
        area_ranges = create_area_ranges(row_query_set[0])
        columns_before_titles = 2

    # Iterate through rows
    row_total = 0
    row_counter = 1
    for row_query_item in row_query_set[-1]:
        if row_query_item[1] != 1:
            print "CONTINUE"
            continue
        row_query_dict = {row_variable_name + "__exact": row_query_item[0] }

        row_list_item = []

        a = results.filter(**row_query_dict)
        print "for row = " + str(row_query_item[0])

        row_values_list = []
        if row_variable_name == "disembarkation_region" and row_counter in area_ranges:
            index = area_ranges.index(row_counter)
            row_list_item.append([row_query_set[0][index], row_query_item, ])
        else:
            row_list_item.append([row_query_item, ])

        row_counter += 1
        for col_query_item in column_query_set[-1]:
            if col_query_item[0] == "Totals":
                continue
            column_query_dict = {column_variable_name + "__exact": col_query_item[0]}
            b = a.filter(**column_query_dict)
            row_values_list.append(sum([int(c.embarked_slaves) for c in b]))
            #print "sum for " + str(col_query_item[0]) + " = " + str(sum([int(c.embarked_slaves) for c in b]))

        row_list_item.append(row_values_list)
        row_sum = sum(row_values_list)
        row_list_item.append(row_sum)
        row_total += row_sum
        row_list.append(row_list_item)

    print "at the end, column query set = " + str(column_query_set)
    column_sums.append(row_total)
    print "row_list = " + str(row_list)
    print "sum = " + str(column_sums)

    return render(request, 'assessment/estimates.html',
        {'first_year': first_year,
         'last_year': last_year,
         'year_form': year_form,
         'export_regions': collections.OrderedDict(sorted(export_regions.items(), key=lambda x: x[0].name)),
         'import_regions': collections.OrderedDict(sorted(import_regions.items(), key=lambda x: x[0].name)),
         'col_labels': column_query_set,
         'row_list': row_list,
         'col_sums': column_sums,
         'columns_before_titles': columns_before_titles,
         'table_form': form})


def create_area_ranges(areas):
    values = []
    values.append(areas[0][1])
    for i, area in enumerate(areas):
        if i > 0:
            values.append(sum([k[1] for k in areas[0:i]]) + 1)

    print "values = " + str(values)
    return values