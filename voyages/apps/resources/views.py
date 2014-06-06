from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.datastructures import SortedDict
from django.core.paginator import Paginator
from haystack.query import SearchQuerySet
from haystack.forms import SearchForm
from .models import *


def get_all_images(request):
    """
    View to get demo images (4 per group).
    :param request: Request to serve
    """

    images = []

    for i in ImageCategory.objects.all().order_by("-value"):
        if i.visible_on_website is True:
            category_images = {}
            category_images["label_name"] = i.label
            category_images["label_code"] = i.value
            category_images["images"] = []
            search_set = SearchQuerySet().models(Image).filter(category_label__exact=i.label, ready_to_go=True).order_by('date')
            category_images["number_of_images"] = len(search_set)
            for j in search_set:
                category_images["images"].append(SortedDict({'file': j.file, 'year': j.date, 'title': j.title}))
                # TODO: May be too ugly, considered to change
                if len(category_images["images"]) == 4:
                    break

            images.append(category_images)

    images = sorted(images, key=lambda k: k["label_name"])

    return render(request, 'resources/images-index.html', {'images': images})


def get_images_category(request, category):
    """
    View to show images by group.

    :param request: Request to serve
    :param category: Get images from this category
    """

    images = []
    category = " ".join(category.split("_"))

    # Pack all images from category with needed data.
    for i in ImageCategory.objects.all().order_by("-value"):
        if i.visible_on_website is True:
            category_images = {}
            category_images["label_name"] = i.label
            category_images["label_code"] = i.value
            category_images["images"] = []
            search_set = SearchQuerySet().models(Image).filter(category_label__exact=i.label, ready_to_go=True).order_by('date')
            category_images["number_of_images"] = len(search_set)
            if i.label == category:
                for i in search_set:
                    category_images["images"].append(SortedDict({'file': i.file, 'year': i.date, 'title': i.title}))

            images.append(category_images)

    images = sorted(images, key=lambda k: k["label_name"])

    # 3/0
    return render(request, 'resources/images-category.html',
                              {'images': images, 'category': category})


def get_images_category_detail(request, category, page):
    """
    View to show images by group in detail.
    :param request: Request to serve
    :param category: Get images from this category
    :param page: Number of page to serve
    """

    category = " ".join(category.split("_"))
    manu = SearchQuerySet().filter(category_label__exact=category, ready_to_go=True).order_by('date')
    images = []

    # Pack all images from category with needed data.
    for i in ImageCategory.objects.all().order_by("-value"):
        if i.visible_on_website is True:
            category_images = {}
            category_images["label_name"] = i.label
            category_images["label_code"] = i.value
            category_images["images"] = []
            search_set = SearchQuerySet().models(Image).filter(category_label__exact=i.label, ready_to_go=True).order_by('date')
            category_images["number_of_images"] = len(search_set)
            if i.label == category:
                # Set paginator on proper page.
                paginator = Paginator(manu, 1)
                pagins = paginator.page(page)

            images.append(category_images)

    images = sorted(images, key=lambda k: k["label_name"])

    return render(request, 'resources/image-category-detail.html',
                              {'images': images,
                               'pagins': pagins,
                               'category': category})


def get_image_detail(request, category, page):
    """
    View to show images in detail.
    :param request: Request to serve
    :param category: Get images from this category
    :param page: Number of page to serve
    """

    category = " ".join(category.split("_"))
    image = SearchQuerySet().filter(category_label__exact=category, ready_to_go=True).order_by('date')[int(page)-1]

    return render(request, 'resources/image-detail.html', {'image': image})


def images_search(request):
    """
    View to make search of images.

    :param request: Request to serve
    """

    query = ''
    time_start = ''
    time_end = ''

    if request.method == 'POST':

        # Check if session have to be deleted
        if request.POST.get('clear_form'):
            request.session.flush()
            pass

        # New search, clear data stored in session
        request.session['results_images'] = None
        form = SearchForm(request.POST)

        if form.is_valid():
            images = []
            categories_to_search = []
            query = form.cleaned_data['q']

            # Get categories to search and get left menu data
            for i in ImageCategory.objects.filter(visible_on_website=True):
                category_images = {}
                category_images["label_name"] = i.label
                category_images["label_code"] = i.value
                category_images["images"] = []
                search_set = SearchQuerySet().models(Image).filter(category_label__exact=i.label, ready_to_go=True).order_by('date')
                category_images["number_of_images"] = len(search_set)
                if request.POST.get("checkbox" + str(i.value)):
                    categories_to_search.append(i.label)

                images.append(category_images)

            images = sorted(images, key=lambda k: k["label_name"])

            time_start = request.POST.get('time_start')
            time_end = request.POST.get('time_end')

            # Options if query is provided
            if query != "":
                if time_start != "" and time_end != "":
                    results = \
                        SearchQuerySet().filter(imgtext__icontains=query, ready_to_go=True,
                                                category_label__in=categories_to_search,
                                                date__gte=time_start,
                                                date__lte=time_end).models(Image).\
                            order_by('date')

                elif time_start != "":
                    results = \
                        SearchQuerySet().filter(imgtext__icontains=query, ready_to_go=True,
                                                category_label__in=categories_to_search,
                                                date__gte=time_start).models(Image).\
                            order_by('date')

                elif time_end != "":
                    results = \
                        SearchQuerySet().filter(imgtext__icontains=query, ready_to_go=True,
                                                category_label__in=categories_to_search,
                                                date__lte=time_end).models(Image).\
                            order_by('date')

                else:
                    results = \
                        SearchQuerySet().filter(imgtext__icontains=query, ready_to_go=True,
                                                category_label__in=categories_to_search).models(Image).\
                            order_by('date')

            elif time_start != "" or time_end != "":
                if time_start != "" and time_end != "":
                    results = \
                        SearchQuerySet().filter(ready_to_go=True,
                                                category_label__in=categories_to_search,
                                                date__gte=time_start,
                                                date__lte=time_end).models(Image).\
                            order_by('date')

                elif time_start != "":
                    results = \
                        SearchQuerySet().filter(ready_to_go=True,
                                                category_label__in=categories_to_search,
                                                date__gte=time_start).models(Image).\
                            order_by('date')

                elif time_end != "":
                    results = \
                        SearchQuerySet().filter(ready_to_go=True,
                                                category_label__in=categories_to_search,
                                                date__lte=time_end).models(Image).\
                            order_by('date')

                else:
                    if len(categories_to_search) == 1:
                        return HttpResponseRedirect(reverse('resources:images-category',
                                                        kwargs={'category': categories_to_search.pop()}))
                    else:
                        results = SearchQuerySet().all().filter(ready_to_go=True,
                                                            category_label__in=categories_to_search).\
                            order_by('date')

            else:
                if len(categories_to_search) > 1:
                    results = SearchQuerySet().all().filter(ready_to_go=True,
                                                            category_label__in=categories_to_search).\
                            order_by('date')
                else:
                    return HttpResponseRedirect(reverse('resources:images-category',
                                                        kwargs={'category': categories_to_search.pop()}))

        else:
            results = SearchQuerySet().model(Image).all()

        # Store results in session
        request.session['results_images'] = results
        request.session['images_images'] = images
        request.session['enabled_categories'] = categories_to_search
        request.session['query'] = query
        request.session['time_start'] = time_start
        request.session['time_end'] = time_end

    else:
        results = request.session['results_images']
        images = request.session['images_images']

    return render(request, 'resources/images-search-results.html',
            {'results': results,
             'images': images,
             'query': request.session['query'],
             'time_start': request.session['time_start'],
             'time_end': request.session['time_end'],
             'enabled_categories': request.session['enabled_categories']})


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

    return render(request, 'resources/images-search-detail.html',
                              {'images': images,
                               'results': pagins,
                               'category': "Search",
                               'query': request.session['query'],
                               'time_start': request.session['time_start'],
                               'time_end': request.session['time_end'],
                               'enabled_categories': request.session['enabled_categories']})


def get_image_search_detail(request, page):
    """
    Get details of one of the found images.

    :param request: Request to serve
    :param page: Number of page to serve details
    """

    image = request.session['results_images'][int(page)-1]

    return render(request, 'resources/image-search-detail-window.html',  {'image': image})
