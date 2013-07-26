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
    var_nationality = indexes.IntegerField()
    var_imputed_nationality = indexes.IntegerField()
    var_year_of_construction = indexes.IntegerField()
    var_registered_place = indexes.IntegerField()
    var_registered_year = indexes.IntegerField()
    var_rig_of_vessel = indexes.IntegerField()
    var_tonnage = indexes.IntegerField()
    var_tonnage_mod = indexes.IntegerField()
    var_guns_mounted = indexes.IntegerField()
    var_owner = indexes.CharField()

    # Captains and Owners
    var_captain = indexes.CharField()
    var_owner = indexes.CharField()
    voyage_ship_owner_name = indexes.CharField()

    # Voyage Ship
    voyage_ship_nationality_ship_value = indexes.InetegerField()
    voyage_ship_nationality_ship_label = indexes.CharField()
    voyage_ship_tonnage_value = indexes.IntegerField()
    voyage_ship_tonnage_label = indexes.CharField()
    voyage_ship_rig_of_vessel_value = indexes.IntegerField()
    voyage_ship_rig_of_vessel_label = indexes.CharField()
    voyage_ship_year_of_construction = indexes.IntegerField()

    var_outcome_voyage = indexes.IntegerField()
    var_outcome_slaves = indexes.IntegerField()
    var_outcome_owner = indexes.IntegerField()
    var_resistance = indexes.IntegerField()
    var_outcome_ship_captured = indexes.IntegerField()

    # Sources

    def get_model(self):
        return Voyage

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_var_ship_name(self, obj):
        return obj.voyage_ship.ship_name

    def prepare_var_nationality(self, obj):
        return obj.voyage_ship.nationality_ship.pk

    def prepare_var_imputed_nationality(self, obj):
        return obj.voyage_ship.nationality_ship.pk

    def prepare_var_vessel_construction_place(self, obj):
        return obj.voyage_ship.vessel_construction_place.pk

    def prepare_var_year_of_construction(self, obj):
        return obj.voyage_ship.year_of_construction

    def prepare_var_registered_place(self, obj):
        return obj.voyage_ship.registered_place.pk

    def prepare_var_registered_year(self, obj):
        return obj.voyage_ship.registered_year

    def prepare_var_var_rig_of_vessel(self, obj):
        return obj.voyage_ship.rig_of_vessel.pk

    def prepare_var_tonnage(self, obj):
        return obj.voyage_ship.tonnage

    def prepare_var_tonnage_mod(self, obj):
        return obj.voyage_ship.tonnage_mod

    def prepare_var_guns_mounted(self, obj):
        return obj.voyage_ship.guns_mounted

    def prepare_var_owner(self, obj):
        return [connection.owner.name for connection in VoyageShipOwnerConnection.objects.filter(voyage=obj)]

    def prepare_var_outcome_voyage(self, obj):
        return VoyageOutcome.objects.filter(voyage=obj)[0].particular_outcome.pk

    def prepare_var_outcome_slaves(self, obj):
        return VoyageOutcome.objects.filter(voyage=obj)[0].outcome_slaves.pk

    def prepare_var_outcome_owner(self, obj):
        return VoyageOutcome.objects.filter(voyage=obj)[0].outcome_owner.pk

    def prepare_var_resistance(self, obj):
        return VoyageOutcome.objects.filter(voyage=obj)[0].resistance.pk

    def prepare_var_outcome_ship_captured(self, obj):
        return VoyageOutcome.objects.filter(voyage=obj)[0].vessel_captured_outcome.pk
