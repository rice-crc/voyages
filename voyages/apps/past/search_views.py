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
    response_data = {}
    total_results = 10
    response_data['recordsTotal'] = total_results
    response_data['recordsFiltered'] = total_results
    response_data['draw'] = 1
    response_data['data'] = [
    	{"name_first":"Name 1", "age":"21", "gender": "male", "stature": "60", "voyage_id" : "1", "ship_name" : "Ship Name 1", "embarkation_port" : "Port 100", "disembarkation_port" : "Port 101", "voyage_arrived" : "1818-7-1", "intended_disembarkation_port": "Port 102", "register_country" : "Gambia", "modern_country" : "South Africa", "ethnicity" : "Ethnicity E1", "language_group" : "Language Group LG1", "post_disembarkation_location" : "Post Location 1", "source" : "Source Port 1"},
    	{"name_first":"Name 2", "age":"22", "gender": "female", "stature": "61", "voyage_id" : "2", "ship_name" : "Ship Name 2", "embarkation_port" : "Port 100", "disembarkation_port" : "Port 101", "voyage_arrived" : "1818-8-1", "intended_disembarkation_port": "Port 102", "register_country" : "Ivory Coast", "modern_country" : "Nigeria", "ethnicity" : "Ethnicity E2", "language_group" : "Language Group LG2", "post_disembarkation_location" : "Post Location 2", "source" : "Source Port 2"},
    	{"name_first":"Name 3", "age":"23", "gender": "male", "stature": "62", "voyage_id" : "3", "ship_name" : "Ship Name 3", "embarkation_port" : "Port 200", "disembarkation_port" : "Port 201", "voyage_arrived" : "1818-9-1", "intended_disembarkation_port": "Port 202", "register_country" : "Gambia", "modern_country" : "South Africa", "ethnicity" : "Ethnicity E1", "language_group" : "Language Group LG1", "post_disembarkation_location" : "Post Location 3", "source" : "Source Port 3"},
    	{"name_first":"Name 4", "age":"24", "gender": "female", "stature": "63", "voyage_id" : "4", "ship_name" : "Ship Name 1", "embarkation_port" : "Port 200", "disembarkation_port" : "Port 201", "voyage_arrived" : "1818-10-1", "intended_disembarkation_port": "Port 202", "register_country" : "Ivory Coast", "modern_country" : "Nigeria", "ethnicity" : "Ethnicity E2", "language_group" : "Language Group LG2", "post_disembarkation_location" : "Post Location 1", "source" : "Source Port 4"},
    	{"name_first":"Name 5", "age":"25", "gender": "male", "stature": "64", "voyage_id" : "5", "ship_name" : "Ship Name 2", "embarkation_port" : "Port 300", "disembarkation_port" : "Port 301", "voyage_arrived" : "1818-11-1", "intended_disembarkation_port": "Port 302", "register_country" : "Gambia", "modern_country" : "South Africa", "ethnicity" : "Ethnicity E1", "language_group" : "Language Group LG1", "post_disembarkation_location" : "Post Location 2", "source" : "Source Port 5"},
    	{"name_first":"Name 6", "age":"26", "gender": "female", "stature": "65", "voyage_id" : "1", "ship_name" : "Ship Name 3", "embarkation_port" : "Port 300", "disembarkation_port" : "Port 301", "voyage_arrived" : "1818-12-1", "intended_disembarkation_port": "Port 302", "register_country" : "Ivory Coast", "modern_country" : "Nigeria", "ethnicity" : "Ethnicity E2", "language_group" : "Language Group LG2", "post_disembarkation_location" : "Post Location 3", "source" : "Source Port 1"},
    	{"name_first":"Name 7", "age":"27", "gender": "male", "stature": "66", "voyage_id" : "2", "ship_name" : "Ship Name 1", "embarkation_port" : "Port 400", "disembarkation_port" : "Port 401", "voyage_arrived" : "1819-1-1", "intended_disembarkation_port": "Port 402", "register_country" : "Gambia", "modern_country" : "South Africa", "ethnicity" : "Ethnicity E1", "language_group" : "Language Group LG1", "post_disembarkation_location" : "Post Location 1", "source" : "Source Port 2"},
    	{"name_first":"Name 8", "age":"28", "gender": "female", "stature": "67", "voyage_id" : "3", "ship_name" : "Ship Name 2", "embarkation_port" : "Port 400", "disembarkation_port" : "Port 401", "voyage_arrived" : "1819-2-1", "intended_disembarkation_port": "Port 402", "register_country" : "Ivory Coast", "modern_country" : "Nigeria", "ethnicity" : "Ethnicity E2", "language_group" : "Language Group LG2", "post_disembarkation_location" : "Post Location 2", "source" : "Source Port 3"},
    	{"name_first":"Name 9", "age":"29", "gender": "male", "stature": "68", "voyage_id" : "4", "ship_name" : "Ship Name 3", "embarkation_port" : "Port 500", "disembarkation_port" : "Port 501", "voyage_arrived" : "1819-3-1", "intended_disembarkation_port": "Port 502", "register_country" : "Gambia", "modern_country" : "South Africa", "ethnicity" : "Ethnicity E1", "language_group" : "Language Group LG1", "post_disembarkation_location" : "Post Location 3", "source" : "Source Port 4"},
    	{"name_first":"Name 10", "age":"30", "gender": "female", "stature": "69", "voyage_id" : "5", "ship_name" : "Ship Name 1", "embarkation_port" : "Port 500", "disembarkation_port" : "Port 501", "voyage_arrived" : "1819-4-1", "intended_disembarkation_port": "Port 502", "register_country" : "Ivory Coast", "modern_country" : "Nigeria", "ethnicity" : "Ethnicity E2", "language_group" : "Language Group LG2", "post_disembarkation_location" : "Post Location 4", "source" : "Source Port 5"}]
    return JsonResponse(response_data)
