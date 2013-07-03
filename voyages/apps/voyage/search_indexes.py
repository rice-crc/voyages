from haystack import indexes
from .models import *

class BroadRegionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    broad_region_name = indexes.CharField(model_attr='question')
    broad_region_code = indexes.CharField(model_attr='code')

    def get_model(self):
        return BroadRegion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class RegionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    region_name = indexes.CharField(model_attr='question')
    region_code = indexes.CharField(model_attr='code')

    def get_model(self):
        return Region

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class PlaceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    place_name = indexes.CharField(model_attr='question')
    place_code = indexes.CharField(model_attr='code')

    def get_model(self):
        return Place

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()