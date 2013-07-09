from haystack import indexes
from .models import *


# Index for Voyage
class VoyageIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Index method for class Voyage.
    """

    voyage_in_cd_rom = indexes.BooleanField(model_attr="voyage_in_cd_rom")
    voyage_groupings_value = indexes.IntegerField()
    voyage_groupings_label = indexes.CharField()

    def get_model(self):
        return Voyage

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_voyage_groupings_value(self, obj):
        return obj.voyage_groupings.value

    def prepare_voyage_groupings_label(self, obj):
        return obj.voyage_groupings.label