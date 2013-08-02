from haystack import indexes
from .models import *

def getMonth(value):
    return value.split(",")[0]


def getDay(value):
    return value.split(",")[1]


def getYear(value):
    return value.split(",")[2]

# Index for Voyage
class VoyageIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Index method for class Voyage.
    """
    text = indexes.CharField(document=True, use_template=True)

    var_imp_voyage_began = indexes.IntegerField(null=True)

    var_voyage_id = indexes.IntegerField(model_attr='voyage_id', null=True)
    var_voyage_in_cd_rom = indexes.BooleanField(model_attr="voyage_in_cd_rom", null=True)
    var_ship_name = indexes.CharField(null=True)
    var_nationality = indexes.CharField(null=True)
    var_imputed_nationality = indexes.CharField(null=True)
    var_year_of_construction = indexes.IntegerField(null=True)
    var_registered_place = indexes.CharField(null=True)
    var_registered_year = indexes.IntegerField(null=True)
    var_rig_of_vessel = indexes.IntegerField(null=True)
    var_tonnage = indexes.FloatField(null=True)
    var_tonnage_mod = indexes.FloatField(null=True)
    var_guns_mounted = indexes.IntegerField(null=True)
    var_owner = indexes.MultiValueField(null=True)

    # Voyage Outcome
    var_outcome_voyage = indexes.CharField(null=True)
    var_outcome_slaves = indexes.CharField(null=True)
    var_outcome_ship_captured = indexes.CharField(null=True)
    var_outcome_owner = indexes.CharField(null=True)
    var_resistance = indexes.CharField(null=True)

    # Voyage itinerary
    var_imp_port_voyage_begin = indexes.CharField(null=True)
    var_first_place_slave_purchase = indexes.CharField(null=True)
    var_second_place_slave_purchase = indexes.CharField(null=True)
    var_third_place_slave_purchase = indexes.CharField(null=True)
    var_principal_place_of_slave_purchase = indexes.CharField(null=True)
    var_port_of_call_before_atl_crossing = indexes.CharField(null=True)
    var_first_landing_place = indexes.CharField(null=True)
    var_second_landing_place = indexes.CharField(null=True)
    var_third_landing_place = indexes.CharField(null=True)
    var_imp_principal_port_of_slave_dis = indexes.CharField(null=True)
    var_place_voyage_ended = indexes.CharField(null=True)

    ## Region variables
    var_imp_region_voyage_begin = indexes.CharField(null=True)
    var_first_region_slave_emb = indexes.CharField(null=True)
    var_second_region_slave_emb = indexes.CharField(null=True)
    var_third_region_slave_emb = indexes.CharField(null=True)
    var_imp_principal_region_of_slave_purchase = indexes.CharField(null=True)
    var_first_landing_region = indexes.CharField(null=True)
    var_second_landing_region = indexes.CharField(null=True)
    var_third_landing_region = indexes.CharField(null=True)
    var_imp_principal_region_slave_dis = indexes.CharField(null=True)
    var_region_voyage_ended = indexes.CharField(null=True)

    # Voyage captain and crew
    var_captain = indexes.MultiValueField(null=True)
    var_crew_voyage_outset = indexes.IntegerField(null=True)
    var_crew_first_landing = indexes.IntegerField(null=True)
    var_crew_died_complete_voyage = indexes.IntegerField(null=True)

    # Voyage dates
    var_imp_arrival_at_port_of_dis = indexes.IntegerField(null=True)
    var_voyage_began = indexes.DateField(null=True)
    var_slave_purchase_began = indexes.DateField(null=True)
    var_vessel_left_port = indexes.DateField(null=True)
    var_first_dis_of_slaves = indexes.DateField(null=True)
    var_departure_last_place_of_landing = indexes.DateField(null=True)
    var_voyage_completed = indexes.DateField(null=True)

    var_imp_length_home_to_disembark = indexes.IntegerField(null=True)
    var_length_middle_passage_days = indexes.IntegerField(null=True)

    # Voyage numbers
    var_num_slaves_carried_first_port = indexes.IntegerField(null=True)
    var_num_slaves_carried_second_port = indexes.IntegerField(null=True)
    var_num_slaves_carried_third_port = indexes.IntegerField(null=True)
    var_total_num_slaves_purchased = indexes.IntegerField(null=True)
    var_imp_total_num_slaves_purchased = indexes.IntegerField(null=True)
    var_total_num_slaves_arr_first_port_embark = indexes.IntegerField(null=True)
    var_num_slaves_disembark_first_place = indexes.IntegerField(null=True)
    var_num_slaves_disembark_second_place = indexes.IntegerField(null=True)
    var_num_slaves_disembark_third_place = indexes.IntegerField(null=True)
    var_imp_total_slaves_disembarked = indexes.IntegerField(null=True)

    # Voyage characteristics
    var_imputed_percentage_men = indexes.FloatField(null=True)
    var_imputed_percentage_women = indexes.FloatField(null=True)
    var_imputed_percentage_boys = indexes.FloatField(null=True)
    var_imputed_percentage_girls = indexes.FloatField(null=True)
    var_imputed_percentage_female = indexes.FloatField(null=True)
    var_imputed_percentage_male = indexes.FloatField(null=True)
    var_imputed_percentage_child = indexes.FloatField(null=True)
    var_imputed_sterling_cash = indexes.FloatField(null=True)
    var_imputed_death_middle_passage = indexes.IntegerField(null=True)
    var_imputed_mortality = indexes.FloatField(null=True)

    # Sources
    var_sources = indexes.MultiValueField(null=True)

    def get_model(self):
        return Voyage

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_var_imp_voyage_began(self, obj):
        try:
            return getYear(obj.voyage_dates.imp_voyage_began)
        except AttributeError, TypeError:
            return None

    def prepare_var_ship_name(self, obj):
        try:
            return obj.voyage_ship.ship_name
        except AttributeError:
            return None

    def prepare_var_nationality(self, obj):
        try:
            return obj.voyage_ship.nationality_ship.label
        except AttributeError:
            return None

    def prepare_var_imputed_nationality(self, obj):
        try:
            return obj.voyage_ship.nationality_ship.label
        except AttributeError:
            return None

    def prepare_var_vessel_construction_place(self, obj):
        try:
            return obj.voyage_ship.vessel_construction_place.place
        except AttributeError:
            return None

    def prepare_var_year_of_construction(self, obj):
        try:
            return obj.voyage_ship.year_of_construction
        except AttributeError:
            return None

    def prepare_var_registered_place(self, obj):
        try:
            return obj.voyage_ship.registered_place.place
        except AttributeError:
            return None

    def prepare_var_registered_year(self, obj):
        try:
            return obj.voyage_ship.registered_year
        except AttributeError:
            return None

    def prepare_var_var_rig_of_vessel(self, obj):
        try:
            return obj.voyage_ship.rig_of_vessel.label
        except AttributeError:
            return None

    def prepare_var_tonnage(self, obj):
        try:
            return obj.voyage_ship.tonnage
        except AttributeError:
            return None

    def prepare_var_tonnage_mod(self, obj):
        try:
            return obj.voyage_ship.tonnage_mod
        except AttributeError:
            return None

    def prepare_var_guns_mounted(self, obj):
        try:
            return obj.voyage_ship.guns_mounted
        except AttributeError:
            return None

    def prepare_var_owner(self, obj):
        try:
            return [connection.owner.name for connection in VoyageShipOwnerConnection.objects.filter(voyage=obj)]
        except AttributeError:
            return None

    def prepare_var_outcome_voyage(self, obj):
        try:
            return VoyageOutcome.objects.filter(voyage=obj)[0].particular_outcome.label
        except AttributeError:
            return None
        except IndexError:
            return None

    def prepare_var_outcome_slaves(self, obj):
        try:
            return VoyageOutcome.objects.filter(voyage=obj)[0].outcome_slaves.label
        except AttributeError:
            return None
        except IndexError:
            return None

    def prepare_var_outcome_owner(self, obj):
        try:
            return VoyageOutcome.objects.filter(voyage=obj)[0].outcome_owner.label
        except AttributeError:
            return None
        except IndexError:
            return None

    def prepare_var_resistance(self, obj):
        try:
            return VoyageOutcome.objects.filter(voyage=obj)[0].resistance.label
        except AttributeError:
            return None
        except IndexError:
            return None

    def prepare_var_outcome_ship_captured(self, obj):
        try:
            return VoyageOutcome.objects.filter(voyage=obj)[0].vessel_captured_outcome.label
        except AttributeError:
            return None
        except IndexError:
            return None

    def prepare_var_imp_principal_place_of_slave_purchase(self, obj):
        try:
            return obj.voyage_itinerary.imp_principal_place_of_slave_purchase.place
        except AttributeError:
            return None

    def prepare_var_imp_port_voyage_begin(self, obj):
        try:
            return obj.voyage_itinerary.imp_port_voyage_begin.place
        except AttributeError:
            return None

    def prepare_var_first_place_slave_purchase(self, obj):
        try:
            return obj.voyage_itinerary.first_place_slave_purchase.place
        except AttributeError:
            return None

    def prepare_var_second_place_slave_purchase(self, obj):
        try:
            return obj.voyage_itinerary.second_place_slave_purchase.place
        except AttributeError:
            return None

    def prepare_var_third_place_slave_purchase(self, obj):
        try:
            return obj.voyage_itinerary.third_place_slave_purchase.place
        except AttributeError:
            return None

    def prepare_var_principal_place_of_slave_purchase(self, obj):
        try:
            return obj.voyage_itinerary.principal_place_of_slave_purchase.place
        except AttributeError:
            return None

    def prepare_var_port_of_call_before_atl_crossing(self, obj):
        try:
            return obj.voyage_itinerary.port_of_call_before_atl_crossing.place
        except AttributeError:
            return None

    def prepare_var_first_landing_place(self, obj):
        try:
            return obj.voyage_itinerary.first_landing_place.place
        except AttributeError:
            return None

    def prepare_var_second_landing_place(self, obj):
        try:
            return obj.voyage_itinerary.second_landing_place.place
        except AttributeError:
            return None

    def prepare_var_third_landing_place(self, obj):
        try:
            return obj.voyage_itinerary.third_landing_place.place
        except AttributeError:
            return None

    def prepare_var_principal_port_of_slave_dis(self, obj):
        try:
            return obj.voyage_itinerary.principal_port_of_slave_dis.place
        except AttributeError:
            return None

    def prepare_var_place_voyage_ended(self, obj):
        try:
            return obj.voyage_itinerary.place_voyage_ended.place
        except AttributeError:
            return None

    def prepare_var_imp_region_voyage_begin(self, obj):
        try:
            return obj.voyage_itineraryimp_region_voyage_begin.region
        except AttributeError:
            return None

    def prepare_var_first_region_slave_emb(self, obj):
        try:
            return obj.voyage_itinerary.principal_place_of_slave_purchase.region.region
        except AttributeError:
            return None
        except IndexError:
            return None

    def prepare_var_second_region_slave_emb(self, obj):
        try:
            return obj.voyage_itinerary.second_region_emb.region
        except AttributeError:
            return None

    def prepare_var_third_region_slave_emb(self, obj):
        try:
            return obj.voyage_itinerary.third_region_emb.region
        except AttributeError:
            return None

    def prepare_var_imp_principal_place_of_slave_purchase(self, obj):
        try:
            return obj.voyage_itinerary.imp_principal_place_of_slave_purchase.place
        except AttributeError:
            return None

    def prepare_var_first_landing_region(self, obj):
        try:
            return obj.voyage_itinerary.first_landing_region.region
        except AttributeError:
            return None

    def prepare_var_second_landing_region(self, obj):
        try:
            return obj.voyage_itinerary.second_landing_region.region
        except AttributeError:
            return None

    def prepare_var_third_landing_region(self, obj):
        try:
            return obj.voyage_itinerary.third_landing_region.region
        except AttributeError:
            return None

    def prepare_var_imp_principal_port_slave_dis(self, obj):
        try:
            return obj.voyage_itinerary.imp_principal_port_slave_dis.place
        except AttributeError:
            return None

    def prepare_var_region_voyage_ended(self, obj):
        try:
            return obj.voyage_itinerary.place_voyage_ended.region.region
        except AttributeError:
            return None

    # Voyage dates
    def prepare_var_imp_arrival_at_port_of_dis(self, obj):
        try:
            return int(getYear(obj.voyage_dates.imp_arrival_at_port_of_dis))
        except AttributeError, TypeError:
            return None

    def prepare_var_voyage_began(self, obj):
        return None

    def prepare_var_slave_purchase_began(self, obj):
        return None

    def prepare_var_vessel_left_port(self, obj):
        return None

    def prepare_var_first_dis_of_slaves(self, obj):
        return None

    def prepare_var_departure_last_place_of_landing(self, obj):
        return None

    def prepare_var_voyage_completed(self, obj):
        return None

    def prepare_var_imp_length_home_to_disembark(self, obj):
        try:
            return obj.voyage_dates.imp_length_home_to_disembark
        except AttributeError:
            return None

    def prepare_var_length_middle_passage_days(self, obj):
        try:
            return obj.voyage_dates.length_middle_passage_days
        except AttributeError:
            return None

    # Voyage number
    def prepare_var_num_slaves_carried_first_port(self, obj):
        try:
            return obj.voyage_slaves_numbers.num_slaves_carried_first_port
        except AttributeError:
            return None

    def prepare_var_num_slaves_carried_second_port(self, obj):
        try:
            return obj.voyage_slaves_numbers.num_slaves_carried_second_port
        except AttributeError:
            return None

    def prepare_var_num_slaves_carried_third_port(self, obj):
        try:
            return obj.voyage_slaves_numbers.num_slaves_carried_third_port
        except AttributeError:
            return None

    def prepare_var_total_num_slaves_purchased(self, obj):
        try:
            return obj.voyage_slaves_numbers.total_num_slaves_purchased
        except AttributeError:
            return None

    def prepare_var_imp_total_num_slaves_purchased(self, obj):
        try:
        # To be corrected
            return obj.voyage_slaves_numbers.total_num_slaves_purchased
        except AttributeError:
            return None

    def prepare_var_total_num_slaves_arr_first_port_embark(self, obj):
        try:
            return obj.voyage_slaves_numbers.total_num_slaves_arr_first_port_embark
        except AttributeError:
            return None

    def prepare_var_num_slaves_disembark_first_place(self, obj):
        try:
            return obj.voyage_slaves_numbers.num_slaves_disembark_first_place
        except AttributeError:
            return None

    def prepare_var_num_slaves_disembark_second_place(self, obj):
        try:
            return obj.voyage_slaves_numbers.num_slaves_disembark_second_place
        except AttributeError:
            return None

    def prepare_var_num_slaves_disembark_third_place(self, obj):
        try:
            return obj.voyage_slaves_numbers.num_slaves_disembark_third_place
        except AttributeError:
            return None

    def prepare_var_imp_total_slaves_disembarked(self, obj):
        return None

    # Voyage characteristics
    def prepare_var_imputed_percentage_men(self, obj):
        return None

    def prepare_var_imputed_percentage_women(self, obj):
        return None

    def prepare_var_imputed_percentage_boys(self, obj):
        return None

    def prepare_var_imputed_percentage_girls(self, obj):
        return None

    def prepare_var_imputed_percentage_female(self, obj):
        return None

    def prepare_var_imputed_percentage_male(self, obj):
        return None

    def prepare_var_imputed_percentage_child(self, obj):
        return None

    def prepare_var_imputed_sterling_cash(self, obj):
        return None

    def prepare_var_imputed_death_middle_passage(self, obj):
        return None

    def prepare_var_imputed_mortality(self, obj):
        return None

    # Voyage crew
    def prepare_var_captain(self, obj):
        return [connection.captain.name for connection in VoyageCaptainConnection.objects.filter(voyage=obj)]

    def prepare_var_crew_voyage_outset(self, obj):
        try:
            return obj.voyage_crew.crew_voyage_outset
        except AttributeError:
            return None

    def prepare_var_crew_first_landing(self, obj):
        try:
            return obj.voyage_crew.crew_first_landing
        except AttributeError:
            return None

    def prepare_var_crew_died_complete_voyage(self, obj):
        try:
            return obj.voyage_crew.crew_died_complete_voyage
        except AttributeError:
            return None

    # Voyage sources
    def prepare_var_sources(self, obj):
        result = []
        for connection in VoyageSourcesConnection.objects.filter(group=obj):
            result.append(connection.text_ref)
            result.append(connection.source.full_ref)
        return result