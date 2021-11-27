from __future__ import absolute_import, unicode_literals

import operator
import threading
import unicodedata
from builtins import range, str
from functools import reduce
from django.conf import settings

from django.contrib.auth.models import User
from django.db import models
from django.db.models import (Case, CharField, F, Func, IntegerField, Q, Value, When)
from django.db.models.expressions import Subquery, OuterRef
from django.db.models.fields import TextField
from django.db.models.functions import Coalesce, Concat, Length, Substr
import Levenshtein_search

from voyages.apps.voyage.models import Place, Voyage, VoyageSources
from voyages.apps.common.validators import date_csv_field_validator

# Levenshtein-distance based search with ranked results.
# https://en.wikipedia.org/wiki/Levenshtein_distance


# function obtained from
# https://stackoverflow.com/questions/517923/
# what-is-the-best-way-to-remove-accents-in-a-python-unicode-string
def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = str(text, 'utf-8')
    except (TypeError, NameError):  # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    return str(text.lower())


class NameSearchCache:
    _loaded = False
    _lock = threading.Lock()
    _index = None
    _name_key = {}
    _sound_recordings = {}

    @classmethod
    def get_recordings(cls, names):
        rec = cls._sound_recordings
        return {
            name: rec[name]
            for name in names
            if name is not None and name in rec
        }

    @classmethod
    def search(cls, name, max_cost=3, max_results=100):
        res = cls.search_full(name, max_cost, max_results)
        return [id for x in res for id in x[0]]

    @classmethod
    def search_full(cls, name, max_cost, max_results):
        res = sorted(Levenshtein_search.lookup(0, strip_accents(name),
                                               max_cost),
                     key=lambda x: x[1])
        return [(cls._name_key[x[0]], x[1], x[0]) for x in res[0:max_results]]

    @classmethod
    def load(cls, force_reload=False):
        with cls._lock:
            if not force_reload and cls._loaded:
                return
            Levenshtein_search.clear_wordset(0)
            cls._name_key = {}
            all_names = set()
            q = Enslaved.objects.values_list('enslaved_id', 'documented_name',
                                             'name_first', 'name_second',
                                             'name_third')
            for item in q:
                ns = {
                    strip_accents(item[i])
                    for i in range(1, 4)
                    if item[i] is not None
                }
                all_names.update(ns)
                item_0 = item[0]
                for name in ns:
                    ids = cls._name_key.setdefault(name, [])
                    ids.append(item_0)
            Levenshtein_search.populate_wordset(0, list(all_names))
            q = EnslavedName.objects.values_list('id', 'name', 'language',
                                                 'recordings_count')
            for item in q:
                current = cls._sound_recordings.setdefault(item[1], {})
                langs = current.setdefault('langs', [])
                lang = {}
                lang['lang'] = item[2]
                lang['id'] = item[0]
                lang['records'] = [
                    f'0{item[0]}.{item[2]}.{index}.mp3'
                    for index in range(1, 1 + item[3])
                ]
                langs.append(lang)
            cls._loaded = True


class EnslaverInfoAbstractBase(models.Model):
    principal_alias = models.CharField(max_length=255)

    # Personal info.
    birth_year = models.IntegerField(null=True)
    birth_month = models.IntegerField(null=True)
    birth_day = models.IntegerField(null=True)
    birth_place = models.CharField(max_length=255, null=True)

    death_year = models.IntegerField(null=True)
    death_month = models.IntegerField(null=True)
    death_day = models.IntegerField(null=True)
    death_place = models.CharField(max_length=255, null=True)

    father_name = models.CharField(max_length=255, null=True)
    father_occupation = models.CharField(max_length=255, null=True)
    mother_name = models.CharField(max_length=255, null=True)

    first_spouse_name = models.CharField(max_length=255, null=True)
    first_marriage_date = models.CharField(max_length=12, null=True)
    second_spouse_name = models.CharField(max_length=255, null=True)
    second_marriage_date = models.CharField(max_length=12, null=True)

    probate_date = models.CharField(max_length=12, null=True)
    will_value_pounds = models.CharField(max_length=12, null=True)
    will_value_dollars = models.CharField(max_length=12, null=True)
    will_court = models.CharField(max_length=12, null=True)

    class Meta:
        abstract = True


class EnslaverIdentity(EnslaverInfoAbstractBase):

    class Meta:
        verbose_name = 'Enslaver unique identity and personal info'


class EnslaverIdentitySourceConnection(models.Model):
    identity = models.ForeignKey(EnslaverIdentity, on_delete=models.CASCADE)
    # Sources are shared with Voyages.
    source = models.ForeignKey(VoyageSources, related_name="+",
                               null=False, on_delete=models.CASCADE)
    source_order = models.IntegerField()
    text_ref = models.CharField(max_length=255, null=False, blank=True)


class EnslaverAlias(models.Model):
    """
    An alias represents a name appearing in a record that is mapped to
    a consolidated identity. The same individual may appear in multiple
    records under different names (aliases).
    """
    identity = models.ForeignKey(EnslaverIdentity, on_delete=models.CASCADE)
    alias = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Enslaver alias'


class EnslaverMerger(EnslaverInfoAbstractBase):
    """
    Represents a merger of two or more identities.
    We inherit from EnslaverInfoAbstractBase so that all personal fields
    are also contained in the merger.
    """
    comments = models.CharField(max_length=1024)


class EnslaverMergerItem(models.Model):
    """
    Represents a single identity that is part of a merger.
    """
    merger = models.ForeignKey('EnslaverMerger',
                               null=False,
                               on_delete=models.CASCADE)
    # We do not use a foreign key to the identity since if the merger
    # is accepted, some/all of the records may be deleted and the keys
    # would either be invalid or set to null.
    enslaver_identity_id = models.IntegerField(null=False)


class EnslaverVoyageConnection(models.Model):
    """
    Associates an enslaver with a voyage at some particular role.
    """

    class Role:
        CAPTAIN = 1
        OWNER = 2
        BUYER = 3
        SELLER = 4

    enslaver_alias = models.ForeignKey('EnslaverAlias',
                                       null=False,
                                       on_delete=models.CASCADE)
    voyage = models.ForeignKey('voyage.Voyage',
                               null=False,
                               on_delete=models.CASCADE)
    role = models.IntegerField(null=False)
    # There might be multiple persons with the same role for the same voyage
    # and they can be ordered (ranked) using the following field.
    order = models.IntegerField(null=True)
    # NOTE: we will have to substitute VoyageShipOwner and VoyageCaptain
    # models/tables by this entity.


class NamedModelAbstractBase(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True


class LanguageGroup(NamedModelAbstractBase):
    longitude = models.DecimalField("Longitude of point",
                                    max_digits=10,
                                    decimal_places=7,
                                    null=True)
    latitude = models.DecimalField("Latitude of point",
                                   max_digits=10,
                                   decimal_places=7,
                                   null=True)


class ModernCountry(NamedModelAbstractBase):
    longitude = models.DecimalField("Longitude of Country",
                                    max_digits=10,
                                    decimal_places=7,
                                    null=False)
    latitude = models.DecimalField("Latitude of Country",
                                   max_digits=10,
                                   decimal_places=7,
                                   null=False)
    languages = models.ManyToManyField(LanguageGroup)


class RegisterCountry(NamedModelAbstractBase):
    pass


class AltLanguageGroupName(NamedModelAbstractBase):
    language_group = models.ForeignKey(LanguageGroup,
                                       null=False,
                                       related_name='alt_names',
                                       on_delete=models.CASCADE)


class EnslavedDataset:
    AFRICAN_ORIGINS = 0
    OCEANS_OF_KINFOLK = 1


class CaptiveFate(NamedModelAbstractBase):
    pass

class CaptiveStatus(NamedModelAbstractBase):
    pass


# TODO: this model will replace resources.AfricanName
class Enslaved(models.Model):
    """
    Enslaved person.
    """
    enslaved_id = models.IntegerField(primary_key=True)

    # For African Origins dataset documented_name is an African Name.
    # For Oceans of Kinfolk, this field is used to store the Western
    # Name of the enslaved.
    documented_name = models.CharField(max_length=100, blank=True)
    name_first = models.CharField(max_length=100, null=True, blank=True)
    name_second = models.CharField(max_length=100, null=True, blank=True)
    name_third = models.CharField(max_length=100, null=True, blank=True)
    modern_name = models.CharField(max_length=100, null=True, blank=True)
    # Certainty is used for African Origins only.
    editor_modern_names_certainty = models.CharField(max_length=255,
                                                     null=True,
                                                     blank=True)
    # Personal data
    age = models.IntegerField(null=True, db_index=True)
    gender = models.IntegerField(null=True, db_index=True)
    height = models.DecimalField(null=True, decimal_places=2, max_digits=6, verbose_name="Height in inches", db_index=True)
    skin_color = models.CharField(max_length=100, null=True, db_index=True)
    language_group = models.ForeignKey(LanguageGroup, null=True,
                                       on_delete=models.CASCADE,
                                       db_index=True)
    register_country = models.ForeignKey(RegisterCountry, null=True,
                                         on_delete=models.CASCADE,
                                        db_index=True)
    # For Kinfolk, this is the Last known location field.
    post_disembark_location = models.ForeignKey(Place, null=True,
                                                on_delete=models.CASCADE,
                                                db_index=True)
    last_known_date = models.CharField(
        max_length=10,
        validators=[date_csv_field_validator],
        blank=True,
        null=True,
        help_text="Date in format: MM,DD,YYYY")
    captive_fate = models.ForeignKey(CaptiveFate, null=True, on_delete=models.SET_NULL, db_index=True)
    captive_status = models.ForeignKey(CaptiveStatus, null=True, on_delete=models.SET_NULL, db_index=True)
    voyage = models.ForeignKey(Voyage, null=False, on_delete=models.CASCADE, db_index=True)
    dataset = models.IntegerField(null=False, default=0, db_index=True)
    notes = models.CharField(null=True, max_length=8192)
    sources = models.ManyToManyField(VoyageSources,
                                     through='EnslavedSourceConnection',
                                     related_name='+')


class EnslavedSourceConnection(models.Model):
    enslaved = models.ForeignKey(Enslaved,
                                 on_delete=models.CASCADE,
                                 related_name='sources_conn')
    # Sources are shared with Voyages.
    source = models.ForeignKey(VoyageSources,
                               on_delete=models.CASCADE,
                               related_name='+',
                               null=False)
    source_order = models.IntegerField()
    text_ref = models.CharField(max_length=255, null=False, blank=True)


class EnslavedContribution(models.Model):
    enslaved = models.ForeignKey(Enslaved, on_delete=models.CASCADE)
    contributor = models.ForeignKey(User, null=True, related_name='+',
                                    on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    is_multilingual = models.BooleanField(default=False)
    status = models.IntegerField()
    token = models.CharField(max_length=40, null=True, blank=True)


class EnslavedContributionNameEntry(models.Model):
    contribution = models.ForeignKey(EnslavedContribution,
                                     on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    order = models.IntegerField()
    notes = models.CharField(max_length=255, null=True, blank=True)


class EnslavedContributionLanguageEntry(models.Model):
    contribution = models.ForeignKey(EnslavedContribution,
                                     on_delete=models.CASCADE)
    language_group = models.ForeignKey(LanguageGroup, null=True,
                                       on_delete=models.CASCADE)
    order = models.IntegerField()
    notes = models.CharField(max_length=255, null=True, blank=True)


class EnslavedName(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    language = models.CharField(max_length=3, null=False, blank=False)
    recordings_count = models.IntegerField()

    class Meta:
        unique_together = ('name', 'language')


class EnslavementRelation(models.Model):
    """
    Represents a relation involving enslavers and enslaved individuals.
    """
    
    id = models.IntegerField(primary_key=True)
    relation_type = models.IntegerField()
    place = models.ForeignKey(Place, null=True, on_delete=models.SET_NULL)
    date = models.CharField(max_length=12, null=True,
        help_text="Date in MM,DD,YYYY format with optional fields.")
    amount = models.DecimalField(null=True, decimal_places=2, max_digits=6)
    voyage = models.ForeignKey(Voyage, related_name="+",
                               null=True, on_delete=models.CASCADE)
    source = models.ForeignKey(VoyageSources, related_name="+",
                               null=True, on_delete=models.CASCADE)
    text_ref = models.CharField(max_length=255, null=False, blank=True, help_text="Source text reference")


class EnslavedInRelation(models.Model):
    """
    Associates an enslaved in a slave relation.
    """

    id = models.IntegerField(primary_key=True)
    transaction = models.ForeignKey(
        EnslavementRelation,
        related_name="enslaved",
        null=False,
        on_delete=models.CASCADE)
    enslaved = models.ForeignKey(Enslaved,
        related_name="transactions",
        null=False,
        on_delete=models.CASCADE)


class EnslaverInRelation(models.Model):
    """
    Associates an enslaver in a slave relation.
    """

    id = models.IntegerField(primary_key=True)
    transaction = models.ForeignKey(
        EnslavementRelation,
        related_name="enslavers",
        null=False,
        on_delete=models.CASCADE)
    enslaver_alias = models.ForeignKey(EnslaverAlias, null=False, on_delete=models.CASCADE)
    role = models.IntegerField(null=False, help_text="The role of the enslaver in this relation")


_special_empty_string_fields = {
    'voyage__voyage_ship__ship_name': 1,
    'voyage__voyage_dates__first_dis_of_slaves': '2'
}

_name_fields = ['documented_name', 'name_first', 'name_second', 'name_third']
# Note: we started with three modern name fields, but it
# was decided (2021-10-05) to drop all but one.
_modern_name_fields = ['modern_name']


class MultiValueHelper:
    """
    This helper uses the GROUP_CONCAT function to fetch multiple values as a
    single string value for the query and supports mapping this single string
    back to a structure (list of dicts, or list of flat values if only one field
    mapping is used).
    """

    _FIELD_SEP = "#@@@#"
    _GROUP_SEP = "@###@"
    _FIELD_SEP_VALUE = Value(_FIELD_SEP)

    def __init__(self, projected_name, m2m_connection_model, fk_name, **field_mappings):
        self.field_mappings = field_mappings
        self.projected_name = projected_name
        self.model = m2m_connection_model
        self.fk_name = fk_name

    def adapt_query(self, q):
        """
        This method adapts the query by including a computed field aliased "projected_name".
        The computed field groups multiple related rows and field by concatenating them into
        a single string. The parse_group method can be used to parse this concatenated
        string and obtain a list of dictionaries, where each entry corresponds to the fields
        in a related row.
        """
        fields_concatenated = []
        for field_map in self.field_mappings.values():
            fields_concatenated.append(F(field_map) if isinstance(field_map, str) else field_map)
            fields_concatenated.append(self._FIELD_SEP_VALUE)
        # Drop the last entry which is a field separator.
        fields_concatenated.pop()
        group_concat_field = Func(
            Concat(*fields_concatenated, output_field=TextField()) if len(fields_concatenated) > 1 else fields_concatenated[0],
            # This value and the arg_joiner is needed so that the ORM produces the right syntax
            # for GROUP_CONCAT(CONCAT(<FieldsToConcatenate>) SEPARATOR <quoted _GROUP_SEP>).
            Value(self._GROUP_SEP),
            arg_joiner=" SEPARATOR ",
            function='GROUP_CONCAT')
        sub_query = self.model.objects.filter(**{ self.fk_name: OuterRef('pk') }) \
            .annotate(group_concat_field=group_concat_field) \
            .values('group_concat_field')
        return q.annotate(**{ self.projected_name: Subquery(sub_query) })

    def parse_grouped(self, value):
        """
        Produce an iterable of dicts by parsing the field produced by this helper.
        """
        flen = len(self.field_mappings)
        if value is None or flen == 0:
            return
        for item in value.split(self._GROUP_SEP):
            values = item.split(self._FIELD_SEP)
            if len(values) == flen:
                # Return a dict when multiple values are mapped otherwise return just the value.
                yield { name: values[index] for (index, name) in enumerate(self.field_mappings.keys()) } if flen > 1 else values[0]

    def patch_row(self, row):
        """
        For a dict row that is obtained by executing the query with the GROUP_CONCAT in this
        helper, patch the projected name to contain a list of entries, each being a dict
        corresponding to an associated entry.
        """
        if self.projected_name in row:
            row[self.projected_name] = list(self.parse_grouped(row[self.projected_name]))
        else:
            row[self.projected_name] = []
        return row


class EnslavedSearch:
    """
    Search parameters for enslaved persons.
    """

    SOURCES_LIST = "sources_list"
    ENSLAVERS_LIST = "enslavers_list"

    sources_helper = MultiValueHelper(
        SOURCES_LIST,
        EnslavedSourceConnection,
        'enslaved_id',
        text_ref="text_ref",
        full_ref="source__full_ref")
    enslavers_helper = MultiValueHelper(
        ENSLAVERS_LIST,
        EnslavedInRelation,
        'enslaved_id',
        enslaver_name="transaction__enslavers__enslaver_alias__alias",
        relation_date="transaction__date",
        enslaver_role="transaction__enslavers__role")

    def __init__(self,
                 enslaved_dataset=None,
                 searched_name=None,
                 exact_name_search=False,
                 gender=None,
                 age_range=None,
                 height_range=None,
                 year_range=None,
                 embarkation_ports=None,
                 disembarkation_ports=None,
                 post_disembark_location=None,
                 language_groups=None,
                 ship_name=None,
                 voyage_id=None,
                 enslaved_id=None,
                 source=None,
                 order_by=None,
                 voyage_dataset=None,
                 skin_color=None):
        """
        Search the Enslaved database. If a parameter is set to None, it will
        not be included in the search.
        @param: enslaved_dataset The enslaved dataset to be searched
                (either None to search all or an integer code).
        @param: searched_name A name string to be searched
        @param: exact_name_search Boolean indicating whether the search is
                exact or fuzzy
        @param: gender The gender ('male' or 'female').
        @param: age_range A pair (a, b) where a is the min and b is maximum age
        @param: voyage_dataset A list of voyage datasets that restrict the search.
        @param: height_range A pair (a, b) where a is the min and b is maximum
                height
        @param: year_range A pair (a, b) where a is the min voyage year and b
                the max
        @param: embarkation_ports A list of port ids where the enslaved
                embarked
        @param: disembarkation_ports A list of port ids where the enslaved
                disembarked
        @param: post_disembark_location A list of place ids where the enslaved
                was located after disembarkation
        @param: language_groups A list of language groups ids for the enslaved
        @param: ship_name The ship name that the enslaved embarked
        @param: voyage_id A pair (a, b) where the a <= voyage_id <= b
        @param: enslaved_id A pair (a, b) where the a <= enslaved_id <= b
        @param: source A text fragment that should match Source's text_ref or
                full_ref
        @param: order_by An array of dicts {
                'columnName': 'NAME', 'direction': 'ASC or DESC' }.
                Note that if the search is fuzzy, then the fallback value of
                order_by is the ranking of the fuzzy search.
        @param: skin_color a textual description for skin color (Racial Descriptor)
        """
        self.enslaved_dataset = enslaved_dataset
        self.searched_name = searched_name
        self.exact_name_search = exact_name_search
        self.gender = gender
        self.age_range = age_range
        self.height_range = height_range
        self.year_range = year_range
        self.embarkation_ports = embarkation_ports
        self.disembarkation_ports = disembarkation_ports
        self.post_disembark_location = post_disembark_location
        self.language_groups = language_groups
        self.ship_name = ship_name
        self.voyage_id = voyage_id
        self.enslaved_id = enslaved_id
        self.source = source
        self.order_by = order_by
        self.voyage_dataset = voyage_dataset
        self.skin_color = skin_color

    def get_order_for_field(self, field):
        if isinstance(self.order_by, list):
            for x in self.order_by:
                if x['columnName'] == field:
                    return x['direction']
        return None

    def execute(self, fields):
        """
        Execute the search and output an enumerable of dictionaries, each
        representing an Enslaved record.
        @param: fields A list of fields that are fetched.
        """
        q = Enslaved.objects \
            .select_related('language_group') \
            .select_related('voyage__voyage_dates') \
            .select_related('voyage__voyage_ship') \
            .select_related('voyage__voyage_itinerary__int_first_port_dis') \
            .select_related('voyage__voyage_itinerary_'
                            '_imp_principal_place_of_slave_purchase') \
            .select_related('voyage__voyage_itinerary_'
                            '_imp_principal_port_slave_dis') \
            .select_related('register_country')

        ranking = None
        is_fuzzy = False
        if self.searched_name and len(self.searched_name):
            if self.exact_name_search:
                qmask = Q(documented_name=self.searched_name)
                qmask |= Q(name_first=self.searched_name)
                qmask |= Q(name_second=self.searched_name)
                qmask |= Q(name_third=self.searched_name)
                q = q.filter(qmask)
            else:
                # Perform a fuzzy search on our cached names.
                NameSearchCache.load()
                fuzzy_ids = NameSearchCache.search(self.searched_name)
                ranking = {x[1]: x[0] for x in enumerate(fuzzy_ids)}
                q = q.filter(pk__in=fuzzy_ids)
                is_fuzzy = True
        if self.gender:
            gender_val = 1 if self.gender == 'male' else 2
            q = q.filter(gender=gender_val)
        if self.voyage_dataset:

            def get_dataset_query(x):
                if x == 'trans':
                    return Q(voyage__dataset=0)
                if x == 'intra':
                    return Q(voyage__dataset=1)
                if x == 'african':
                    return Q(voyage__dataset=2)
                raise Exception('Invalid Voyage Dataset value')

            conditions = [get_dataset_query(x) for x in self.voyage_dataset]
            q = q.filter(reduce(operator.or_, conditions))
        if self.enslaved_dataset is not None:
            q = q.filter(dataset=self.enslaved_dataset)
        if self.age_range:
            q = q.filter(age__range=self.age_range)
        if self.height_range:
            q = q.filter(height__range=self.height_range)
        if self.post_disembark_location:
            q = q.filter(
                post_disembark_location__pk__in=self.post_disembark_location)
        if self.source:
            qmask = Q(sources_conn__text_ref__contains=self.source)
            qmask |= Q(sources__full_ref__contains=self.source)
            q = q.filter(qmask)
        if self.voyage_id:
            q = q.filter(voyage__pk__range=self.voyage_id)
        if self.enslaved_id:
            q = q.filter(pk__range=self.enslaved_id)
        if self.year_range:
            # Search on YEARAM field. Note that we have a 'MM,DD,YYYY' format
            # even though the only year should be present.
            q = q.filter(
                voyage__voyage_dates__imp_arrival_at_port_of_dis__range=[
                    ',,' + str(y) for y in self.year_range
                ])
        if self.embarkation_ports:
            # Search on MJBYPTIMP field.
            q = q.filter(
                voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__pk__in=self.embarkation_ports)
        if self.disembarkation_ports:
            # Search on MJSLPTIMP field.
            q = q.filter(
                voyage__voyage_itinerary__imp_principal_port_slave_dis__pk__in=self.disembarkation_ports)
        if self.language_groups:
            q = q.filter(language_group__pk__in=self.language_groups)
        if self.ship_name:
            q = q.filter(
                voyage__voyage_ship__ship_name__icontains=self.ship_name)
        order_by_ranking = 'asc'
        if isinstance(self.order_by, list):
            order_by_ranking = None
            for x in self.order_by:
                if x['columnName'] == 'ranking':
                    order_by_ranking = x['direction']
                    break
            orm_orderby = []
            for x in self.order_by:
                col_name = x['columnName']
                if col_name == 'ranking':
                    continue
                is_desc = x['direction'].lower() == 'desc'
                nulls_last = True
                order_field = F(col_name)
                empty_string_field_min_char_len = (
                    _special_empty_string_fields.get(col_name))
                if empty_string_field_min_char_len:
                    nulls_last = True
                    # Add a "length > min_char_len_for_field" field and sort it
                    # first. Note that we use a non-zero value for
                    # min_char_len_for_field because some fields uses a string
                    # ' ' to represent blank entries while some date fields use
                    # ',,' to represent a blank date.
                    count_field = 'count_' + col_name
                    isempty_field = 'isempty_' + col_name
                    q = q.annotate(**{count_field: Length(order_field)})
                    q = q.annotate(**{
                        isempty_field:
                            Case(
                                When(**{
                                    'then': Value(1),
                                    count_field + '__gt':
                                        empty_string_field_min_char_len
                                }),
                                default=Value(0),
                                output_field=IntegerField())})
                    orm_orderby.append('-' + isempty_field)
                    if 'date' in col_name:
                        # The date formats MM,DD,YYYY with possible blank
                        # values are very messy to sort. Here we add sorting by
                        # the last 4 characters to first sort by year (which is
                        # always present for non blank dates).
                        year_field = 'yearof_' + col_name
                        q = q.annotate(
                            **{
                                year_field:
                                Substr(order_field, 4 * Value(-1), 4)})
                        orm_orderby.append((
                            '-' if is_desc else '') + year_field)

                def add_names_sorting(sorted_name_fields, col_name, q,
                                      is_desc=is_desc):
                    # The next lines create a list made of the name fields with
                    # a separator constant value between each consecutive pair.
                    names_sep = Value(';')
                    names_concat = [names_sep] * \
                        (2 * len(sorted_name_fields) - 1)
                    names_concat[0::2] = sorted_name_fields
                    # We now properly handle
                    fallback_name_val = Value('AAAAA' if is_desc else 'ZZZZZ')
                    expressions = [
                        Coalesce(F(name_field),
                                 fallback_name_val,
                                 output_field=CharField())
                        for name_field in sorted_name_fields
                    ]
                    q = q.annotate(**{
                        col_name:
                            Func(*expressions,
                                 function='GREATEST' if is_desc else 'LEAST'
                                 )
                    })
                    order_field = F(col_name)
                    order_field = order_field.desc(
                    ) if is_desc else order_field.asc()
                    return q, order_field

                if col_name == 'names':
                    col_name = '_names_sort'
                    (q, order_field) = add_names_sorting(
                        _name_fields, col_name, q)
                    fields = fields + [col_name]
                elif col_name == 'modern_names':
                    col_name = '_modern_names_sort'
                    (q,
                     order_field) = add_names_sorting(_modern_name_fields,
                                                      col_name, q)
                    fields = fields + [col_name]
                elif is_desc:
                    order_field = order_field.desc(nulls_last=nulls_last)
                else:
                    order_field = order_field.asc(nulls_last=nulls_last)
                if order_field:
                    orm_orderby.append(order_field)
            if orm_orderby:
                q = q.order_by(*orm_orderby)
            else:
                q = q.order_by('enslaved_id')

        if self.skin_color:
            q = q.filter(skin_color__contains=self.skin_color)

        if self.SOURCES_LIST in fields:
            q = self.sources_helper.adapt_query(q)
        if self.ENSLAVERS_LIST in fields:
            q = self.enslavers_helper.adapt_query(q)

        if settings.DEBUG:
            print(q.query)

        q = q.values(*fields)
        if is_fuzzy:
            # Convert the QuerySet to a concrete list and include the ranking
            # as a member of each object in that list.
            q = list(q)
            for x in q:
                x['ranking'] = ranking[x['enslaved_id']]
            if order_by_ranking:
                q = sorted(q,
                           key=lambda x: x['ranking'],
                           reverse=(order_by_ranking == 'desc'))
        return q

    @classmethod
    def patch_row(cls, row):
        cls.sources_helper.patch_row(row)
        cls.enslavers_helper.patch_row(row)
