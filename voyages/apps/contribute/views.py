# Create your views here.
from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def index(request):
    if request.user.is_authenticated():
        return render_to_response('contribute/index.html', {}, context_instance=RequestContext(request));
