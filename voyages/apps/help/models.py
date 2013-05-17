from django.db import models

# Create your models here.

class Glossary(models.Model):
    term = models.CharField(('Term'),max_length=50)
    description = models.TextField(('Description'), max_length=1000)

    def __unicode__(self):
        return self.term

