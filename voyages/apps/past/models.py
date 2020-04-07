from django.db import models

# NOTES:
# Enslaved model will have a revision mechanism so we can try to
# use inheritance to produce an identical table for Enslaved with
# an additional revision/timestamp field.

class EnslaverIdentity(models.Model):
    principal_alias = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Enslaver unique identity'

class EnslaverAlias(models.Model):
    identity = models.ForeignKey('EnslaverIdentity', on_delete=models.CASCADE)
    alias = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Enslaver alias'

class EnslaverVoyage(models.Model):
    class Role(models.IntegerChoices):
        CAPTAIN = 1
        OWNER = 2
        BUYER = 3
        SELLER = 4

    enslaver_alias = models.ForeignKey('EnslaverAlias', null=False, on_delete=models.CASCADE)
    voyage = models.ForeignKey('Voyage', null=False, on_delete=models.CASCADE)
    role = models.IntegerField(choices=Role.choices)
    # NOTE: we will have to substitute VoyageShipOwner and VoyageCaptain
    # models/tables by this entity.

# class AgeSexGroup(models.Model):
#     """
#     Model stores Age Sex codes
#     """
# 
#     age_sex_group_id = models.IntegerField("AgeSex Group Id", primary_key=True)
#     name = models.CharField(max_length=50, blank=True, null=True)
# 
#     class Meta:
#         verbose_name = "Age Sex group"
#         ordering = ['age_sex_group_id', ]
# 
#     def __unicode__(self):
#         return self.name

class Enslaved(models.Model):
    """
    Enslaved person.
    """
    enslaved_id = models.IntegerField(primary_key=True)
    principal_alias = models.CharField(max_length=255)
    # Personal data
    age = models.IntegerField(blank=True, null=True)
    #age_sex_group = models.ForeignKey('AgeSexGroup', blank=True, null=True)
    height = models.FloatField(blank=True, null=True, verbose_name="Height in inches")

    voyage = models.ForeignKey('Voyage', null=False)
    # NOTE: this model will replace resources.AfricanName

class EnslavedRevision(Enslaved):
    revision = models.IntegerField()

