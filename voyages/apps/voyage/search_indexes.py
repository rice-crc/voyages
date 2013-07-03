from haystack import indexes
from .models import *


# Voyage Regions and Places
class BroadRegionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    broad_region_name = indexes.CharField(model_attr='question')
    broad_region_code = indexes.IntegerField(model_attr='code')

    def get_model(self):
        return BroadRegion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class RegionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    region_name = indexes.CharField(model_attr='question')
    region_code = indexes.IntegerField(model_attr='code')

    def get_model(self):
        return Region

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class PlaceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    place_name = indexes.CharField(model_attr='question')
    place_code = indexes.IntegerField(model_attr='code')

    def get_model(self):
        return Place

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


# Voyage Groupings
class VoyageGroupingsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    voyage_groupings_value = indexes.CharField(model_attr='value')
    voyage_groupings_label = indexes.IntegerField(model_attr='label')

    def get_model(self):
        return VoyageGroupings

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


# Voyage Ship, Nation, Owners
class VoyageShipIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    voyage_ship_ship_name = indexes.CharField(model_attr='ship_name')
    voyage_ship_tonnage = indexes.IntegerField(model_attr='tonnage')
    voyage_ship_guns_mounted = indexes.IntegerField(model_attr='guns_mounted')
    voyage_ship_year_of_construction = indexes.IntegerField\
            (model_attr='year_of_construction')
    voyage_ship_registered_year = indexes.IntegerField\
            (model_attr='registered_year')
    voyage_ship_tonnage_mod = indexes.DecimalField(model_attr='tonnage_mod')

    def get_model(self):
        return VoyageShip

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class NationalityIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    nationality_nationality = indexes.CharField(model_attr='nationality')
    nationality_code = indexes.IntegerField(model_attr='code')

    def get_model(self):
        return VoyageShip.Nationality

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class TonTypeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    ton_type_ton_type = indexes.CharField(model_attr='ton_type')
    ton_type_code = indexes.IntegerField(model_attr='code')

    def get_model(self):
        return VoyageShip.TonType

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class RigOfVesselIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    rig_of_vessel_rig_of_vessel = indexes.CharField(model_attr='rig_of_vessel')
    rig_of_vessel_code = indexes.IntegerField(model_attr='code')

    def get_model(self):
        return VoyageShip.RigOfVessel

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class VoyageShipOwnerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    voyage_ship_owner_name = indexes.CharField(model_attr='name')

    def get_model(self):
        return VoyageShipOwner

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


# Voyage Outcome
class VoyageParticularOutcomeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    voyage_particular_outcome_name = indexes.CharField(model_attr='name')
    voyage_particular_outcome_code = indexes.IntegerField(model_attr='code')

    def get_model(self):
        return VoyageOutcome.ParticularOutcome

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class VoyageSlavesOutcomeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    voyage_particular_outcome_name = indexes.CharField(model_attr='name')
    voyage_particular_outcome_code = indexes.IntegerField(model_attr='code')

    def get_model(self):
        return VoyageOutcome.SlavesOutcome

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class VoyageVesselCapturedOutcomeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    voyage_vessel_captured_outcome_name = indexes.CharField(model_attr='name')
    voyage_vessel_captured_outcome_code = indexes.IntegerField\
            (model_attr='code')

    def get_model(self):
        return VoyageOutcome.VesselCapturedOutcome

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class VoyageOwnerOutcomeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    voyage_owner_outcome_name = indexes.CharField(model_attr='name')
    voyage_owner_outcome_code = indexes.IntegerField\
            (model_attr='code')

    def get_model(self):
        return VoyageOutcome.OwnerOutcome

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class VoyageResistanceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    resistance_name = indexes.CharField(model_attr='name')
    resistance_code = indexes.IntegerField\
            (model_attr='code')

    def get_model(self):
        return VoyageOutcome.Resistance

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


# Voyage Itinerary
