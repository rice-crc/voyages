from __future__ import unicode_literals

from haystack import indexes

from .models import (Estimate, ExportArea, ExportRegion, ImportArea,
                     ImportRegion, Nation)


class ExportAreaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")
    order_num = indexes.IntegerField(model_attr="order_num")
    latitude = indexes.FloatField(model_attr="latitude")
    longitude = indexes.FloatField(model_attr="longitude")
    show_at_zoom = indexes.IntegerField(model_attr="show_at_zoom")
    show_on_map = indexes.BooleanField(model_attr="show_at_zoom")

    def get_model(self):
        return ExportArea


class ExportRegionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")
    order_num = indexes.IntegerField(model_attr="order_num")
    latitude = indexes.FloatField(model_attr="latitude")
    longitude = indexes.FloatField(model_attr="longitude")
    show_at_zoom = indexes.IntegerField(model_attr="show_at_zoom")
    show_on_map = indexes.BooleanField(model_attr="show_at_zoom")
    export_area = indexes.CharField()

    def get_model(self):
        return ExportRegion

    def prepare_export_area(self, obj):
        if obj.export_area:
            return obj.export_area.name
        return None


class ImportAreaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")
    order_num = indexes.IntegerField(model_attr="order_num")
    latitude = indexes.FloatField(model_attr="latitude")
    longitude = indexes.FloatField(model_attr="longitude")
    show_at_zoom = indexes.IntegerField(model_attr="show_at_zoom")
    show_on_map = indexes.BooleanField(model_attr="show_at_zoom")

    def get_model(self):
        return ImportArea


class ImportRegionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")
    order_num = indexes.IntegerField(model_attr="order_num")
    latitude = indexes.FloatField(model_attr="latitude")
    longitude = indexes.FloatField(model_attr="longitude")
    show_at_zoom = indexes.IntegerField(model_attr="show_at_zoom")
    show_on_map = indexes.BooleanField(model_attr="show_at_zoom")
    import_area = indexes.CharField()

    def get_model(self):
        return ImportRegion

    def prepare_import_area(self, obj):
        if obj.import_area:
            return obj.import_area.name
        return None


class NationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")
    order_num = indexes.CharField(model_attr="order_num")

    def get_model(self):
        return Nation


class EstimateIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    year = indexes.IntegerField(model_attr="year")
    embarked_slaves = indexes.FloatField(model_attr="embarked_slaves")
    disembarked_slaves = indexes.FloatField(model_attr="disembarked_slaves")
    nation = indexes.CharField()
    embarkation_region = indexes.CharField()
    disembarkation_region = indexes.CharField()
    broad_disembarkation_region = indexes.CharField()

    def get_model(self):
        return Estimate

    def prepare_nation(self, obj):
        if obj.nation:
            return obj.nation.name
        return None

    def prepare_embarkation_region(self, obj):
        if obj.embarkation_region:
            return obj.embarkation_region.name
        return None

    def prepare_disembarkation_region(self, obj):
        if obj.disembarkation_region:
            return obj.disembarkation_region.name
        return None

    def prepare_broad_disembarkation_region(self, obj):
        if obj.disembarkation_region and obj.disembarkation_region.import_area:
            return obj.disembarkation_region.import_area.name
        return None
