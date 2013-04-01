# Create your views here.
from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.conf.urls.defaults import *


def get_intro(request, pagenum):
    # We might want to do some error checking for pagenum here. Even though 404 will be raised if needed
    pagepath = "assessment/intro_page_" + pagenum + ".html"
    return render_to_response("assessment/essays-intro-generic.html", {}, 
                              context_instance=RequestContext(request, {"pagepath" : pagepath}));
                              
def get_seasonality(request, pagenum):
    # We might want to do some error checking for pagenum here. Even though 404 will be raised if needed
    pagepath = "assessment/seasonality_page_" + pagenum + ".html"
    return render_to_response("assessment/essays-seasonality-generic.html", {},
                              context_instance=RequestContext(request, {"pagepath" : pagepath}));
                              