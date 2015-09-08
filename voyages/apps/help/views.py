from django.shortcuts import render
from django.utils.datastructures import SortedDict
from .models import Glossary, Faq
from haystack.query import SearchQuerySet
from haystack.forms import HighlightedSearchForm
from unidecode import unidecode
import string

def _sort_glossary(qresult, lang):
    """
    Sort the result into categories and questions from response returned by the backend engine
    """
    glossary_content = []
    letters = []
    letters_found = SortedDict()
    field = 'glossary_term_lang_' + lang

    for i in string.ascii_uppercase:
        letters.append(i)
        letters_found[i] = 0

    if len(qresult) > 0:
        # Process results
        from itertools import groupby
        items = [o.get_stored_fields() for o in qresult]
        items = sorted(items, key=lambda x: unidecode(x[field]))
        for k, g in groupby(items, key=lambda x: unidecode(x[field])[0]):
            letters_found[k] = 1
            glossary_content.append({'letter': k,
                                     'terms': [{'term': item[field],
                                               'description': item['glossary_description_lang_' + lang]}
                                               for item in g]})

    return letters, letters_found, glossary_content



def glossary_page(request):
    """
    Display the entire Glossary page if there is no user query and allows users to search for terms
    The view will fetch the result from the search engine and display the results.

       Uses :class:`~voyages.apps.help.models.Glossary`
    """

    query = ""
    lang = request.LANGUAGE_CODE
    field = 'glossary_term_lang_' + lang
    results = SearchQuerySet().models(Glossary)

    if request.method == 'POST':
        form = HighlightedSearchForm(request.POST)

        if form.is_valid():
            # Perform the query
            query = form.cleaned_data['q']
            results = results.filter(content=query)
        else:
            form = HighlightedSearchForm()
    else:
        form = HighlightedSearchForm()
    results = results.order_by(field)

    letters, letters_found, glossary_content = _sort_glossary(results, lang)

    try:
        glossary_content = sorted(glossary_content, key=lambda k: k['letter'])
    except:
        pass

    return render(request, 'help/page_glossary.html',
                              {'glossary': glossary_content,
                               'letters': letters, 'form': form,
                               'letters_found': letters_found,
                               'results': results,
                               'query': query})


def _sort_faq(qresult, lang):
    """
    Sort the result into categories and questions from response returned by the backend engine
    """
    faq_list = []
    count = 0
    category_field = 'faq_category_desc_lang_' + lang
    question_field = 'faq_question_lang_' + lang
    answer_field = 'faq_answer_lang_' + lang

    if len(qresult) > 0:
        # Process results
        from itertools import groupby
        items = [o.get_stored_fields() for o in qresult]
        for k, g in groupby(items, key=lambda x: unidecode(x[category_field])):
            questions = [{'question': item[question_field], 'answer': item[answer_field]} for item in g]
            count += 1
            faq_list.append({'qorder': count,
                             'text': k,
                             'questions': questions})
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

    faq_list = _sort_faq(query_result, request.LANGUAGE_CODE)

    return render(request, 'help/page_faqs.html',
                              {'form': form, "faq_list": faq_list, 'current_query': current_query})
