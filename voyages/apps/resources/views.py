from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
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

    images = SortedDict()

    for i in ImageCategory.objects.all().order_by("-value"):
        images[i.label] = []
        for j in Image.objects.filter(category__label=i.label, ready_to_go=True).order_by('date', 'image_id'):
            images[i.label].append(SortedDict({'file': j.file, 'year': j.date, 'title': j.title}))
            # TODO: May be too ugly, considered to change
            if len(images[i.label]) == 4:
                break

    dict = sorted(images, key=lambda key: images[key])
    return render_to_response('resources/images-index.html',
                              {'images': images},
                              context_instance=RequestContext(request))


def get_images_category(request, category):
    """
    View to show images by group.

    :param request: Request to serve
    :param category: Get images from this category
    """

    images = SortedDict()

    # Pack all images from category with needed data.
    for i in Image.objects.filter(category__label=category, ready_to_go=True).order_by('date', 'image_id'):
        images[i.image_id] = SortedDict({'file': i.file, 'year': i.date, 'title': i.title})

    return render_to_response('resources/images-category.html',
                              {'images': images, 'category': category},
                              context_instance=RequestContext(request))


def get_images_category_detail(request, category, page):
    """
    View to show images by group in detail.
    :param request: Request to serve
    :param category: Get images from this category
    :param page: Number of page to serve
    """

    manu = Image.objects.filter(category__label=category, ready_to_go=True).order_by('date', 'image_id')

    # Set paginator on proper page.
    paginator = Paginator(manu, 1)
    pagins = paginator.page(page)

    return render_to_response('resources/image-category-detail.html',
                              {'images': pagins, 'category': category},
                              context_instance=RequestContext(request))


def get_image_detail(request, category, page):
    """
    View to show images in detail.
    :param request: Request to serve
    :param category: Get images from this category
    :param page: Number of page to serve
    """

    image = Image.objects.filter(category__label=category, ready_to_go=True).order_by('date', 'image_id')[int(page)]

    return render_to_response('resources/image-detail.html',
                              {'image': image},
                              context_instance=RequestContext(request))


def images_search(request):
    query = ''
    time_start = ''
    time_end = ''

    if request.method == 'POST':
        # Check if session have to be deleted
        if request.POST.get('clear_form'):
            request.session.flush()
        # New search, clear data stored in session
        request.session['results'] = None
        form = SearchForm(request.POST)

        if form.is_valid():
            categories_to_search = []
            query = form.cleaned_data['q']

            # Get categories to search.
            for i in range(1,5):
                if request.POST.get("checkbox" + str(i)):
                    categories_to_search.append(ImageCategory.objects.get(value=i).label)

            time_start = request.POST.get('time_start')
            time_end = request.POST.get('time_end')

            if query != "":
                #if time_start != "":
                if time_start != "" and time_end != "":
                    results = \
                        SearchQuerySet().filter(content__icontains=query, ready_to_go=True,
                                                category_label__in=categories_to_search,
                                                date__gte=time_start,
                                                date__lte=time_end).models(Image).\
                            order_by('date', 'image_id')

                elif time_start != "":
                    results = \
                        SearchQuerySet().filter(content__icontains=query, ready_to_go=True,
                                                category_label__in=categories_to_search,
                                                date__gte=time_start).models(Image).\
                            order_by('date', 'image_id')

                elif time_end != "":
                    results = \
                        SearchQuerySet().filter(content__icontains=query, ready_to_go=True,
                                                category_label__in=categories_to_search,
                                                date__lte=time_end).models(Image).\
                            order_by('date', 'image_id')

                else:
                    results = \
                        SearchQuerySet().filter(content__icontains=query, ready_to_go=True,
                                                category_label__in=categories_to_search).models(Image).\
                            order_by('date', 'image_id')

            elif time_start != "" or time_end != "":
                if time_start != "" and time_end != "":
                    results = \
                        SearchQuerySet().filter(ready_to_go=True,
                                                category_label__in=categories_to_search,
                                                date__gte=time_start,
                                                date__lte=time_end).models(Image).\
                            order_by('date', 'image_id')

                elif time_start != "":
                    results = \
                        SearchQuerySet().filter(ready_to_go=True,
                                                category_label__in=categories_to_search,
                                                date__gte=time_start).models(Image).\
                            order_by('date', 'image_id')

                elif time_end != "":
                    results = \
                        SearchQuerySet().filter(ready_to_go=True,
                                                category_label__in=categories_to_search,
                                                date__lte=time_end).models(Image).\
                            order_by('date', 'image_id')

                else:
                    if len(categories_to_search) == 1:
                        return get_images_category(request, categories_to_search.pop())
                    else:
                        results = SearchQuerySet().all().filter(ready_to_go=True,
                                                            category_label__in=categories_to_search).\
                            order_by('date', 'image_id')

            else:
                results = SearchQuerySet().all().filter(ready_to_go=True,
                                                            category_label__in=categories_to_search).\
                            order_by('date', 'image_id')

        else:
            form = SearchForm()
            results = SearchQuerySet().all()

        # Store results in session
        request.session['results'] = results
        request.session['enabled_categories'] = categories_to_search
        request.session['query'] = query
        request.session['time_start'] = time_start
        request.session['time_end'] = time_end

    else:
        results = request.session['results']

    return render_to_response('resources/images-search-results.html',
            {'results': results,
             'query': request.session['query'],
             'time_start': request.session['time_start'],
             'time_end': request.session['time_end'],
             'enabled_categories': request.session['enabled_categories']},
            context_instance=RequestContext(request))


def images_search_detail(request, page):
    images = request.session['results']

    paginator = Paginator(images, 1)
    pagins = paginator.page(page)

    return render_to_response('resources/images-search-detail.html',
                              {'images': pagins, 'category': "Search",
                               'all_images': request.session['all_images'],
                               'query': request.session['query'],
                               'time_start': request.session['time_start'],
                               'time_end': request.session['time_end'],
                               'enabled_categories': request.session['enabled_categories']},
                              context_instance=RequestContext(request))
