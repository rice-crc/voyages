from django.db import models

class Voyage(models.Model):
    """
    Class stores technical variables about voyages.
    """
    voyage_id = models.AutoField(primary_key=True)
    voyage_in_cdrom = models.IntegerField("Voyage in 1999 CD-ROM", max_length=1)
    voyage_groupings = models.IntegerField("Voyage groupings for estimating imputed slaves",\
                                        max_length=3)

class VoyageInformation(models.Model):
    ship_name = models.CharField("Name of vessel", max_length=60)
    national = models.IntegerField("Country in which ship registered", max_length=2)
    tonnage = models.IntegerField("Tonnage of vessel", max_length=4)
    ton_type = models.IntegerField("Definition of ton used in tonnage", max_length=2)
    rig_of_vessel = models.IntegerField("Rig of vessel", max_length=2)
    guns = models.IntegerField("Guns mounted", max_length=2)
    year_of_constr = models.DateField("Year of vessel's construction")
    constr_place = models.IntegerField("Place where vessel constructed", max_length=5)
    constr_region = models.IntegerField("Region where vessel constructed", max_length=5)
    year_of_reg = models.DateField("Year of vessel's registration")
    reg_place = models.IntegerField("Place where vessel registered", max_length=5)
    reg_region = models.IntegerField("Region where vessel registered", max_length=5)
    owner_of_venture = models.CharField("First owner of venture", max_length=60)

    voyage = models.ForeignKey(Voyage)

class VoyageVentureOwner(models.Model):
    voyage_information = models.ForeignKey(VoyageInformation)
    number_of_owner = models.IntegerField("Number of owner", max_length=2)
    name_of_owner = models.CharField("Name of the owner", max_length=40)

class VoyageOutcome(models.Model):
    particular_outcome = models.IntegerField("Particular outcome"
                                             "of voyage", max_length=3)
    outcome_slaves = models.IntegerField("Outcome of voyage for slaves",
                                         max_length=1)
    outcome_vessel_captures = models.IntegerField("Outcome of voyage"
                                                  "if vessel captured",
                                                  max_length=2)
    outcome_owner = models.IntegerField("Outcome of voyage or owner",
                                        max_length=2)
    resistance = models.IntegerField("African resistance", max_length=1)

    voyage = models.ForeignKey(Voyage)