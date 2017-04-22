from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_POST
from haystack.query import SearchQuerySet
from search_indexes import VoyageIndex
from voyages.apps.common.export import download_xls
from voyages.apps.voyage.models import *
import json

class SearchOperator():
    def __init__(self, front_end_op_str, back_end_op_str, list_type):
        self.front_end_op_str = front_end_op_str
        self.back_end_op_str = back_end_op_str
        self.list_type = list_type

# A list of operators used with Solr/Haystack to perform searches.
_operators_list = [
    SearchOperator('equals', 'exact', False),
    SearchOperator('is at most', 'lte', False),
    SearchOperator('is at least', 'gte', False), 
    SearchOperator('is between', 'range', True),
    SearchOperator('contains', 'contains', False),
    SearchOperator('is one of', 'in', True),
]
_operators_dict = {op.front_end_op_str: op for op in _operators_list}

index = VoyageIndex()
plain_text_suffix = '_plaintext'
plain_text_suffix_list = [f[:-len(plain_text_suffix)] for f in index.fields.keys() if f.endswith(plain_text_suffix)]
translate_suffix = '_lang_en'
translated_field_list = [f[:-len(translate_suffix)] for f in index.fields.keys() if f.endswith(translate_suffix)]

def perform_search(search, lang):
    items = search['items']
    search_terms = {}
    for item in items:
        term = item['searchTerm']
        operator = _operators_dict[item['op']]
        is_list = isinstance(term, list)
        if is_list and not operator.list_type:
            term = term[0]
        search_terms[u'var_' + unicode(item['varName']) + u'__' + unicode(operator.back_end_op_str)] = term
    result = SearchQuerySet().models(Voyage).filter(**search_terms)
    order_fields = search.get('orderBy')
    if order_fields:
        remaped_fields = []
        for field in order_fields:
            # Remap field names if they are plain text or language dependent.
            order_by_field = u'var_' + unicode(field['name'])
            if order_by_field in translated_field_list:
                order_by_field += '_lang_' + lang + '_exact'
            elif order_by_field in plain_text_suffix_list:
                order_by_field += '_plaintext_exact'
            if field['direction'] == 'desc':
                order_by_field = '-' + order_by_field
            remaped_fields.append(order_by_field)
        print 'hello'
        print remaped_fields
        result = result.order_by(*remaped_fields)
    return result

def get_results_table(results, post):
    # Here we output a data set page.
    table_params = post['tableParams']
    rows_per_page = int(table_params['length'])
    current_page_num = 1 + int(table_params['start']) / rows_per_page
    paginator = Paginator(results, rows_per_page)
    page = paginator.page(current_page_num)
    reponse_data = {}
    total_results = results.count()
    reponse_data['recordsTotal'] = total_results
    reponse_data['recordsFiltered'] = total_results
    reponse_data['draw'] = int(table_params['draw'])
    reponse_data['data'] = [{k: v if v != '[]' else '' for k, v in x.get_stored_fields().items()} for x in page]
    return reponse_data

@require_POST
def ajax_search(request):
    #try:
    data = json.loads(request.body)
    search = data['searchData']
    lang = request.LANGUAGE_CODE
    results = perform_search(search, lang)
    # The output now depends on which type of
    # result the caller expects.
    response_data = {}
    if data['output'] == 'resultsTable':
        response_data = get_results_table(results, data)
    else:
        return HttpResponseBadRequest('Unkown type of output.')
    return JsonResponse(response_data)
    #except Exception as e:
    #    return HttpResponseBadRequest(str(e))

@require_POST
def ajax_download(request):
    data = json.loads(request.POST['data'])
    search = data['searchData']
    lang = request.LANGUAGE_CODE
    results = perform_search(search, lang)
    columns = data['cols']
    return download_xls(
        [[(col, 1) for col in columns]],
        [[item[col] for col in columns] for item in [x.get_stored_fields() for x in results]])

def search_view(request):
    return render(request, 'voyage/beta_search_main.html')