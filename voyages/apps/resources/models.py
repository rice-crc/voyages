from django.db import models
from os.path import basename
from voyages.apps.voyage.models import Voyage, Place
from django.conf import settings


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
    order_num = models.IntegerField('Code value', null=True, blank=True, max_length=2)

    date = models.IntegerField('Date(Year YYYY)', max_length=4, null=True, blank=True)

    # Category
    category = models.ForeignKey('ImageCategory', verbose_name="Image category")
    voyage = models.ForeignKey(Voyage, to_field='voyage_id', null=True, blank=True)

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
    visible_on_website = models.BooleanField("Visible on website (If checked, category will display on website "
                                             "if there is at least one image to display.)",
                                             default=True)

    class Meta:
        verbose_name = "Image Category"
        verbose_name_plural = "Image Categories"
        ordering = ['value', ]

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
        ordering = ['country_id', ]


class SexAge(models.Model):
    """
    Model stores Sex Age codes
    """

    sex_age_id = models.IntegerField("SexAge Id", unique=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Sex Age"
        verbose_name_plural = "Sex Ages"
        ordering = ['sex_age_id', ]


class AfricanName(models.Model):
    """
    Model stores information about African Name
    """

    slave_id = models.IntegerField("Slave id", unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    source = models.CharField(max_length=30, blank=True, null=True)
    date_arrived = models.IntegerField(max_length=4, verbose_name="Arrival", blank=True, null=True)
    ship_name = models.CharField(max_length=70, verbose_name="Ship Name", blank=True, null=True)
    voyage_number = models.IntegerField()

    sex_age = models.ForeignKey(SexAge, verbose_name="Sex Age", to_field='sex_age_id', blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name="Country", to_field='country_id', blank=True, null=True)
    disembarkation_port = models.ForeignKey(Place, verbose_name="Disembarkation Port", to_field='value',
                                            related_name="disembarkation_port", blank=True, null=True)
    embarkation = models.ForeignKey(Place, verbose_name="Embarkation Port", to_field='value',
                                    related_name="embarkation_port", blank=True, null=True)
    voyage = models.ForeignKey(Voyage, verbose_name="Voyage", to_field='voyage_id', blank=True, null=True)

    class Meta:
        verbose_name = "African Name"
        verbose_name_plural = "African Names"
        ordering = ['slave_id', ]


from .search_indexes import ImagesIndex


# We are using this instead of the real time processor, since automatic update seems to fail (serializing strings)
def reindex_image_category(sender, **kwargs):
    for obj in Image.objects.filter(category=kwargs['instance']):
        ImagesIndex().update_object(obj)


if hasattr(settings, 'HAYSTACK_SIGNAL_PROCESSOR'):
    models.signals.post_save.connect(reindex_image_category, sender=ImageCategory)
    #models.signals.post_save.connect(reindex_image_category, sender=Image)
