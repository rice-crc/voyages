from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.shortcuts import render_to_response
from .models import Glossary, Faq
from .forms import GlossarySearchForm

def glossaryPage(request):
    letters = []
    glossary_content = [];
    glossary_dict = {};

    for i in Glossary.objects.all():
        if i.term[0] not in letters:
            glossary_content.append(glossary_dict);
            letters.append(i.term[0]);
            glossary_dict = {};
            glossary_dict["letter"] = i.term[0];
            glossary_dict["terms"] = [];
        glossary_dict["terms"].append({"term": i.term, "description": i.description});

    letters.sort();
    form = GlossarySearchForm();

    return render_to_response('help/page_glossary.html', {'letters': letters, 'glossary': glossary_content, 'form': form},
                              context_instance=RequestContext(request));

    #return render_to_response('help/page_glossary.html', {'letters': letters, 'glossary': Glossary.objects.all()},
    #                                      context_instance=RequestContext(request));

def get_faqs(request):
    """
    Display the lesson entire glossary page
    containing faq entries from :model:`help.Faq`
    """
    return render_to_response('help/page_faqs.html', {"faq_list" : Faq.objects.all(),},
                              context_instance=RequestContext(request));
                            
