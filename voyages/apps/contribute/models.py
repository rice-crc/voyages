from django.db import models
from django.contrib.auth.models import User

class AdminFaq(models.Model):
    """
    This is for the use of the site admins only.  This info is not
    displayed anywhere else on the site and is means of Admins documenting and sharing
    information about using the site.
    """
    question = models.TextField(max_length=1000)
    answer = models.TextField(max_length=1000)

    def __unicode__(self):
        return "%s" % self.question

    class Meta:
        ordering = ['question']
        verbose_name = 'Frequently Asked Question For Admins'
        verbose_name_plural = 'Frequently Asked Question For Admins'
        #app_label = "AdminHelp"
        db_table = "contribute_adminfaq"

class UserProfile(models.Model):
    """
    This model stores additional information related to users of the site.
    """

    user = models.OneToOneField(User)
    institution = models.TextField(max_length=255)
    new_material_and_sources = models.TextField(max_length=1000)
