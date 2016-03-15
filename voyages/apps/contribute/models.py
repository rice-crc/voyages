from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from voyages.apps import voyage

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
    institution = models.CharField(max_length=255)
    new_material_and_sources = models.TextField(max_length=1000)

class InterimVoyage(models.Model):
    """
    Describes an interim voyage, which may be a new entry in the database,
    a modification of an existing entry or the merger of several existing
    entries.
    """

    # Ship, nation, owners
    name_of_vessel = models.CharField(max_length=255, null=True, blank=True)
    year_ship_constructed = models.IntegerField(null=True, blank=True)
    year_ship_registered = models.IntegerField(null=True, blank=True)
    ship_construction_place = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)
    ship_registration_place = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)
    national_carrier = models.ForeignKey(voyage.models.Nationality, related_name='+', null=True, blank=True)
    rig_of_vessel = models.ForeignKey(voyage.models.RigOfVessel, related_name='+', null=True, blank=True)
    tonnage_of_vessel = models.IntegerField(null=True, blank=True)
    ton_type = models.ForeignKey(voyage.models.TonType, related_name='+', null=True, blank=True)
    guns_mounted = models.IntegerField(null=True, blank=True)
    first_ship_owner = models.CharField(max_length=255, null=True, blank=True)
    second_ship_owner = models.CharField(max_length=255, null=True, blank=True)
    additional_ship_owners = models.TextField(max_length=1000, null=True, blank=True)

    # Outcome
    voyage_outcome = models.ForeignKey(voyage.models.ParticularOutcome, related_name='+', null=True, blank=True)
    african_resistance = models.ForeignKey(voyage.models.Resistance, related_name='+', null=True, blank=True)

    # Itinerary
    first_port_intended_embarkation = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)
    second_port_intended_embarkation = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)
    first_port_intended_disembarkation = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)
    second_port_intended_disembarkation = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)
    port_of_departure = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)
    number_of_ports_called_prior_to_slave_purchase = models.IntegerField(null=True, blank=True)
    first_place_of_slave_purchase = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)
    second_place_of_slave_purchase = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)
    third_place_of_slave_purchase = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)
    principal_place_of_slave_purchase = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)
    place_of_call_before_atlantic_crossing = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)
    number_of_new_world_ports_called_prior_to_disembarkation = models.IntegerField(null=True, blank=True)
    first_place_of_landing = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)
    second_place_of_landing = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)
    third_place_of_landing = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)
    principal_place_of_slave_disembarkation = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)
    port_voyage_ended = models.ForeignKey(voyage.models.Place, related_name='+', null=True, blank=True)

    # Dates
    date_departure = models.CommaSeparatedIntegerField(max_length=10, blank=True, null=True)
    date_slave_purchase_began = models.CommaSeparatedIntegerField(max_length=10, blank=True, null=True)
    date_vessel_left_last_slaving_port = models.CommaSeparatedIntegerField(max_length=10, blank=True, null=True)
    date_first_slave_disembarkation = models.CommaSeparatedIntegerField(max_length=10, blank=True, null=True)
    date_second_slave_disembarkation = models.CommaSeparatedIntegerField(max_length=10, blank=True, null=True)
    date_third_slave_disembarkation = models.CommaSeparatedIntegerField(max_length=10, blank=True, null=True)
    date_return_departure = models.CommaSeparatedIntegerField(max_length=10, blank=True, null=True)
    date_voyage_completed = models.CommaSeparatedIntegerField(max_length=10, blank=True, null=True)
    length_of_middle_passage = models.IntegerField(null=True, blank=True)

    # Captains
    first_captain = models.CharField(max_length=255, null=True, blank=True)
    second_captain = models.CharField(max_length=255, null=True, blank=True)
    third_captain = models.CharField(max_length=255, null=True, blank=True)

    notes = models.TextField('Notes', max_length=10000, null=True, blank=True, help_text='Notes for the interim voyage')

class InterimArticleSource(models.Model):
    """
    Article source for an interim voyage.models.
    """
    interim_voyage = models.ForeignKey(InterimVoyage, null=False,
                                       related_name='article_sources')
    authors = models.TextField(max_length=1000, null=True, blank=True)
    article_title = models.CharField(max_length=255, null=True, blank=True)
    journal = models.CharField(max_length=255, null=True, blank=True)
    volume_number = models.CharField(max_length=20, null=True, blank=True)
    year = models.IntegerField(null=True)
    page_start = models.IntegerField(null=True)
    page_end = models.IntegerField(null=True)
    information = models.TextField(max_length=1000, null=True, blank=True)
    url = models.TextField(max_length=400, null=True, blank=True)

class InterimBookSource(models.Model):
    """
    Book source for an interim voyage.models.
    """
    interim_voyage = models.ForeignKey(InterimVoyage, null=False,
                                       related_name='book_sources')
    authors = models.TextField(max_length=1000, null=True, blank=True)
    book_title = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    place_of_publication = models.CharField(max_length=20, null=True, blank=True)
    year = models.IntegerField(null=True)
    page_start = models.IntegerField(null=True)
    page_end = models.IntegerField(null=True)
    information = models.TextField(max_length=1000, null=True, blank=True)
    url = models.TextField(max_length=400, null=True, blank=True)

class InterimOtherSource(models.Model):
    """
    Book source for an interim voyage.models.
    """
    interim_voyage = models.ForeignKey(InterimVoyage, null=False,
                                       related_name='other_sources')
    title = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    page = models.CharField(max_length=20, null=True, blank=True)
    information = models.TextField(max_length=1000, null=True, blank=True)
    url = models.TextField(max_length=400, null=True, blank=True)

class InterimPrimarySource(models.Model):
    """
    Primary source for an interim voyage.models.
    """
    interim_voyage = models.ForeignKey(InterimVoyage, null=False,
                                       related_name='primary_sources')
    name_of_library_or_archive = models.CharField(max_length=255, null=True, blank=True)
    location_of_library_or_archive = models.CharField(max_length=255, null=True, blank=True)
    series_or_collection = models.CharField(max_length=255, null=True, blank=True)
    volume_or_box_or_bundle = models.CharField(max_length=255, null=True, blank=True)
    document_detail = models.CharField(max_length=255, null=True, blank=True)
    information = models.TextField(max_length=1000, null=True, blank=True)
    url = models.TextField(max_length=400, null=True, blank=True)

class InterimPreExistingSourceActions:
    accepted = 0,
    edit = 1,
    exclude = 2

class InterimPreExistingSource(models.Model):
    """
    A reference to a pre-existing source and any changes
    that should be made to it.
    """
    interim_voyage = models.ForeignKey(InterimVoyage, null=False,
                                       related_name='pre_existing_sources')
    voyage_ids = models.CommaSeparatedIntegerField(null=False, max_length=255)
    action = models.IntegerField(null=False, default=0)
    original_ref = models.CharField(max_length=255, null=False)
    full_ref = models.TextField(max_length=1000, null=False)
    notes = models.TextField(max_length=1000, null=True, blank=True)

class InterimSlaveNumber(models.Model):
    """
    An interim number corresponding to some Voyage variable.
    """
    interim_voyage = models.ForeignKey(InterimVoyage, null=False,
                                       related_name='slave_numbers')
    var_name = models.CharField(
        'Slave number code-book variable name', max_length=20,
        null=False, blank=False)
    number = models.IntegerField('Number')

class ReviewRequest(models.Model):
    """
    A request made to a reviewer for a contribution.
    """
    editor = models.ForeignKey(User, null=False, related_name='+')
    suggested_reviewer = models.ForeignKey(User, null=False, related_name='+')
    contribution_id = models.TextField(null=False)
    email_sent = models.BooleanField(default=False)
    response = models.IntegerField(default=0)
    editor_comments = models.TextField('Editor comments')
    final_decision = models.IntegerField(default=0)
    archived = models.BooleanField(default=False)

class ReviewVoyageContribution(models.Model):
    request = models.ForeignKey(ReviewRequest)
    review_interim_voyage = models.ForeignKey(InterimVoyage, null=False,
                                              related_name='+')
    notes = models.TextField('Notes', max_length=10000, help_text='Reviewer notes')


class ContributionStatus:
    pending = 0
    committed = 1
    under_review = 2
    approved = 3
    rejected = 4
    published = 5

class BaseVoyageContribution(models.Model):
    """
    Base (abstract) model for all types of contributions.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    contributor = models.ForeignKey(User, null=False, related_name='+')
    notes = models.TextField('Notes', max_length=10000, help_text='Notes for the contribution')
    # see the enumeration ContributionStatus
    status = models.IntegerField(
        'Status', help_text='Indicates whether the contribution is still being edited, committed, discarded etc')

    def get_related_voyage_ids(self):
        return []

    def get_related_voyages(self):
        x = list(voyage.models.Voyage.objects.filter(voyage_id__in=self.get_related_voyage_ids()))
        return x

    class Meta:
        abstract = True

# NOTE: Contributions may reference Voyages using the
# voyage_id field (not the primary key), however, there
# is no enforcement of referential integrity since the
# corresponding voyages may be deleted from the database.

class DeleteVoyageContribution(BaseVoyageContribution):
    """
    A contribution that consists of deleting selected voyages.
    """
    deleted_voyages_ids = models.CommaSeparatedIntegerField(
        'Deleted voyage ids',
        max_length=255,
        help_text='The voyage_id of each Voyage being deleted by this contribution')

    type = 'delete'

    def get_related_voyage_ids(self):
        return [int(x) for x in self.deleted_voyages_ids.split(',')]

class EditVoyageContribution(BaseVoyageContribution):
    """
    A contribution that consists of an exiting voyage being edited.
    """
    interim_voyage = models.ForeignKey(InterimVoyage, null=False,
                                       related_name='+')
    edited_voyage_id = models.IntegerField(
        'Edited voyage id',
        help_text='The voyage_id of the Voyage edited by this contribution')
    help_text = _('Edit each variable as required, or leave as is if you think no change is necessary.')

    type = 'edit'

    def __unicode__(self):
        return _('Edit an existing voyage')

    def get_related_voyage_ids(self):
        return [self.edited_voyage_id]

class MergeVoyagesContribution(BaseVoyageContribution):
    """
    A contribution that consists of merging existing voyages.
    """
    interim_voyage = models.ForeignKey(InterimVoyage, null=False,
                                       related_name='+')
    merged_voyages_ids = models.CommaSeparatedIntegerField(
        'Merged voyage ids',
        max_length=255,
        help_text='The voyage_id of each Voyage being merged by this contribution')
    help_text = _('Enter your preferred data to the right. If required use the box for '
                  'notes to explain your reasons for recommending the merge.')

    type = 'merge'

    def __unicode__(self):
        return _('Merge two or more voyages into one')

    def get_related_voyage_ids(self):
        return [int(x) for x in self.merged_voyages_ids.split(',')]

class NewVoyageContribution(BaseVoyageContribution):
    """
    A contribution that consists of a new voyage being added.
    """
    interim_voyage = models.ForeignKey(InterimVoyage, null=False,
                                       related_name='+')
    help_text = _('Complete as many boxes in each category as your source(s) allow.')

    type = 'new'

    def __unicode__(self):
        return _('New voyage')