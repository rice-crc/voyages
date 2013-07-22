from django.template import RequestContext
from django.shortcuts import render_to_response
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

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            # Perform the query
            query = form.cleaned_data['q']
            category = form.cleaned_data['category']
            try:
                time_start = form.cleaned_data['time_start']
                time_end = form.cleaned_data['time_end']
                results = \
                    SearchQuerySet().filter(content=query,
                                            category_label__exact=category,
                                            date__gte=time_start,
                                            date__lte=time_end).models(Image)
            except:
                results = \
                    SearchQuerySet().filter(content=query,
                                            category_label__exact=category).models(Image)

        else:
            form = SearchForm()
            results = SearchQuerySet().models(Image).order_by('date', 'image_id')

        return render_to_response('resources/images-search-results.html',
            {'results': results, 'query': query},
            context_instance=RequestContext(request))