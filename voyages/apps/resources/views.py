from __future__ import absolute_import, unicode_literals

from builtins import str
from collections import OrderedDict
from itertools import groupby

from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as u_
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet

from voyages.apps.common.export import download_xls
from voyages.apps.common.models import get_values_from_haystack_results
from voyages.apps.voyage.globals import structure_places
from voyages.apps.voyage.views import prepare_paginator_variables

from .forms import ResultsPerPageOptionForm
from .globals import names_search_strict_text, names_sort_fields
from .models import (AfricanName, AfricanNamesIndex, Country, Image,
                     ImageCategory, Place)


def image_search_results(adapt_query_set=lambda cat, q: q):
    images = []

    for i in ImageCategory.objects.all().order_by("-value"):
        if i.visible_on_website is True:
            category_images = {}
            category_images["label_name"] = i.label
            category_images["label_code"] = i.value
            category_images["images"] = []
            search_set = SearchQuerySet().models(Image).filter(
                category_label__exact=i.label,
                ready_to_go=True
            ).order_by('date')
            category_images["number_of_images"] = search_set.count()
            for j in adapt_query_set(i.label, search_set):
                category_images["images"].append(
                    OrderedDict({
                        'file': j.file,
                        'year': j.date,
                        'title': j.title
                    }))

            images.append(category_images)

    images = sorted(images, key=lambda k: k["label_name"])
    return images


def get_all_images(request):
    """
    View to get demo images (4 per group).
    :param request: Request to serve
    """

    images = image_search_results(lambda _, q: q[:4])
    return render(request, 'resources/images-index.html', {'images': images})


def get_images_category(request, category):
    """
    View to show images by group.

    :param request: Request to serve
    :param category: Get images from this category
    """

    category = " ".join(category.split("_"))
    images = image_search_results(lambda cat, q: q if cat == category else [])
    return render(request, 'resources/images-category.html', {
        'images': images,
        'category': category
    })


def get_images_category_detail(request, category, page):
    """
    View to show images by group in detail.
    :param request: Request to serve
    :param category: Get images from this category
    :param page: Number of page to serve
    """

    category = " ".join(category.split("_"))
    manu = SearchQuerySet().filter(category_label__exact=category,
                                   ready_to_go=True).order_by('date')
    images = []

    # Pack all images from category with needed data.
    for i in ImageCategory.objects.all().order_by("-value"):
        if i.visible_on_website is True:
            category_images = {}
            category_images["label_name"] = i.label
            category_images["label_code"] = i.value
            category_images["images"] = []
            search_set = SearchQuerySet().models(Image).filter(
                category_label__exact=i.label,
                ready_to_go=True
            ).order_by('date')
            category_images["number_of_images"] = search_set.count()
            if i.label == category:
                # Set paginator on proper page.
                paginator = Paginator(manu, 1)
                pagins = paginator.page(page)

            images.append(category_images)

    images = sorted(images, key=lambda k: k["label_name"])

    return render(request, 'resources/image-category-detail.html', {
        'images': images,
        'pagins': pagins,
        'category': category
    })


def get_image_detail(request, category, page):
    """
    View to show images in detail.
    :param request: Request to serve
    :param category: Get images from this category
    :param page: Number of page to serve
    """

    category = " ".join(category.split("_"))
    image = SearchQuerySet().filter(
        category_label__exact=category,
        ready_to_go=True).order_by('date')[int(page) - 1]
    images = image_search_results(lambda cat, q: [])
    return render(request, 'resources/image-detail.html', {
        'image': image,
        'images': images
    })


def images_search(request):
    """
    View to make search of images.

    :param request: Request to serve
    """

    query = ''
    time_start = ''
    time_end = ''
    post = request.POST
    enable_checkboxes = False

    if request.method == 'GET' and request.GET.get('q') is not None:
        request.method = 'POST'
        enable_checkboxes = True
        post = {
            'q': request.GET['q'],
            'time_start': request.GET.get('time_start', ''),
            'time_end': request.GET.get('time_end', '')
        }

    if request.method == 'POST':

        # Check if session have to be deleted
        if post.get('clear_form'):
            request.session.flush()

        # New search, clear data stored in session
        results = None
        request.session['results_images'] = None
        form = SearchForm(post)
        restart = post.get('restart') is not None
        base_query = SearchQuerySet().models(Image).order_by('category_label')

        if form.is_valid():
            images = []
            categories_to_search = []
            query = form.cleaned_data['q'] if not restart else ''

            # Get categories to search and get left menu data
            for i in ImageCategory.objects.filter(visible_on_website=True):
                category_images = {}
                category_images["label_name"] = i.label
                category_images["label_code"] = i.value
                category_images["images"] = []
                search_set = base_query.filter(
                    category_label__exact=i.label,
                    ready_to_go=True).order_by('date')
                category_images["number_of_images"] = len(search_set)
                if restart or enable_checkboxes or post.get(
                        "checkbox" + str(i.value)):
                    categories_to_search.append(i.label)

                images.append(category_images)

            images = sorted(images, key=lambda k: k["label_name"])

            time_start = post.get('time_start') if not restart else ''
            time_end = post.get('time_end') if not restart else ''

            # Options if query is provided
            if query != "":
                if time_start != "" and time_end != "":
                    results = base_query.filter(
                        imgtext__icontains=query,
                        ready_to_go=True,
                        category_label__in=categories_to_search,
                        date__gte=time_start,
                        date__lte=time_end
                    ).order_by('date')

                elif time_start != "":
                    results = base_query.filter(
                        imgtext__icontains=query, ready_to_go=True,
                        category_label__in=categories_to_search,
                        date__gte=time_start
                    ).order_by('date')

                elif time_end != "":
                    results = base_query.filter(
                        imgtext__icontains=query, ready_to_go=True,
                        category_label__in=categories_to_search,
                        date__lte=time_end
                    ).order_by('date')

                else:
                    results = base_query.filter(
                        imgtext__icontains=query,
                        ready_to_go=True,
                        category_label__in=categories_to_search
                    ).order_by('date')

            elif time_start != "" or time_end != "":
                if time_start != "" and time_end != "":
                    results = base_query.filter(
                        ready_to_go=True,
                        category_label__in=categories_to_search,
                        date__gte=time_start,
                        date__lte=time_end
                    ).order_by('date')

                elif time_start != "":
                    results = base_query.filter(
                        ready_to_go=True,
                        category_label__in=categories_to_search,
                        date__gte=time_start
                    ).order_by('date')

                elif time_end != "":
                    results = base_query.filter(
                        ready_to_go=True,
                        category_label__in=categories_to_search,
                        date__lte=time_end
                    ).order_by('date')

                else:
                    if len(categories_to_search) == 1:
                        return HttpResponseRedirect(
                            reverse('resources:images-category',
                                    kwargs={
                                        'category': categories_to_search.pop()
                                    }))
                    results = base_query.all().filter(
                        ready_to_go=True,
                        category_label__in=categories_to_search
                    ).order_by('date')

            else:
                if len(categories_to_search) > 1:
                    results = base_query.all().filter(
                        ready_to_go=True,
                        category_label__in=categories_to_search
                    ).order_by('date')
                elif len(categories_to_search) == 1:
                    return HttpResponseRedirect(
                        reverse('resources:images-category',
                                kwargs={'category': categories_to_search.pop()
                                        }))

        if results is None:
            results = base_query.all()

        # Store results in session
        request.session['results_images'] = results
        request.session['images_images'] = images
        request.session['enabled_categories'] = categories_to_search
        request.session['query'] = query
        request.session['time_start'] = time_start
        request.session['time_end'] = time_end

    else:
        results = request.session.get('results_images')
        images = request.session.get('images_images')

    categorized = {
        cat: sorted(g, key=lambda x: u_(x.title))
        for cat, g in groupby(results, key=lambda x: x.category_label)}

    return render(
        request, 'resources/images-search-results.html', {
            'results': results,
            'images': images,
            'query': request.session['query'],
            'time_start': request.session['time_start'],
            'time_end': request.session['time_end'],
            'enabled_categories': request.session['enabled_categories'],
            'categorized': categorized
        })


def images_search_detail(request, page):
    """
    Get image search subpage divided by paginator

    :param request: Request to serve
    :param page: Number of page to serve
    """

    results = request.session['results_images']
    images = request.session['images_images']

    paginator = Paginator(results, 1)
    pagins = paginator.page(page)

    return render(
        request, 'resources/images-search-detail.html', {
            'images': images,
            'results': pagins,
            'category': "Search",
            'query': request.session['query'],
            'time_start': request.session['time_start'],
            'time_end': request.session['time_end'],
            'enabled_categories': request.session['enabled_categories']
        })


def get_image_search_detail(request, page):
    """
    Get details of one of the found images.

    :param request: Request to serve
    :param page: Number of page to serve details
    """

    image = request.session['results_images'][int(page) - 1]
    images = image_search_results(lambda cat, q: [])
    return render(request, 'resources/image-search-detail-window.html', {
        'image': image,
        'images': images
    })


AFRICAN_NAME_SOLR_FIELDS = list(AfricanNamesIndex.fields)


def download_slaves_helper(data):
    """
    Generate a spreadsheet file with slave data.
    :param data: A list of dicts each representing an African name.
    :return:
    """
    rows = [[x.get(field_name)
             for field_name in AFRICAN_NAME_SOLR_FIELDS]
            for x in data]
    return download_xls([[(f, 1) for f in AFRICAN_NAME_SOLR_FIELDS]], rows)


def get_all_slaves(request):
    """
    Retrieve and return all slaves

    :param request: Request to serve
    :return: slaves to display
    """

    results_per_page_form = None
    results_per_page = 20
    current_page = 1
    sort_string = ""

    # Try to retrieve session
    try:
        results = request.session["names_results"]
    except KeyError:
        results = {}

    try:
        current_query = request.session["names_current_query"]
    except KeyError:
        current_query = {}

    try:
        query_dict = request.session["names_query_dict"]
    except KeyError:
        query_dict = {}

    try:
        sort_column = request.session["sort_column"]
    except KeyError:
        sort_column = "slave_id"
        request.session["sort_column"] = "slave_id"

    try:
        sort_mode = request.session["sort_mode"]
    except KeyError:
        sort_mode = "1"
        request.session["sort_mode"] = "1"

    try:
        opened_tabs = request.session["names_opened_tabs"]
    except KeyError:
        opened_tabs = {
            'section_1': True,
            'section_2': False,
            'section_3': False
        }
        request.session["names_opened_tabs"] = opened_tabs

    # If there is no requested page number, serve 1
    desired_page = request.POST.get('desired_page')
    if desired_page:
        current_page = desired_page

    # Collect Origins (it's now done by sql query, in the Haystack there is no
    # easy way to get this list (facet is similar, but not what we want to
    # have)
    countries_from_names = AfricanName.objects.exclude(
        country__isnull=True).values('country__name')
    countries = Country.objects.filter(
        name__in=countries_from_names).order_by('name')

    # Collect places
    places_from_embarkation = AfricanName.objects.exclude(
        embarkation_port__isnull=True).values('embarkation_port__place')
    places_from_disembarkation = AfricanName.objects.exclude(
        disembarkation_port__isnull=True).values('disembarkation_port__place')
    places = Place.objects.all()

    used = []
    places_separated_embarkation = []
    places_separated_disembarkation = []

    # For embarkation and disembarkation collect ids of places
    for i in places_from_embarkation:
        if i['embarkation_port__place'] not in used:
            places_separated_embarkation.append(
                places.filter(
                    place=i['embarkation_port__place']).values('id')[0]['id'])
            used.append(i['embarkation_port__place'])
    used = []
    for i in places_from_disembarkation:
        if i['disembarkation_port__place'] not in used:
            places_separated_disembarkation.append(
                places.filter(place=i['disembarkation_port__place']).values(
                    'id')[0]['id'])
            used.append(i['disembarkation_port__place'])

    # Retrieve structured places
    embarkation_list = structure_places(places_separated_embarkation)
    disembarkation_list = structure_places(places_separated_disembarkation)

    if request.method == "GET":
        results_per_page_form = ResultsPerPageOptionForm()

        # If no results in session, retrieve
        if len(results) == 0:
            if sort_mode == "1":
                sort_string = sort_column
            if sort_mode == "2":
                sort_string = "-" + sort_column

            # If this is ngram, sort by string field
            if sort_column in names_sort_fields:
                sort_string += "_sort"

            results = SearchQuerySet().models(
                AfricanName).order_by(sort_string)

            request.session['names_results'] = results
            request.session['sort_column'] = sort_column
            request.session['sort_mode'] = sort_mode

    if request.method == "POST":
        results_per_page_form = ResultsPerPageOptionForm(request.POST)

        if request.POST.get("action") is not None and request.POST.get(
                "action") == "New Query":
            # Clicked "New Query", reset all session variables
            results = SearchQuerySet().models(AfricanName).order_by("slave_id")
            query_dict = {}
            current_query = {}
            request.session['names_results'] = results
            request.session['names_query_dict'] = {}
            request.session['names_current_query'] = {}
            request.session['sort_column'] = "slave_id"
            sort_column = "slave_id"
            sort_mode = "1"
            request.session['sort_mode'] = "1"
            results_per_page = 20
            request.session['slaves_per_page_choice'] = None
            request.session['slaves_per_page'] = results_per_page
            current_page = 1
            opened_tabs = {
                'section_1': True,
                'section_2': False,
                'section_3': False
            }
            request.session["names_opened_tabs"] = opened_tabs

        elif request.POST.get("sort_column") is not None:
            # One of the headers clicked, perform sort
            # If column has changed, reset the sort_mode
            if request.session["sort_column"] != request.POST.get(
                    "sort_column"):
                sort_column = request.POST.get("sort_column")
                sort_mode = "2"

            # If previously it was "2", set as "1" and vice versa
            if sort_mode == "1":
                sort_mode = "2"
                sort_string = "-" + sort_column
            else:
                sort_mode = "1"
                sort_string = sort_column

            # If this is ngram, sort by string field
            if sort_column in names_sort_fields:
                sort_string += "_sort"

            # Perform query and store results
            if len(query_dict) > 0:
                results = SearchQuerySet().filter(
                    **query_dict).models(AfricanName).order_by(sort_string)
            else:
                results = SearchQuerySet().models(AfricanName).order_by(
                    sort_string)

            request.session['names_results'] = results
            request.session["sort_column"] = sort_column
            request.session["sort_mode"] = sort_mode

        elif request.POST.get("action") == "Search":
            # Encode and store query dict/opened tabs/current query
            query_dict, opened_tabs, current_query = create_query_dict(
                request.POST, embarkation_list, disembarkation_list, countries)
            request.session['names_query_dict'] = query_dict
            request.session['names_opened_tabs'] = opened_tabs
            request.session['names_current_query'] = current_query

            # If any sorting option exist
            if sort_mode == "1":
                sort_string = sort_column
            if sort_mode == "2":
                sort_string = "-" + sort_column

            # If this is ngram, sort by string field
            if sort_column in names_sort_fields:
                sort_string += "_sort"

            # Filter only if query_dict is not empty
            if len(query_dict) > 0:
                results = SearchQuerySet().filter(
                    **query_dict).models(AfricanName).order_by(sort_string)
            else:
                results = SearchQuerySet().models(AfricanName).order_by(
                    sort_string)
            request.session['names_results'] = results
        elif request.POST.get("action") == "download_all":
            # Build download file.
            data = get_values_from_haystack_results(results,
                                                    AFRICAN_NAME_SOLR_FIELDS)
            return download_slaves_helper(data)

        # Manage results per page
        if results_per_page_form.is_valid():
            results_per_page = results_per_page_form.cleaned_option()
            request.session[
                'slaves_per_page_choice'] = results_per_page_form.cleaned_data[
                    'option']
            request.session['slaves_per_page'] = results_per_page
        elif set({'results_per_page', 'results_per_page_choice'}).issubset(
                set(request.session)):
            results_per_page = request.session['slaves_per_page']
            results_per_page_form.fields['option'].initial = request.session[
                'slaves_per_page_choice']
            results_per_page_form = ResultsPerPageOptionForm(
                {u'option': request.session['slaves_per_page_choice']})

    # Paginate results to pages
    paginator = Paginator(results, results_per_page)
    pagins = paginator.page(current_page)
    if request.method == "POST" and request.POST.get(
            "action") == "download_current_view":
        data = [x.get_stored_fields() for x in pagins.object_list]
        return download_slaves_helper(data)

    # Get ranges and number of pages
    (paginator_range,
     pages_range) = prepare_paginator_variables(paginator, current_page,
                                                results_per_page)

    return render(
        request, 'resources/names-index.html', {
            'results': pagins,
            'paginator_range': paginator_range,
            'pages_range': pages_range,
            'options_results_per_page_form': results_per_page_form,
            'sort_column': sort_column,
            'sort_mode': sort_mode,
            'origins': countries,
            'embarkation_list': embarkation_list,
            'disembarkation_list': disembarkation_list,
            'query_dict': query_dict,
            'opened_tabs': opened_tabs,
            'current_query': current_query
        })


def create_query_dict(var_list, embarkation_list, disembarkation_list,
                      countries):
    query_dict = {}
    sex_list = []
    origins = []
    embarkation = []
    embarkation_cq = []
    disembarkation = []
    opened_tabs = {}
    current_query = OrderedDict()

    # Iterate and collect all options
    # Mark sections as True/False (collapsed/expanded)
    for key, value in var_list.items():
        if key in names_search_strict_text:
            if value != "":
                query_dict[key] = value
                opened_tabs['section_1'] = True

                # Create appropriate entry in current query dict
                if key == "slave_name":
                    fill_current_query_dict(current_query, "African name",
                                            value)
                elif key == "slave_ship_name":
                    fill_current_query_dict(current_query, "Ship name", value)
                elif key == "slave_voyage_number":
                    fill_current_query_dict(current_query, "Voyage ID", value)

        elif key.startswith("sex_"):
            if value != "":
                sex_list.append(key.split("_")[1])
                opened_tabs['section_1'] = True
        elif key.startswith("origin_"):
            origins.append(int(key.split("_")[1]))
            opened_tabs['section_2'] = True
        elif key.startswith("checkbox_"):
            embarkation.append(int(key.split("_")[-1]))
            if len(key.split("_")[-1]) == 4:
                embarkation_cq.append(key.split("_")[-1])
            opened_tabs['section_3'] = True
        elif key.startswith("disembarkation_"):
            disembarkation.append(int(key.split("_")[-1]))
            opened_tabs['section_3'] = True

    # Include list-like fields if any of these have been chosen
    if len(sex_list) > 0:
        query_dict['slave_sex_age__in'] = sex_list
        sex_list_str = ""
        for i in sex_list:
            if i in ("Boy", "Girl", "Male", "Female"):
                sex_list_str += i + "s "
            elif i == "Man":
                sex_list_str += "Men "
            elif i == "Woman":
                sex_list_str += "Women "
        fill_current_query_dict(current_query, "Sex/Age", sex_list_str)

    if len(origins) > 0:
        query_dict['slave_country__in'] = origins

        # Collect names of checked origins and add to the current query
        value = ""
        if len(origins) == len(countries):
            fill_current_query_dict(current_query, "Place of origin",
                                    "all places selected")
        else:
            for j in origins:
                value += countries.filter(
                    country_id=j).values('name')[0]['name'] + ", "
            value = value.rstrip().rstrip(",")
            fill_current_query_dict(current_query, "Place of origin", value)

    if len(embarkation) > 0:
        query_dict['slave_embarkation_port__in'] = embarkation

        # Get list of checked embarkation and add to the current query
        fill_current_query_dict(
            current_query, "Place of embarkation",
            get_embarkation_checked(embarkation_list, embarkation))

    if len(disembarkation) > 0:
        query_dict['slave_disembarkation_port__in'] = disembarkation
        value = ""

        # Find names of checked disembarkation ports and add to the current
        # query
        for _, region_list in disembarkation_list.items():
            for _, ports_list in region_list.items():
                for port in ports_list:
                    if port.value in disembarkation:
                        value += port.place + ", "

        value = value.rstrip().rstrip(",")
        fill_current_query_dict(
            current_query, "Place of disembarkation", value)

    # Include 'gte' and 'lte' fields in current query
    def fill_query_dict_with(query_dict, dkey, current_query, qkey):
        from_to = None
        gte = dkey + "__gte"
        lte = dkey + "__lte"
        if gte in query_dict and lte in query_dict:
            from_to = query_dict[gte] + " - " + query_dict[lte]
        elif gte in query_dict:
            from_to = "from " + query_dict[gte]
        elif lte in query_dict:
            from_to = "up to " + query_dict[lte]
        if from_to is not None:
            fill_current_query_dict(current_query, qkey, from_to)

    fill_query_dict_with(
        query_dict, "slave_date_arrived", current_query, "Time frame")
    fill_query_dict_with(query_dict, "slave_age", current_query, "Age")
    fill_query_dict_with(
        query_dict, "slave_height", current_query, "Height (inches)")
    return query_dict, opened_tabs, sorted(current_query.items())


def get_embarkation_checked(embarkation_list, checked):
    emb_str = ""

    # Iterate through broad regions and their children (regions)
    for broad_region, region_list in embarkation_list.items():
        regions_to_add = []

        # Iterate through regions and their children (ports)
        for region, port_list in region_list.items():
            ports_to_add = []

            # Iterate through ports in region and collect ports to add to the
            # current query
            for port in port_list:
                if port.value in checked:
                    ports_to_add.append(port.place)

            # If all ports have been selected in region, the entire region is
            # marked as "all ports" Otherwise, add ports to the string
            if len(ports_to_add) == len(port_list):
                regions_to_add.append(region.region + " - all ports selected")
            else:
                if len(ports_to_add) > 0:
                    emb_str += ", ".join(ports_to_add) + ", "

        # If all regions have been selected in the broad region,
        # the entire broad region is marked as "all ports"
        # Otherwise, add remaining entire regions to the string
        if len(regions_to_add) == len(region_list):
            emb_str += broad_region.broad_region + " - all ports selected, "
        elif len(regions_to_add) > 0:
            emb_str += ", ".join(regions_to_add) + ", "

    return emb_str.rstrip().rstrip(",")


def fill_current_query_dict(dictionary=None, key=None, value=None):
    # Find a key and put the value
    name_to_idx = {
        "African name": 1,
        "Ship name": 2,
        "Voyage ID": 3,
        "Time frame": 4,
        "Age": 5,
        "Height (inches)": 6,
        "Sex/Age": 7,
        "Place of origin": 8,
        "Place of embarkation": 9,
        "Place of disembarkation": 10
    }
    val = name_to_idx.get(key, None)
    if val:
        dictionary[val] = {key: value}
