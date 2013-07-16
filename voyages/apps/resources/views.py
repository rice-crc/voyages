from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.utils.datastructures import SortedDict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *


def get_all_images(request):
    """
    View to get demo images (4 per group).
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


def get_images_category(request, category, page):
    """
    View to show images by group.
    """
    manu = Image.objects.filter(category__label=category)
    paginator = Paginator(manu, 1)
    pagins = paginator.page(page)

    return render_to_response('resources/image-category.html',
                              {'images': pagins, 'category': category},
                              context_instance=RequestContext(request))
