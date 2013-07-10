from django.db import models
from voyages.apps.voyage.models import Voyage

class Image(models.Model):
    file_name = models.CharField(max_length=256, null=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    mime_type = models.CharField(max_length=100, null=True)
    creator = models.CharField(max_length=200, null=True)
    language = models.CharField(max_length=2, null=True)
    size = models.IntegerField(null=True)
    source = models.CharField(max_length=500, null=True)
    comments = models.CharField(max_length=2000, null=True)
    other_references = models.CharField(max_length=500, null=True)
    emory = models.BooleanField()
    emory_location = models.CharField(max_length=500, null=True)
    authorization_status = models.IntegerField()
    image_status = models.IntegerField()
    ready_to_go = models.BooleanField()
    order_num = models.IntegerField()
    category = models.IntegerField()
    date = models.IntegerField(max_length=4)
    external_id = models.CharField(max_length=2000)

    # Category
    category = models.ForeignKey('ImageCategory', verbose_name="Image category")
    voyage = models.ForeignKey(Voyage)

class ImageCategory(models.Model):
    name = models.CharField(max_length=20)