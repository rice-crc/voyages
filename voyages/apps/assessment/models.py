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
    export_area = models.ForeignKey(ExportArea)


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
    import_area = models.ForeignKey(ImportArea)


class Nation(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    order_num = models.IntegerField()


class Estimate(models.Model):
    """
    Class represents Estimate entity
    """

    nation = models.ForeignKey(Nation)
    year = models.IntegerField(max_length=4)
    embarkation_region = models.ForeignKey(ExportRegion, null=True, blank=True)
    disembarkation_region = models.ForeignKey(ImportRegion, null=True, blank=True)
    embarked_slaves = models.FloatField(null=True, blank=True)
    disembarked_slaves = models.FloatField(null=True, blank=True)