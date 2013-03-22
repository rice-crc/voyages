# Create your views here.
from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.conf.urls.defaults import *
from voyages.apps.leftmenu.models import LeftMenuItem

def getmethodology(request, pagenum):
    # We might want to do some error checking for pagenum here. Even though 404 will be raised if needed
    parentSection = LeftMenuItem.objects.filter(text='Voyage Database')[0]
    parentNum = parentSection.id
    prefix = parentSection.url
   
    if (not pagenum):
        pagenum = "00"
   
    left_menu_list = []
    left_menu = LeftMenuItem.objects.filter(parent=parentNum).order_by('orderNum').exclude(pk=1)
    
    # Iterate and retrieve all nested submenus
    for item in left_menu:
        sub_menu = LeftMenuItem.objects.filter(parent=item.id).order_by('orderNum')
        left_menu_list.append(item.get_html_code())
        
        if item.text == 'Methodology':
            sub_list = []
            for idx, subitem in enumerate(sub_menu):
                countS = sub_menu.count;
                if (subitem.orderNum == pagenum):
                    prev_page_link = sub_menu[idx - 1].get_html_code() if (pagenum > '01') else False;
                    next_page_link = sub_menu[idx + 1].get_html_code() if (int(pagenum) + 1 < len(sub_menu)) else False;
                sub_list.append(subitem.get_html_code())
            left_menu_list.append(sub_list)
        else:
            if sub_menu.count > 0:
                sub_list = []
                for subitem in sub_menu:
                    sub_list.append(subitem.get_html_code())
                    
                left_menu_list.append(sub_list)
    # Retrieve the content 
    methodPageNum = "voyage/page_" + pagenum + ".html"
    return render_to_response('voyage/methodology.html', {'subpagenum': methodPageNum,}, 
                              context_instance=RequestContext(request, 
                                    {'menu_items': left_menu_list,
                                     'prev_page_link': prev_page_link,
                                     'next_page_link': next_page_link,
                                     }));

def getguide(request):
      # We might want to do some error checking for pagenum here. Even though 404 will be raised if needed
    left_menu_list = _getMenuList()
      
    return render_to_response('voyage/guide.html', {}, 
                              context_instance=RequestContext(request, {'menu_items': left_menu_list, }));
 
 
def _getMenuList():
     # Retrieve the left menu for the particular section
    parentSection = LeftMenuItem.objects.filter(text='Voyage Database')[0]
    parentNum = parentSection.id
    prefix = parentSection.url
   
    
    left_menu_list = []
    left_menu = LeftMenuItem.objects.filter(parent=parentNum).order_by('orderNum').exclude(pk=1)
    
    # Iterate and retrieve all nested submenus
    for item in left_menu:
        sub_menu = LeftMenuItem.objects.filter(parent=item.id).order_by('orderNum')
        left_menu_list.append(item.get_html_code())
        if sub_menu.count > 0:
            sub_list = []
            for subitem in sub_menu:
                sub_list.append(subitem.get_html_code())
                
            left_menu_list.append(sub_list)
    return left_menu_list