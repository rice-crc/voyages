from __future__ import unicode_literals

import itertools

from django.contrib.auth.models import User
from django.core.validators import (MinLengthValidator,
                                    validate_comma_separated_integer_list)
from django.db import models
from django.utils.translation import ugettext as _

from voyages.apps import voyage
from voyages.apps.common.validators import date_csv_field_validator
from voyages.apps.voyage.models import VoyageDataset


class AdminFaq(models.Model):
    """
    This is for the use of the site admins only.  This info is not displayed
    anywhere else on the site and is means of Admins documenting and sharing
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
        # app_label = "AdminHelp"
        db_table = "contribute_adminfaq"


class UserProfile(models.Model):
    """
    This model stores additional information related to users of the site.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    ship_construction_place = models.ForeignKey(voyage.models.Place,
                                                related_name='+',
                                                null=True,
                                                blank=True,
                                                on_delete=models.CASCADE)
    ship_registration_place = models.ForeignKey(voyage.models.Place,
                                                related_name='+',
                                                null=True,
                                                blank=True,
                                                on_delete=models.CASCADE)
    national_carrier = models.ForeignKey(voyage.models.Nationality,
                                         related_name='+',
                                         null=True,
                                         blank=True,
                                         on_delete=models.CASCADE)
    rig_of_vessel = models.ForeignKey(voyage.models.RigOfVessel,
                                      related_name='+',
                                      null=True,
                                      blank=True,
                                      on_delete=models.CASCADE)
    tonnage_of_vessel = models.IntegerField(null=True, blank=True)
    ton_type = models.ForeignKey(voyage.models.TonType,
                                 related_name='+',
                                 null=True,
                                 blank=True,
                                 on_delete=models.CASCADE)
    guns_mounted = models.IntegerField(null=True, blank=True)
    first_ship_owner = models.CharField(max_length=255, null=True, blank=True)
    second_ship_owner = models.CharField(max_length=255, null=True, blank=True)
    additional_ship_owners = models.TextField(max_length=1000,
                                              null=True,
                                              blank=True)

    # Outcome
    voyage_outcome = models.ForeignKey(voyage.models.ParticularOutcome,
                                       related_name='+',
                                       null=True,
                                       blank=True,
                                       on_delete=models.CASCADE)
    african_resistance = models.ForeignKey(voyage.models.Resistance,
                                           related_name='+',
                                           null=True,
                                           blank=True,
                                           on_delete=models.CASCADE)

    # Itinerary
    first_port_intended_embarkation = models.ForeignKey(
        voyage.models.Place,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    second_port_intended_embarkation = models.ForeignKey(
        voyage.models.Place,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    first_port_intended_disembarkation = models.ForeignKey(
        voyage.models.Place,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    second_port_intended_disembarkation = models.ForeignKey(
        voyage.models.Place,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    port_of_departure = models.ForeignKey(
        voyage.models.Place,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    number_of_ports_called_prior_to_slave_purchase = models.IntegerField(
        null=True, blank=True)
    first_place_of_slave_purchase = models.ForeignKey(
        voyage.models.Place,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    second_place_of_slave_purchase = models.ForeignKey(
        voyage.models.Place,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    third_place_of_slave_purchase = models.ForeignKey(
        voyage.models.Place,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    principal_place_of_slave_purchase = models.ForeignKey(
        voyage.models.Place,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    place_of_call_before_atlantic_crossing = models.ForeignKey(
        voyage.models.Place,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    number_of_new_world_ports_called_prior_to_disembarkation = (
        models.IntegerField(null=True, blank=True))
    first_place_of_landing = models.ForeignKey(voyage.models.Place,
                                               related_name='+',
                                               null=True,
                                               blank=True,
                                               on_delete=models.CASCADE)
    second_place_of_landing = models.ForeignKey(voyage.models.Place,
                                                related_name='+',
                                                null=True,
                                                blank=True,
                                                on_delete=models.CASCADE)
    third_place_of_landing = models.ForeignKey(voyage.models.Place,
                                               related_name='+',
                                               null=True,
                                               blank=True,
                                               on_delete=models.CASCADE)
    principal_place_of_slave_disembarkation = models.ForeignKey(
        voyage.models.Place,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    port_voyage_ended = models.ForeignKey(voyage.models.Place,
                                          related_name='+',
                                          null=True,
                                          blank=True,
                                          on_delete=models.CASCADE)

    # Dates
    date_departure = models.CharField(validators=[date_csv_field_validator],
                                      max_length=10,
                                      blank=True,
                                      null=True)
    date_slave_purchase_began = models.CharField(
        validators=[date_csv_field_validator],
        max_length=10,
        blank=True,
        null=True)
    date_vessel_left_last_slaving_port = models.CharField(
        validators=[date_csv_field_validator],
        max_length=10,
        blank=True,
        null=True)
    date_first_slave_disembarkation = models.CharField(
        validators=[date_csv_field_validator],
        max_length=10,
        blank=True,
        null=True)
    date_second_slave_disembarkation = models.CharField(
        validators=[date_csv_field_validator],
        max_length=10,
        blank=True,
        null=True)
    date_third_slave_disembarkation = models.CharField(
        validators=[date_csv_field_validator],
        max_length=10,
        blank=True,
        null=True)
    date_return_departure = models.CharField(
        validators=[date_csv_field_validator],
        max_length=10,
        blank=True,
        null=True)
    date_voyage_completed = models.CharField(
        validators=[date_csv_field_validator],
        max_length=10,
        blank=True,
        null=True)
    length_of_middle_passage = models.IntegerField(null=True, blank=True)

    # Captains
    first_captain = models.CharField(max_length=255, null=True, blank=True)
    second_captain = models.CharField(max_length=255, null=True, blank=True)
    third_captain = models.CharField(max_length=255, null=True, blank=True)

    notes = models.TextField('Notes',
                             max_length=10000,
                             null=True,
                             blank=True,
                             help_text='Notes for the interim voyage')

    # Imputed variables (used for reviewer and editor)

    imputed_national_carrier = models.ForeignKey(voyage.models.Nationality,
                                                 related_name='+',
                                                 null=True,
                                                 blank=True,
                                                 on_delete=models.CASCADE)
    imputed_standardized_tonnage = models.FloatField(null=True, blank=True)
    imputed_region_ship_constructed = models.ForeignKey(
        voyage.models.Region,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    imputed_outcome_of_voyage_for_slaves = models.ForeignKey(
        voyage.models.SlavesOutcome,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    imputed_outcome_of_voyage_if_ship_captured = models.ForeignKey(
        voyage.models.VesselCapturedOutcome,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    imputed_outcome_of_voyage_for_owner = models.ForeignKey(
        voyage.models.OwnerOutcome,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    imputed_port_where_voyage_began = models.ForeignKey(
        voyage.models.Place,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    imputed_principal_place_of_slave_purchase = models.ForeignKey(
        voyage.models.Place,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    imputed_principal_port_of_slave_disembarkation = models.ForeignKey(
        voyage.models.Place,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    imputed_region_where_voyage_began = models.ForeignKey(
        voyage.models.Region,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    imputed_first_region_of_slave_landing = models.ForeignKey(
        voyage.models.Region,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    imputed_second_region_of_slave_landing = models.ForeignKey(
        voyage.models.Region,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    imputed_third_region_of_slave_landing = models.ForeignKey(
        voyage.models.Region,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    imputed_first_region_of_embarkation_of_slaves = models.ForeignKey(
        voyage.models.Region,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    imputed_second_region_of_embarkation_of_slaves = models.ForeignKey(
        voyage.models.Region,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    imputed_third_region_of_embarkation_of_slaves = models.ForeignKey(
        voyage.models.Region,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    imputed_year_voyage_began = models.IntegerField(null=True, blank=True)
    imputed_year_departed_africa = models.IntegerField(null=True, blank=True)
    imputed_year_arrived_at_port_of_disembarkation = models.IntegerField(
        null=True, blank=True)
    imputed_quinquennium_in_which_voyage_occurred = models.IntegerField(
        null=True, blank=True)
    imputed_decade_in_which_voyage_occurred = models.IntegerField(null=True,
                                                                  blank=True)
    imputed_quarter_century_in_which_voyage_occurred = models.IntegerField(
        null=True, blank=True)
    imputed_century_in_which_voyage_occurred = models.IntegerField(null=True,
                                                                   blank=True)
    imputed_voyage_length_home_port_to_first_port_of_disembarkation = (
        models.IntegerField(null=True, blank=True))
    imputed_length_of_middle_passage = models.IntegerField(null=True,
                                                           blank=True)

    imputed_voyage_groupings_for_estimating_imputed_slaves = (
        models.ForeignKey(
            voyage.models.VoyageGroupings,
            related_name='+',
            null=True,
            blank=True,
            on_delete=models.CASCADE))
    imputed_total_slaves_embarked = models.IntegerField(null=True, blank=True)
    imputed_total_slaves_disembarked = models.IntegerField(null=True,
                                                           blank=True)

    imputed_number_of_slaves_embarked_for_mortality_calculation = (
        models.IntegerField(null=True, blank=True))
    imputed_total_slave_deaths_during_middle_passage = models.IntegerField(
        null=True, blank=True)
    imputed_mortality_rate = models.FloatField(null=True, blank=True)
    imputed_standardized_price_of_slaves = models.FloatField(null=True,
                                                             blank=True)

    persisted_form_data = models.TextField(
        max_length=10000,
        null=True,
        blank=True,
        help_text='Auxiliary form data that is persisted in JSON format')


class InterimContributedSource(models.Model):
    # Fileds which are common to all contributed source types.
    information = models.TextField(max_length=1000, null=True, blank=True)
    url = models.TextField(max_length=400, null=True, blank=True)
    # Fields required to link created sources to published voyages.
    created_voyage_sources = models.ForeignKey(voyage.models.VoyageSources,
                                               null=True,
                                               on_delete=models.SET_NULL,
                                               related_name='+')
    source_ref_text = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class InterimArticleSource(InterimContributedSource):
    """
    Article source for an interim voyage.models.
    """
    interim_voyage = models.ForeignKey(InterimVoyage,
                                       null=False,
                                       related_name='article_sources',
                                       on_delete=models.CASCADE)
    authors = models.TextField(max_length=1000, null=True, blank=True)
    article_title = models.CharField(max_length=255, null=True, blank=True)
    journal = models.CharField(max_length=255, null=True, blank=True)
    volume_number = models.CharField(max_length=20, null=True, blank=True)
    year = models.IntegerField(null=True)
    page_start = models.IntegerField(null=True)
    page_end = models.IntegerField(null=True)


class InterimBookSource(InterimContributedSource):
    """
    Book/essay in book source for an interim voyage.models.
    """
    interim_voyage = models.ForeignKey(InterimVoyage,
                                       null=False,
                                       related_name='book_sources',
                                       on_delete=models.CASCADE)
    authors = models.TextField(max_length=1000, null=True, blank=True)
    book_title = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    place_of_publication = models.CharField(max_length=20,
                                            null=True,
                                            blank=True)
    year = models.IntegerField(null=True)
    page_start = models.IntegerField(null=True)
    page_end = models.IntegerField(null=True)
    source_is_essay_in_book = models.BooleanField(default=False)
    essay_title = models.CharField(max_length=255, null=True, blank=True)
    editors = models.TextField(max_length=1000, null=True, blank=True)


class InterimPrivateNoteOrCollectionSource(InterimContributedSource):
    """
    Other source for an interim voyage.models.
    """
    interim_voyage = models.ForeignKey(
        InterimVoyage,
        null=False,
        related_name='private_note_or_collection_sources',
        on_delete=models.CASCADE)
    authors = models.TextField(max_length=1000, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField(null=True)
    page = models.CharField(max_length=20, null=True, blank=True)


class InterimUnpublishedSecondarySource(InterimContributedSource):
    """
    Other source for an interim voyage.models.
    """
    interim_voyage = models.ForeignKey(
        InterimVoyage,
        null=False,
        related_name='unpublished_secondary_sources',
        on_delete=models.CASCADE)
    authors = models.TextField(max_length=1000, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField(null=True)
    page = models.CharField(max_length=20, null=True, blank=True)


class InterimPrimarySource(InterimContributedSource):
    """
    Primary source for an interim voyage.models.
    """
    interim_voyage = models.ForeignKey(InterimVoyage,
                                       null=False,
                                       related_name='primary_sources',
                                       on_delete=models.CASCADE)
    name_of_library_or_archive = models.CharField(max_length=255,
                                                  null=True,
                                                  blank=True)
    location_of_library_or_archive = models.CharField(max_length=255,
                                                      null=True,
                                                      blank=True)
    series_or_collection = models.CharField(max_length=255,
                                            null=True,
                                            blank=True)
    volume_or_box_or_bundle = models.CharField(max_length=255,
                                               null=True,
                                               blank=True)
    document_detail = models.CharField(max_length=255, null=True, blank=True)


class InterimNewspaperSource(InterimContributedSource):
    """
    Newspaper source
    """
    interim_voyage = models.ForeignKey(InterimVoyage,
                                       null=False,
                                       related_name='newspaper_sources',
                                       on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    alternative_name = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=60, null=True, blank=True)


class InterimPreExistingSourceActions:
    accepted = 0
    edit = 1
    exclude = 2


class InterimPreExistingSource(models.Model):
    """
    A reference to a pre-existing source and any changes
    that should be made to it.
    """
    interim_voyage = models.ForeignKey(InterimVoyage,
                                       null=False,
                                       related_name='pre_existing_sources',
                                       on_delete=models.CASCADE)
    voyage_ids = models.CharField(
        validators=[validate_comma_separated_integer_list],
        null=False,
        max_length=255)
    action = models.IntegerField(null=False, default=0)
    original_short_ref = models.CharField(max_length=255,
                                          null=False,
                                          validators=[MinLengthValidator(1)])
    original_ref = models.CharField(max_length=255, null=False)
    full_ref = models.TextField(max_length=1000, null=False)
    notes = models.TextField(max_length=1000, null=True, blank=True)


class InterimSlaveNumber(models.Model):
    """
    An interim number corresponding to some Voyage variable.
    """
    interim_voyage = models.ForeignKey(InterimVoyage,
                                       null=False,
                                       related_name='slave_numbers',
                                       on_delete=models.CASCADE)
    var_name = models.CharField('Slave number code-book variable name',
                                max_length=20,
                                null=False,
                                blank=False)
    number = models.FloatField('Number')


class ReviewRequestDecision:
    under_review = 0
    accepted_by_reviewer = 1
    rejected_by_reviewer = 2
    accepted_by_editor = 3
    rejected_by_editor = 4
    deleted = 5
    begun_editorial_review = 1000


class ReviewRequestResponse:
    no_reply = 0
    accepted = 1
    rejected = 2
    begun_editorial_review = 1000


class ReviewRequest(models.Model):
    """
    A request made to a reviewer for a contribution.
    """
    editor = models.ForeignKey(
        User,
        null=False,
        related_name='+',
        on_delete=models.CASCADE)
    suggested_reviewer = models.ForeignKey(
        User,
        null=False,
        related_name='+',
        on_delete=models.CASCADE)
    contribution_id = models.TextField(null=False)
    email_sent = models.BooleanField(default=False)
    response = models.IntegerField(default=0)
    editor_comments = models.TextField()
    reviewer_comments = models.TextField(null=True)
    decision_message = models.TextField(null=True)
    final_decision = models.IntegerField(default=0)
    archived = models.BooleanField(default=False)
    created_voyage_id = models.IntegerField(
        null=True,
        help_text='The voyage id that should be used for the newly created '
        'voyage (in case of new or merged contributions)'
    )
    dataset = models.IntegerField(
        null=False,
        default=VoyageDataset.Transatlantic,
        help_text='Which dataset the voyage belongs to (e.g. Transatlantic, '
        'IntraAmerican)'
    )

    def contribution(self):
        return get_contribution_from_id(self.contribution_id)

    def requires_created_voyage_id(self):
        return self.contribution_id.startswith(
            'merge') or self.contribution_id.startswith('new')

    def get_status_msg(self):
        decision_values = {
            ReviewRequestDecision.under_review: _('Under review'),
            ReviewRequestDecision.accepted_by_reviewer:
            _('Accepted (reviewer)'),
            ReviewRequestDecision.rejected_by_reviewer:
            _('Rejected (reviewer)'),
            ReviewRequestDecision.accepted_by_editor: _('Accepted'),
            ReviewRequestDecision.rejected_by_editor: _('Rejected'),
            ReviewRequestDecision.begun_editorial_review: _('Editor bypass')}
        response_values = {
            ReviewRequestResponse.no_reply: _('No reply'),
            ReviewRequestResponse.accepted: _('Will review'),
            ReviewRequestResponse.rejected: _('Cannot review')}
        if self.final_decision == 0:
            return response_values.get(self.response, '')
        return decision_values.get(self.final_decision, '')


class ReviewVoyageContribution(models.Model):
    """
    The reviewer's input on the contribution.
    """
    request = models.ForeignKey(ReviewRequest,
                                related_name='review_contribution',
                                on_delete=models.CASCADE)
    interim_voyage = models.ForeignKey(InterimVoyage,
                                       null=True,
                                       related_name='+',
                                       on_delete=models.CASCADE)
    notes = models.TextField('Notes',
                             null=True,
                             max_length=10000,
                             help_text='Reviewer notes')

    def __unicode__(self):
        return _('Review a contribution')

    def get_related_voyage_ids(self):
        return self.request.contribution().get_related_voyage_ids()


class EditorVoyageContribution(models.Model):
    """
    The editor's input on the contribution.
    """
    request = models.ForeignKey(ReviewRequest,
                                related_name='editor_contribution',
                                on_delete=models.CASCADE)
    interim_voyage = models.ForeignKey(InterimVoyage,
                                       null=True,
                                       related_name='+',
                                       on_delete=models.CASCADE)
    notes = models.TextField('Notes',
                             null=True,
                             max_length=10000,
                             help_text='Editor notes')
    ran_impute = models.BooleanField(default=False)

    def __unicode__(self):
        return _('Editorial review of contribution')

    def get_related_voyage_ids(self):
        return self.request.contribution().get_related_voyage_ids()


class ContributionStatus:
    pending = 0
    committed = 1
    under_review = 2
    approved = ReviewRequestDecision.accepted_by_editor
    rejected = ReviewRequestDecision.rejected_by_editor
    deleted = ReviewRequestDecision.deleted
    published = 6
    active_statuses = [0, 1, 2, 3, 4]


class BaseVoyageContribution(models.Model):
    """
    Base (abstract) model for all types of contributions.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    contributor = models.ForeignKey(
        User,
        null=False,
        related_name='+',
        on_delete=models.CASCADE)
    notes = models.TextField('Notes',
                             max_length=10000,
                             help_text='Notes for the contribution')
    # see the enumeration ContributionStatus
    status = models.IntegerField(
        'Status',
        help_text='Indicates whether the contribution is still being edited, '
        'committed, discarded etc'
    )

    def get_related_voyage_ids(self):
        return []

    def get_related_voyages(self):
        return list(
            voyage.models.Voyage.all_dataset_objects.filter(
                voyage_id__in=self.get_related_voyage_ids()))

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
    deleted_voyages_ids = models.CharField(
        'Deleted voyage ids',
        validators=[validate_comma_separated_integer_list],
        max_length=255,
        help_text='The voyage_id of each Voyage being deleted by this '
                  'contribution')

    type = 'delete'

    def get_related_voyage_ids(self):
        return [int(x) for x in self.deleted_voyages_ids.split(',')]


class EditVoyageContribution(BaseVoyageContribution):
    """
    A contribution that consists of an exiting voyage being edited.
    """
    interim_voyage = models.ForeignKey(InterimVoyage,
                                       null=False,
                                       related_name='+',
                                       on_delete=models.CASCADE)
    edited_voyage_id = models.IntegerField(
        'Edited voyage id',
        help_text='The voyage_id of the Voyage edited by this contribution')
    help_text = _(
        'Edit each variable as required, or leave as is if you think no '
        'change is necessary.')

    type = 'edit'

    def __unicode__(self):
        return _('Edit an existing voyage')

    def get_related_voyage_ids(self):
        return [self.edited_voyage_id]


class MergeVoyagesContribution(BaseVoyageContribution):
    """
    A contribution that consists of merging existing voyages.
    """
    interim_voyage = models.ForeignKey(InterimVoyage,
                                       null=False,
                                       related_name='+',
                                       on_delete=models.CASCADE)
    merged_voyages_ids = models.CharField(
        'Merged voyage ids',
        validators=[validate_comma_separated_integer_list],
        max_length=255,
        help_text='The voyage_id of each Voyage being merged by this '
                  'contribution')
    help_text = _('Enter your preferred data to the right. If required use '
                  'the box for '
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
    interim_voyage = models.ForeignKey(InterimVoyage,
                                       null=False,
                                       related_name='+',
                                       on_delete=models.CASCADE)
    help_text = _(
        'Complete as many boxes in each category as your source(s) allow.')

    type = 'new'

    def __unicode__(self):
        return _('New voyage')


contribution_model_by_type = {
    'delete': DeleteVoyageContribution,
    'edit': EditVoyageContribution,
    'merge': MergeVoyagesContribution,
    'new': NewVoyageContribution,
    'review': ReviewVoyageContribution,
    'editorial_review': EditorVoyageContribution
}


def get_contribution(contribution_type, contribution_id):
    model = contribution_model_by_type.get(contribution_type)
    if model is None:
        return None
    return model.objects.filter(pk=contribution_id).first()


def get_contribution_from_id(contribution_id):
    if contribution_id is None:
        return None
    contribution_pair = contribution_id.split('/')
    contribution_type = contribution_pair[0]
    contribution_id = int(contribution_pair[1])
    return get_contribution(contribution_type, contribution_id)


source_type_dict = {
    'Primary source': InterimPrimarySource,
    'Article source': InterimArticleSource,
    'Book source': InterimBookSource,
    'Newspaper source': InterimNewspaperSource,
    'Private note or collection source': InterimPrivateNoteOrCollectionSource,
    'Unpublished secondary source': InterimUnpublishedSecondarySource
}


def get_all_new_sources_for_interim(interim_pk):
    all_sources = [
        list(src_type.objects.filter(interim_voyage__id=interim_pk))
        for src_type in list(source_type_dict.values())
    ]
    return list(itertools.chain.from_iterable(all_sources))
