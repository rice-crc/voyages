# Create your views here.

from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.utils.http import base36_to_int, is_safe_url
from django.template import RequestContext
from django.shortcuts import render

def abouthome(request):
    context = {}
    return render(request, 'about/index.html', context)
