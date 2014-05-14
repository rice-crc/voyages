from __future__ import division
from haystack import indexes
from .models import *
from datetime import date


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
        month = None
    day = getDay(value)
    if not day or day == "" or int(day) == 0:
        day = None
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
        elif not month or not day:
            return None
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


# Index for Voyage
class VoyageIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Index method for class Voyage.
    """
    text = indexes.CharField(document=True, use_template=True)

    var_imp_voyage_began = indexes.IntegerField(null=True)

    var_voyage_id = indexes.IntegerField(null=True)
    var_voyage_in_cd_rom = indexes.BooleanField(model_attr="voyage_in_cd_rom", null=True)
    var_ship_name = indexes.NgramField(null=True)
    var_nationality = indexes.CharField(null=True)
    var_imputed_nationality = indexes.CharField(null=True)
    var_vessel_construction_place = indexes.CharField(null=True)
    var_year_of_construction = indexes.IntegerField(null=True)
    var_registered_place = indexes.CharField(null=True)
    var_registered_year = indexes.IntegerField(null=True)
    var_rig_of_vessel = indexes.CharField(null=True)
    var_tonnage = indexes.FloatField(null=True, faceted=True)
    var_tonnage_mod = indexes.FloatField(null=True)
    var_guns_mounted = indexes.IntegerField(null=True)
    var_owner = indexes.NgramField(null=True)

    var_nationality_idnum = indexes.IntegerField(null=True)
    var_imputed_nationality_idnum = indexes.IntegerField(null=True)
    var_vessel_construction_place_idnum = indexes.IntegerField(null=True)
    var_registered_place_idnum = indexes.IntegerField(null=True)
    var_rig_of_vessel_idnum = indexes.IntegerField(null=True)

    # Voyage Outcome
    var_outcome_voyage = indexes.CharField(null=True)
    var_outcome_slaves = indexes.CharField(null=True)
    var_outcome_ship_captured = indexes.CharField(null=True)
    var_outcome_owner = indexes.CharField(null=True)
    var_resistance = indexes.CharField(null=True)
    
    var_outcome_voyage_idnum = indexes.IntegerField(null=True)
    var_outcome_slaves_idnum = indexes.IntegerField(null=True)
    var_outcome_ship_captured_idnum = indexes.IntegerField(null=True)
    var_outcome_owner_idnum = indexes.IntegerField(null=True)
    var_resistance_idnum = indexes.IntegerField(null=True)

    # Voyage itinerary
    var_imp_port_voyage_begin = indexes.CharField(null=True)

    var_first_place_slave_purchase = indexes.CharField(null=True)
    var_second_place_slave_purchase = indexes.CharField(null=True)
    var_third_place_slave_purchase = indexes.CharField(null=True)

    var_imp_principal_place_of_slave_purchase = indexes.CharField(null=True)

    var_port_of_call_before_atl_crossing = indexes.NgramField(null=True)

    var_first_landing_place = indexes.CharField(null=True)
    var_second_landing_place = indexes.CharField(null=True)
    var_third_landing_place = indexes.CharField(null=True)

    var_imp_principal_port_slave_dis = indexes.NgramField(null=True)
    var_place_voyage_ended = indexes.CharField(null=True)
    
    var_imp_port_voyage_begin_idnum = indexes.IntegerField(null=True)
    var_first_place_slave_purchase_idnum = indexes.IntegerField(null=True)
    var_second_place_slave_purchase_idnum = indexes.IntegerField(null=True)
    var_third_place_slave_purchase_idnum = indexes.IntegerField(null=True)
    var_imp_principal_place_of_slave_purchase_idnum = indexes.IntegerField(null=True)
    var_port_of_call_before_atl_crossing_idnum = indexes.IntegerField(null=True)
    var_first_landing_place_idnum = indexes.IntegerField(null=True)
    var_second_landing_place_idnum = indexes.IntegerField(null=True)
    var_third_landing_place_idnum = indexes.IntegerField(null=True)
    var_imp_principal_port_slave_dis_idnum = indexes.IntegerField(null=True)
    var_place_voyage_ended_idnum = indexes.IntegerField(null=True)

    ## Region variables
    var_imp_region_voyage_begin = indexes.CharField(null=True)

    var_first_region_slave_emb = indexes.CharField(null=True)
    var_second_region_slave_emb = indexes.CharField(null=True)
    var_third_region_slave_emb = indexes.CharField(null=True)

    var_imp_principal_region_of_slave_purchase = indexes.CharField(null=True)

    var_first_landing_region = indexes.CharField(null=True)
    var_second_landing_region = indexes.CharField(null=True)
    var_third_landing_region = indexes.CharField(null=True)

    var_imp_principal_region_slave_dis = indexes.CharField(null=True)

    var_region_voyage_ended = indexes.CharField(null=True)

    var_imp_region_voyage_begin_idnum = indexes.IntegerField(null=True)
    var_first_region_slave_emb_idnum = indexes.IntegerField(null=True)
    var_second_region_slave_emb_idnum = indexes.IntegerField(null=True)
    var_third_region_slave_emb_idnum = indexes.IntegerField(null=True)
    var_imp_principal_region_of_slave_purchase_idnum = indexes.IntegerField(null=True)
    var_first_landing_region_idnum = indexes.IntegerField(null=True)
    var_second_landing_region_idnum = indexes.IntegerField(null=True)
    var_imp_principal_region_slave_dis_idnum = indexes.IntegerField(null=True)
    var_region_voyage_ended_idnum = indexes.IntegerField(null=True)

    # Broad Region variables
    
    var_imp_principal_broad_region_disembark_idnum = indexes.IntegerField(null=True)
    var_imp_broad_region_voyage_begin_idnum = indexes.IntegerField(null=True)

    # Voyage captain and crew
    var_captain = indexes.NgramField(null=True)
    var_crew_voyage_outset = indexes.IntegerField(null=True)
    var_crew_first_landing = indexes.IntegerField(null=True)
    var_crew_died_complete_voyage = indexes.IntegerField(null=True)

    # Voyage dates
    # Month field is used for filtering by month
    var_imp_arrival_at_port_of_dis = indexes.IntegerField(null=True)
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
    var_num_slaves_intended_first_port = indexes.IntegerField(null=True)
    var_num_slaves_carried_first_port = indexes.IntegerField(null=True)
    var_num_slaves_carried_second_port = indexes.IntegerField(null=True)
    var_num_slaves_carried_third_port = indexes.IntegerField(null=True)
    var_total_num_slaves_purchased = indexes.IntegerField(null=True, faceted=True)
    var_imp_total_num_slaves_purchased = indexes.IntegerField(null=True, faceted=True)
    var_total_num_slaves_arr_first_port_embark = indexes.IntegerField(null=True)
    var_num_slaves_disembark_first_place = indexes.IntegerField(null=True)
    var_num_slaves_disembark_second_place = indexes.IntegerField(null=True)
    var_num_slaves_disembark_third_place = indexes.IntegerField(null=True)
    var_imp_total_slaves_disembarked = indexes.IntegerField(null=True, faceted=True)

    # Voyage characteristics
    var_imputed_percentage_men = indexes.FloatField(null=True)
    var_imputed_percentage_women = indexes.FloatField(null=True)
    var_imputed_percentage_boys = indexes.FloatField(null=True)
    var_imputed_percentage_girls = indexes.FloatField(null=True)
    var_imputed_percentage_female = indexes.FloatField(null=True)
    var_imputed_percentage_male = indexes.FloatField(null=True, faceted=True)
    var_imputed_percentage_child = indexes.FloatField(null=True, faceted=True)
    var_imputed_sterling_cash = indexes.FloatField(null=True)
    var_imputed_death_middle_passage = indexes.IntegerField(null=True)
    var_imputed_mortality = indexes.FloatField(null=True, faceted=True)

    # Sources
    var_sources = indexes.MultiValueField(indexed=True, stored=True, null=True)
    var_short_ref = indexes.MultiValueField()
    var_long_ref = indexes.CharField(null=True)

    def get_model(self):
        return Voyage

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_var_voyage_id(self, obj):
        try:
            print obj.pk
            return obj.voyage_id
        except AttributeError:
            return None

    def prepare_var_imp_voyage_began(self, obj):
        try:
            return getYear(obj.voyage_dates.imp_voyage_began)
        except AttributeError, TypeError:
            return None

    def prepare_var_ship_name(self, obj):
        try:
            return obj.voyage_ship.ship_name
        except AttributeError:
            return None

    def prepare_var_nationality(self, obj):
        try:
            return obj.voyage_ship.nationality_ship.label
        except AttributeError:
            return None
    def prepare_var_nationality_idnum(self, obj):
        try:
            return obj.voyage_ship.nationality_ship.value
        except AttributeError:
            return None

    def prepare_var_imputed_nationality(self, obj):
        try:
            return obj.voyage_ship.imputed_nationality.label
        except AttributeError:
            return None
    def prepare_var_imputed_nationality_idnum(self, obj):
        try:
            return obj.voyage_ship.imputed_nationality.value
        except AttributeError:
            return None

    def prepare_var_vessel_construction_place(self, obj):
        try:
            return obj.voyage_ship.vessel_construction_place.place
        except AttributeError:
            return None
    def prepare_var_vessel_construction_place_idnum(self, obj):
        try:
            return obj.voyage_ship.vessel_construction_place.value
        except AttributeError:
            return None

        
    def prepare_var_year_of_construction(self, obj):
        try:
            return obj.voyage_ship.year_of_construction
        except AttributeError:
            return None

    def prepare_var_registered_place(self, obj):
        try:
            return obj.voyage_ship.registered_place.place
        except AttributeError:
            return None
    def prepare_var_registered_place_idnum(self, obj):
        try:
            return obj.voyage_ship.registered_place.value
        except AttributeError:
            return None

    def prepare_var_registered_year(self, obj):
        try:
            return obj.voyage_ship.registered_year
        except AttributeError:
            return None

    def prepare_var_rig_of_vessel(self, obj):
        try:
            return obj.voyage_ship.rig_of_vessel.label
        except AttributeError:
            return None
    def prepare_var_rig_of_vessel_idnum(self, obj):
        try:
            return obj.voyage_ship.rig_of_vessel.value
        except AttributeError:
            return None

    def prepare_var_tonnage(self, obj):
        try:
            return obj.voyage_ship.tonnage
        except AttributeError:
            return None

    def prepare_var_tonnage_mod(self, obj):
        try:
            return obj.voyage_ship.tonnage_mod
        except AttributeError:
            return None

    def prepare_var_guns_mounted(self, obj):
        try:
            return obj.voyage_ship.guns_mounted
        except AttributeError:
            return None

    def prepare_var_owner(self, obj):
        try:
            return '<br/> '.join(
                [connection.owner.name for connection in VoyageShipOwnerConnection.objects.filter(voyage=obj)])
        except AttributeError:
            return None

    def prepare_var_outcome_voyage(self, obj):
        try:
            return VoyageOutcome.objects.filter(voyage=obj)[0].particular_outcome.label
        except AttributeError:
            return None
        except IndexError:
            return None
    def prepare_var_outcome_voyage_idnum(self, obj):
        try:
            return VoyageOutcome.objects.filter(voyage=obj)[0].particular_outcome.value
        except AttributeError:
            return None
        except IndexError:
            return None

    def prepare_var_outcome_slaves(self, obj):
        try:
            return VoyageOutcome.objects.filter(voyage=obj)[0].outcome_slaves.label
        except AttributeError:
            return None
        except IndexError:
            return None
    def prepare_var_outcome_slaves_idnum(self, obj):
        try:
            return VoyageOutcome.objects.filter(voyage=obj)[0].outcome_slaves.value
        except AttributeError:
            return None
        except IndexError:
            return None

    def prepare_var_outcome_owner(self, obj):
        try:
            return VoyageOutcome.objects.filter(voyage=obj)[0].outcome_owner.label
        except AttributeError:
            return None
        except IndexError:
            return None
    def prepare_var_outcome_owner_idnum(self, obj):
        try:
            return VoyageOutcome.objects.filter(voyage=obj)[0].outcome_owner.value
        except AttributeError:
            return None
        except IndexError:
            return None

    def prepare_var_resistance(self, obj):
        try:
            return VoyageOutcome.objects.filter(voyage=obj)[0].resistance.label
        except AttributeError:
            return None
        except IndexError:
            return None
    def prepare_var_resistance_idnum(self, obj):
        try:
            return VoyageOutcome.objects.filter(voyage=obj)[0].resistance.value
        except AttributeError:
            return None
        except IndexError:
            return None

    def prepare_var_outcome_ship_captured(self, obj):
        try:
            return VoyageOutcome.objects.filter(voyage=obj)[0].vessel_captured_outcome.label
        except AttributeError:
            return None
        except IndexError:
            return None
    def prepare_var_outcome_ship_captured_idnum(self, obj):
        try:
            return VoyageOutcome.objects.filter(voyage=obj)[0].vessel_captured_outcome.value
        except AttributeError:
            return None
        except IndexError:
            return None

    # Voyage itinerary

    def prepare_var_imp_port_voyage_begin(self, obj):
        try:
            return obj.voyage_itinerary.imp_port_voyage_begin.place
        except AttributeError:
            return None
    def prepare_var_imp_port_voyage_begin_idnum(self, obj):
        try:
            return obj.voyage_itinerary.imp_port_voyage_begin.value
        except AttributeError:
            return None

    def prepare_var_first_place_slave_purchase(self, obj):
        try:
            return obj.voyage_itinerary.first_place_slave_purchase.place
        except AttributeError:
            return None
    def prepare_var_first_place_slave_purchase_idnum(self, obj):
        try:
            return obj.voyage_itinerary.first_place_slave_purchase.value
        except AttributeError:
            return None

    def prepare_var_second_place_slave_purchase(self, obj):
        try:
            return obj.voyage_itinerary.second_place_slave_purchase.place
        except AttributeError:
            return None
    def prepare_var_second_place_slave_purchase_idnum(self, obj):
        try:
            return obj.voyage_itinerary.second_place_slave_purchase.value
        except AttributeError:
            return None

    def prepare_var_third_place_slave_purchase(self, obj):
        try:
            return obj.voyage_itinerary.third_place_slave_purchase.place
        except AttributeError:
            return None
    def prepare_var_third_place_slave_purchase_idnum(self, obj):
        try:
            return obj.voyage_itinerary.third_place_slave_purchase.value
        except AttributeError:
            return None

    def prepare_var_imp_principal_place_of_slave_purchase(self, obj):
        try:
            return obj.voyage_itinerary.imp_principal_place_of_slave_purchase.place
        except AttributeError:
            return None
    def prepare_var_imp_principal_place_of_slave_purchase_idnum(self, obj):
        try:
            return obj.voyage_itinerary.imp_principal_place_of_slave_purchase.value
        except AttributeError:
            return None

    def prepare_var_port_of_call_before_atl_crossing(self, obj):
        try:
            return obj.voyage_itinerary.port_of_call_before_atl_crossing.place
        except AttributeError:
            return None
    def prepare_var_port_of_call_before_atl_crossing_idnum(self, obj):
        try:
            return obj.voyage_itinerary.port_of_call_before_atl_crossing.value
        except AttributeError:
            return None

    def prepare_var_first_landing_place(self, obj):
        try:
            return obj.voyage_itinerary.first_landing_place.place
        except AttributeError:
            return None
    def prepare_var_first_landing_place_idnum(self, obj):
        try:
            return obj.voyage_itinerary.first_landing_place.value
        except AttributeError:
            return None

    def prepare_var_second_landing_place(self, obj):
        try:
            return obj.voyage_itinerary.second_landing_place.place
        except AttributeError:
            return None
    def prepare_var_second_landing_place_idnum(self, obj):
        try:
            return obj.voyage_itinerary.second_landing_place.value
        except AttributeError:
            return None

    def prepare_var_third_landing_place(self, obj):
        try:
            return obj.voyage_itinerary.third_landing_place.place
        except AttributeError:
            return None
    def prepare_var_third_landing_place_idnum(self, obj):
        try:
            return obj.voyage_itinerary.third_landing_place.value
        except AttributeError:
            return None

    def prepare_var_imp_principal_port_slave_dis(self, obj):
        try:
            return obj.voyage_itinerary.imp_principal_port_slave_dis.place
        except AttributeError:
            return None
    def prepare_var_imp_principal_port_slave_dis_idnum(self, obj):
        try:
            return obj.voyage_itinerary.imp_principal_port_slave_dis.value
        except AttributeError:
            return None

    def prepare_var_place_voyage_ended(self, obj):
        try:
            return obj.voyage_itinerary.place_voyage_ended.place
        except AttributeError:
            return None
    def prepare_var_place_voyage_ended_idnum(self, obj):
        try:
            return obj.voyage_itinerary.place_voyage_ended.value
        except AttributeError:
            return None

    def prepare_var_imp_principal_broad_region_disembark_idnum(self, obj):
        try:
            return obj.voyage_itinerary.imp_broad_region_slave_dis.value
        except AttributeError:
            return None
    def prepare_var_imp_broad_region_voyage_begin_idnum(self, obj):
        try:
            return obj.voyage_itinerary.imp_broad_region_voyage_begin.value
        except AttributeError:
            return None

    # Region variables
    def prepare_var_imp_region_voyage_begin(self, obj):
        try:
            return obj.voyage_itinerary.imp_region_voyage_begin.region
        except AttributeError:
            return None
    def prepare_var_imp_region_voyage_begin_idnum(self, obj):
        try:
            return obj.voyage_itinerary.imp_region_voyage_begin.value
        except AttributeError:
            return None

    def prepare_var_first_region_slave_emb(self, obj):
        try:
            return obj.voyage_itinerary.first_region_slave_emb.region
        except AttributeError:
            return None
        except IndexError:
            return None
    def prepare_var_first_region_slave_emb_idnum(self, obj):
        try:
            return obj.voyage_itinerary.first_region_slave_emb.value
        except AttributeError:
            return None
        except IndexError:
            return None

    def prepare_var_second_region_slave_emb(self, obj):
        try:
            return obj.voyage_itinerary.second_region_emb.region
        except AttributeError:
            return None
    def prepare_var_second_region_slave_emb_idnum(self, obj):
        try:
            return obj.voyage_itinerary.second_region_emb.value
        except AttributeError:
            return None

    def prepare_var_third_region_slave_emb(self, obj):
        try:
            return obj.voyage_itinerary.third_region_emb.region
        except AttributeError:
            return None
    def prepare_var_third_region_slave_emb_idnum(self, obj):
        try:
            return obj.voyage_itinerary.third_region_emb.value
        except AttributeError:
            return None

    def prepare_var_imp_principal_region_of_slave_purchase(self, obj):
        try:
            return obj.voyage_itinerary.imp_principal_region_of_slave_purchase.region
        except AttributeError:
            return None
    def prepare_var_imp_principal_region_of_slave_purchase_idnum(self, obj):
        try:
            return obj.voyage_itinerary.imp_principal_region_of_slave_purchase.value
        except AttributeError:
            return None

    def prepare_var_first_landing_region(self, obj):
        try:
            return obj.voyage_itinerary.first_landing_region.region
        except AttributeError:
            return None
    def prepare_var_first_landing_region_idnum(self, obj):
        try:
            return obj.voyage_itinerary.first_landing_region.value
        except AttributeError:
            return None

    def prepare_var_second_landing_region(self, obj):
        try:
            return obj.voyage_itinerary.second_landing_region.region
        except AttributeError:
            return None
    def prepare_var_second_landing_region_idnum(self, obj):
        try:
            return obj.voyage_itinerary.second_landing_region.value
        except AttributeError:
            return None

    def prepare_var_third_landing_region(self, obj):
        try:
            return obj.voyage_itinerary.third_landing_region.region
        except AttributeError:
            return None
    def prepare_var_third_landing_region_idnum(self, obj):
        try:
            return obj.voyage_itinerary.third_landing_region.value
        except AttributeError:
            return None

    def prepare_var_imp_principal_region_slave_dis(self, obj):
        try:
            return obj.voyage_itinerary.imp_principal_region_slave_dis.region
        except AttributeError:
            return None
    def prepare_var_imp_principal_region_slave_dis_idnum(self, obj):
        try:
            return obj.voyage_itinerary.imp_principal_region_slave_dis.value
        except AttributeError:
            return None

    def prepare_var_region_voyage_ended(self, obj):
        try:
            return obj.voyage_itinerary.place_voyage_ended.region.region
        except AttributeError:
            return None
    def prepare_var_region_voyage_ended_idnum(self, obj):
        try:
            return obj.voyage_itinerary.place_voyage_ended.region.value
        except AttributeError:
            return None

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

    def prepare_var_num_slaves_intended_first_port(self, obj):
        try:
            return obj.voyage_slaves_numbers.num_slaves_intended_first_port
        except AttributeError:
            return None

    # Voyage number
    def prepare_var_num_slaves_carried_first_port(self, obj):
        try:
            return obj.voyage_slaves_numbers.num_slaves_carried_first_port
        except AttributeError:
            return None

    def prepare_var_num_slaves_carried_second_port(self, obj):
        try:
            return obj.voyage_slaves_numbers.num_slaves_carried_second_port
        except AttributeError:
            return None

    def prepare_var_num_slaves_carried_third_port(self, obj):
        try:
            return obj.voyage_slaves_numbers.num_slaves_carried_third_port
        except AttributeError:
            return None

    def prepare_var_total_num_slaves_purchased(self, obj):
        try:
        # To be corrected
            return obj.voyage_slaves_numbers.total_num_slaves_dep_last_slaving_port
        except AttributeError:
            return None

    def prepare_var_imp_total_num_slaves_purchased(self, obj):
        try:
        # To be corrected
            return obj.voyage_slaves_numbers.imp_total_num_slaves_embarked
        except AttributeError:
            return None

    def prepare_var_total_num_slaves_arr_first_port_embark(self, obj):
        try:
            return obj.voyage_slaves_numbers.total_num_slaves_arr_first_port_embark
        except AttributeError:
            return None

    def prepare_var_num_slaves_disembark_first_place(self, obj):
        try:
            return obj.voyage_slaves_numbers.num_slaves_disembark_first_place
        except AttributeError:
            return None

    def prepare_var_num_slaves_disembark_second_place(self, obj):
        try:
            return obj.voyage_slaves_numbers.num_slaves_disembark_second_place
        except AttributeError:
            return None

    def prepare_var_num_slaves_disembark_third_place(self, obj):
        try:
            return obj.voyage_slaves_numbers.num_slaves_disembark_third_place
        except AttributeError:
            return None

    def prepare_var_imp_total_slaves_disembarked(self, obj):
        try:
            return obj.voyage_slaves_numbers.imp_total_num_slaves_disembarked
        except AttributeError:
            return None

    # Voyage characteristics
    def prepare_var_imputed_percentage_men(self, obj):
        try:
            return obj.voyage_slaves_numbers.percentage_men
        except (AttributeError, TypeError):
            return None

    def prepare_var_imputed_percentage_women(self, obj):
        try:
            return obj.voyage_slaves_numbers.percentage_women
        except (AttributeError, TypeError):
            return None

    def prepare_var_imputed_percentage_boys(self, obj):
        try:
            return obj.voyage_slaves_numbers.percentage_boy
        except (AttributeError, TypeError):
            return None

    def prepare_var_imputed_percentage_girls(self, obj):
        try:
            return obj.voyage_slaves_numbers.percentage_girl
        except (AttributeError, TypeError):
            return None

    def prepare_var_imputed_percentage_female(self, obj):
        try:
            return obj.voyage_slaves_numbers.percentage_female
        except (AttributeError, TypeError):
            return None

    def prepare_var_imputed_percentage_male(self, obj):
        try:
            return obj.voyage_slaves_numbers.percentage_male
        except (AttributeError, TypeError):
            return None

    def prepare_var_imputed_percentage_child(self, obj):
        try:
            return obj.voyage_slaves_numbers.percentage_child
        except (AttributeError, TypeError):
            return None

    def prepare_var_imputed_sterling_cash(self, obj):
        try:
            return obj.voyage_slaves_numbers.imp_jamaican_cash_price
        except AttributeError:
            return None

    def prepare_var_imputed_death_middle_passage(self, obj):
        try:
            return obj.voyage_slaves_numbers.imp_mortality_during_voyage
        except AttributeError:
            return None

    def prepare_var_imputed_mortality(self, obj):
        try:
            return obj.voyage_slaves_numbers.imp_mortality_ratio
        except (AttributeError, TypeError):
            return None

    # Voyage crew
    def prepare_var_captain(self, obj):
        return '<br/> '.join(
            [connection.captain.name for connection in VoyageCaptainConnection.objects.filter(voyage=obj)])

    def prepare_var_crew_voyage_outset(self, obj):
        try:
            return obj.voyage_crew.crew_voyage_outset
        except AttributeError:
            return None

    def prepare_var_crew_first_landing(self, obj):
        try:
            return obj.voyage_crew.crew_first_landing
        except AttributeError:
            return None

    def prepare_var_crew_died_complete_voyage(self, obj):
        try:
            return obj.voyage_crew.crew_died_complete_voyage
        except AttributeError:
            return None

    # Voyage sources
    def prepare_var_sources(self, obj):
        result = []
        for connection in VoyageSourcesConnection.objects.filter(group=obj):
            fr = ""
            if connection.source is not None:
                fr = connection.source.full_ref
            result.append(connection.text_ref + "<>" + fr)
        return result
