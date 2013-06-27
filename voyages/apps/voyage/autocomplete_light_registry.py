import autocomplete_light
from .models import *


"""
Register autocomplete for 'autocomplete as you type'
"""
autocomplete_light.register(VoyageGroupings, search_fields=('grouping_name',),
    autocomplete_js_attributes={'placeholder': 'Grouping name...'})

autocomplete_light.register(VoyageCaptain, search_fields=('name',),
    autocomplete_js_attributes={'placeholder': 'Captain name...'})