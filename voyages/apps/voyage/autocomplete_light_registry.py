import autocomplete_light
from .models import *


# Register autocomplete for 'autocomplete as you type'

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

autocomplete_light.register(BroadRegion, search_fields=('name',),
    autocomplete_js_attributes={'placeholder': 'Broad region...'})

autocomplete_light.register(VoyageShipOwner, search_fields=('name',),
    autocomplete_js_attributes={'placeholder': 'Owner name...'})

autocomplete_light.register(VoyageOutcome.ParticularOutcome,
                            search_fields=('name',),
                            autocomplete_js_attributes=
                            {'placeholder': 'Particular outcome...'})

autocomplete_light.register(VoyageOutcome.SlavesOutcome,
                            search_fields=('name',),
                            autocomplete_js_attributes=
                            {'placeholder': 'Slave outcome...'})

autocomplete_light.register(VoyageOutcome.VesselCapturedOutcome,
                            search_fields=('name',),
                            autocomplete_js_attributes=
                            {'placeholder': 'Vessel captured outcome...'})

autocomplete_light.register(VoyageOutcome.OwnerOutcome,
                            search_fields=('name',),
                            autocomplete_js_attributes=
                            {'placeholder': 'Owner outcome...'})

autocomplete_light.register(VoyageOutcome.Resistance,
                            search_fields=('name',),
                            autocomplete_js_attributes=
                            {'placeholder': 'Resistance...'})

autocomplete_light.register(VoyageSources,
                            search_fields=('short_ref',),
                            autocomplete_js_attributes=
                            {'placeholder': 'Short reference...'})