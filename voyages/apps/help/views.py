from django.shortcuts import render
from django.utils.datastructures import SortedDict
from .models import Glossary, Faq
from haystack.query import SearchQuerySet
from haystack.forms import HighlightedSearchForm
import string

def _sort_glossary(qresult):
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



def glossary_page(request):
    """
    Display the entire Glossary page if there is no user query and allows users to search for terms
    The view will fetch the result from the search engine and display the results.

       Uses :class:`~voyages.apps.help.models.Glossary`
    """

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

    letters, letters_found, glossary_content = _sort_glossary(results)

    try:
        glossary_content = sorted(glossary_content, key=lambda k: k['letter'])
    except:
        pass

    return render(request, 'help/page_glossary.html',
                              {'glossary': glossary_content,
                               'letters': letters, 'form': form,
                               'letters_found': letters_found, 'results': results,
                               'query': query})


def _sort_faq(qresult):
    """
    Sort the result into categories and questions from response returned by the backend engine
    """
    faq_list = []
    count = 0

    if qresult and len(qresult) > 0:
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
        faq_list.append({'qorder': count,
                         'text': prev_obj['faq_category_desc'],
                         'questions': groupedList})
    return faq_list


def get_faqs(request):
    """
    Display the FAQ page if there is no user query and allows users to search for terms
    The view will fetch the result from the search engine and display the results

     Uses  :class:`~voyages.apps.help.models.Faq` and
     and :class:`~voyages.apps.help.models.FaqCategory`
    """
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

    faq_list = _sort_faq(query_result)

    return render(request, 'help/page_faqs.html',
                              {'form': form, "faq_list": faq_list, 'current_query': current_query})
