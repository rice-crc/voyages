# Create your views here.
from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.shortcuts import render_to_response

                              
def get_page(request, chapternum, sectionnum, pagenum):
    """
    Essay subsection of the Assessment part
    
    Display an html page corresponding to the chapter-section-page passed in
    ** Context **
    ``RequestContext``
    
    ** Basic templates that might be rendered**
    :template:`assessment/c01_s01_generic.html`
    :template:`assessment/c01_s02_generic.html`
    
    The further content is rendered using the pagepath parameter 
    """
    # We might want to do some error checking for pagenum here. Even though 404 will be raised if needed
    pagepath = "assessment/c" + chapternum + "_s" + sectionnum + "_p" + pagenum + ".html"
    templatename = "assessment/c" + chapternum + "_s" + sectionnum + "_generic" + ".html"
    try:
        loader.get_template(pagepath)
        loader.get_template(templatename)
        return render_to_response(templatename, {},
                              context_instance=RequestContext(request, {"pagepath" : pagepath}))
    except TemplateDoesNotExist:
        raise Http404                          