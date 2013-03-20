# Create your views here.
from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.conf.urls.defaults import *
from voyages.apps.leftmenu.models import LeftMenuItem
    
def getmethodology(request, pagenum):
    # We might want to do some error checking for pagenum here. Even though 404 will be raised if needed
    parent = LeftMenuItem.objects.filter(text='Methodology')[0]
    parentNum = parent.id
    prefix = parent.url 
    nav_menu = LeftMenuItem.objects.filter(ParentID=parentNum).order_by('orderNum').exclude(pk=1)
    
    methodPageNum = "voyage/page_" + pagenum + ".html"
    return render_to_response('voyage/methodology.html', {'subpagenum': methodPageNum,}, 
                              context_instance=RequestContext(request, {'menu_items': nav_menu, 'subsectionPrefix' : prefix}));
