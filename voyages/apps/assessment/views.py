# Create your views here.
from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.shortcuts import render
from haystack.query import SearchQuerySet

                              
def get_page(request, chapternum, sectionnum, pagenum):
    """
    Essay subsection of the Assessment secton
    
    Display an html page corresponding to the chapter-section-page

    The remaining content is rendered using the pagepath parameter
    """
    # We might want to do some error checking for pagenum here. Even though 404 will be raised if needed
    pagepath = "assessment/c" + chapternum + "_s" + sectionnum + "_p" + pagenum + ".html"
    templatename = "assessment/c" + chapternum + "_s" + sectionnum + "_generic" + ".html"
    try:
        loader.get_template(pagepath)
        loader.get_template(templatename)
        return render(request, templatename, {"pagepath" : pagepath})
    except TemplateDoesNotExist:
        raise Http404


def get_estimates(request):

    a = SearchQuerySet().models()

    return render(request, 'assessment/estimates.html')