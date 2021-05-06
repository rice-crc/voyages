from __future__ import absolute_import, unicode_literals

import operator
import threading
import unicodedata
from builtins import range, str
from functools import reduce

from django.contrib.auth.models import User
from django.db import models
from django.db.models import (Case, CharField, F, Func, IntegerField, Q, Value,
                              When)
from django.db.models.functions import Coalesce, Length, Substr
import Levenshtein_search

from voyages.apps.voyage.models import Place, Voyage, VoyageSources

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


class ModernCountry(NamedModelAbstractBase):
    longitude = models.DecimalField("Longitude of Country",
                                    max_digits=10,
                                    decimal_places=7,
                                    null=False)
    latitude = models.DecimalField("Latitude of Country",
                                   max_digits=10,
                                   decimal_places=7,
                                   null=False)


class RegisterCountry(NamedModelAbstractBase):
    pass


class LanguageGroup(NamedModelAbstractBase):
    longitude = models.DecimalField("Longitude of point",
                                    max_digits=10,
                                    decimal_places=7,
                                    null=False)
    latitude = models.DecimalField("Latitude of point",
                                   max_digits=10,
                                   decimal_places=7,
                                   null=False)
    modern_country = models.ForeignKey(ModernCountry,
                                       null=False,
                                       related_name='language_groups',
                                       on_delete=models.CASCADE)


class AltLanguageGroupName(NamedModelAbstractBase):
    language_group = models.ForeignKey(LanguageGroup,
                                       null=False,
                                       related_name='alt_names',
                                       on_delete=models.CASCADE)


class Ethnicity(NamedModelAbstractBase):
    language_group = models.ForeignKey(LanguageGroup,
                                       null=False,
                                       related_name='ethnicities',
                                       on_delete=models.CASCADE)


class AltEthnicityName(NamedModelAbstractBase):
    ethnicity = models.ForeignKey(Ethnicity,
                                  null=False,
                                  related_name='alt_names',
                                  on_delete=models.CASCADE)


# TODO: this model will replace resources.AfricanName


class Enslaved(models.Model):
    """
    Enslaved person.
    """
    enslaved_id = models.IntegerField(primary_key=True)

    documented_name = models.CharField(max_length=25, blank=True)
    name_first = models.CharField(max_length=25, null=True, blank=True)
    name_second = models.CharField(max_length=25, null=True, blank=True)
    name_third = models.CharField(max_length=25, null=True, blank=True)

    modern_name_first = models.CharField(max_length=25, null=True, blank=True)
    modern_name_second = models.CharField(max_length=25, null=True, blank=True)
    modern_name_third = models.CharField(max_length=25, null=True, blank=True)

    editor_modern_names_certainty = models.CharField(max_length=255,
                                                     null=True,
                                                     blank=True)

    # Personal data
    age = models.IntegerField(null=True)
    # For some records, the exact age may be unknown and only
    # an adult/child status is determined.
    is_adult = models.NullBooleanField(null=True)
    gender = models.IntegerField(null=True)
    height = models.FloatField(null=True, verbose_name="Height in inches")

    # The ethnicity, language and country could be null.
    # The possibility of including 'Unknown' values in the
    # reference tables and using them instead of null was
    # proposed and discarded.
    ethnicity = models.ForeignKey(Ethnicity, null=True,
                                  on_delete=models.CASCADE)
    language_group = models.ForeignKey(LanguageGroup, null=True,
                                       on_delete=models.CASCADE)
    register_country = models.ForeignKey(RegisterCountry, null=True,
                                         on_delete=models.CASCADE)

    post_disembark_location = models.ForeignKey(Place, null=True,
                                                on_delete=models.CASCADE)

    voyage = models.ForeignKey(Voyage, null=False, on_delete=models.CASCADE)
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
    ethnicity = models.ForeignKey(Ethnicity, null=True,
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


_special_empty_string_fields = {
    'voyage__voyage_ship__ship_name': 1,
    'voyage__voyage_dates__first_dis_of_slaves': '2'
}

_name_fields = ['documented_name', 'name_first', 'name_second', 'name_third']
_modern_name_fields = [
    'modern_name_first', 'modern_name_second', 'modern_name_third'
]


class EnslavedSearch:
    """
    Search parameters for enslaved persons.
    """

    def __init__(self,
                 searched_name=None,
                 exact_name_search=False,
                 age_gender=None,
                 age_range=None,
                 height_range=None,
                 year_range=None,
                 embarkation_ports=None,
                 disembarkation_ports=None,
                 post_disembark_location=None,
                 language_groups=None,
                 modern_country=None,
                 ship_name=None,
                 voyage_id=None,
                 enslaved_id=None,
                 source=None,
                 order_by=None,
                 dataset=None):
        """
        Search the Enslaved database. If a parameter is set to None, it will
        not be included in the search.
        @param: searched_name A name string to be searched
        @param: exact_name_search Boolean indicating whether the search is
                exact or fuzzy
        @param: age_gender A list of pairs (bool is_adult, male = 1/female = 2)
                with all combinations filtered.
        @param: age_range A pair (a, b) where a is the min and b is maximum age
        @param: dataset A list of datasets
        @param: height_range A pair (a, b) where a is the min and b is maximum
                height
        @param: is_adult Whether the search is for adults or children only
        @param: year_range A pair (a, b) where a is the min voyage year and b
                the max
        @param: embarkation_ports A list of port ids where the enslaved
                embarked
        @param: disembarkation_ports A list of port ids where the enslaved
                disembarked
        @param: post_disembark_location A list of place ids where the enslaved
                was located after disembarkation
        @param: language_groups A list of language groups ids for the enslaved
        @param: modern_country A list of country ids
        @param: ship_name The ship name that the enslaved embarked
        @param: voyage_id A pair (a, b) where the a <= voyage_id <= b
        @param: enslaved_id A pair (a, b) where the a <= enslaved_id <= b
        @param: source A text fragment that should match Source's text_ref or
                full_ref
        @param: order_by An array of dicts {
                'columnName': 'NAME', 'direction': 'ASC or DESC' }.
                Note that if the search is fuzzy, then the fallback value of
                order_by is the ranking of the fuzzy search.
        """
        self.searched_name = searched_name
        self.exact_name_search = exact_name_search
        self.age_gender = age_gender
        self.age_range = age_range
        self.height_range = height_range
        self.year_range = year_range
        self.embarkation_ports = embarkation_ports
        self.disembarkation_ports = disembarkation_ports
        self.post_disembark_location = post_disembark_location
        self.language_groups = language_groups
        self.modern_country = modern_country
        self.ship_name = ship_name
        self.voyage_id = voyage_id
        self.enslaved_id = enslaved_id
        self.source = source
        self.order_by = order_by
        self.dataset = dataset

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
            .select_related('ethnicity') \
            .select_related('language_group') \
            .select_related('language_group__modern_country') \
            .select_related('voyage__voyage_dates') \
            .select_related('voyage__voyage_ship') \
            .select_related('voyage__voyage_itinerary__int_first_port_dis') \
            .select_related('voyage__voyage_itinerary_'
                            '_imp_principal_place_of_slave_purchase') \
            .select_related('voyage__voyage_itinerary_'
                            '_imp_principal_port_slave_dis') \
            .select_related('register_country') \
            .all()
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
        if self.age_gender:

            def get_ag_query(x):
                if x == 'male':
                    return Q(gender=1)
                if x == 'female':
                    return Q(gender=2)
                if x == 'man':
                    return Q(is_adult=True, gender=1)
                if x == 'woman':
                    return Q(is_adult=True, gender=2)
                if x == 'boy':
                    return Q(is_adult=False, gender=1)
                if x == 'girl':
                    return Q(is_adult=False, gender=2)
                raise Exception('Invalid AgeGender value')

            conditions = [get_ag_query(x) for x in self.age_gender]
            q = q.filter(reduce(operator.or_, conditions))
        if self.dataset:

            def get_dataset_query(x):
                if x == 'trans':
                    return Q(voyage__dataset=0)
                if x == 'intra':
                    return Q(voyage__dataset=1)
                if x == 'african':
                    return Q(voyage__dataset=2)
                raise Exception('Invalid Dataset value')

            conditions = [get_dataset_query(x) for x in self.dataset]
            q = q.filter(reduce(operator.or_, conditions))
        if self.age_range:
            q = q.filter(age__range=self.age_range)
        if self.height_range:
            q = q.filter(height__range=self.height_range)
        if self.modern_country:
            q = q.filter(
                language_group__modern_country__pk__in=self.modern_country)
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
                orm_orderby.append(order_field)
            q = q.order_by(*orm_orderby)
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
