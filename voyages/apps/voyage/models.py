from django.db import models

# Create your models here.
class MenuItem(models.Model):
    ParentID = models.ForeignKey('self')
    text = models.CharField(max_length=20)
    url = models.CharField(max_length=200)

    def __unicode__(self):
       return self.text
    def render(self):
       return '<a href = "' + self.url + '">' + self.text + '</a>'
