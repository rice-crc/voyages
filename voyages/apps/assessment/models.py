from __future__ import unicode_literals

import threading
from builtins import str
from itertools import groupby

from django.db import models


class ExportArea(models.Model):
    """
    Class represents Export area entity.
    """

    name = models.CharField(max_length=200, verbose_name="Export area name")
    order_num = models.IntegerField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    show_at_zoom = models.IntegerField()
    show_on_map = models.BooleanField()

    def __lt__(self, other):
        return (self.name, self.order_num) < (other.name, other.order_num)

    def __unicode__(self):
        return self.name


class ExportRegion(models.Model):
    """
    Class represents Export region entity.
    """

    name = models.CharField(max_length=200, verbose_name="Export region name")
    order_num = models.IntegerField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    show_at_zoom = models.IntegerField()
    show_on_map = models.BooleanField()
    export_area = models.ForeignKey(ExportArea, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name


class ImportArea(models.Model):
    """
    Class represents Import area entity.
    """

    name = models.CharField(max_length=200, verbose_name="Import area name")
    order_num = models.IntegerField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    show_at_zoom = models.IntegerField()
    show_on_map = models.BooleanField()

    def __unicode__(self):
        return self.name

    def __lt__(self, other):
        return (self.name, self.order_num) < (other.name, other.order_num)


class ImportRegion(models.Model):
    """
    Class represents Import region entity.
    """

    name = models.CharField(max_length=200, verbose_name="Import region name")
    order_num = models.IntegerField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    show_at_zoom = models.IntegerField()
    show_on_map = models.BooleanField()
    import_area = models.ForeignKey(ImportArea, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name


class Nation(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    order_num = models.IntegerField()

    def __unicode__(self):
        return self.name


class Estimate(models.Model):
    """
    Class represents Estimate entity
    """

    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
    year = models.IntegerField()
    embarkation_region = models.ForeignKey(
        ExportRegion, null=True, blank=True, on_delete=models.CASCADE)
    disembarkation_region = models.ForeignKey(
        ImportRegion, null=True, blank=True, on_delete=models.CASCADE)
    embarked_slaves = models.FloatField(null=True, blank=True)
    disembarked_slaves = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return str(self.id)


class EstimateManager(models.Manager):
    estimates = {}
    export_areas = {}
    import_areas = {}
    export_regions = {}
    import_regions = {}
    nations = {}

    export_hierarchy = {}
    import_hierarchy = {}

    _has_loaded = False
    _lock = threading.Lock()

    @classmethod
    def cache(cls):
        with cls._lock:
            if not cls._has_loaded:
                cls._has_loaded = True
                cls.export_areas = {a.pk: a for a in ExportArea.objects.all()}
                cls.import_areas = {a.pk: a for a in ImportArea.objects.all()}

                def extract_export_region(r):
                    r.export_area = cls.export_areas[r.export_area_id]
                    return r

                cls.export_regions = {
                    r.pk: extract_export_region(r)
                    for r in ExportRegion.objects.all()
                }

                def extract_import_region(r):
                    r.import_area = cls.import_areas[r.import_area_id]
                    return r

                cls.import_regions = {
                    r.pk: extract_import_region(r)
                    for r in ImportRegion.objects.all()
                }

                # Build hierarchies
                def exp_key(r):
                    return r.export_area

                sorted_regions = sorted(list(cls.export_regions.values()),
                                        key=exp_key)
                cls.export_hierarchy = {
                    k: list(g) for k, g in groupby(sorted_regions, key=exp_key)
                }

                def imp_key(r):
                    return r.import_area

                sorted_regions = sorted(list(cls.import_regions.values()),
                                        key=imp_key)
                cls.import_hierarchy = {
                    k: list(g) for k, g in groupby(sorted_regions, key=imp_key)
                }

                cls.nations = {n.pk: n for n in Nation.objects.all()}

                def extract_estimate(e):
                    e.nation = cls.nations[e.nation_id]
                    e.embarkation_region = cls.export_regions[
                        e.embarkation_region_id]
                    e.disembarkation_region = cls.import_regions[
                        e.disembarkation_region_id]
                    return e

                cls.estimates = {
                    e.pk: extract_estimate(e) for e in Estimate.objects.all()
                }
        return cls.estimates
