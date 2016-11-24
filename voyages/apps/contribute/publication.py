from django.db import transaction
from voyages.apps.contribute.models import *
from voyages.apps.contribute.views import full_contribution_id, get_contribution_from_id, get_filtered_contributions
from voyages.apps.voyage.models import *

def publish_accepted_contributions(log_file):
    if log_file: log_file.write('Fetching contributions...')
    contribution_info = get_filtered_contributions({'status': ContributionStatus.approved})
    review_requests = []
    for info in contribution_info:
        reqs = list(ReviewRequest.objects.filter(contribution_id=full_contribution_id(info['type'], info['id']), archived=False))
        if len(reqs) != 1:
            raise Exception('Expected a single active review request for approved contributions')
        review_requests.append(reqs[0])
    if log_file: log_file.write('Publishing...\n')
    try:
        with transaction.atomic():
            count = 0
            for req in review_requests:
                # Basic validation.
                count += 1
                if log_file and count % 10 == 0:
                    log_file.write('Published ' + str(count) + ' voyages')
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
        if log_file: log_file.write('Finished all publications.\n')
    except Exception as exception:
        if log_file:
            log_file.write('An error occurred. Database transaction was rolledback\n')
            log_file.write(str(exception))
            import traceback
            log_file.write(traceback.format_exc())

def _delete_child_fk(obj, child_attr):
    child = getattr(obj, child_attr)
    if child:
        setattr(obj, child_attr, None)
        obj.save()
        child.delete()

def _save_editorial_version(review_request, contrib_type):
    editor_contribution = review_request.editor_contribution.first()
    if editor_contribution is None or editor_contribution.interim_voyage is None:
        raise Exception('This type of contribution requires an editor review interim voyage for publication')
    interim = editor_contribution.interim_voyage
    # Create or load a voyage with the appropriate voyage id.
    voyage = Voyage()
    contrib = get_contribution_from_id(review_request.contribution_id)
    contrib.status = ContributionStatus.published
    contrib.save()
    if contrib_type == 'merge' or contrib_type == 'new':
        if not review_request.created_voyage_id:
            raise Exception('For new or merged contributions, an explicit voyage_id must be set')
        voyage.voyage_id = review_request.created_voyage_id
    elif contrib_type == 'edit':
        voyage = Voyage.objects.get(voyage_id=contrib.edited_voyage_id)
    else:
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
    
    # Voyage Ship Owners
    def create_ship_owner(owner_name, order):
        owner = VoyageShipOwner()
        owner.name = owner_name
        owner.save()
        conn = VoyageShipOwnerConnection()
        conn.owner = owner
        conn.owner_order = order
        conn.voyage = voyage
        conn.save()
    
    if interim.first_ship_owner:
        create_ship_owner(interim.first_ship_owner, 1)
    if interim.second_ship_owner:
        create_ship_owner(interim.second_ship_owner, 2)
    if interim.additional_ship_owners:
        additional = interim.additional_ship_owners.split('\n')
        for index, owner in enumerate(additional):
            create_ship_owner(owner, index + 3)
            
    # Voyage Ship Captains
    def create_captain(name, order):
        captain = VoyageCaptain()
        captain.name = name
        captain.save()
        conn = VoyageCaptainConnection()
        conn.captain = captain
        conn.captain_order = order
        conn.voyage = voyage
        conn.save()
    
    if interim.first_captain:
        create_captain(interim.first_captain, 1)
    if interim.second_captain:
        create_captain(interim.second_captain, 2)
    if interim.third_captain:
        create_captain(interim.third_captain, 3)
    
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
    dates.voyage_began = interim.date_departure
    dates.slave_purchase_began = interim.date_slave_purchase_began
    dates.vessel_left_port = interim.date_vessel_left_last_slaving_port
    dates.first_dis_of_slaves = interim.date_first_slave_disembarkation
    #dates.date_departed_africa = interim.???  TODO: check this
    dates.arrival_at_second_place_landing = interim.date_second_slave_disembarkation
    dates.third_dis_of_slaves = interim.date_third_slave_disembarkation
    dates.departure_last_place_of_landing = interim.date_return_departure
    dates.voyage_completed = interim.date_voyage_completed
    dates.length_middle_passage_days = interim.length_of_middle_passage
    dates.imp_voyage_began = interim.imputed_year_voyage_began
    dates.imp_departed_africa = interim.imputed_year_departed_africa
    dates.imp_arrival_at_port_of_dis = interim.imputed_year_arrived_at_port_of_disembarkation
    dates.imp_length_home_to_disembark = interim.imputed_voyage_length_home_port_to_first_port_of_disembarkation
    dates.imp_length_leaving_africa_to_disembark = interim.imputed_length_of_middle_passage
    dates.save()
    
    numbers = {n.var_name.upper(): n.number for n in interim.slave_numbers.all()}
    
    # Voyage crew
    crew = VoyageCrew()
    crew.voyage = voyage
    crew.crew_voyage_outset = numbers.get('CREW1')
    crew.crew_departure_last_port = numbers.get('CREW2')
    crew.crew_first_landing = numbers.get('CREW3')
    crew.crew_return_begin = numbers.get('CREW4')
    crew.crew_end_voyage = numbers.get('CREW5')
    crew.unspecified_crew = numbers.get('CREW')
    crew.crew_died_before_first_trade = numbers.get('SAILD1')
    crew.crew_died_while_ship_african = numbers.get('SAILD2')
    crew.crew_died_middle_passage = numbers.get('SAILD3')
    crew.crew_died_in_americas = numbers.get('SAILD4')
    crew.crew_died_on_return_voyage = numbers.get('SAILD5')
    crew.crew_died_complete_voyage = numbers.get('CREWDIED')
    crew.crew_deserted = numbers.get('NDESERT')
    crew.save()
    
    # Voyage slave numbers
    slaves_numbers = VoyageSlavesNumbers()
    slaves_numbers.voyage = voyage
    slaves_numbers.slave_deaths_before_africa = numbers.get('SLADAFRI')
    slaves_numbers.slave_deaths_between_africa_america = numbers.get('SLADVOY')
    slaves_numbers.slave_deaths_between_arrival_and_sale = numbers.get('SLADAMER')
    slaves_numbers.num_slaves_intended_first_port = numbers.get('SLINTEND')
    slaves_numbers.num_slaves_intended_second_port = numbers.get('SLINTEN2')
    slaves_numbers.num_slaves_carried_first_port = numbers.get('NCAR13')
    slaves_numbers.num_slaves_carried_second_port = numbers.get('NCAR15')
    slaves_numbers.num_slaves_carried_third_port = numbers.get('NCAR17')
    slaves_numbers.total_num_slaves_purchased = numbers.get('TSLAVESP')
    slaves_numbers.total_num_slaves_dep_last_slaving_port = numbers.get('TSLAVESD')
    slaves_numbers.total_num_slaves_arr_first_port_embark = numbers.get('SLAARRIV')
    slaves_numbers.num_slaves_disembark_first_place = numbers.get('SLAS32')
    slaves_numbers.num_slaves_disembark_second_place = numbers.get('SLAS36')
    slaves_numbers.num_slaves_disembark_third_place = numbers.get('SLAS39')
    slaves_numbers.imp_total_num_slaves_embarked = numbers.get('SLAXIMP')
    slaves_numbers.imp_total_num_slaves_disembarked = numbers.get('SLAMIMP')
    slaves_numbers.imp_jamaican_cash_price = numbers.get('JAMCASPR')
    slaves_numbers.imp_mortality_during_voyage = numbers.get('VYMRTIMP')
    slaves_numbers.num_men_embark_first_port_purchase = numbers.get('MEN1')
    slaves_numbers.num_women_embark_first_port_purchase = numbers.get('WOMEN1')
    slaves_numbers.num_boy_embark_first_port_purchase = numbers.get('BOY1')
    slaves_numbers.num_girl_embark_first_port_purchase = numbers.get('GIRL1')
    slaves_numbers.num_adult_embark_first_port_purchase = numbers.get('ADULT1')
    slaves_numbers.num_child_embark_first_port_purchase = numbers.get('CHILD1')
    slaves_numbers.num_infant_embark_first_port_purchase = numbers.get('INFANT1')
    slaves_numbers.num_males_embark_first_port_purchase = numbers.get('MALE1')
    slaves_numbers.num_females_embark_first_port_purchase = numbers.get('FEMALE1')
    slaves_numbers.num_men_died_middle_passage = numbers.get('MEN2')
    slaves_numbers.num_women_died_middle_passage = numbers.get('WOMEN2')
    slaves_numbers.num_boy_died_middle_passage = numbers.get('BOY2')
    slaves_numbers.num_girl_died_middle_passage = numbers.get('GIRL2')
    slaves_numbers.num_adult_died_middle_passage = numbers.get('ADULT2')
    slaves_numbers.num_child_died_middle_passage = numbers.get('CHILD2')
    slaves_numbers.num_infant_died_middle_passage = numbers.get('INFANT2')
    slaves_numbers.num_males_died_middle_passage = numbers.get('MALE2')
    slaves_numbers.num_females_died_middle_passage = numbers.get('FEMALE2')
    slaves_numbers.num_men_disembark_first_landing = numbers.get('MEN3')
    slaves_numbers.num_women_disembark_first_landing = numbers.get('WOMEN3')
    slaves_numbers.num_boy_disembark_first_landing = numbers.get('BOY3')
    slaves_numbers.num_girl_disembark_first_landing = numbers.get('GIRL3')
    slaves_numbers.num_adult_disembark_first_landing = numbers.get('ADULT3')
    slaves_numbers.num_child_disembark_first_landing = numbers.get('CHILD3')
    slaves_numbers.num_infant_disembark_first_landing = numbers.get('INFANT3')
    slaves_numbers.num_males_disembark_first_landing = numbers.get('MALE3')
    slaves_numbers.num_females_disembark_first_landing = numbers.get('FEMALE3')
    slaves_numbers.num_men_embark_second_port_purchase = numbers.get('MEN4')
    slaves_numbers.num_women_embark_second_port_purchase = numbers.get('WOMEN4')
    slaves_numbers.num_boy_embark_second_port_purchase = numbers.get('BOY4')
    slaves_numbers.num_girl_embark_second_port_purchase = numbers.get('GIRL4')
    slaves_numbers.num_adult_embark_second_port_purchase = numbers.get('ADULT4')
    slaves_numbers.num_child_embark_second_port_purchase = numbers.get('CHILD4')
    slaves_numbers.num_infant_embark_second_port_purchase = numbers.get('INFANT4')
    slaves_numbers.num_males_embark_second_port_purchase = numbers.get('MALE4')
    slaves_numbers.num_females_embark_second_port_purchase = numbers.get('FEMALE4')
    slaves_numbers.num_men_embark_third_port_purchase = numbers.get('MEN5')
    slaves_numbers.num_women_embark_third_port_purchase = numbers.get('WOMEN5')
    slaves_numbers.num_boy_embark_third_port_purchase = numbers.get('BOY5')
    slaves_numbers.num_girl_embark_third_port_purchase = numbers.get('GIRL5')
    slaves_numbers.num_adult_embark_third_port_purchase = numbers.get('ADULT5')
    slaves_numbers.num_child_embark_third_port_purchase = numbers.get('CHILD5')
    slaves_numbers.num_infant_embark_third_port_purchase = numbers.get('INFANT5')
    slaves_numbers.num_males_embark_third_port_purchase = numbers.get('MALE5')
    slaves_numbers.num_females_embark_third_port_purchase = numbers.get('FEMALE5')
    slaves_numbers.num_men_disembark_second_landing = numbers.get('MEN6')
    slaves_numbers.num_women_disembark_second_landing = numbers.get('WOMEN6')
    slaves_numbers.num_boy_disembark_second_landing = numbers.get('BOY6')
    slaves_numbers.num_girl_disembark_second_landing = numbers.get('GIRL6')
    slaves_numbers.num_adult_disembark_second_landing = numbers.get('ADULT6')
    slaves_numbers.num_child_disembark_second_landing = numbers.get('CHILD6')
    slaves_numbers.num_infant_disembark_second_landing = numbers.get('INFANT6')
    slaves_numbers.num_males_disembark_second_landing = numbers.get('MALE6')
    slaves_numbers.num_females_disembark_second_landing = numbers.get('FEMALE6')
    slaves_numbers.imp_num_adult_embarked = numbers.get('ADLT1IMP')
    slaves_numbers.imp_num_children_embarked = numbers.get('CHIL1IMP')
    slaves_numbers.imp_num_male_embarked = numbers.get('MALE1IMP')
    slaves_numbers.imp_num_female_embarked = numbers.get('FEML1IMP')
    slaves_numbers.total_slaves_embarked_age_identified = numbers.get('SLAVEMA1')
    slaves_numbers.total_slaves_embarked_gender_identified = numbers.get('SLAVEMX1')
    slaves_numbers.imp_adult_death_middle_passage = numbers.get('ADLT2IMP')
    slaves_numbers.imp_child_death_middle_passage = numbers.get('CHIL2IMP')
    slaves_numbers.imp_male_death_middle_passage = numbers.get('MALE2IMP')
    slaves_numbers.imp_female_death_middle_passage = numbers.get('FEML2IMP')
    slaves_numbers.imp_num_adult_landed = numbers.get('ADLT3IMP')
    slaves_numbers.imp_num_child_landed = numbers.get('CHIL3IMP')
    slaves_numbers.imp_num_male_landed = numbers.get('MALE3IMP')
    slaves_numbers.imp_num_female_landed = numbers.get('FEML3IMP')
    slaves_numbers.total_slaves_landed_age_identified = numbers.get('SLAVEMA3')
    slaves_numbers.total_slaves_landed_gender_identified = numbers.get('SLAVEMX3')
    slaves_numbers.total_slaves_dept_or_arr_age_identified = numbers.get('SLAVEMA7')
    slaves_numbers.total_slaves_dept_or_arr_gender_identified = numbers.get('SLAVEMX7')
    slaves_numbers.imp_slaves_embarked_for_mortality = numbers.get('TSLMTIMP')
    slaves_numbers.imp_num_men_total = numbers.get('MEN7')
    slaves_numbers.imp_num_women_total = numbers.get('WOMEN7')
    slaves_numbers.imp_num_boy_total = numbers.get('BOY7')
    slaves_numbers.imp_num_girl_total = numbers.get('GIRL7')
    slaves_numbers.imp_num_adult_total = numbers.get('ADULT7')
    slaves_numbers.imp_num_child_total = numbers.get('CHILD7')
    slaves_numbers.imp_num_males_total = numbers.get('MALE7')
    slaves_numbers.imp_num_females_total = numbers.get('FEMALE7')
    slaves_numbers.save()
    
    # Voyage sources
    def create_source_connection(src, conn_ref, order):
        conn = VoyageSourcesConnection()
        conn.source = src
        conn.group = voyage
        conn.source_order = order
        conn.text_ref = conn_ref
        conn.save()
    
    def create_source_reference(short_ref, conn_ref, order):
        src = VoyageSources.objects.filter(short_ref=short_ref).first()
        if src is None:
            raise Exception('Source "' + short_ref + '" not found')
        create_source_connection(src, conn_ref, order)
    
    created_sources = list(interim.article_sources.all()) + list(interim.book_sources.all()) + \
        list(interim.newspaper_sources.all()) + list(interim.private_note_or_collection_sources.all()) + \
        list(interim.unpublished_secondary_sources.all()) + list(interim.primary_sources.all())
    pre_existing_sources = list(interim.pre_existing_sources.all())
    if contrib_type != 'edit' and contrib_type != 'merge' and len(pre_existing_sources) > 0:
        raise Exception('A contribution with type "' + contrib_type + '" cannot have pre existing sources')
    source_order = 1 # TODO: ask Dr. Eltis to see how we should order references
    for src in created_sources:
        # Each src here has as type a subclass of InterimContributedSource
        if not src.created_voyage_sources:
            raise Exception('Invalid state: a new source must have been created to match "' + src.source_ref_text + '"')
        create_source_connection(src.created_voyage_sources, src.source_ref_text, source_order)
        source_order += 1
    for src in pre_existing_sources:
        if src.action == InterimPreExistingSourceActions.exclude: continue
        create_source_reference(src.original_ref, src.full_ref, source_order)
        source_order += 1
    
    # Set voyage foreign keys (this is redundant, but we are keeping the original model design)
    voyage.voyage_ship = ship
    voyage.voyage_itinerary = itinerary
    voyage.voyage_dates = dates
    voyage.voyage_crew = crew
    voyage.voyage_slaves_numbers = slaves_numbers
    voyage.save()
    
    return voyage
    
def _delete_voyages(ids):
    delete_voyages = list(Voyage.objects.filter(voyage_id__in=ids))
    if len(ids) != len(delete_voyages):
        raise Exception("Voyage not found for deletion, voyage ids=" + str(ids))
    for v in delete_voyages:
        v.delete()
    
def _publish_single_review_delete(review_request):
    contribution = get_contribution_from_id(review_request.contribution_id)
    ids = list(contribution.get_related_voyage_ids())
    _delete_voyages(ids)
    
def _publish_single_review_merge(review_request):
    contribution = get_contribution_from_id(review_request.contribution_id)
    # Delete previous records and create a new one to replace them.
    ids = list(contribution.get_related_voyage_ids())
    _delete_voyages(ids)
    _save_editorial_version(review_request, 'merge')
    
def _publish_single_review_new(review_request):
    _save_editorial_version(review_request, 'new')
    
def _publish_single_review_update(review_request):
    _save_editorial_version(review_request, 'edit')