# Create your models here.
from django.db import models

class DownloadFile(models.Model):
    file = models.FileField(upload_to='download')
    filetitle = models.CharField(('File name'),max_length=50)

    def __unicode__(self):
        return self.filetitle
