from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.shortcuts import render_to_response
from .models import Glossary, Faq

def glossaryPage(request):
    letters = []

    for i in Glossary.objects.all():
        if i.term[0] not in letters:
            letters.append(i.term[0]);

    letters.sort();
    return render_to_response('help/page_glossary.html', {'letters': letters, 'glossary': Glossary.objects.all()},
                              context_instance=RequestContext(request));

def get_faqs(request):
    """
    Display the lesson entire glossary page
    containing faq entries from :model:`help.Faq`
    """
    return render_to_response('help/page_faqs.html', {"faq_list" : Faq.objects.all(),},
                              context_instance=RequestContext(request));
                            
