from django.http import Http404, HttpResponseRedirect
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.shortcuts import render_to_response
from .models import *


def get_all_images(request):
    images = {}

    for i in ImageCategory.objects.all():
        images[i.name] = []
        for j in Image.objects.filter(category__name=i.name):
            images[i.name].append({'file': j.file})

    return render_to_response('resources/images-index.html',
                              {'images': images},
                              context_instance=RequestContext(request))

def get_image_detail(request):
    pass
