from django.db import models
from os.path import basename
from voyages.apps.voyage.models import Voyage

class Image(models.Model):
    """
    Model to store information about image.
    """

    file = models.FileField(upload_to='images')
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=100, null=True, blank=True)
    creator = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=2, null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=500, null=True, blank=True)
    comments = models.CharField(max_length=2000, null=True, blank=True)
    other_references = models.CharField(max_length=500, null=True, blank=True)
    emory = models.BooleanField()
    emory_location = models.CharField(max_length=500, null=True, blank=True)
    authorization_status = models.IntegerField()
    image_status = models.IntegerField()
    ready_to_go = models.BooleanField()
    order_num = models.IntegerField()
    category = models.IntegerField()
    date = models.IntegerField(max_length=4)
    external_id = models.CharField(max_length=2000)

    # Category
    category = models.ForeignKey('ImageCategory', verbose_name="Image category")
    # FIXME: 'null=True, blank=True' will be removed (for tests)
    voyage = models.ForeignKey(Voyage, null=True, blank=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

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

    def __unicode__(self):
        return str(self.value) + ", " + self.label