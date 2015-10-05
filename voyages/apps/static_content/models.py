from django.db import models


class ContentGroup(models.Model):
    """
    Model stores static content groups.
    """

    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Static content group"
        verbose_name_plural = "Static content groups"

    def __unicode__(self):
        return self.name


class ContentPage(models.Model):
    """
    Model stores static content pages.
    """

    title = models.TextField(max_length=50)
    description = models.TextField(max_length=2000)
    order = models.IntegerField(max_length=1)
    group = models.ForeignKey(ContentGroup)

    class Meta:
        verbose_name = "Static content page"
        verbose_name_plural = "Static content pages"

    def __unicode__(self):
        return self.title