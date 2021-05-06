from __future__ import absolute_import, division, unicode_literals

import calendar
from builtins import str
from itertools import groupby

from django.utils.translation import ugettext_lazy as _
from past.utils import old_div

from voyages.apps.common.models import (get_values_from_haystack_results,
                                        year_mod)

from .models import (BroadRegion, Nationality, OwnerOutcome, ParticularOutcome,
                     Place, Region, Resistance, RigOfVessel, SlavesOutcome,
                     VesselCapturedOutcome)


class Axis:
    AVERAGE_MODE = 'avg'
    COUNT_MODE = 'count'
    # Determines the frequency of non-null values in a list.
    FREQUENCY_MODE = 'freq'
    SUM_MODE = 'sum'

    def __init__(self, var_name, description, mode=None):
        self.var_name = var_name
        self.description = _(description)
        self.mode = mode

    def __str__(self):
        return "Axis " + self.description

    def id(self):
        return self.var_name

    def get_group_key(self, d):
        """
        Override this method in sub-classes so that
        the values can be sorted by this key.
        :param d: The dictionary representing the data point
        :return: The value used to group data points on this axis.
        """
        return self.get_value(d)

    def get_stat(self, lst):
        """
        Computes an aggregate value over the given list.
        :param lst: The list of data points.
        :return: The aggregate result.
        """
        if self.mode is None:
            return None
        values = [b.get(self.var_name) for b in lst]
        count = sum([0.0 if x is None else 1.0 for x in values])
        if self.mode == Axis.COUNT_MODE:
            return count
        if count == 0:
            return None
        if self.mode == Axis.SUM_MODE:
            return sum([0.0 if x is None else float(x) for x in values])
        if self.mode == Axis.AVERAGE_MODE:
            return old_div(
                sum([0.0 if x is None else float(x) for x in values]), count)
        if self.mode == Axis.FREQUENCY_MODE:
            return old_div(100.0 * count, len(lst))
        raise Exception

    def get_value(self, d):
        """
        Retrieves the axis value by accessing
        the appropriate dictionary key.
        :param d: The dictionary representing the data point
        :return: The value of the data point projected on this axis.
        """
        return d.get(self.var_name)


class ForeignKeyAxis(Axis):

    def __init__(self, var_name, description, related_objects, mode=None):
        Axis.__init__(self, var_name + '_idnum', description, mode)
        self.original_var_name = var_name
        self.related_objects = related_objects

    def get_group_key(self, d):
        return d.get(self.var_name)

    def get_value(self, d):
        key = d.get(self.var_name)
        return self.related_objects.get(key)

    def id(self):
        return self.original_var_name


class MonthAxis(Axis):

    def __init__(self, var_name, description, mode=None):
        Axis.__init__(self, var_name + '_month', description, mode)

    def get_group_key(self, d):
        month = d.get(self.var_name)
        return None if month is None else int(month)

    def get_value(self, d):
        month = self.get_group_key(d)
        if month is None:
            return None
        return _(calendar.month_abbr[month])


class PercentageAxis(Axis):

    def __init__(self, var_name, description):
        Axis.__init__(self, var_name, description, Axis.AVERAGE_MODE)

    def get_stat(self, lst):
        result = Axis.get_stat(self, lst)
        if result is None:
            return None
        return round(result * 100, 1)


class YearRangeAxis(Axis):

    def __init__(self, var_name, description, year_mod, mode=None):
        Axis.__init__(self, var_name, description, mode)
        self.year_mod = year_mod

    def id(self):
        return self.var_name + '_mod_' + str(self.year_mod)

    def get_value(self, d):
        year = d.get(self.var_name)
        if year is None:
            return None
        # The ranges are always of the form [n * year_mod + 1, (n + 1) *
        # year_mod]
        n = year_mod(year, self.year_mod, 0) - 1
        # At this point we have
        # year == n * self.year_mod + 1 + (year % self.year_mod)
        return str(n * self.year_mod + 1) + '-' + str((n + 1) * self.year_mod)


graphs_x_axes = [
    Axis('var_imp_arrival_at_port_of_dis', 'Year arrived with slaves*'),
    Axis('var_imp_length_home_to_disembark',
         'Voyage length, home port to slaves landing (days)*'),
    Axis('var_length_middle_passage_days', 'Middle passage (days)*'),
    Axis('var_crew_voyage_outset', 'Crew at voyage outset'),
    Axis('var_crew_first_landing', 'Crew at first landing of slaves'),
    Axis('var_imp_total_num_slaves_purchased', 'Slaves embarked'),
    Axis('var_imp_total_slaves_disembarked', 'Slaves disembarked')
]

graphs_y_axes = [
    Axis('var_voyage_id', 'Number of voyages', Axis.COUNT_MODE),
    Axis('var_imp_length_home_to_disembark',
         'Average voyage length, home port to slaves landing (days)*',
         Axis.AVERAGE_MODE),
    Axis('var_length_middle_passage_days', 'Average middle passage (days)*',
         Axis.AVERAGE_MODE),
    Axis('var_tonnage_mod', 'Standardized tonnage*', Axis.AVERAGE_MODE),
    Axis('var_crew_voyage_outset', 'Average crew at voyage outset',
         Axis.AVERAGE_MODE),
    Axis('var_crew_first_landing', 'Average crew at first landing of slaves',
         Axis.AVERAGE_MODE),
    Axis('var_crew_voyage_outset', 'Total crew at voyage outset',
         Axis.SUM_MODE),
    Axis('var_crew_first_landing', 'Total crew at first landing of slaves',
         Axis.SUM_MODE),
    Axis('var_imp_total_num_slaves_purchased',
         'Average number of slaves embarked', Axis.AVERAGE_MODE),
    Axis('var_imp_total_slaves_disembarked',
         'Average number of slaves disembarked', Axis.AVERAGE_MODE),
    Axis('var_imp_total_num_slaves_purchased',
         'Total number of slaves embarked', Axis.SUM_MODE),
    Axis('var_imp_total_slaves_disembarked',
         'Total number of slaves disembarked', Axis.SUM_MODE),
    PercentageAxis('var_imputed_percentage_men', 'Percentage men*'),
    PercentageAxis('var_imputed_percentage_women', 'Percentage women*'),
    PercentageAxis('var_imputed_percentage_boys', 'Percentage boys*'),
    PercentageAxis('var_imputed_percentage_girls', 'Percentage girls*'),
    PercentageAxis('var_imputed_percentage_child', 'Percentage children*'),
    PercentageAxis('var_imputed_percentage_male', 'Percentage male*'),
    Axis('var_imputed_sterling_cash', 'Sterling cash price in Jamaica*',
         Axis.AVERAGE_MODE),
    Axis('var_resistance', 'Rate of resistance', Axis.FREQUENCY_MODE),
    PercentageAxis('var_imputed_mortality',
                   'Percentage of slaves embarked who died during voyage*')
]

# TODO: value SHOULD be used as the pk for several of our Django models.
# Once this is in place, we can use VoyageCache to store this data.


def cache_labels(model, label_field='label'):
    try:
        return {
            x[0]: _(x[1])
            for x in model.objects.values_list('value', label_field).iterator()
        }
    except Exception:
        return {}


_ports = cache_labels(Place, 'place')
_regions = cache_labels(Region, 'region')
_broad_regions = cache_labels(BroadRegion, 'broad_region')
_nations = cache_labels(Nationality)
_rigs = cache_labels(RigOfVessel)
_particular_outcomes = cache_labels(ParticularOutcome)
_slave_outcomes = cache_labels(SlavesOutcome)
_owner_outcomes = cache_labels(OwnerOutcome)
_captured_outcomes = cache_labels(VesselCapturedOutcome)
_resistances = cache_labels(Resistance)

other_graphs_x_axes = [
    ForeignKeyAxis('var_imputed_nationality', 'Flag*', _nations),
    ForeignKeyAxis('var_rig_of_vessel', 'Rig', _rigs),
    ForeignKeyAxis('var_outcome_voyage', 'Particular outcome of the voyage',
                   _particular_outcomes),
    ForeignKeyAxis('var_outcome_slaves', 'Outcome for slaves*',
                   _slave_outcomes),
    ForeignKeyAxis('var_outcome_owner', 'Outcome for owner*', _owner_outcomes),
    ForeignKeyAxis('var_outcome_ship_captured', 'Outcome if ship captured*',
                   _captured_outcomes),
    ForeignKeyAxis('var_resistance', 'African resistance', _resistances),
    ForeignKeyAxis('var_imp_port_voyage_begin', 'Place where voyage began*',
                   _ports),
    ForeignKeyAxis('var_imp_region_voyage_begin', 'Region where voyage began*',
                   _regions),
    ForeignKeyAxis('var_imp_principal_place_of_slave_purchase',
                   'Principal place of slave purchase*', _ports),
    ForeignKeyAxis('var_imp_principal_region_of_slave_purchase',
                   'Principal region of slave purchase*', _regions),
    ForeignKeyAxis('var_imp_principal_port_slave_dis',
                   'Principal place of slave landing*', _ports),
    ForeignKeyAxis('var_imp_principal_region_slave_dis',
                   'Principal region of slave landing*', _regions),
    ForeignKeyAxis('var_imp_principal_broad_region_disembark',
                   'Broad region of slave landing*', _broad_regions),
    ForeignKeyAxis('var_place_voyage_ended', 'Place where voyage ended',
                   _ports),
    ForeignKeyAxis('var_region_voyage_ended', 'Region where voyage ended',
                   _regions),
    MonthAxis('var_voyage_began', 'Month voyage began'),
    MonthAxis('var_slave_purchase_began', 'Month trade began in Africa'),
    MonthAxis('var_date_departed_africa', 'Month vessel departed Africa'),
    MonthAxis('var_first_dis_of_slaves', 'Month vessel arrived with slaves'),
    MonthAxis('var_departure_last_place_of_landing',
              'Month vessel departed for home port'),
    MonthAxis('var_voyage_completed', 'Month voyage completed'),
    YearRangeAxis('var_imp_arrival_at_port_of_dis',
                  'Year arrived with slaves (5 year periods)', 5),
    YearRangeAxis('var_imp_arrival_at_port_of_dis',
                  'Year arrived with slaves (10 year periods)', 10),
    YearRangeAxis('var_imp_arrival_at_port_of_dis',
                  'Year arrived with slaves (25 year periods)', 25)
]


def get_graph_data(search_query_set, x_axis, y_axes):
    """
    Obtain the graph data for the given axes extracted from
    the SearchQuerySet results.
    :param search_query_set: A SearchQuerySet object.
    :param x_axis: The X-Axis.
    :param y_axes: A list of axes that will be plotted along the Y-axis.
    :return: A dictionary containing an entry for each element in
    y_axes (with key equal to the axis description).
    The dictionary values are 2D point arrays, representing (x, y) values.
    """
    if len(y_axes) == 0:
        return {}
    # Fetch only the required data from the search query set.
    fields = [y_axis.var_name for y_axis in y_axes]
    fields.append(x_axis.var_name)
    data = get_values_from_haystack_results(search_query_set, fields)

    def sorting(d):
        return x_axis.get_group_key(d)

    data = sorted(data, key=sorting)
    result = {y_axis.description: [] for y_axis in y_axes}
    for x_key, e in groupby(data, key=sorting):
        if x_key is None:
            continue
        lst = list(e)
        x_val = x_axis.get_value(lst[0])
        for y_axis in y_axes:
            y_val = y_axis.get_stat(lst)
            # We may omit groups which cannot compute their statistic.
            if y_val is None:
                continue
            result[y_axis.description].append((x_val, y_val))
    return result
