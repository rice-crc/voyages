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
    reponse_data['data'] = [
    	{"var_searched_name":"Name 1", "var_age":"21", "var_gender": "male", "var_stature": "60"},
    	{"var_searched_name":"Name 2", "var_age":"22", "var_gender": "female", "var_stature": "61"},
    	{"var_searched_name":"Name 3", "var_age":"23", "var_gender": "male", "var_stature": "62"},
    	{"var_searched_name":"Name 4", "var_age":"24", "var_gender": "female", "var_stature": "63"},
    	{"var_searched_name":"Name 5", "var_age":"25", "var_gender": "male", "var_stature": "64"},
    	{"var_searched_name":"Name 6", "var_age":"26", "var_gender": "female", "var_stature": "65"},
    	{"var_searched_name":"Name 7", "var_age":"27", "var_gender": "male", "var_stature": "66"},
    	{"var_searched_name":"Name 8", "var_age":"28", "var_gender": "female", "var_stature": "67"},
    	{"var_searched_name":"Name 9", "var_age":"29", "var_gender": "male", "var_stature": "68"},
    	{"var_searched_name":"Name 10", "var_age":"30", "var_gender": "female", "var_stature": "69"}]
    return JsonResponse(reponse_data)
