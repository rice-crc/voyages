from __future__ import unicode_literals

from builtins import str
from os.path import basename
from django.db import models

from voyages.apps.voyage.models import Place, Voyage


class Image(models.Model):
    """
    Model to store information about image.
    """

    file = models.ImageField(upload_to='images')
    title = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=2000, default="")
    creator = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=2, null=True, blank=True)
    source = models.CharField(max_length=500, null=True, blank=True)

    ready_to_go = models.BooleanField(default=False)
    order_num = models.IntegerField('Code value', null=True, blank=True)

    date = models.IntegerField('Date(Year YYYY)', null=True, blank=True)

    # Category
    category = models.ForeignKey(
        'ImageCategory', verbose_name="Image category",
        on_delete=models.CASCADE)
    voyage = models.ForeignKey(Voyage,
                               to_field='voyage_id',
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

        ordering = ["date"]

    def get_file_name(self):
        """
        Returns file name of each file
        """
        return basename(self.file.name)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return str(self.id) + ", " + self.get_file_name()


class ImageCategory(models.Model):
    """
    Model stores categories for images.
    """

    value = models.IntegerField("Code")
    label = models.CharField("Category name", max_length=20)
    visible_on_website = models.BooleanField(
        "Visible on website (If checked, category will display on website "
        "if there is at least one image to display.)",
        default=True)

    class Meta:
        verbose_name = "Image Category"
        verbose_name_plural = "Image Categories"
        ordering = [
            'value',
        ]

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.label


class Country(models.Model):
    """
    Model stores countries with their codes
    """

    country_id = models.IntegerField("Country id", unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = [
            'country_id',
        ]

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return str(self.country_id)


class SexAge(models.Model):
    """
    Model stores Sex Age codes
    """

    sex_age_id = models.IntegerField("SexAge Id", unique=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Sex Age"
        verbose_name_plural = "Sex Ages"
        ordering = [
            'sex_age_id',
        ]

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.name


class AfricanName(models.Model):
    """
    Model stores information about African Name
    """

    slave_id = models.IntegerField("African id", unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    height = models.FloatField(blank=True,
                               null=True,
                               verbose_name="Height in inches")
    source = models.CharField(max_length=30,
                              blank=True,
                              null=True,
                              verbose_name="Modern name")
    date_arrived = models.IntegerField(verbose_name="Voyage year",
                                       blank=True,
                                       null=True)
    ship_name = models.CharField(max_length=70,
                                 verbose_name="Ship Name",
                                 blank=True,
                                 null=True)
    # This field might seem redundant in view of the voyage FK below but it is
    # used when the voyage number is part of an external dataset not included
    # in this db, which means that the FK value must be null. In most cases,
    # the two fields will be the same.
    voyage_number = models.IntegerField(verbose_name="Voyage ID")

    sex_age = models.ForeignKey(SexAge,
                                verbose_name="Sex Age",
                                to_field='sex_age_id',
                                blank=True,
                                null=True,
                                on_delete=models.CASCADE)
    country = models.ForeignKey(Country,
                                verbose_name="Country of Origin",
                                to_field='country_id',
                                blank=True,
                                null=True,
                                on_delete=models.CASCADE)
    disembarkation_port = models.ForeignKey(Place,
                                            verbose_name="Disembarkation",
                                            to_field='value',
                                            related_name="disembarkation_port",
                                            blank=True,
                                            null=True,
                                            on_delete=models.CASCADE)
    embarkation_port = models.ForeignKey(Place,
                                         verbose_name="Embarkation",
                                         to_field='value',
                                         related_name="embarkation_port",
                                         blank=True,
                                         null=True,
                                         on_delete=models.CASCADE)
    voyage = models.ForeignKey(Voyage,
                               verbose_name="Voyage",
                               to_field='voyage_id',
                               blank=True,
                               null=True,
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = "African Name"
        verbose_name_plural = "African Names"
        ordering = [
            'slave_id',
        ]

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if Voyage.objects.filter(voyage_id=self.voyage_number).exists():
            self.voyage = Voyage.objects.get(voyage_id=self.voyage_number)
        super().save(*args, **kwargs)
