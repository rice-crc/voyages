from __future__ import unicode_literals

from builtins import str
from os.path import basename

from django.conf import settings
from django.db import models
from haystack import indexes

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

    def __unicode__(self):
        return self.label


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
        return None

    def prepare_voyage_vessel_name(self, obj):
        if obj.voyage is not None:
            return obj.voyage.voyage_ship.ship_name
        return None

    def prepare_voyage_imp_voyage_began(self, obj):
        if obj.voyage is not None:
            return obj.voyage.voyage_dates.imp_voyage_began
        return None

    def prepare_voyage_year(self, obj):
        if obj.voyage is not None:
            return obj.voyage.voyage_dates.imp_voyage_began
        return None

    def index_queryset(self, _=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


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

    def __unicode__(self):
        return str(self.country_id)


class CountryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    country_id = indexes.IntegerField(model_attr="country_id")
    country_name = indexes.CharField(model_attr="name")

    def get_model(self):
        return Country

    def index_queryset(self, _=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


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

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if Voyage.objects.filter(voyage_id=self.voyage_number).exists():
            self.voyage = Voyage.objects.get(voyage_id=self.voyage_number)
        super().save(*args, **kwargs)


class AfricanNamesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    slave_id = indexes.IntegerField(model_attr="slave_id")
    slave_name = indexes.NgramField(model_attr="name", null=True)
    slave_name_sort = indexes.CharField(model_attr="name", null=True)
    slave_age = indexes.IntegerField(model_attr="age", null=True)
    slave_height = indexes.FloatField(model_attr="height", null=True)
    slave_source = indexes.CharField(model_attr="source", null=True)
    slave_date_arrived = indexes.IntegerField(model_attr="date_arrived",
                                              null=True)
    slave_ship_name = indexes.NgramField(model_attr="ship_name", null=True)
    slave_ship_name_sort = indexes.CharField(model_attr="ship_name", null=True)
    slave_voyage_number = indexes.CharField(model_attr="voyage_number")
    slave_voyage = indexes.CharField(model_attr="voyage", null=True)
    slave_sex_age = indexes.CharField()
    slave_country = indexes.CharField(null=True)
    slave_country_sort = indexes.CharField(null=True)
    slave_embarkation_port = indexes.CharField(null=True)
    slave_embarkation_port_sort = indexes.CharField(null=True)
    slave_disembarkation_port = indexes.CharField(null=True)
    slave_disembarkation_port_sort = indexes.CharField(null=True)

    def get_model(self):
        return AfricanName

    def prepare_slave_voyage(self, obj):
        if obj.voyage is not None:
            return obj.voyage.voyage_id
        return None

    def prepare_slave_sex_age(self, obj):
        if obj.sex_age is not None:
            return obj.sex_age.name
        return None

    def prepare_slave_country(self, obj):
        if obj.country is not None:
            return obj.country.country_id
        return None

    def prepare_slave_country_sort(self, obj):
        if obj.country is not None:
            return obj.country.name
        return None

    def prepare_slave_embarkation_port(self, obj):
        if obj.embarkation_port is not None:
            return obj.embarkation_port.value
        return None

    def prepare_slave_embarkation_port_sort(self, obj):
        if obj.embarkation_port is not None:
            return obj.embarkation_port.place
        return None

    def prepare_slave_disembarkation_port(self, obj):
        if obj.disembarkation_port is not None:
            return obj.disembarkation_port.value
        return None

    def prepare_slave_disembarkation_port_sort(self, obj):
        if obj.disembarkation_port is not None:
            return obj.disembarkation_port.place
        return None

    def index_queryset(self, _=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


# We are using this instead of the real time processor, since automatic update
# seems to fail (serializing strings)
def reindex_image_category(_, **kwargs):
    for obj in Image.objects.filter(category=kwargs['instance']):
        ImagesIndex().update_object(obj)


if hasattr(settings, 'HAYSTACK_SIGNAL_PROCESSOR'):
    models.signals.post_save.connect(reindex_image_category,
                                     sender=ImageCategory)
    # models.signals.post_save.connect(reindex_image_category, sender=Image)
