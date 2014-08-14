# Create your views here.
from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.shortcuts import render
from haystack.query import SearchQuerySet
from .models import *
import collections

                              
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

    export_regions = {}
    a = SearchQuerySet().models(ExportArea)
    for i in a:
        b = SearchQuerySet().models(ExportRegion).filter(export_area__exact=i.name)
        export_regions[i] = [[a.name, a.pk] for a in b]

    import_regions = {}
    a = SearchQuerySet().models(ImportArea)
    for i in a:
        b = SearchQuerySet().models(ImportRegion).filter(import_area__exact=i.name)
        import_regions[i] = [[a.name, a.pk] for a in b]

    return render(request, 'assessment/estimates.html',
        {'export_regions': collections.OrderedDict(sorted(export_regions.items(), key=lambda x: x[0].name)),
         'import_regions': collections.OrderedDict(sorted(import_regions.items(), key=lambda x: x[0].name))})