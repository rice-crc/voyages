# Create your views here.
from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.shortcuts import render_to_response
from voyages.apps.help.models import Faq

def get_faqs(request):
    """
    Display the lesson entire glossary page
    containing faq entries from :model:`help.Faq`
    """
    return render_to_response('help/page_faqs.html', {"faq_list" : Faq.objects.all(),},
                              context_instance=RequestContext(request));
                            