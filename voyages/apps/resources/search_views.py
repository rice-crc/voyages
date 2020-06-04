from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import get_language
from django.utils.translation import ugettext as _
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from haystack.query import SearchQuerySet
from haystack.inputs import Raw
import csv
import itertools
import json
import os
import re
import unicodecsv

@require_POST
@csrf_exempt
def ajax_search(request):
    reponse_data = {}
    total_results = 10
    reponse_data['recordsTotal'] = total_results
    reponse_data['recordsFiltered'] = total_results
    reponse_data['draw'] = 1
    reponse_data['data'] = [{"var_documented_name":"Name 1"},{"var_documented_name":"Name 2"},{"var_documented_name":"Name 3"},{"var_documented_name":"Name 4"},{"var_documented_name":"Name 5"},{"var_documented_name":"Name 6"},{"var_documented_name":"Name 7"},{"var_documented_name":"Name 8"},{"var_documented_name":"Name 9"},{"var_documented_name":"Name 10"}]
    return JsonResponse(reponse_data)
