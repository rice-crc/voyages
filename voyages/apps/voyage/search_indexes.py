from haystack import indexes
from .models import *


# Index for Voyage
class VoyageIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Index method for class Voyage.
    """
    text = indexes.CharField(document=True, use_template=True)

    var_voyage_id = indexes.IntegerField(model_attr='voyage_id', null=True)
    var_voyage_in_cd_rom = indexes.BooleanField(model_attr="voyage_in_cd_rom", null=True)
    var_ship_name = indexes.CharField(null=True)
    var_nationality = indexes.IntegerField(null=True)
    var_imputed_nationality = indexes.IntegerField(null=True)
    var_year_of_construction = indexes.IntegerField(null=True)
    var_registered_place = indexes.IntegerField(null=True)
    var_registered_year = indexes.IntegerField(null=True)
    var_rig_of_vessel = indexes.IntegerField(null=True)
    var_tonnage = indexes.IntegerField(null=True)
    var_tonnage_mod = indexes.IntegerField(null=True)
    var_guns_mounted = indexes.IntegerField(null=True)
    var_owner = indexes.CharField(null=True)

    # Captains and Owners
    var_captain = indexes.CharField(null=True)
    var_owner = indexes.CharField(null=True)
    voyage_ship_owner_name = indexes.CharField(null=True)

    # Voyage Ship
    voyage_ship_nationality_ship_value = indexes.IntegerField(null=True)
    voyage_ship_nationality_ship_label = indexes.CharField(null=True)
    voyage_ship_tonnage_value = indexes.IntegerField(null=True)
    voyage_ship_tonnage_label = indexes.CharField(null=True)
    voyage_ship_rig_of_vessel_value = indexes.IntegerField(null=True)
    voyage_ship_rig_of_vessel_label = indexes.CharField(null=True)
    voyage_ship_year_of_construction = indexes.IntegerField(null=True)

    var_outcome_voyage = indexes.CharField(null=True)
    var_outcome_slaves = indexes.CharField(null=True)
    var_outcome_owner = indexes.CharField(null=True)
    var_resistance = indexes.CharField(null=True)
    var_outcome_ship_captured = indexes.CharField(null=True)

    # Sources
    var_sources = indexes.MultiValueField(null=True)

    def get_model(self):
        return Voyage

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

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

    def prepare_var_port_of_departure(self, obj):
        try:
            return obj.voyage_itinerary.port_of_departure.place
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
            return obj.voyage_itinerary.var_place_voyage_ended.place
        except AttributeError:
            return None

    def prepare_var_imp_port_voyage_begin(self, obj):
        try:
            return obj.voyage_itinerary.imp_port_voyage_begin.place
        except AttributeError:
            return None

    def prepare_var_imp_principal_place_of_slave_purchase(self, obj):
        try:
            return obj.voyage_itinerary.imp_principal_place_of_slave_purchase.place
        except AttributeError:
            return None

    def prepare_var_imp_principal_port_slave_dis(self, obj):
        try:
            return obj.voyage_itinerary.imp_principal_port_slave_dis.place
        except AttributeError:
            return None

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
        return obj.voyage_sources