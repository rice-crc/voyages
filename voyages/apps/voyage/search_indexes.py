from __future__ import division
from haystack import indexes
from .models import *
from datetime import date
from django.utils import translation
from django.utils.translation import ugettext as _
import re

def getMonth(value):
    return str(value.split(",")[0]).zfill(2)


def getDay(value):
    return str(value.split(",")[1]).zfill(2)


def getYear(value):
    return str(value.split(",")[2]).zfill(2)

def getDate(value):
    if not value:
        return value
    month = getMonth(value)
    if not month or month == "" or int(month) == 0:
        month = 1
    day = getDay(value)
    if not day or day == "" or int(day) == 0:
        day = 1
    year = getYear(value)
    return mkdate(int(year), int(month), int(day))

def mkdate(year, month, day):
    try:
        return date(year, month, day)
    except ValueError:
        print("Warning attempting to estimate invalid date, Day: " + day + " Month: " + month + " Year: " + year)
        if month > 12:
            return mkdate(year, 12, day)
        elif day > 1:
            return mkdate(year, month, day-1)
        else:
            print("Error with date Day: " + day + " Month: " + month + " Year: " + year)
            return date(year, month, day)

# Index for Sources
class VoyageSourcesIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Index method for class Voyage.
    """
    text = indexes.CharField(document=True, use_template=True)

    short_ref = indexes.CharField(model_attr='short_ref', null=True)
    full_ref = indexes.CharField(model_attr='full_ref', null=True)
    group_id = indexes.IntegerField()
    group_name = indexes.CharField()

    def get_model(self):
        return VoyageSources

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_group_id(self, obj):
        return obj.source_type.group_id

    def prepare_group_name(self, obj):
        return obj.source_type.group_name

class TranslatedTextField(indexes.SearchField):
    field_type = 'string'

    # Regular expression that extracts name and language code from the index declaration.
    re_translated_fieldname = re.compile('(.*)_lang_([a-z]{2})$')

    def __init__(self, unidecode=True, **kwargs):
        kwargs['faceted'] = True
        self.language_code = None
        self.unidecode = unidecode
        super(TranslatedTextField, self).__init__(**kwargs)

    def set_instance_name(self, instance_name):
        super(TranslatedTextField, self).set_instance_name(instance_name)
        if instance_name is not None:
            m = self.re_translated_fieldname.search(instance_name)
            if m is None:
                raise Exception('Invalid index field name for TranslatedTextField')
            self.language_code = m.group(2)

    def prepare(self, obj):
        original = super(TranslatedTextField, self).prepare(obj)
        if original is None:
            return None
        with translation.override(self.language_code):
            translated = _(unicode(original).replace('\n', '').replace('\r', ''))
            if not self.unidecode:
                return translated
            from unidecode import unidecode
            return unidecode(translated)

class RelatedModelIndexMixin(object):
    def __init__(self, related_model, *args, **kwargs):
        super(RelatedModelIndexMixin, self).__init__(*args, **kwargs)
        self.related_model = related_model

    def prepare(self, obj):
        try:
            related = self.related_model.objects.filter(voyage=obj)
            if len(related) == 1:
                return super(RelatedModelIndexMixin, self).prepare(related[0])
        except Exception:
            pass
        if self.has_default():
            return self.default
        else:
            return None

class RelatedCharField(RelatedModelIndexMixin, indexes.CharField):
    pass

class RelatedIntegerField(RelatedModelIndexMixin, indexes.IntegerField):
    pass

class RelatedTranslatedTextField(RelatedModelIndexMixin, TranslatedTextField):
    pass

# Index for Voyage
class VoyageIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Index method for class Voyage.
    """
    text = indexes.CharField(document=True, use_template=True)

    var_imp_voyage_began = indexes.IntegerField(null=True)

    var_voyage_id = indexes.IntegerField(null=True, model_attr='voyage_id')
    var_voyage_in_cd_rom = indexes.BooleanField(null=True, model_attr="voyage_in_cd_rom")
    var_ship_name = indexes.NgramField(null=True, model_attr='voyage_ship__ship_name')
    var_ship_name_plaintext = indexes.CharField(null=True, faceted=True, indexed=True, model_attr='voyage_ship__ship_name')
    var_nationality = indexes.CharField(null=True, model_attr='voyage_ship__nationality_ship__label')
    var_nationality_plaintext = indexes.CharField(null=True, faceted=True, model_attr='voyage_ship__nationality_ship__label')
    var_imputed_nationality = indexes.CharField(null=True, model_attr='voyage_ship__imputed_nationality__label')
    var_imputed_nationality_plaintext = indexes.CharField(null=True, faceted=True, model_attr='voyage_ship__imputed_nationality__label')
    var_vessel_construction_place = indexes.CharField(null=True, model_attr='voyage_ship__vessel_construction_place__place')
    var_vessel_construction_place_lang_en = TranslatedTextField(null=True, model_attr='voyage_ship__vessel_construction_place__place')
    var_vessel_construction_place_lang_pt = TranslatedTextField(null=True, model_attr='voyage_ship__vessel_construction_place__place')
    var_year_of_construction = indexes.IntegerField(null=True, model_attr='voyage_ship__year_of_construction')
    var_registered_place = indexes.CharField(null=True, model_attr='voyage_ship__registered_place__place')
    var_registered_place_lang_en = TranslatedTextField(null=True, model_attr='voyage_ship__registered_place__place')
    var_registered_place_lang_pt = TranslatedTextField(null=True, model_attr='voyage_ship__registered_place__place')
    var_registered_year = indexes.IntegerField(null=True, model_attr='voyage_ship__registered_year')
    var_rig_of_vessel = indexes.CharField(null=True, model_attr='voyage_ship__rig_of_vessel__label')
    var_rig_of_vessel_plaintext = indexes.CharField(null=True, faceted=True, model_attr='voyage_ship__rig_of_vessel__label')
    var_tonnage = indexes.FloatField(null=True, faceted=True, model_attr='voyage_ship__tonnage')
    var_tonnage_mod = indexes.FloatField(null=True, model_attr='voyage_ship__tonnage_mod')
    var_guns_mounted = indexes.IntegerField(null=True, model_attr='voyage_ship__guns_mounted')
    var_owner = indexes.NgramField(null=True)
    var_owner_plaintext = indexes.CharField(null=True, faceted=True)

    var_nationality_idnum = indexes.IntegerField(null=True, model_attr='voyage_ship__nationality_ship__value')
    var_imputed_nationality_idnum = indexes.IntegerField(null=True, model_attr='voyage_ship__imputed_nationality__value')
    var_vessel_construction_place_idnum = indexes.IntegerField(null=True, model_attr='voyage_ship__vessel_construction_place__value')
    var_registered_place_idnum = indexes.IntegerField(null=True, model_attr='voyage_ship__registered_place__value')
    var_rig_of_vessel_idnum = indexes.IntegerField(null=True, model_attr='voyage_ship__rig_of_vessel__value')

    # Voyage Outcome
    var_outcome_voyage = RelatedCharField(null=True, related_model=VoyageOutcome, model_attr='particular_outcome__label')
    var_outcome_voyage_lang_en = RelatedTranslatedTextField(null=True, related_model=VoyageOutcome, model_attr='particular_outcome__label')
    var_outcome_voyage_lang_pt = RelatedTranslatedTextField(null=True, related_model=VoyageOutcome, model_attr='particular_outcome__label')
    var_outcome_slaves = RelatedCharField(null=True, related_model=VoyageOutcome, model_attr='outcome_slaves__label')
    var_outcome_slaves_lang_en = RelatedTranslatedTextField(null=True, related_model=VoyageOutcome, model_attr='outcome_slaves__label')
    var_outcome_slaves_lang_pt = RelatedTranslatedTextField(null=True, related_model=VoyageOutcome, model_attr='outcome_slaves__label')
    var_outcome_ship_captured = RelatedCharField(null=True, related_model=VoyageOutcome, model_attr='vessel_captured_outcome__label')
    var_outcome_ship_captured_lang_en = RelatedTranslatedTextField(null=True, related_model=VoyageOutcome, model_attr='vessel_captured_outcome__label')
    var_outcome_ship_captured_lang_pt = RelatedTranslatedTextField(null=True, related_model=VoyageOutcome, model_attr='vessel_captured_outcome__label')
    var_outcome_owner = RelatedCharField(null=True, related_model=VoyageOutcome, model_attr='outcome_owner__label')
    var_outcome_owner_lang_en = RelatedTranslatedTextField(null=True, related_model=VoyageOutcome, model_attr='outcome_owner__label')
    var_outcome_owner_lang_pt = RelatedTranslatedTextField(null=True, related_model=VoyageOutcome, model_attr='outcome_owner__label')
    var_resistance = RelatedCharField(null=True, related_model=VoyageOutcome, model_attr='resistance__label')
    var_resistance_lang_en = RelatedTranslatedTextField(null=True, related_model=VoyageOutcome, model_attr='resistance__label')
    var_resistance_lang_pt = RelatedTranslatedTextField(null=True, related_model=VoyageOutcome, model_attr='resistance__label')

    var_outcome_voyage_idnum = RelatedIntegerField(null=True, related_model=VoyageOutcome, model_attr='particular_outcome__value')
    var_outcome_slaves_idnum = RelatedIntegerField(null=True, related_model=VoyageOutcome, model_attr='outcome_slaves__value')
    var_outcome_ship_captured_idnum = RelatedIntegerField(null=True, related_model=VoyageOutcome, model_attr='vessel_captured_outcome__value')
    var_outcome_owner_idnum = RelatedIntegerField(null=True, related_model=VoyageOutcome, model_attr='outcome_owner__value')
    var_resistance_idnum = RelatedIntegerField(null=True, related_model=VoyageOutcome, model_attr='resistance__value')

    # Voyage itinerary
    var_imp_port_voyage_begin = indexes.CharField(null=True, model_attr='voyage_itinerary__imp_port_voyage_begin__place')
    var_imp_port_voyage_begin_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__imp_port_voyage_begin__place')
    var_imp_port_voyage_begin_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__imp_port_voyage_begin__place')
    var_first_place_slave_purchase = indexes.CharField(null=True, model_attr='voyage_itinerary__first_place_slave_purchase__place')
    var_first_place_slave_purchase_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__first_place_slave_purchase__place')
    var_first_place_slave_purchase_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__first_place_slave_purchase__place')
    var_second_place_slave_purchase = indexes.CharField(null=True, model_attr='voyage_itinerary__second_place_slave_purchase__place')
    var_second_place_slave_purchase_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__second_place_slave_purchase__place')
    var_second_place_slave_purchase_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__second_place_slave_purchase__place')
    var_third_place_slave_purchase = indexes.CharField(null=True, model_attr='voyage_itinerary__third_place_slave_purchase__place')
    var_third_place_slave_purchase_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__third_place_slave_purchase__place')
    var_third_place_slave_purchase_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__third_place_slave_purchase__place')
    var_imp_principal_place_of_slave_purchase = indexes.CharField(null=True, model_attr='voyage_itinerary__imp_principal_place_of_slave_purchase__place')
    var_imp_principal_place_of_slave_purchase_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__imp_principal_place_of_slave_purchase__place')
    var_imp_principal_place_of_slave_purchase_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__imp_principal_place_of_slave_purchase__place')
    var_port_of_call_before_atl_crossing = indexes.NgramField(null=True, model_attr='voyage_itinerary__port_of_call_before_atl_crossing__place')
    var_port_of_call_before_atl_crossing_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__port_of_call_before_atl_crossing__place')
    var_port_of_call_before_atl_crossing_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__port_of_call_before_atl_crossing__place')
    var_first_landing_place = indexes.CharField(null=True, model_attr='voyage_itinerary__first_landing_place__place')
    var_first_landing_place_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__first_landing_place__place')
    var_first_landing_place_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__first_landing_place__place')
    var_second_landing_place = indexes.CharField(null=True, model_attr='voyage_itinerary__second_landing_place__place')
    var_second_landing_place_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__second_landing_place__place')
    var_second_landing_place_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__second_landing_place__place')
    var_third_landing_place = indexes.CharField(null=True, model_attr='voyage_itinerary__third_landing_place__place')
    var_third_landing_place_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__third_landing_place__place')
    var_third_landing_place_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__third_landing_place__place')
    var_imp_principal_port_slave_dis = indexes.NgramField(null=True, model_attr='voyage_itinerary__imp_principal_port_slave_dis__place')
    var_imp_principal_port_slave_dis_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__imp_principal_port_slave_dis__place')
    var_imp_principal_port_slave_dis_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__imp_principal_port_slave_dis__place')
    var_place_voyage_ended = indexes.CharField(null=True, model_attr='voyage_itinerary__place_voyage_ended__place')
    var_place_voyage_ended_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__place_voyage_ended__place')
    var_place_voyage_ended_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__place_voyage_ended__place')

    var_imp_port_voyage_begin_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__imp_port_voyage_begin__value')
    var_first_place_slave_purchase_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__first_place_slave_purchase__value')
    var_second_place_slave_purchase_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__second_place_slave_purchase__value')
    var_third_place_slave_purchase_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__third_place_slave_purchase__value')
    var_imp_principal_place_of_slave_purchase_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__imp_principal_place_of_slave_purchase__value')
    var_port_of_call_before_atl_crossing_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__port_of_call_before_atl_crossing__value')
    var_first_landing_place_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__first_landing_place__value')
    var_second_landing_place_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__second_landing_place__value')
    var_third_landing_place_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__third_landing_place__value')
    var_imp_principal_port_slave_dis_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__imp_principal_port_slave_dis__value')
    var_place_voyage_ended_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__place_voyage_ended__value')

    ## Region variables
    var_imp_region_voyage_begin = indexes.CharField(null=True, model_attr='voyage_itinerary__imp_region_voyage_begin__region')
    var_imp_region_voyage_begin_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__imp_region_voyage_begin__region')
    var_imp_region_voyage_begin_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__imp_region_voyage_begin__region')
    var_first_region_slave_emb = indexes.CharField(null=True, model_attr='voyage_itinerary__first_region_slave_emb__region')
    var_first_region_slave_emb_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__first_region_slave_emb__region')
    var_first_region_slave_emb_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__first_region_slave_emb__region')
    var_second_region_slave_emb = indexes.CharField(null=True, model_attr='voyage_itinerary__second_region_slave_emb__region')
    var_second_region_slave_emb_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__second_region_slave_emb__region')
    var_second_region_slave_emb_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__second_region_slave_emb__region')
    var_third_region_slave_emb = indexes.CharField(null=True, model_attr='voyage_itinerary__third_region_slave_emb__region')
    var_third_region_slave_emb_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__third_region_slave_emb__region')
    var_third_region_slave_emb_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__third_region_slave_emb__region')
    var_imp_principal_region_of_slave_purchase = indexes.CharField(null=True, model_attr='voyage_itinerary__imp_principal_region_of_slave_purchase__region')
    var_imp_principal_region_of_slave_purchase_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__imp_principal_region_of_slave_purchase__region')
    var_imp_principal_region_of_slave_purchase_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__imp_principal_region_of_slave_purchase__region')
    var_first_landing_region = indexes.CharField(null=True, model_attr='voyage_itinerary__first_landing_region__region')
    var_first_landing_region_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__first_landing_region__region')
    var_first_landing_region_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__first_landing_region__region')
    var_second_landing_region = indexes.CharField(null=True, model_attr='voyage_itinerary__second_landing_region__region')
    var_second_landing_region_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__second_landing_region__region')
    var_second_landing_region_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__second_landing_region__region')
    var_third_landing_region = indexes.CharField(null=True, model_attr='voyage_itinerary__third_landing_region__region')
    var_third_landing_region_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__third_landing_region__region')
    var_third_landing_region_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__third_landing_region__region')
    var_imp_principal_region_slave_dis = indexes.CharField(null=True, model_attr='voyage_itinerary__imp_principal_region_slave_dis__region')
    var_imp_principal_region_slave_dis_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__imp_principal_region_slave_dis__region')
    var_imp_principal_region_slave_dis_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__imp_principal_region_slave_dis__region')
    var_region_voyage_ended = indexes.CharField(null=True, model_attr='voyage_itinerary__place_voyage_ended__region')
    var_region_voyage_ended_lang_en = TranslatedTextField(null=True, model_attr='voyage_itinerary__place_voyage_ended__region')
    var_region_voyage_ended_lang_pt = TranslatedTextField(null=True, model_attr='voyage_itinerary__place_voyage_ended__region')

    var_imp_region_voyage_begin_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__imp_region_voyage_begin__value')
    var_first_region_slave_emb_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__first_region_slave_emb__value')
    var_second_region_slave_emb_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__second_region_slave_emb__value')
    var_third_region_slave_emb_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__third_region_slave_emb__value')
    var_imp_principal_region_of_slave_purchase_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__imp_principal_region_of_slave_purchase__value')
    var_first_landing_region_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__first_landing_region__value')
    var_second_landing_region_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__second_landing_region__value')
    var_imp_principal_region_slave_dis_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__imp_principal_region_slave_dis__value')
    var_region_voyage_ended_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__place_voyage_ended__region__value')

    # Broad Region variables

    var_imp_principal_broad_region_disembark_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__imp_broad_region_slave_dis__value')
    var_imp_broad_region_voyage_begin_idnum = indexes.IntegerField(null=True, model_attr='voyage_itinerary__imp_broad_region_voyage_begin__value')

    # Voyage captain and crew
    var_captain = indexes.NgramField(null=True)
    var_captain_plaintext = indexes.CharField(null=True, faceted=True, indexed=True)
    var_crew_voyage_outset = indexes.IntegerField(null=True, model_attr='voyage_crew__crew_voyage_outset')
    var_crew_first_landing = indexes.IntegerField(null=True, model_attr='voyage_crew__crew_first_landing')
    var_crew_died_complete_voyage = indexes.IntegerField(null=True, model_attr='voyage_crew__crew_died_complete_voyage')

    # Voyage dates
    # Month field is used for filtering by month
    var_imp_arrival_at_port_of_dis = indexes.IntegerField(null=True, faceted=True)
    var_voyage_began = indexes.DateField(null=True)
    var_voyage_began_month = indexes.IntegerField(null=True)
    var_slave_purchase_began = indexes.DateField(null=True)
    var_slave_purchase_began_month = indexes.IntegerField(null=True)
    var_date_departed_africa = indexes.DateField(null=True)
    var_date_departed_africa_month = indexes.IntegerField(null=True)
    var_first_dis_of_slaves = indexes.DateField(null=True)
    var_first_dis_of_slaves_month = indexes.IntegerField(null=True)
    var_departure_last_place_of_landing = indexes.DateField(null=True)
    var_departure_last_place_of_landing_month = indexes.IntegerField(null=True)
    var_voyage_completed = indexes.DateField(null=True)
    var_voyage_completed_month = indexes.IntegerField(null=True)

    var_imp_length_home_to_disembark = indexes.IntegerField(null=True)
    var_length_middle_passage_days = indexes.IntegerField(null=True, faceted=True)

    # Voyage numbers
    var_num_slaves_intended_first_port = indexes.IntegerField(null=True, model_attr='voyage_slaves_numbers__num_slaves_intended_first_port')
    var_num_slaves_carried_first_port = indexes.IntegerField(null=True, model_attr='voyage_slaves_numbers__num_slaves_carried_first_port')
    var_num_slaves_carried_second_port = indexes.IntegerField(null=True, model_attr='voyage_slaves_numbers__num_slaves_carried_second_port')
    var_num_slaves_carried_third_port = indexes.IntegerField(null=True, model_attr='voyage_slaves_numbers__num_slaves_carried_third_port')
    # To be corrected (copied from previous comment)
    var_total_num_slaves_purchased = indexes.IntegerField(null=True, faceted=True, model_attr='voyage_slaves_numbers__total_num_slaves_dep_last_slaving_port')
    # To be corrected (copied from previous comment)
    var_imp_total_num_slaves_purchased = indexes.IntegerField(null=True, faceted=True, model_attr='voyage_slaves_numbers__imp_total_num_slaves_embarked')
    var_total_num_slaves_arr_first_port_embark = indexes.IntegerField(null=True, model_attr='voyage_slaves_numbers__total_num_slaves_arr_first_port_embark')
    var_num_slaves_disembark_first_place = indexes.IntegerField(null=True, model_attr='voyage_slaves_numbers__num_slaves_disembark_first_place')
    var_num_slaves_disembark_second_place = indexes.IntegerField(null=True, model_attr='voyage_slaves_numbers__num_slaves_disembark_second_place')
    var_num_slaves_disembark_third_place = indexes.IntegerField(null=True, model_attr='voyage_slaves_numbers__num_slaves_disembark_third_place')
    var_imp_total_slaves_disembarked = indexes.IntegerField(null=True, faceted=True, model_attr='voyage_slaves_numbers__imp_total_num_slaves_disembarked')

    # Voyage characteristics
    var_imputed_percentage_men = indexes.FloatField(null=True, model_attr='voyage_slaves_numbers__percentage_men')
    var_imputed_percentage_women = indexes.FloatField(null=True, model_attr='voyage_slaves_numbers__percentage_women')
    var_imputed_percentage_boys = indexes.FloatField(null=True, model_attr='voyage_slaves_numbers__percentage_boy')
    var_imputed_percentage_girls = indexes.FloatField(null=True, model_attr='voyage_slaves_numbers__percentage_girl')
    var_imputed_percentage_female = indexes.FloatField(null=True, model_attr='voyage_slaves_numbers__percentage_female')
    var_imputed_percentage_male = indexes.FloatField(null=True, faceted=True, model_attr='voyage_slaves_numbers__percentage_male')
    var_imputed_percentage_child = indexes.FloatField(null=True, faceted=True, model_attr='voyage_slaves_numbers__percentage_child')
    var_imputed_sterling_cash = indexes.FloatField(null=True, model_attr='voyage_slaves_numbers__imp_jamaican_cash_price')
    var_imputed_death_middle_passage = indexes.IntegerField(null=True, model_attr='voyage_slaves_numbers__imp_mortality_during_voyage')
    var_imputed_mortality = indexes.FloatField(null=True, faceted=True, model_attr='voyage_slaves_numbers__imp_mortality_ratio')

    # Sources
    var_sources = indexes.MultiValueField(indexed=True, stored=True, null=True)
    var_sources_plaintext = indexes.CharField(null=True, faceted=True, indexed=True)
    var_short_ref = indexes.MultiValueField()
    var_long_ref = indexes.CharField(null=True)

    def get_model(self):
        return Voyage

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_var_imp_voyage_began(self, obj):
        try:
            return getYear(obj.voyage_dates.imp_voyage_began)
        except AttributeError, TypeError:
            return None

    def prepare_var_owner(self, obj):
        try:
            return '<br/> '.join(
                [connection.owner.name for connection in VoyageShipOwnerConnection.objects.filter(voyage=obj)])
        except AttributeError:
            return None

    def prepare_var_owner_plaintext(self, obj):
        return self.prepare_var_owner(obj)

    # Voyage dates
    def prepare_var_imp_arrival_at_port_of_dis(self, obj):
        try:
            return int(getYear(obj.voyage_dates.imp_arrival_at_port_of_dis))
        except (AttributeError, TypeError):
            return None

    def prepare_var_voyage_began(self, obj):
        try:
            data = obj.voyage_dates.voyage_began
            if data == ',,' or len(data) == 0:
                return None
            else:
                return getDate(data)
        except (AttributeError, TypeError):
            return None
    def prepare_var_voyage_began_month(self, obj):
        try:
            data = getMonth(obj.voyage_dates.voyage_began)
            if data == ',,' or data == '' or len(data) == 0 or int(data) == 0:
                return None
            else:
                return data
        except (AttributeError, TypeError):
            return None

    def prepare_var_slave_purchase_began(self, obj):
        try:
            data = obj.voyage_dates.slave_purchase_began
            if data == ',,' or len(data) == 0:
                return None
            else:
                return getDate(data)
        except (AttributeError, TypeError):
            return None
    def prepare_var_slave_purchase_began_month(self, obj):
        try:
            data = getMonth(obj.voyage_dates.slave_purchase_began)
            if data == ',,' or data == '' or len(data) == 0 or int(data) == 0:
                return None
            else:
                return data
        except (AttributeError, TypeError):
            return None

    # departed Africa
    def prepare_var_date_departed_africa(self, obj):
        try:
            data = obj.voyage_dates.date_departed_africa
            if data == ',,' or len(data) == 0:
                return None
            else:
                return getDate(data)
        except (AttributeError, TypeError):
            return None
    def prepare_var_date_departed_africa_month(self, obj):
        try:
            data = getMonth(obj.voyage_dates.date_departed_africa)
            if data == ',,' or data == '' or len(data) == 0 or int(data) == 0:
                return None
            else:
                return data
        except (AttributeError, TypeError):
            return None

    def prepare_var_first_dis_of_slaves(self, obj):
        try:
            data = obj.voyage_dates.first_dis_of_slaves
            if data == ',,' or len(data) == 0:
                return None
            else:
                return getDate(data)
        except (AttributeError, TypeError):
            return None
    def prepare_var_first_dis_of_slaves_month(self, obj):
        try:
            data = getMonth(obj.voyage_dates.first_dis_of_slaves)
            if data == ',,' or data == '' or len(data) == 0 or int(data) == 0:
                return None
            else:
                return data
        except (AttributeError, TypeError):
            return None

    def prepare_var_departure_last_place_of_landing(self, obj):
        try:
            data = obj.voyage_dates.departure_last_place_of_landing
            if data == ',,' or len(data) == 0:
                return None
            else:
                return getDate(data)
        except (AttributeError, TypeError):
            return None
    def prepare_var_departure_last_place_of_landing_month(self, obj):
        try:
            data = getMonth(obj.voyage_dates.departure_last_place_of_landing)
            if data == ',,' or data == '' or len(data) == 0 or int(data) == 0:
                return None
            else:
                return data
        except (AttributeError, TypeError):
            return None

    def prepare_var_voyage_completed(self, obj):
        try:
            data = obj.voyage_dates.voyage_completed
            if data == ',,' or len(data) == 0:
                return None
            else:
                return getDate(data)
        except (AttributeError, TypeError):
            return None
    def prepare_var_voyage_completed_month(self, obj):
        try:
            data = getMonth(obj.voyage_dates.voyage_completed)
            if data == ',,' or data == '' or len(data) == 0 or int(data) == 0:
                return None
            else:
                return data
        except (AttributeError, TypeError):
            return None

    def prepare_var_imp_length_home_to_disembark(self, obj):
        try:
            return obj.voyage_dates.imp_length_home_to_disembark
        except AttributeError:
            return None

    def prepare_var_length_middle_passage_days(self, obj):
        try:
            return obj.voyage_dates.imp_length_leaving_africa_to_disembark
        except AttributeError:
            return None

    # Voyage crew
    def prepare_var_captain(self, obj):
        return '<br/> '.join(
            [connection.captain.name for connection in VoyageCaptainConnection.objects.filter(voyage=obj)])

    def prepare_var_captain_plaintext(self, obj):
        return self.prepare_var_captain(obj)

    # Voyage sources
    def prepare_var_sources(self, obj):
        result = []
        for connection in VoyageSourcesConnection.objects.filter(group=obj):
            fr = ""
            if connection.source is not None:
                fr = connection.source.full_ref
            result.append(connection.text_ref + "<>" + fr)
        return result

    def prepare_var_sources_plaintext(self, obj):
        return ", ".join(self.prepare_var_sources(obj))
