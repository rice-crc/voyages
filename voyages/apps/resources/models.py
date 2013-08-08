from django.db import models
from os.path import basename, getsize
from voyages.apps.voyage.models import Voyage

class Image(models.Model):
    """
    Model to store information about image.
    """

    image_id = models.IntegerField('Image ID number', null=True, blank=True)

    file = models.ImageField(upload_to='images')
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, null=True, blank=True)
    mime_type = models.CharField(max_length=100, null=True, blank=True)
    creator = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=2, null=True, blank=True)
    source = models.CharField(max_length=500, null=True, blank=True)
    comments = models.CharField(max_length=2000, null=True, blank=True)

    ready_to_go = models.BooleanField(default=False)
    order_num = models.IntegerField('Code value')

    date = models.IntegerField('Date(Year YYYY)', max_length=4, null=True, blank=True)

    # Category
    category = models.ForeignKey('ImageCategory', verbose_name="Image category")
    voyage = models.ForeignKey(Voyage, null=True, blank=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

        ordering = ["date", "image_id"]

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

    class Meta:
        verbose_name = "Image Category"
        verbose_name_plural = "Image Categories"
        ordering = ['value',]

    def __unicode__(self):
        return self.label


from .search_indexes import ImagesIndex

# We are using this instead of the real time processor, since automatic update seems to fail (serializing strings)
def reindex_image_category(sender, **kwargs):
    ImagesIndex().update()
models.signals.post_save.connect(reindex_image_category, sender=ImageCategory)