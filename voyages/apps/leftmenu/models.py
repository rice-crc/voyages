# Create your models here.
from django.db import models
from django.utils.translation import ugettext as _

# Left menu item
class LeftMenuItem(models.Model):
    ParentID = models.ForeignKey('self', null=True, blank=True)
    text = models.CharField(_('text'),max_length=50)
    url = models.CharField(max_length=200)
    orderNum = models.CharField(max_length=3)

    def __unicode__(self):
       return self.text
    def render(self):
       return '<a href = "' + self.url + '">' + self.text + '</a>'
