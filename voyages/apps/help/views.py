from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.utils.datastructures import SortedDict
from .models import Glossary, Faq, FaqCategory
from haystack.query import SearchQuerySet
from haystack.forms import HighlightedSearchForm

def glossary_page(request):
    """
    Display the entire glossary page
    containing glossary entries from :model:`help.Glossary`
    """

    letters = []
    glossary_content = []
    glossary_dict = {}

    if request.method == 'POST':
        letters_found = SortedDict()
        results = []
        query = ""

        form = HighlightedSearchForm(request.POST)

        if form.is_valid():
            # Perform the query
            query = form.cleaned_data['q']
            results = SearchQuerySet().filter(content=query).models(Glossary)

            # Gather all letters
            for i in Glossary.objects.all():
                if letters_found.get(i.term[0]) == None:
                    letters_found[i.term[0]] = 0
                    letters.append(i.term[0])

            # Collect results
            for i in results:
                # If letter does not exist in found letters
                if letters_found[i.glossary_term[0]] == 0:
                    letters_found[i.glossary_term[0]] = 1
                    glossary_dict = {};
                    glossary_dict["letter"] = i.glossary_term[0];
                    glossary_dict["terms"] = [];
                    glossary_content.append(glossary_dict);

                # Add item to proper letter
                for j in glossary_content:
                    if j["letter"] == i.glossary_term[0]:
                        j["terms"].append({"term": i.glossary_term, "description": i.glossary_description});

        return render_to_response('help/page_glossary.html', {'glossary': sorted(glossary_content, key=lambda k: k['letter']), 
            'letters': letters, 'form': form, 'letters_found': letters_found, 'results': results, 
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
        return render_to_response('help/page_glossary.html', {'letters': letters, 
                                    'glossary': sorted(glossary_content, key=lambda k: k['letter']), 'form': form,},
                                    context_instance=RequestContext(request));


def get_faqs(request):
    """
    Display the lesson entire glossary page
    containing faq entries from :model:`help.Faq`
    """
    count = 0;
    faq_list = []
    
    if request.method == 'POST':
        form = HighlightedSearchForm(request.POST)
        if form.is_valid():
            # Perform the query
            current_query = form.cleaned_data['q']
            qresult = SearchQuerySet().filter(content=current_query).models(Faq).order_by('faq_category_order', 'faq_question_order')
            
            current_item = None
            if qresult:
                # process results
                prev_obj = None
                groupedList = []
                
                for current_item in qresult:
                    tmp = qresult.faq_category
                    5/0
                    if prev_obj is None:
                        prev_obj = current_item.object
                        groupedList.append(current_item.object)
                    else:
                        if prev_obj.category == current_item.object.category:
                            # Questions belong to the same category
                            groupedList.append(current_item.object)
                            prev_obj = current_item.object
                        else:
                             # Starts a new group of question (different category)
                             faq_list.append({ 'qorder' : count, 'text' : prev_obj.category.text, 'questions' : groupedList })
                             count += 1
                             prev_obj = current_item.object
                             groupedList = []
                             groupedList.append(prev_obj)
                    # Add the last result group
                faq_list.append({ 'qorder' : count, 'text' : prev_obj.category.text, 'questions' : groupedList })
        return render_to_response('help/page_faqs.html', {'form' : form, "faq_list" : faq_list, 'current_query' : current_query},
                              context_instance=RequestContext(request));
    else:
        form = HighlightedSearchForm()
        for faq_cat in FaqCategory.objects.all():
            faq_list.append({ 'qorder' : count, 'text' : faq_cat.text, 'questions' : Faq.objects.filter(category=faq_cat) })
            count += 1
        return render_to_response('help/page_faqs.html', {'form' : form, "faq_list" : faq_list,},
                              context_instance=RequestContext(request));
   
                            

                            
