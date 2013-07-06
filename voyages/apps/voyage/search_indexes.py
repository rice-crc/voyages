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
class VoyageItineraryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    voyage_itinerary_ports_called_buying_slaves = indexes.IntegerField\
            (model_attr='ports_called_buying_slaves')
    voyage_itinerary_number_of_ports_of_call = indexes.IntegerField\
            (model_attr='number_of_ports_of_call')

    def get_model(self):
        return VoyageOutcome.OwnerOutcome

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


# Voyage Captain and Crew
class VoyageCaptainIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return VoyageCaptain

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class VoyageCrewIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    voyage_crew_crew_voyage_outset = indexes.IntegerField\
            (model_attr='crew_voyage_outset')
    voyage_crew_crew_departure_last_port = indexes.IntegerField\
            (model_attr='crew_departure_last_port')
    voyage_crew_crew_first_landing = indexes.IntegerField\
            (model_attr='crew_first_landing')
    voyage_crew_crew_return_begin = indexes.IntegerField\
            (model_attr='crew_return_begin')
    voyage_crew_crew_end_voyage = indexes.IntegerField\
            (model_attr='crew_end_voyage')
    voyage_crew_unspecified_crew = indexes.IntegerField\
            (model_attr='unspecified_crew')
    voyage_crew_crew_died_before_first_trade = indexes.IntegerField\
            (model_attr='crew_died_before_first_trade')
    voyage_crew_crew_died_while_ship_african = indexes.IntegerField\
            (model_attr='crew_died_while_ship_african')
    voyage_crew_crew_died_middle_passge = indexes.IntegerField\
            (model_attr='crew_died_middle_passge')
    voyage_crew_crew_died_in_americas = indexes.IntegerField\
            (model_attr='crew_died_in_americas')
    voyage_crew_crew_died_on_return_voyage = indexes.IntegerField\
            (model_attr='crew_died_on_return_voyage')
    voyage_crew_crew_died_complete_voyage = indexes.IntegerField\
            (model_attr='crew_died_complete_voyage')
    voyage_crew_crew_deserted = indexes.IntegerField\
            (model_attr='crew_deserted')

    def get_model(self):
        return VoyageCrew

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


# Voyage Slaves (numbers)
class VoyageSourcesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    voyage_sources_short_ref = indexes.CharField\
            (model_attr='short_ref')
    voyage_sources_full_ref = indexes.CharField\
            (model_attr='full_ref')

    def get_model(self):
        return VoyageSources

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()