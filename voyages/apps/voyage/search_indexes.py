from haystack import indexes
from .models import *


# Index for Voyage
# class VoyageIndex(indexes.SearchIndex, indexes.Indexable):
#     """
#     Index method for class Voyage.
#     """

    # voyage_in_cd_rom = indexes.BooleanField(model_attr="voyage_in_cd_rom")
    # # Groupings
    # voyage_groupings_value = indexes.IntegerField()
    # voyage_groupings_label = indexes.CharField()
    #
    # # Captains and Owners
    # voyage_captain_name = indexes.CharField()
    # voyage_ship_owner_name = indexes.CharField()
    #
    # # Voyage Ship
    # voyage_ship_ship_name = indexes.CharField
    # voyage_ship_nationality_ship_value = indexes.IntegerField()
    # voyage_ship_nationality_ship_label = indexes.CharField()
    # voyage_ship_tonnage_value = indexes.IntegerField()
    # voyage_ship_tonnage_label = indexes.CharField()
    # voyage_ship_rig_of_vessel_value = indexes.IntegerField()
    # voyage_ship_rig_of_vessel_label = indexes.CharField()
    # voyage_ship_year_of_construction = indexes.IntegerField()
    #
    #
    # def get_model(self):
    #     return Voyage
    #
    # def index_queryset(self, using=None):
    #     """Used when the entire index for model is updated."""
    #     return self.get_model().objects.all()
    #
    # def prepare_voyage_groupings_value(self, obj):
    #     return obj.voyage_groupings.value
    #
    # def prepare_voyage_groupings_label(self, obj):
    #     return obj.voyage_groupings.label
    #
    # def prepare_voyage_captain_name(self, obj):
    #     return obj.voyage_captain_name
    #
    # def prepare_voyage_ship_owner_name(self, obj):
    #     return obj.voyage_ship_owner_name