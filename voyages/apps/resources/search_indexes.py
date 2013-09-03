from haystack import indexes
from .models import Image
from __future__ import division


class ImagesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    imgtext = indexes.NgramField(use_template=True)
    file = indexes.CharField(model_attr="file")
    ready_to_go = indexes.BooleanField(model_attr="ready_to_go", default=False)
    date = indexes.IntegerField(model_attr="date", null=True)
    language = indexes.CharField(model_attr="language", null=True)
    title = indexes.CharField(model_attr="title")
    description = indexes.CharField(model_attr="description", null=True)
    source = indexes.CharField(model_attr="source", null=True)
    category_label = indexes.CharField()
    voyage_id = indexes.IntegerField(null=True)
    voyage_vessel_name = indexes.CharField(null=True)
    voyage_imp_voyage_began = indexes.CharField(null=True)
    voyage_year = indexes.CharField(null=True)

    def get_model(self):
        return Image

    def prepare_category_label(self, obj):
        return obj.category.label

    def prepare_voyage_id(self, obj):
        if obj.voyage is not None:
            return obj.voyage.voyage_id
        else:
            return None

    def prepare_voyage_vessel_name(self, obj):
        if obj.voyage is not None:
            return obj.voyage.voyage_ship.ship_name
        else:
            return None

    def prepare_voyage_imp_voyage_began(self, obj):
        if obj.voyage is not None:
            return obj.voyage.voyage_dates.imp_voyage_began
        else:
            return None

    def prepare_voyage_year(self, obj):
        if obj.voyage is not None:
            return obj.voyage.voyage_dates.imp_voyage_began
        else:
            return None

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
