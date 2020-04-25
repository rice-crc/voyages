from django.db import models
from name_search import NameSearchCache

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
    class Role:
        CAPTAIN = 1
        OWNER = 2
        BUYER = 3
        SELLER = 4

    enslaver_alias = models.ForeignKey('EnslaverAlias', null=False, on_delete=models.CASCADE)
    voyage = models.ForeignKey('Voyage', null=False, on_delete=models.CASCADE)
    role = models.IntegerField(null=False)
    # NOTE: we will have to substitute VoyageShipOwner and VoyageCaptain
    # models/tables by this entity.

class Ethnicity(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class LanguageGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class ModernCountry(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

# TODO: this model will replace resources.AfricanName
class Enslaved(models.Model):
    # TODO: Apply models.IntegerChoices when we migrate to Django 3+
    class Gender:
        MALE = 1
        FEMALE = 2

    """
    Enslaved person.
    """
    enslaved_id = models.IntegerField(primary_key=True)

    modern_name_first = models.CharField(max_length=25, blank=True)
    modern_name_second = models.CharField(max_length=25, blank=True)
    modern_name_third = models.CharField(max_length=25, blank=True)

    # Personal data
    age = models.IntegerField(null=True)
    gender = models.IntegerField(null=True)
    height = models.FloatField(null=True, verbose_name="Height in inches")

    # The ethnicity, language and country could be null.
    # The possibility of including 'Unknown' values in the
    # reference tables and using them instead of null was
    # proposed and discarded.
    ethnicity = models.ForeignKey('LanguageGroup', null=True)
    language_group = models.ForeignKey('LanguageGroup', null=True)
    country = models.ForeignKey('ModernCountry', null=True)

    voyage = models.ForeignKey('Voyage', null=False)

class EnslavedRevision(Enslaved):
    # Enslaved model will have a revision mechanism so we can
    # use inheritance to produce an identical table for Enslaved with
    # an additional revision/timestamp field.
    revision = models.IntegerField()
    # Note: a revision should be saved only once. If changes are made
    # to a revision, a new entry should be created.
    timestamp = models.DateField(auto_now_add=True)

class EnslavedSearch:
    """
    Search parameters for enslaved persons.
    """

    def __init__(self, searched_name=None, exact_name_search=False, gender=None, age_range=None, year_range=None, embarkation_ports=None, language_groups=None, ship_name=None):
        """
        Search the Enslaved database. If a parameter is set to None, it will not
        be included in the search.
        @param: searched_name A name string to be searched
        @param: exact_name_search Boolean indicating whether the search is exact or fuzzy
        @param: gender The gender of the enslaved
        @param: age_range A pair (a, b) where a is the min and b is maximum age.
        @param: year_range A pair (a, b) where a is the min voyage year and b the max
        @param: embarkation_ports A list of embarkation ports where the enslaved embarked
        @param: language_groups A list of language groups for the enslaved
        @param: ship_name The ship name that the enslaved embarked
        """
        self.searched_name = searched_name
        self.exact_name_search = exact_name_search
        self.gender = gender
        self.age_range = age_range
        self.year_range = year_range
        self.embarkation_ports = embarkation_ports
        self.language_groups = language_groups
        self.ship_name = ship_name

    def search(self):
        """
        Execute the search. If we require fuzzy name search, then this is done
        outside of the database on our special search data structure and then
        filter the ids on the db query.
        """
        q = Enslaved.objects.all()
        if not self.exact_name_search and self.searched_name and len(self.searched_name):
            NameSearchCache.load()
            ids = list(NameSearchCache.search(self.searched_name))
            q = q.filter(pk__in=ids)
        if self.gender:
            q = q.filter(gender=self.gender)
        if self.age_range:
            q = q.filter(age__range=self.age_range)
        if self.year_range:
            # TODO: check that we are using the correct field
            q = q.filter(voyage__voyage_dates__imp_arrival_at_port_of_dis__range=self.year_range)
        if self.embarkation_ports:
            # TODO: check that we are using the correct field
            q = q.filter(voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__pk__in=self.embarkation_ports)
        if self.language_groups:
            q = q.filter(language_group__pk__in=self.language_groups)
        if self.ship_name:
            q = q.filter(voyage__voyage_ship__ship_name__icontains=self.ship_name)
        return q