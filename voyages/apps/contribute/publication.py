from django.db import transaction
from voyages.apps.contribute.models import *
from voyages.apps.voyage.models import *

def publish_reviewed_contributions(review_requests):
    with transaction.atomic():
        for req in review_requests:
            # Basic validation.
            if req.final_decision != ReviewRequestDecision.accepted_by_editor:
                raise Exception('Review cannot be published since it was not accepted by editor')
            if req.contribution_id.startswith('delete'):
                _publish_single_review_delete(req)
            elif req.contribution_id.startswith('merge'):
                _publish_single_review_merge(req)
            elif req.contribution_id.startswith('new'):
                _publish_single_review_new(req)
            elif req.contribution_id.startswith('edit'):
                _publish_single_review_update(req)
    pass

def _delete_child_fk(obj, child_attr):
    child = getattr(obj, child_attr)
    if child:
        setattr(obj, child_attr, None)
        obj.save()
        child.delete()

def _get_editorial_version(review_request, contrib_type):
    editor_contribution = review_request.editor_contribution
    if editor_contribution is None or editor_contribution.interim_voyage is None:
        raise Exception('This type of contribution requires an editor review interim voyage for publication')
    interim = editor_contribution.interim_voyage
    # Create or load a voyage with the appropriate voyage id.
    voyage = Voyage()
    if contrib_type == 'merge' or contrib_type == 'new':
        if not review_request.created_voyage_id:
            raise Exception('For new or merged contributions, an explicit voyage_id must be set')
        voyage.voyage_id = review_request.created_voyage_id
    elif contrib_type == 'edit':
        contrib_id = int(review_request.contribution_id.split('/')[1])
        contrib = EditVoyageContribution.objects.get(pk=contrib_id)
        voyage = Voyage.objects.get(voyage_id=contrib.edited_voyage_id)
    else
        raise Exception('Unsupported contribution type ' + contrib_type)
    # Edit field values and create child records for the voyage.
    if contrib_type != 'edit':
        voyage.voyage_in_cd_rom = False
    else:
        _delete_child_fk(voyage, 'voyage_ship')
        _delete_child_fk(voyage, 'voyage_itinerary')
        _delete_child_fk(voyage, 'voyage_dates')
        _delete_child_fk(voyage, 'voyage_crew')
        _delete_child_fk(voyage, 'voyage_slaves_numbers')
        voyage.voyage_captain.clear()
        voyage.voyage_ship_owner.clear()
        voyage.voyage_sources.clear()
    
    # Save voyage so that the database generates a primary key for it.
    voyage.voyage_groupings = interim.imputed_voyage_groupings_for_estimating_imputed_slaves
    voyage.save()
    
    def region(place):
        return None if place is None else place.region
        
    def broad_region(place):
        r = region(place)
        return None if r is None else r.broad_region
        
    # Voyage Ship
    ship = VoyageShip()
    ship.voyage = voyage
    ship.ship_name = interim.name_of_vessel
    ship.nationality_ship = interim.national_carrier
    ship.tonnage = interim.tonnage_of_vessel
    ship.ton_type = interim.ton_type
    ship.rig_of_vessel = interim.rig_of_vessel
    ship.guns_mounted = interim.guns_mounted
    ship.year_of_construction = interim.year_ship_constructed
    ship.vessel_construction_place = interim.ship_construction_place
    ship.vessel_construction_region = interim.imputed_region_ship_constructed
    ship.registered_year = interim.year_ship_registered
    ship.registered_place = interim.ship_registration_place
    ship.registered_region = region(interim.ship_registration_place)
    ship.imputed_nationality = interim.imputed_national_carrier
    ship.tonnage_mod = interim.imputed_standardized_tonnage
    ship.save()
    if interim.first_ship_owner:
        voyage.voyage_ship_owner.create(name=interim.first_ship_owner)
    if interim.second_ship_owner:
        voyage.voyage_ship_owner.create(name=interim.second_ship_owner)
    if interim.additional_ship_owners:
        additional = interim.additional_ship_owners.split('\n')
        for owner in additional:
            voyage.voyage_ship_owner.create(name=owner)
    
    # Voyage Itinerary    
    itinerary = VoyageItinerary()
    itinerary.voyage = voyage
    itinerary.int_first_port_emb = interim.first_port_intended_embarkation
    itinerary.int_second_port_emb = interim.second_port_intended_embarkation
    itinerary.int_first_region_purchase_slaves = region(interim.first_port_intended_embarkation)
    itinerary.int_second_region_purchase_slaves = region(interim.second_port_intended_embarkation)
    itinerary.int_first_port_dis = interim.first_port_intended_disembarkation
    itinerary.int_second_port_dis = interim.second_port_intended_disembarkation
    itinerary.int_first_region_slave_landing = region(interim.first_port_intended_disembarkation)
    itinerary.int_second_place_region_slave_landing = region(interim.second_port_intended_disembarkation)
    itinerary.ports_called_buying_slaves = interim.number_of_ports_called_prior_to_slave_purchase
    itinerary.first_place_slave_purchase = interim.first_place_of_slave_purchase
    itinerary.second_place_slave_purchase = interim.second_place_of_slave_purchase
    itinerary.third_place_slave_purchase = interim.third_place_of_slave_purchase
    itinerary.first_region_slave_emb = region(interim.first_place_of_slave_purchase)
    itinerary.second_region_slave_emb = region(interim.second_place_of_slave_purchase)
    itinerary.third_region_slave_emb = region(interim.third_place_of_slave_purchase)
    itinerary.port_of_call_before_atl_crossing = interim.place_of_call_before_atlantic_crossing
    itinerary.number_of_ports_of_call = interim.number_of_new_world_ports_called_prior_to_disembarkation
    itinerary.first_landing_place = interim.first_place_of_landing
    itinerary.second_landing_place = interim.second_place_of_landing
    itinerary.third_landing_place = interim.third_place_of_landing
    itinerary.first_landing_region = region(interim.first_place_of_landing)
    itinerary.second_landing_region = region(interim.second_place_of_landing)
    itinerary.third_landing_region = region(interim.third_place_of_landing)
    itinerary.place_voyage_ended = interim.port_voyage_ended
    itinerary.region_of_return = region(interim.port_voyage_ended)
    itinerary.broad_region_of_return = broad_region(interim.port_voyage_ended)
    itinerary.imp_port_voyage_begin = interim.imputed_port_where_voyage_began
    itinerary.imp_region_voyage_begin = interim.imputed_region_where_voyage_began
    itinerary.imp_broad_region_voyage_begin = broad_region(interim.imputed_port_where_voyage_began)
    itinerary.principal_place_of_slave_purchase = interim.principal_place_of_slave_purchase
    itinerary.imp_principal_place_of_slave_purchase = interim.imputed_principal_place_of_slave_purchase
    itinerary.imp_principal_region_of_slave_purchase = region(interim.imputed_principal_place_of_slave_purchase)
    itinerary.imp_broad_region_of_slave_purchase = broad_region(interim.imputed_principal_place_of_slave_purchase)
    itinerary.principal_port_of_slave_dis = interim.principal_place_of_slave_disembarkation
    itinerary.imp_principal_port_slave_dis = interim.imputed_principal_port_of_slave_disembarkation
    itinerary.imp_principal_region_slave_dis = region(interim.imputed_principal_port_of_slave_disembarkation)
    itinerary.imp_broad_region_slave_dis = broad_region(interim.imputed_principal_port_of_slave_disembarkation)
    itinerary.save()
    
    # Voyage dates.
    dates = VoyageDates()
    dates.voyage = voyage
    dates.save()
    
    # Voyage crew
    crew = VoyageCrew()
    crew.voyage = voyage
    crew.save()
    
    # Voyage slave numbers
    slaves_numbers = VoyageSlavesNumbers()
    slaves_numbers.voyage = voyage
    slaves_numbers.save()
    
    # Set voyage foreign keys (this is redundant, but we are keeping the original model design)
    voyage.voyage_ship = ship
    voyage.voyage_itinerary = itinerary
    voyage.voyage_dates = dates
    voyage.voyage_crew = crew
    voyage.voyage_slaves_numbers = slaves_numbers
    voyage.save()
    
    return voyage
    
def _publish_single_review_delete(review_request):
    pass
    
def _publish_single_review_merge(review_request):
    # Delete previous records and create a new one to replace them.
    pass
    
def _publish_single_review_new(review_request):
    pass
    
def _publish_single_review_update(review_request):
    pass