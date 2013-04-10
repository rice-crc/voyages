# Create your views here.
from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.conf.urls.defaults import *

def get_page(request, chapternum, sectionnum, pagenum):
    # We might want to do some error checking for pagenum here. Even though 404 will be raised if needed
    pagepath = "voyage/c" + chapternum + "_s" + sectionnum + "_p" + pagenum + ".html"
    templatename = "voyage/c" + chapternum + "_s" + sectionnum + "_generic" + ".html"
    return render_to_response(templatename, {},
                              context_instance=RequestContext(request, {"pagepath" : pagepath}));
                              