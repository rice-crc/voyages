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
    	{"searched_name":"Name 1", "age":"21", "gender": "male", "stature": "60", "register_country" : "Gambia", "modern_country" : "South Africa", "ethnicity" : "Ethnicity E1", "language_group" : "Language Group LG1"},
    	{"searched_name":"Name 2", "age":"22", "gender": "female", "stature": "61", "register_country" : "Ivory Coast", "modern_country" : "Nigeria", "ethnicity" : "Ethnicity E2", "language_group" : "Language Group LG2"},
    	{"searched_name":"Name 3", "age":"23", "gender": "male", "stature": "62", "register_country" : "Gambia", "modern_country" : "South Africa", "ethnicity" : "Ethnicity E1", "language_group" : "Language Group LG1"},
    	{"searched_name":"Name 4", "age":"24", "gender": "female", "stature": "63", "register_country" : "Ivory Coast", "modern_country" : "Nigeria", "ethnicity" : "Ethnicity E2", "language_group" : "Language Group LG2"},
    	{"searched_name":"Name 5", "age":"25", "gender": "male", "stature": "64", "register_country" : "Gambia", "modern_country" : "South Africa", "ethnicity" : "Ethnicity E1", "language_group" : "Language Group LG1"},
    	{"searched_name":"Name 6", "age":"26", "gender": "female", "stature": "65", "register_country" : "Ivory Coast", "modern_country" : "Nigeria", "ethnicity" : "Ethnicity E2", "language_group" : "Language Group LG2"},
    	{"searched_name":"Name 7", "age":"27", "gender": "male", "stature": "66", "register_country" : "Gambia", "modern_country" : "South Africa", "ethnicity" : "Ethnicity E1", "language_group" : "Language Group LG1"},
    	{"searched_name":"Name 8", "age":"28", "gender": "female", "stature": "67", "register_country" : "Ivory Coast", "modern_country" : "Nigeria", "ethnicity" : "Ethnicity E2", "language_group" : "Language Group LG2"},
    	{"searched_name":"Name 9", "age":"29", "gender": "male", "stature": "68", "register_country" : "Gambia", "modern_country" : "South Africa", "ethnicity" : "Ethnicity E1", "language_group" : "Language Group LG1"},
    	{"searched_name":"Name 10", "age":"30", "gender": "female", "stature": "69", "register_country" : "Ivory Coast", "modern_country" : "Nigeria", "ethnicity" : "Ethnicity E2", "language_group" : "Language Group LG2"}]
    return JsonResponse(reponse_data)
