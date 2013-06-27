import autocomplete_light
from .models import *


"""
Register autocomplete for 'autocomplete as you type'
"""
autocomplete_light.register(VoyageGroupings, search_fields=('grouping_name',),
    autocomplete_js_attributes={'placeholder': 'Grouping name...'})

autocomplete_light.register(VoyageCaptain, search_fields=('name',),
    autocomplete_js_attributes={'placeholder': 'Captain name...'})

autocomplete_light.register(VoyageShip.Nationality, search_fields=('nationality',),
    autocomplete_js_attributes={'placeholder': 'Nationality of ship...'})

autocomplete_light.register(VoyageShip.TonType, search_fields=('ton_type',),
    autocomplete_js_attributes={'placeholder': 'Ton type...'})

autocomplete_light.register(VoyageShip.RigOfVessel, search_fields=('rig_of_vessel',),
    autocomplete_js_attributes={'placeholder': 'Rig_of_vessel...'})

autocomplete_light.register(Place, search_fields=('name',),
    autocomplete_js_attributes={'placeholder': 'Place...'})

autocomplete_light.register(Region, search_fields=('name',),
    autocomplete_js_attributes={'placeholder': 'Region...'})