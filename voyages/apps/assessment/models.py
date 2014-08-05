from django.db import models


class ExportArea(models.Model):
    """
    Class represents Export area entity.
    """

    area_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200, verbose_name="Export area name")
    order_num = models.IntegerField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    show_at_zoom = models.IntegerField()
    show_on_map = models.BooleanField()


class ExportRegion(models.Model):
    """
    Class represents Export region entity.
    """
    region_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200, verbose_name="Export region name")
    order_num = models.IntegerField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    show_at_zoom = models.IntegerField()
    show_on_map = models.BooleanField()


class ImportArea(models.Model):
    """
    Class represents Import area entity.
    """
    area_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200, verbose_name="Import area name")
    order_num = models.IntegerField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    show_at_zoom = models.IntegerField()
    show_on_map = models.BooleanField()


class ImportRegion(models.Model):
    """
    Class represents Import region entity.
    """
    region_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200, verbose_name="Import region name")
    order_num = models.IntegerField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    show_at_zoom = models.IntegerField()
    show_on_map = models.BooleanField()