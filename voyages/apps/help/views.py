from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.shortcuts import render_to_response
from .models import Glossary, Faq, FaqCategory
from haystack.query import SearchQuerySet
from haystack.forms import HighlightedSearchForm

def glossary_page(request):
    letters = []
    letters_found = {}
    glossary_content = []
    glossary_dict = {}
    results = []
    query = ""

    if request.method == 'POST':
        form = HighlightedSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['q']
            results = SearchQuerySet().filter(content=query).models(Glossary)
            # find letters
            for i in Glossary.objects.all():
                if letters_found.get(i.term[0]) == None:
                    letters_found[i.term[0]] = 0
                    letters.append(i.term[0])
            for i in results:
                # if letter does not exist in found letters
                if letters_found[i.term[0]] == 0:
                    letters_found[i.term[0]] = 1
                    glossary_dict = {};
                    glossary_dict["letter"] = i.term[0];
                    glossary_dict["terms"] = [];
                    glossary_content.append(glossary_dict);

                # add item to proper place
                for j in glossary_content:
                    if j["letter"] == i.term[0]:
                        j["terms"].append({"term": i.term, "description": i.description});

        return render_to_response('help/page_glossary.html', {'glossary': sorted(glossary_content, key=lambda k: k['letter']), 
            'letters': letters, 'form': form, 'letters_found': sorted(letters_found, key=lambda key: letters_found[key]), 'results': results, 
                                    'query': query}, context_instance=RequestContext(request))


    else:
        form = HighlightedSearchForm()
        for i in Glossary.objects.all():
            if i.term[0] not in letters:
                if glossary_dict:
                    glossary_content.append(glossary_dict);
                letters.append(i.term[0]);
                glossary_dict = {};
                glossary_dict["letter"] = i.term[0];
                glossary_dict["terms"] = [];
            glossary_dict["terms"].append({"term": i.term, "description": i.description});
        glossary_content.append(glossary_dict);
        letters.sort();
        #response = "help/page_glossary.html, {'glossary': sorted(glossary_content, key=lambda k: k['letter']), 'letters': letters, 'form': form}, context_instance=RequestContext(request)"
        return render_to_response('help/page_glossary.html', {'letters': letters, 'glossary': sorted(glossary_content, key=lambda k: k['letter']), 'form': form, 
                                    'results': results, 'query': query},
                                    context_instance=RequestContext(request));


def get_faqs(request):
    """
    Display the lesson entire glossary page
    containing faq entries from :model:`help.Faq`
    """
    myresult = []
    current_query = ""
    
    if request.method == 'POST':
        form = HighlightedSearchForm(request.POST)
        if form.is_valid():
            # Perform the query
            current_query = form.cleaned_data['q']
            myresult = SearchQuerySet().filter(content=current_query).highlight()
    else:
        form = HighlightedSearchForm()
        
    faq_list = []
    count = 0;
    for faq_cat in FaqCategory.objects.all():
        faq_list.append({ 'qorder' : count, 'text' : faq_cat.text, 'questions' : Faq.objects.filter(category=faq_cat) })
        count += 1
    
    return render_to_response('help/page_faqs.html', {'form' : form, "faq_list" : faq_list, 'result' : myresult, 'current_query' : current_query},
                              context_instance=RequestContext(request));
                            
