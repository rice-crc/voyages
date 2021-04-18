from __future__ import unicode_literals

from autocomplete_light import shortcuts as autocomplete_light

from .models import (BroadRegion, Nationality, OwnerOutcome, ParticularOutcome,
                     Place, Region, Resistance, RigOfVessel, SlavesOutcome,
                     TonType, VesselCapturedOutcome, VoyageCaptain,
                     VoyageGroupings, VoyageShipOwner, VoyageSources)

# Register autocomplete for 'autocomplete as you type'

autocomplete_light.register(
    VoyageGroupings,
    search_fields=('value',),
    autocomplete_js_attributes={'placeholder': 'Grouping name...'})

autocomplete_light.register(
    VoyageCaptain,
    search_fields=('name',),
    autocomplete_js_attributes={'placeholder': 'Captain name...'})

autocomplete_light.register(
    Nationality,
    search_fields=('label',),
    autocomplete_js_attributes={'placeholder': 'Nationality of ship...'})

autocomplete_light.register(
    TonType,
    search_fields=('label',),
    autocomplete_js_attributes={'placeholder': 'Ton type...'})

autocomplete_light.register(
    RigOfVessel,
    search_fields=('label',),
    autocomplete_js_attributes={'placeholder': 'Rig of vessel...'})

autocomplete_light.register(
    Place,
    search_fields=('place',),
    autocomplete_js_attributes={'placeholder': 'Place...'})

autocomplete_light.register(
    Region,
    search_fields=('region',),
    autocomplete_js_attributes={'placeholder': 'Region...'})

autocomplete_light.register(
    BroadRegion,
    search_fields=('broad_region',),
    autocomplete_js_attributes={'placeholder': 'Broad region...'})

autocomplete_light.register(
    VoyageShipOwner,
    search_fields=('name',),
    autocomplete_js_attributes={'placeholder': 'Owner name...'})

autocomplete_light.register(
    ParticularOutcome,
    search_fields=('label',),
    autocomplete_js_attributes={'placeholder': 'Particular outcome...'})

autocomplete_light.register(
    SlavesOutcome,
    search_fields=('label',),
    autocomplete_js_attributes={'placeholder': 'Slave outcome...'})

autocomplete_light.register(
    VesselCapturedOutcome,
    search_fields=('label',),
    autocomplete_js_attributes={'placeholder': 'Vessel captured outcome...'})

autocomplete_light.register(
    OwnerOutcome,
    search_fields=('label',),
    autocomplete_js_attributes={'placeholder': 'Owner outcome...'})

autocomplete_light.register(
    Resistance,
    search_fields=('label',),
    autocomplete_js_attributes={'placeholder': 'Resistance...'})

autocomplete_light.register(
    VoyageSources,
    search_fields=('short_ref',),
    autocomplete_js_attributes={'placeholder': 'Short reference...'})
