from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.shortcuts import render_to_response
from .models import Glossary, Faq, FaqCategory

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
    faq_list = []
    count = 0;
    for faq_cat in FaqCategory.objects.all():
        faq_list.append({ 'qorder' : count, 'text' : faq_cat.text, 'questions' : Faq.objects.filter(category=faq_cat) })
        count += 1
    
    return render_to_response('help/page_faqs.html', {"faq_list" : faq_list,},
                              context_instance=RequestContext(request));
                            
