from haystack import indexes
from .models import *


# Index for Voyage
class VoyageIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Index method for class Voyage.
    """
    text = indexes.CharField(document=True, use_template=True)

    var_voyage_id = indexes.IntegerField(model_attr='voyage_id')
    var_voyage_in_cd_rom = indexes.BooleanField(model_attr="voyage_in_cd_rom")
    var_ship_name = indexes.CharField()
    var_nationality = indexes.CharField()
    var_imputed_nationality = indexes.CharField()
    var_year_of_construction = indexes.IntegerField()
    var_registered_place = indexes.CharField()
    var_registered_year = indexes.IntegerField()
    var_rig_of_vessel = indexes.CharField()
    var_tonnage = indexes.CharField()
    var_tonnage_mod = indexes.IntegerField()
    var_guns_mounted = indexes.IntegerField()
    ### Multi-value field
    var_owner = indexes.MultiValueField()

    # Voyage outcome
    var_outcome_voyage = indexes.CharField()
    var_outcome_slaves = indexes.CharField()
    var_outcome_owner = indexes.CharField()
    var_resistance = indexes.CharField()
    var_outcome_ship_captured = indexes.CharField()

    # Voyage itinerary
    var_port_of_departure = indexes.CharField()
    var_first_place_slave_purchase = indexes.CharField()
    var_second_place_slave_purchase = indexes.CharField()
    var_third_place_slave_purchase = indexes.CharField()
    var_principal_place_of_slave_purchase = indexes.CharField()
    var_port_of_call_before_atl_crossing = indexes.CharField()
    var_first_landing_place = indexes.CharField()
    var_second_landing_place = indexes.CharField()
    var_third_landing_place = indexes.CharField()
    var_principal_port_of_slave_dis = indexes.CharField()
    var_place_voyage_ended = indexes.CharField()
    var_imp_port_voyage_begin = indexes.CharField()
    var_imp_principal_place_of_slave_purchase = indexes.CharField()
    var_imp_principal_port_slave_dis = indexes.CharField()

    # Voyage dates
    # TO BE UPDATED

    # Captain and crew
    var_captain = indexes.MultiValueField()
    var_crew_voyage_outset = indexes.CharField()
    var_crew_first_landing = indexes.CharField()
    var_crew_died_complete_voyage = indexes.CharField()

    # Slave numbers
    var_num_slaves_carried_first_port = indexes.IntegerField()
    var_num_slaves_carried_second_port = indexes.IntegerField()
    var_num_slaves_carried_third_port = indexes.IntegerField()
    var_total_num_slaves_purchased = indexes.IntegerField()
    var_imp_total_num_slaves_purchased = indexes.IntegerField()
    var_total_num_slaves_arr_first_port_embark = indexes.IntegerField()
    var_num_slaves_disembark_first_place = indexes.IntegerField()
    var_second_place_of_landing = indexes.IntegerField()
    var_num_slaves_disembark_third_place = indexes.IntegerField()
    var_imp_total_slaves_disembarked = indexes.IntegerField()

    # Sources
    var_sources = indexes.MultiValueField()

    def get_model(self):
        return Voyage

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_var_ship_name(self, obj):
        return obj.voyage_ship.ship_name

    def prepare_var_nationality(self, obj):
        return obj.voyage_ship.nationality_ship.label

    def prepare_var_imputed_nationality(self, obj):
        return obj.voyage_ship.nationality_ship.label

    def prepare_var_vessel_construction_place(self, obj):
        return obj.voyage_ship.vessel_construction_place.place

    def prepare_var_year_of_construction(self, obj):
        return obj.voyage_ship.year_of_construction

    def prepare_var_registered_place(self, obj):
        return obj.voyage_ship.registered_place.place

    def prepare_var_registered_year(self, obj):
        return obj.voyage_ship.registered_year

    def prepare_var_var_rig_of_vessel(self, obj):
        return obj.voyage_ship.rig_of_vessel.label

    def prepare_var_tonnage(self, obj):
        return obj.voyage_ship.tonnage

    def prepare_var_tonnage_mod(self, obj):
        return obj.voyage_ship.tonnage_mod

    def prepare_var_guns_mounted(self, obj):
        return obj.voyage_ship.guns_mounted

    def prepare_var_owner(self, obj):
        return obj.voyage_ship_owner.name
        #return [connection.owner.name for connection in VoyageShipOwnerConnection.objects.filter(voyage=obj)]

    def prepare_var_outcome_voyage(self, obj):
        return VoyageOutcome.objects.filter(voyage=obj)[0].particular_outcome.label

    def prepare_var_outcome_slaves(self, obj):
        return VoyageOutcome.objects.filter(voyage=obj)[0].outcome_slaves.label

    def prepare_var_outcome_owner(self, obj):
        return VoyageOutcome.objects.filter(voyage=obj)[0].outcome_owner.label

    def prepare_var_resistance(self, obj):
        return VoyageOutcome.objects.filter(voyage=obj)[0].resistance.label

    def prepare_var_outcome_ship_captured(self, obj):
        return VoyageOutcome.objects.filter(voyage=obj)[0].vessel_captured_outcome.label

    def prepare_var_port_of_departure(self, obj):
        return obj.voyage_itinerary.port_of_departure

    def prepare_var_first_place_slave_purchase(self, obj):
        return obj.voyage_itinerary.first_place_slave_purchase.place

    def prepare_var_second_place_slave_purchase(self, obj):
        return obj.voyage_itinerary.second_place_slave_purchase.place

    def prepare_var_third_place_slave_purchase(self, obj):
        return obj.voyage_itinerary.third_place_slave_purchase.place

    def prepare_var_principal_place_of_slave_purchase(self, obj):
        return obj.voyage_itinerary.principal_place_of_slave_purchase.place

    def prepare_var_port_of_call_before_atl_crossing(self, obj):
        return obj.voyage_itinerary.port_of_call_before_atl_crossing.place

    def prepare_var_first_landing_place(self, obj):
        return obj.voyage_itinerary.first_landing_place.place

    def prepare_var_second_landing_place(self, obj):
        return obj.voyage_itinerary.second_landing_place.place

    def prepare_var_third_landing_place(self, obj):
        return obj.voyage_itinerary.third_landing_place.place

    def prepare_var_principal_port_of_slave_dis(self, obj):
        return obj.voyage_itinerary.principal_port_of_slave_dis.place

    def prepare_var_place_voyage_ended(self, obj):
        return obj.voyage_itinerary.var_place_voyage_ended.place

    def prepare_var_imp_port_voyage_begin(self, obj):
        return obj.voyage_itinerary.imp_port_voyage_begin.place

    def prepare_var_imp_principal_place_of_slave_purchase(self, obj):
        return obj.voyage_itinerary.imp_principal_place_of_slave_purchase.place

    def prepare_var_imp_principal_port_slave_dis(self, obj):
        return obj.voyage_itinerary.imp_principal_port_slave_dis.place

    def prepare_var_captain(self, obj):
        return [connection.captain.name for connection in VoyageCaptainConnection.objects.filter(voyage=obj)]

    def prepare_var_crew_voyage_outset(self, obj):
        return obj.voyage_crew.crew_voyage_outset

    def prepare_var_crew_first_landing(self, obj):
        return obj.voyage_crew.crew_first_landing

    def prepare_var_crew_died_complete_voyage(self, obj):
        return obj.voyage_crew.crew_died_complete_voyage

    def prepare_var_num_slaves_carried_first_port(self, obj):
        return obj.voyage_slaves_numbers.num_slaves_carried_first_port

    def prepare_var_num_slaves_carried_second_port(self, obj):
        return obj.voyage_slaves_numbers.num_slaves_carried_second_port

    def prepare_var_num_slaves_carried_third_port(self, obj):
        return obj.voyage_slaves_numbers.num_slaves_carried_third_port

    def prepare_var_total_num_slaves_purchased(self, obj):
        return obj.voyage_slaves_numbers.total_num_slaves_purchased

    def prepare_var_imp_total_num_slaves_purchased(self, obj):
        return obj.voyage_slaves_numbers.imp_total_num_slaves_purchased

    def prepare_var_total_num_slaves_arr_first_port_embark(self, obj):
        return obj.voyage_slaves_numbers.total_num_slaves_arr_first_port_embark

    def prepare_var_num_slaves_disembark_first_place(self, obj):
        return obj.voyage_slaves_numbers.num_slaves_disembark_first_place

    def prepare_var_second_place_of_landing(self, obj):
        return obj.voyage_slaves_numbers.second_place_of_landing

    def prepare_var_num_slaves_disembark_third_place(self, obj):
        return obj.voyage_slaves_numbers.var_num_slaves_disembark_third_place

    def prepare_var_imp_total_slaves_disembarked(self, obj):
        return obj.voyage_slaves_numbers.imp_total_slaves_disembarked

    def prepare_var_sources(self, obj):
        return [connection.captain.name for connection in VoyageSourcesConnection.objects.filter(voyage=obj)]
