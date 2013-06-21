from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.datastructures import SortedDict
from .models import Glossary, Faq
from haystack.query import SearchQuerySet
from haystack.forms import HighlightedSearchForm
import string


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

    def sort_dict(dict):
        """
        Sort the dictionary if the dictionary is not empty
        """
        try:
            return sorted(dict, key=lambda k: k['letter'])
        except:
            return dict

    def getsortedresults(qresult):
        """
        Sort the result into categories and questions from response returned by the backend engine
        """
        glossary_content = []
        letters = []
        letters_found = SortedDict()

        for i in string.ascii_uppercase:
            letters.append(i)
            letters_found[i] = 0

        if qresult:
            # Process results
            prev_letter = None
            groupedList = []

            for search_result_obj in qresult:
                current_item = search_result_obj.get_stored_fields()

                if prev_letter is None:
                    # Update the first letter
                    prev_letter = current_item['glossary_term'][0]
                else:
                    if prev_letter != current_item['glossary_term'][0]:
                        # Starts a new group of terms
                        # Add the previous group to glossary_content
                        glossary_content.append({'letter': prev_letter, 'terms': groupedList})
                        letters_found[prev_letter] = 1

                        prev_letter = current_item['glossary_term'][0]
                        groupedList = []

                # Add the question to the grouped list
                groupedList.append(
                    {'term': current_item['glossary_term'], 'description': current_item['glossary_description']})

            # Add the last result group
            letters_found[prev_letter] = 1
            glossary_content.append({'letter': prev_letter, 'terms': groupedList})

        return letters, letters_found, glossary_content

    query = ""

    if request.method == 'POST':
        form = HighlightedSearchForm(request.POST)

        if form.is_valid():
            # Perform the query
            query = form.cleaned_data['q']
            results = SearchQuerySet().filter(content=query).models(Glossary).order_by('glossary_term_exact')
        else:
            form = HighlightedSearchForm()
            results = SearchQuerySet().models(Glossary).order_by('glossary_term_exact')
    else:
        form = HighlightedSearchForm()
        results = SearchQuerySet().models(Glossary).order_by('glossary_term_exact')

    letters, letters_found, glossary_content = getsortedresults(results)

    return render_to_response('help/page_glossary.html',
                              {'glossary': sort_dict(glossary_content),
                               'letters': letters, 'form': form,
                               'letters_found': letters_found, 'results': results,
                               'query': query}, context_instance=RequestContext(request))


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

    def getsortedresults(qresult):
        """
        Sort the result into categories and questions from response returned by the backend engine
        """
        faq_list = []
        count = 0

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
                        faq_list.append(
                            {'qorder': count, 'text': prev_obj['faq_category_desc'], 'questions': groupedList})
                        count += 1
                        prev_obj = current_item
                        groupedList = []
                        # Add the question to the grouped list
                groupedList.append({'question': current_item['faq_question'], 'answer': current_item['faq_answer']})
                # Add the last result group
            faq_list.append({'qorder': count, 'text': prev_obj['faq_category_desc'], 'questions': groupedList})
        return faq_list

    current_query = ''

    if request.method == 'POST':
        # Convert the posted data into Haystack search form
        form = HighlightedSearchForm(request.POST)
        if form.is_valid():
            # Perform the query by specifying the search term and sort orders (category and then questions)
            current_query = form.cleaned_data['q']
            query_result = SearchQuerySet().filter(content=current_query).models(Faq).order_by('faq_category_order',
                                                                                          'faq_question_order')
        else:
            form = HighlightedSearchForm()
            query_result = SearchQuerySet().models(Faq).order_by('faq_category_order', 'faq_question_order')
    else:
        # return the form if there is no form and display the entire faq (from the database)
        form = HighlightedSearchForm()
        query_result = SearchQuerySet().models(Faq).order_by('faq_category_order', 'faq_question_order')

    faq_list = getsortedresults(query_result)

    3/0

    return render_to_response('help/page_faqs.html',
                              {'form': form, "faq_list": faq_list, 'current_query': current_query},
                              context_instance=RequestContext(request))
