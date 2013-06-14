from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from django.utils.datastructures import SortedDict
from .models import Glossary, Faq, FaqCategory
from haystack.query import SearchQuerySet
from haystack.forms import HighlightedSearchForm

def glossary_page(request):
    """
    Display the entire Glossary page if there is no user query and allows users to search for terms
    The view will fetch the result from the search engine and display the results
    
    ** Context **
    ``RequestContext``
    ``mymodel``
        An instance of 
        :model:`voyages.apps.help.Glossary`
    
    ** Template **
    :template:`help/page_glossary.html`
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

        return render_to_response('help/page_glossary.html', {'glossary': sort_dict(glossary_content),
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
                                    'glossary': sort_dict(glossary_content), 'form': form,},
                                    context_instance=RequestContext(request));


def get_faqs(request):
    """
    Display the FAQ page if there is no user query and allows users to search for terms
    The view will fetch the result from the search engine and display the results
    ** Context **
    ``RequestContext``
    ``mymodel``
        An instance of 
        :model:`voyages.apps.help.Faq`
        requires :model:`voyages.apps.help.FaqCategory`
    
    ** Template **
    :template:`help/page_faqs.html`
    """
    count = 0;
    faq_list = []
    
    if request.method == 'POST':
        # Convert the posted data into Haystack search form
        form = HighlightedSearchForm(request.POST)
        if form.is_valid():
            # Perform the query by specifying the search term and sort orders (category and then questions)
            current_query = form.cleaned_data['q']
            qresult = SearchQuerySet().filter(content=current_query).models(Faq).order_by('faq_category_order', 'faq_question_order')
            
            current_item = None
            if qresult:
                # Process results
                prev_obj = None
                groupedList = []
                
                for search_result_obj in qresult:
                    current_item = search_result_obj.get_stored_fields()
                    if prev_obj is None:
                        prev_obj = current_item
                        
                    else:
                        if prev_obj['faq_category_desc'] == current_item['faq_category_desc']:
                            # Questions belong to the same category
                            prev_obj = current_item
                        else:
                             # Starts a new group of question (different category)
                             # Add the previous group to faq_list
                             faq_list.append({ 'qorder' : count, 'text' : prev_obj['faq_category_desc'], 'questions' : groupedList })
                             count += 1
                             prev_obj = current_item
                             groupedList = []
                    # Add the question to the grouped list
                    groupedList.append({ 'question': current_item['faq_question'], 'answer' : current_item['faq_answer']})
                    # Add the last result group
                faq_list.append({ 'qorder' : count, 'text' : prev_obj['faq_category_desc'], 'questions' : groupedList })
     
        return render_to_response('help/page_faqs.html', {'form' : form, "faq_list" : faq_list, 'current_query' : current_query},
                              context_instance=RequestContext(request));
    else:
        # return the form if there is no form and display the entire faq (from the database)
        form = HighlightedSearchForm()
        for faq_cat in FaqCategory.objects.order_by('type_order'):
            groupedList = Faq.objects.filter(category=faq_cat)
            if groupedList:
                # Hides category with no questions
                faq_list.append({ 'qorder' : count, 'text' : faq_cat.text, 'questions' : groupedList})
                count += 1
        return render_to_response('help/page_faqs.html', {'form' : form, "faq_list" : faq_list,},
                              context_instance=RequestContext(request));

def sort_dict(dict):
    """
    Sort the dictionary if the dictionary is not empty
    """
    try:
        return sorted(dict, key=lambda k: k['letter'])
    except:
        return dict