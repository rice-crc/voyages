# Calculation of imputed variables
# Python code based on original SPSS script.

from __future__ import \
    division  # Make the / operator use floating point division.
from __future__ import print_function, unicode_literals

import inspect
from builtins import map, next, range, str
from datetime import datetime
from itertools import takewhile

from django.core.exceptions import ObjectDoesNotExist

from voyages.apps.common.models import year_mod
from voyages.apps.voyage.models import (Nationality, OwnerOutcome, Place,
                                        Region, SlavesOutcome,
                                        VesselCapturedOutcome, VoyageGroupings)

slave_number_var_names = [
    'adlt1imp', 'chil1imp', 'male1imp', 'feml1imp', 'slavmax1', 'slavema1',
    'slavemx1', 'menrat1', 'womrat1', 'boyrat1', 'girlrat1', 'chilrat1',
    'malrat1', 'adlt2imp', 'chil2imp', 'male2imp', 'feml2imp', 'adlt3imp',
    'chil3imp', 'male3imp', 'feml3imp', 'slavmax3', 'slavema3', 'slavemx3',
    'menrat3', 'womrat3', 'boyrat3', 'girlrat3', 'chilrat3', 'malrat3', 'men7',
    'women7', 'boy7', 'girl7', 'adult7', 'child7', 'male7', 'female7',
    'slavmax7', 'slavema7', 'slavemx7', 'menrat7', 'womrat7', 'boyrat7',
    'girlrat7', 'chilrat7', 'malrat7', 'tslmtimp', 'vymrtimp', 'vymrtrat'
]


def all_or_nothing(var_names, value_dict):
    """
    Fetch all numerical values from value_dict with keys
    given by var_names. If any of the values is positive,
    set all entries of value_dict equal to None, or any
    keys in var_names missing to ZERO.

    Otherwise, set all of the values for var_names to None.
    """
    nonzero = [value_dict[k] for k in var_names if value_dict.get(k)]
    if next(iter(nonzero), None):
        for k in var_names:
            if not value_dict.get(k):
                value_dict[k] = 0
    else:
        for k in var_names:
            value_dict[k] = None


def fn_from_value(model):

    def fn(val):
        if val is None or val == '':
            return None
        try:
            val = int(val)
            return model.objects.get(value=val)
        except ObjectDoesNotExist:
            print('Could not found ' + str(model) + ' with value=' + str(val))
            print(inspect.stack())
            return None
        except ValueError:
            return None

    return fn

def safe_ge(a, b):
    # Emulate the Python 2 behavior (anything >= None)
    if a is None:
        return b is None
    return b is None or a >= b

def safe_lt(a, b):
    return not safe_ge(a, b)

def safe_in_range(a, start_inclusive, end_exclusive):
    return safe_ge(a, start_inclusive) and safe_lt(a, end_exclusive)

def safe_in_exclusiverange(a, start_exclusive, end_exclusive):
    return safe_lt(start_exclusive, a) and safe_lt(a, end_exclusive)

def range_id(yearam, base, yearlist):
    return base + len(list(takewhile(
        lambda x: safe_ge(yearam, x), yearlist)))

def identity(x):
    return x

# Construct a dictionary that will map imputed variable names to
# _interimVoyage model fields, with an adapter function that converts
# the value to the expected type (e.g., from numerical code value to
# actual model from the database).
place_from_val = fn_from_value(Place)
region_from_val = fn_from_value(Region)
# Map between imputed SPSS variables and our model.
imputed_vars_model_map = {
    'natinimp': ('imputed_national_carrier', fn_from_value(Nationality)),
    'tonmod': ('imputed_standardized_tonnage', identity),
    'fate2': ('imputed_outcome_of_voyage_for_slaves',
              fn_from_value(SlavesOutcome)),
    'fate3': ('imputed_outcome_of_voyage_if_ship_captured',
              fn_from_value(VesselCapturedOutcome)),
    'fate4':
        ('imputed_outcome_of_voyage_for_owner', fn_from_value(OwnerOutcome)),
    'ptdepimp': ('imputed_port_where_voyage_began', place_from_val),
    'mjbyptimp': ('imputed_principal_place_of_slave_purchase', place_from_val),
    'mjslptimp':
        ('imputed_principal_port_of_slave_disembarkation', place_from_val),
    'deptregimp': ('imputed_region_where_voyage_began', region_from_val),
    'regdis1': ('imputed_first_region_of_slave_landing', region_from_val),
    'regdis2': ('imputed_second_region_of_slave_landing', region_from_val),
    'regdis3': ('imputed_third_region_of_slave_landing', region_from_val),
    'regem1':
        ('imputed_first_region_of_embarkation_of_slaves', region_from_val),
    'regem2':
        ('imputed_second_region_of_embarkation_of_slaves', region_from_val),
    'regem3':
        ('imputed_third_region_of_embarkation_of_slaves', region_from_val),
    'yeardep': ('imputed_year_voyage_began', identity),
    'yearaf': ('imputed_year_departed_africa', identity),
    'yearam': ('imputed_year_arrived_at_port_of_disembarkation', identity),
    'year5': ('imputed_quinquennium_in_which_voyage_occurred', identity),
    'year10': ('imputed_decade_in_which_voyage_occurred', identity),
    'year25': ('imputed_quarter_century_in_which_voyage_occurred', identity),
    'year100': ('imputed_century_in_which_voyage_occurred', identity),
    'voy1imp':
        ('imputed_voyage_length_home_port_to_first_port_of_disembarkation',
         identity),
    'voy2imp': ('imputed_length_of_middle_passage', identity),
    'xmimpflag': ('imputed_voyage_groupings_for_estimating_imputed_slaves',
                  fn_from_value(VoyageGroupings)),
    'slaximp': ('imputed_total_slaves_embarked', identity),
    'slamimp': ('imputed_total_slaves_disembarked', identity),
    'tslmtimp':
        ('imputed_number_of_slaves_embarked_for_mortality_calculation', identity),
    'vymrtimp': ('imputed_total_slave_deaths_during_middle_passage', identity),
    'vymrtrat': ('imputed_mortality_rate', identity),
    # Manually imputed -- 'jamcaspr': ('imputed_standardized_price_of_slaves',
    # identity)
}


def clear_mod(x, mod):
    return x if x is None else x - (x % mod)


def region_value(x):
    return clear_mod(x, 100)


def broad_value(x):
    return clear_mod(x, 10000) if safe_ge(80000, x) else 80000


def extract_year(csv_date):
    """
    Extract the four-digit year from a comma separated date in the format
    MM,DD,YYYY
    """
    if not csv_date:
        return None
    split = csv_date.split(',')
    if len(split) != 3 or len(split[2]) != 4:
        return None
    return int(split[2])


def extract_datetime(csv_date):
    if not csv_date:
        return None
    split = csv_date.split(',')
    if len(split) != 3 or len(split[2]) != 4 or len(split[1]) == 0 or len(
            split[0]) == 0:
        return None
    year = int(split[2])
    month = int(split[0])
    day = int(split[1])
    return datetime(year, month, day)


def date_diff(csv_date_one, csv_date_two):
    first = extract_datetime(csv_date_one)
    second = extract_datetime(csv_date_two)
    if first is None or second is None:
        return None
    diff = first - second
    return diff.days


def first_valid(lst):
    """
    Iterates over a list to retrieve the first value which is not None.
    If such a value is not found, None is returned.
    """
    for x in lst:
        if x is not None:
            return x
    return None


def get_obj_value(obj):
    return obj.value if obj else None


def recode_var(dictionary, value):
    """
    Recode a variable based on groups of values.
    :param dictionary: a dictionary of (key, [list]) which
                 each lists are pairwise disjoint and
                 one of them should contain the parameter
                 value.
    :param value: the value to search on the lists indexed by dictionary
    """
    for key, lst in list(dictionary.items()):
        if value in lst:
            return key
    return None


def threshold(value, low_limit):
    return value if (value is None or value >= low_limit) else None


def compute_imputed_vars(_interim, is_iam=False):
    """
    This method will calculate all imputed variables.
    :return a triple (imputed_model_vars, imputed_numbers, imputed_dict)

    The first is a dictionary with keys corresponding to InterimVoyage
    model fields and corresponding values.

    The second is a dictionary with keys corresponding to the SPSS
    number variable name and the value being the number (or None).

    The third is a dictionary that contains all values indexed
    by SPSS variable names, even those that do not belong to
    the model or numbers.
    """

    _named_sources = {
        'd1slatrc': _interim.date_slave_purchase_began,
        'datarr34': _interim.date_first_slave_disembarkation,
        'datarr45': _interim.date_voyage_completed,
        'datedepc': _interim.date_departure,
        'dlslatrc': _interim.date_vessel_left_last_slaving_port,
        'ddepamc': _interim.date_return_departure,
    }

    def _extract_year_from_sources(sources):
        return first_valid(
            list(
                map(extract_year,
                    [_named_sources.get(var_name) for var_name in sources])))

    # YEARDEP - Year voyage began (imputed)
    _yeardep_sources = [
        'datedepc', 'd1slatrc', 'dlslatrc', 'datarr34', 'ddepamc', 'datarr45'
    ]
    yeardep = _extract_year_from_sources(_yeardep_sources)

    # YEARAF - Year departed Africa (imputed)
    _yearaf_sources = [
        'dlslatrc', 'd1slatrc', 'datedepc', 'datarr34', 'ddepamc', 'datarr45'
    ]
    yearaf = _extract_year_from_sources(_yearaf_sources)

    # YEARAM Year of arrival at port of disembarkation (imputed)
    _yearam_sources = [
        'datarr34', 'dlslatrc', 'd1slatrc', 'datedepc', 'ddepamc', 'datedepc',
        'datarr45'
    ]
    if is_iam:
        _yearam_sources.remove('ddepamc')
        _yearam_sources.remove('datarr45')
        _yearam_sources.append('datarr38')
    yearam = _extract_year_from_sources(_yearam_sources)

    year5 = year_mod(yearam, 5, 1500)
    year10 = year_mod(yearam, 10, 1500)
    year25 = year_mod(yearam, 25, 1500)
    year100 = (year_mod(yearam, 100, 0) - 1) * 100 if yearam else None
    # VOY1IMP = DATEDIF(DATE_LAND1, DATE_DEP, "days").
    voy1imp = date_diff(_interim.date_first_slave_disembarkation,
                        _interim.date_departure)
    voy1imp = threshold(voy1imp, 39)
    # VOY2IMP = DATEDIF(DATE_LAND1, DATE_LEFTAFR, "days").
    voy2imp = date_diff(_interim.date_first_slave_disembarkation,
                        _interim.date_vessel_left_last_slaving_port)
    try:
        _interim_length = int(_interim.length_of_middle_passage)
    except Exception:
        _interim_length = 0
    if voy2imp is None or (_interim_length and voy2imp < (
            _interim_length if is_iam else min(20, _interim_length - 10))):
        voy2imp = _interim_length
    if not is_iam:
        voy2imp = threshold(voy2imp, 10)
    else:
        voy2imp = threshold(voy2imp, 1)

    natinimp = get_obj_value(_interim.national_carrier)
    natinimp = recode_var(
        {
            3: [1, 2],
            6: [4, 5],
            7: [7],
            8: [8],
            9: [9],
            10: [10],
            15: list(range(11, 15)),
            30: list(range(16, 25))
        }, natinimp)
    tonnage = _interim.tonnage_of_vessel
    tonmod = None
    tontype = None
    if tonnage:

        def update_tonmod(tonmod, tonnage):
            if safe_lt(250, tonmod):
                return 13.1 + 1.1 * tonnage
            if safe_lt(150, tonmod):
                return 65.3 + 1.2 * tonnage
            return 2.3 + 1.8 * tonnage

        tonnage = int(tonnage)
        tontype = get_obj_value(_interim.ton_type)
        tonmod = tonnage
        if tontype == 13:
            tonmod = tonnage
        elif (yearam and ((tontype and safe_lt(tontype, 3)) or tontype in (4, 5))):
            tonmod = tonnage if safe_lt(1773, yearam) else update_tonmod(
                tonnage, tonnage)
        if tontype == 4:
            if yearam and safe_in_exclusiverange(yearam, 1783, 1794):
                tonmod = None
        elif tontype in (3, 6, 9, 16):
            tonmod = 71 + (0.86 * tonnage)
            if yearam and safe_lt(yearam, 1774):
                tonmod = update_tonmod(tonmod, tonnage)
        elif tontype == 7:
            tonmod = tonnage * 2
            if safe_lt(1773, yearam):
                tonmod = update_tonmod(tonmod, tonmod)
        elif tontype == 21:
            tonmod = -6.093 + (0.76155 * tonnage)
            if safe_lt(1773, yearam):
                tonmod = update_tonmod(tonmod, tonmod)
        if all([tontype is None, yearam, safe_in_exclusiverange(yearam, 1714, 1786),
                safe_lt(0, tonnage), natinimp == 7]):
            tontype = 22
            tonmod = update_tonmod(tonnage, tonnage)
        elif tontype in (14, 15, 17):
            tonmod = 52.86 + (1.22 * tonnage)

    fate2 = None
    fate3 = None
    fate4 = None
    if _interim.voyage_outcome:
        _outcome_value = get_obj_value(_interim.voyage_outcome)
        # fate2 - Outcome of voyage for slaves
        fate2 = recode_var(
            {
                1: [
                    1, 4, 5, 7, 8, 9, 11, 12, 15, 16, 17, 19, 20, 24, 26, 29,
                    30, 39, 40, 46, 47, 48, 49, 51, 52, 54, 58, 68, 70, 71, 72,
                    76, 78, 79, 80, 81, 82, 85, 88, 92, 95, 97, 104, 108, 109,
                    122, 123, 124, 125, 132, 134, 135, 142, 144, 148, 154, 157,
                    159, 161, 162, 163, 170, 171, 172, 173, 174, 176, 177, 178,
                    179, 180, 181, 182, 183, 184, 185, 187, 189, 201, 203, 205,
                    304, 305, 306, 307, 309, 311, 313
                ],
                2: [
                    2, 6, 10, 14, 18, 22, 25, 27, 31, 41, 45, 50, 57, 74, 90,
                    93, 94, 96, 102, 103, 106, 110, 111, 112, 118, 121, 126,
                    127, 128, 130, 138, 141, 153, 155, 156, 160, 192, 193, 198,
                    202
                ],
                3: [42, 44, 69, 73, 114, 120, 206, 207, 310],
                4: [3, 66, 99],
                5: [
                    13, 21, 23, 43, 53, 55, 56, 59, 67, 77, 86, 87, 113, 164,
                    165, 166, 188, 191, 194, 195, 196, 199
                ],
                6: [208, 308],
                7: [28, 75, 89, 91, 98]
            }, _outcome_value)
        # fate3 - Outcome of voyage If vessel captured
        fate3 = recode_var(
            {
                1: [2, 3, 4, 5, 27, 28, 29, 30, 75, 85, 86, 91, 94, 95, 97],
                2: [6, 7, 8, 9, 31, 48, 96, 159, 192, 193, 306, 307],
                3: [
                    10, 11, 12, 13, 54, 58, 102, 103, 104, 106, 108, 109, 110,
                    111, 112, 113, 114, 118, 120, 121, 122, 123, 124, 125, 126,
                    127, 128, 130, 132, 134, 135, 138, 141, 144, 148, 155, 156,
                    194, 196, 198, 202, 203, 205
                ],
                4: [14, 15, 16, 17, 309],
                5: [18, 19, 20, 21, 187, 188, 189, 191, 195],
                6: [22, 23, 24, 25, 55],
                8: [
                    43, 50, 51, 52, 53, 164, 165, 166, 170, 171, 172, 173, 174,
                    176, 177, 178, 179, 180, 181, 182, 183, 184
                ],
                9: [160, 161, 162, 163, 185],
                10: [42, 56, 66, 69, 73, 76, 80, 81, 82, 87, 99, 310],
                11: [57, 74, 79, 89, 90, 98],
                12: [142, 199],
                13: [26, 39, 45, 46, 47, 67, 71, 72, 78, 153, 154, 157],
                14: [
                    1, 40, 41, 44, 49, 59, 68, 70, 77, 88, 92, 93, 206, 207,
                    304, 305, 308, 311, 313
                ],
                15: [208],
                16: [201],
                17: [211],
                18: [212]
            }, _outcome_value)
        # fate4 - Outcome of voyage for owner
        fate4 = recode_var(
            {
                1: [
                    1, 49, 68, 77, 79, 88, 92, 135, 203, 205, 206, 207, 208,
                    304, 308
                ],
                2: [
                    2, 3, 4, 5, 27, 28, 29, 30, 54, 58, 59, 85, 86, 91, 94, 95,
                    97, 311, 313
                ],
                3: [
                    6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
                    22, 23, 24, 25, 26, 31, 39, 41, 42, 43, 44, 45, 46, 47, 48,
                    50, 51, 52, 53, 55, 56, 57, 66, 67, 69, 71, 72, 73, 74, 75,
                    76, 78, 80, 81, 82, 87, 89, 90, 93, 98, 99, 102, 103, 104,
                    106, 108, 109, 110, 111, 112, 113, 114, 118, 120, 121, 122,
                    123, 124, 125, 126, 127, 128, 130, 132, 134, 138, 141, 142,
                    144, 148, 153, 154, 155, 156, 157, 159, 160, 161, 162, 163,
                    164, 165, 166, 170, 171, 172, 173, 174, 176, 177, 178, 179,
                    180, 181, 182, 183, 184, 185, 187, 188, 189, 191, 192, 193,
                    194, 195, 196, 198, 199, 201, 202, 305, 306, 307, 309, 310
                ],
                4: [40, 70, 96, 208]
            }, _outcome_value)

    # At the equivalent point in SPSS, regions are infered from places.
    # This is probably redundant given our models already connect places
    # to regions, so lines 293-406 of the SPSS script are skipped.

    embport = get_obj_value(_interim.first_port_intended_embarkation)
    embport2 = get_obj_value(_interim.second_port_intended_embarkation)

    _numbers = {n.var_name: n.number for n in _interim.slave_numbers.all()}

    # mjbyptimp - Principal port of slave purchase (replaces majbuypt as
    # imputed variable)

    ncar13 = _numbers.get('NCAR13', 0)
    ncar15 = _numbers.get('NCAR15', 0)
    ncar17 = _numbers.get('NCAR17', 0)
    if is_iam:
        ncar17 = 0
    ncartot = ncar13 + ncar15 + ncar17
    tslavesd = _numbers.get('TSLAVESD')
    tslavesp = _numbers.get('TSLAVESP')
    tslaves_unknown = not tslavesd and not tslavesp
    if is_iam:
        tslavesp = None
    pctemb = ncartot / tslavesd if tslavesd else None
    if pctemb is None and tslavesp:
        pctemb = ncartot / tslavesp

    _places = [
        get_obj_value(_interim.first_place_of_slave_purchase),
        get_obj_value(_interim.second_place_of_slave_purchase),
        get_obj_value(_interim.third_place_of_slave_purchase)
    ]
    _num_places = sum(1 for x in _places if x)
    if _num_places == 1:
        if _places[0]:
            mjbyptimp = _places[0]
        elif _places[1]:
            mjbyptimp = _places[1]
        else:
            mjbyptimp = _places[2]
    else:
        mjbyptimp = None

    if _num_places == 0:
        if safe_ge(embport, 1) and not embport2:
            mjbyptimp = embport
        elif not embport and safe_ge(embport2, 1):
            mjbyptimp = embport2
        elif safe_ge(embport, 1) and safe_ge(embport2, 1):
            embreg = region_value(embport)
            embreg2 = region_value(embport2)
            if embreg == embreg2:
                mjbyptimp = embreg + 99
            else:
                mjbyptimp = 60999

    regem1 = region_value(_places[0])
    regem2 = region_value(_places[1])
    regem3 = region_value(_places[2])
    if regem1 and regem1 == regem2 and not regem3:
        mjbyptimp = regem1 + 99
    if regem1 and regem1 == regem3 and not regem2:
        mjbyptimp = regem1 + 99
    if regem2 and regem2 == regem3 and not regem1:
        mjbyptimp = regem2 + 99
    if regem1 and regem1 == regem2 and regem1 == regem3:
        mjbyptimp = regem1 + 99
    if regem1 != regem2 and regem1 != regem3 and regem2 != regem3:
        mjbyptimp = 60999

    if safe_lt(ncar15, ncar13) and safe_lt(ncar17, ncar13):
        mjbyptimp = _places[0]
    if safe_lt(ncar13, ncar15) and safe_lt(ncar17, ncar15):
        mjbyptimp = _places[1]
    if safe_lt(ncar13, ncar17) and safe_lt(ncar15, ncar17):
        mjbyptimp = _places[2]

    if ncar13 == ncar15 and safe_lt(ncar17, ncar13) and regem1 and regem1 == regem2:
        mjbyptimp = regem1 + 99
    if ncar13 == ncar15 and safe_lt(ncar17, ncar13) and regem1 != regem2:
        mjbyptimp = 60999
    if ncar13 == ncar17 and safe_lt(ncar15, ncar13) and regem1 and regem1 == regem3:
        mjbyptimp = regem1 + 99
    if ncar13 == ncar17 and safe_lt(ncar15, ncar13) and regem1 != regem3:
        mjbyptimp = 60999
    if ncar15 == ncar17 and safe_lt(ncar13, ncar15) and regem2 and regem2 == regem3:
        mjbyptimp = regem2 + 99
    if ncar15 == ncar17 and safe_lt(ncar17, ncar15) and regem2 != regem3:
        mjbyptimp = 60999

    if (pctemb and safe_lt(pctemb, 0.5)) or (safe_lt(ncartot, 50) and tslaves_unknown):
        if ncar13 == 0 and ncar15 == 0:
            if safe_lt(0, ncar17):
                if regem1 == regem2 and regem1 is not None:
                    mjbyptimp = regem1 + 99
                if regem1 != regem2 and regem1 and regem2:
                    mjbyptimp = 60999
        elif ncar13 == 0:
            if safe_lt(0, ncar17):
                mjbyptimp = _places[0]
            else:
                if _places[2] is None:
                    mjbyptimp = _places[0]
                if regem1 == regem3 and regem1 is not None:
                    mjbyptimp = regem1 + 99
                if regem1 != regem3 and regem1 and regem3:
                    mjbyptimp = 60999
        elif ncar15 == 0:
            if safe_lt(0, ncar17):
                mjbyptimp = _places[1]
            else:
                if _places[1] and _places[2] is None:
                    mjbyptimp = _places[1]
                if regem2 == regem3 and regem2 is not None:
                    mjbyptimp = regem2 + 99
                if regem2 != regem3 and regem2 and regem3:
                    mjbyptimp = 60999
        elif ncar17 == 0:
            mjbyptimp = _places[2]

    if not ncartot:
        if all([safe_ge(_places[0], 1), safe_ge(_places[1], 1), regem1 == regem2, regem1]):
            mjbyptimp = regem1 + 99
        elif all([safe_ge(_places[0], 1), safe_ge(_places[2], 1), regem1 == regem3, regem1]):
            mjbyptimp = regem1 + 99
        elif all([safe_ge(_places[1], 1), safe_ge(_places[2], 1), regem2 == regem3, regem2]):
            mjbyptimp = regem2 + 99
        elif safe_ge(_num_places, 2):
            mjbyptimp = 60999

    if embport and embport2 is None and _num_places == 0:
        mjbyptimp = embport
    if embport2 and _num_places == 0:
        mjbyptimp = embport2
    if not mjbyptimp and (
            embport or embport2 or safe_lt(0, ncartot) or safe_ge(_num_places, 1)):
        if get_obj_value(_interim.imputed_outcome_of_voyage_for_slaves) != 2:
            mjbyptimp = 60999

    majbuypt = get_obj_value(_interim.principal_place_of_slave_purchase)
    if not mjbyptimp and safe_ge(majbuypt, 1):
        mjbyptimp = majbuypt

    if is_iam:
        # For I-Am use a simpler routine (Greg)
        plac1tra = get_obj_value(_interim.first_place_of_slave_purchase)
        plac2tra = get_obj_value(_interim.second_place_of_slave_purchase)
        if safe_ge(plac1tra, 1) and (plac2tra is None or safe_lt(ncar15, ncar13)):
            mjbyptimp = plac1tra
        if safe_lt(ncar13, ncar15):
            mjbyptimp = plac2tra
        if ncar13 == ncar15 and regem1 == regem2:
            mjbyptimp = regem1 + 99
        if ncar13 == ncar15 and regem1 != regem2:
            mjbyptimp = 80299
        if mjbyptimp is None and safe_ge(majbuypt, 1):
            mjbyptimp = majbuypt

    # mjslptimp - Principal port of slave disembarkation

    sla1port = get_obj_value(_interim.first_place_of_landing)
    adpsale1 = get_obj_value(_interim.second_place_of_landing)
    adpsale2 = get_obj_value(_interim.third_place_of_landing)
    arrport = get_obj_value(_interim.first_port_intended_disembarkation)
    arrport2 = get_obj_value(_interim.second_port_intended_disembarkation)
    if is_iam:
        arrport2 = None
    mjslptimp = None
    if sla1port and not adpsale1 and not adpsale2:
        mjslptimp = sla1port
    if adpsale1 and not sla1port and not adpsale2:
        mjslptimp = adpsale1
    if adpsale2 and not sla1port and not adpsale1:
        mjslptimp = adpsale2

    regarr = region_value(arrport)
    regarr2 = region_value(arrport2)

    have_sale_info = sla1port or adpsale1 or adpsale2
    if not have_sale_info:
        if safe_ge(arrport, 1) and not arrport2:
            mjslptimp = arrport
        if not arrport and safe_ge(arrport2, 1):
            mjslptimp = arrport2
        if safe_ge(arrport, 1) and safe_ge(arrport2, 1) and regarr and regarr == regarr2:
            mjslptimp = regarr + 99
        if safe_ge(arrport, 1) and safe_ge(arrport2, 1) and regarr != regarr2:
            mjslptimp = 99801

    regdis1 = region_value(sla1port)
    regdis2 = region_value(adpsale1)
    regdis3 = region_value(adpsale2)

    if regdis1 and regdis1 == regdis2 and not regdis3:
        mjslptimp = regdis1 + 99
    if regdis1 and regdis1 == regdis3 and not regdis2:
        mjslptimp = regdis1 + 99
    if regdis2 and regdis2 == regdis3 and not regdis1:
        mjslptimp = regdis2 + 99
    if regdis1 and regdis1 == regdis2 and regdis1 == regdis3:
        mjslptimp = regdis1 + 99
    if regdis1 != regdis2 and regdis1 != regdis3 and regdis2 != regdis3:
        mjslptimp = 99801

    if sla1port and sla1port == adpsale1:
        mjslptimp = sla1port
    if sla1port and sla1port == adpsale2:
        mjslptimp = sla1port
    if adpsale1 and adpsale1 == adpsale2:
        mjslptimp = adpsale1

    slas32 = _numbers.get('SLAS32', 0)
    slas36 = _numbers.get('SLAS36', 0)
    slas39 = _numbers.get('SLAS39', 0)

    if safe_lt(slas36, slas32) and safe_lt(slas39, slas32):
        mjslptimp = sla1port
    if safe_lt(slas32, slas36) and safe_lt(slas39, slas36):
        mjslptimp = adpsale1
    if safe_lt(slas32, slas39) and safe_lt(slas36, slas39):
        mjslptimp = adpsale2

    if slas32 == slas36 and safe_lt(slas39, slas32) and regdis1 and regdis1 == regdis2:
        mjslptimp = regdis1 + 99
    if slas32 == slas36 and safe_lt(slas39, slas32) and regdis1 != regdis2:
        mjslptimp = 99801
    if slas32 == slas39 and safe_lt(slas36, slas32) and regdis1 and regdis1 == regdis3:
        mjslptimp = regdis1 + 99
    if slas32 == slas39 and safe_lt(slas36, slas32) and regdis1 != regdis3:
        mjslptimp = 99801
    if slas36 == slas39 and safe_lt(slas32, slas36) and regdis2 and regdis2 == regdis3:
        mjslptimp = regdis2 + 99
    if slas36 == slas39 and safe_lt(slas39, slas36) and regdis2 != regdis3:
        mjslptimp = 99801

    slaarriv = _numbers.get('SLAARRIV', 0)
    slastot = slas32 + slas36 + slas39
    if all([slastot < (0.5 * slaarriv if slaarriv else 50),
            sla1port,
            adpsale1]):
        if adpsale2:
            mjslptimp = 99801
        else:
            if safe_ge(slas36, 1) and safe_ge(slas32, 1):
                mjslptimp = regdis1 + 99 if regdis1 == regdis2 else 99801
            elif safe_ge(slas36, 1):
                mjslptimp = sla1port
            elif safe_ge(slas32, 1):
                mjslptimp = adpsale1

    if not slastot and sla1port:
        if adpsale1 and adpsale2:
            if regdis1 in (regdis2, regdis3):
                mjslptimp = regdis1 + 99
            else:
                mjslptimp = regdis2 + 99 if regdis2 == regdis3 else 99801
        elif adpsale1:
            mjslptimp = regdis1 + 99 if regdis1 == regdis2 else 99801
        elif adpsale2:
            mjslptimp = regdis1 + 99 if regdis1 == regdis3 else 99801
    elif not slastot and adpsale1 and adpsale2:
        mjslptimp = regdis2 + 99 if regdis2 == regdis3 else 99801

    if arrport and not have_sale_info:
        mjslptimp = arrport

    if not mjslptimp and fate2 in (1, 3, 5):
        if arrport or arrport2 or have_sale_info or safe_lt(0, slastot):
            mjslptimp = 99801

    majselpt = get_obj_value(_interim.principal_place_of_slave_disembarkation)
    if not mjslptimp and safe_ge(majselpt, 1):
        mjslptimp = majselpt

    # ptdepimp - Imputed port where voyage began
    portdep = get_obj_value(_interim.port_of_departure)
    ptdepimp = portdep
    if portdep is None and safe_ge(50200, mjslptimp):
        if safe_lt(mjslptimp, 50300):
            ptdepimp = 50299
        elif safe_lt(mjslptimp, 50400):
            ptdepimp = 50399
        elif safe_lt(mjslptimp, 50500):
            ptdepimp = 50422

    _region_mod = 100
    deptregimp = clear_mod(ptdepimp, _region_mod)
    majbyimp = clear_mod(mjbyptimp, _region_mod)
    mjselimp = clear_mod(mjslptimp, _region_mod)
    deptregimp1 = broad_value(ptdepimp)
    majbyimp1 = broad_value(mjbyptimp)
    mjselimp1 = broad_value(mjslptimp)
    portret = get_obj_value(_interim.port_voyage_ended)
    retrnreg1 = broad_value(portret)

    # xmimpflag - Voyage groupings for estimating imputed slaves
    xmimpflag = None
    rig = get_obj_value(_interim.rig_of_vessel)
    if safe_in_range(yearam, 1626, 1876) and (rig is None or rig in (
            26, 29, 42, 43, 54, 59, 61, 65, 80, 86)):
        xmimpflag = range_id(yearam, 127, [
            1651, 1676, 1701, 1726, 1751, 1776, 1801, 1826, 1851])
    if yearam and majbyimp == 60100:
        xmimpflag = range_id(yearam, 101, [1700, 1801])
    if yearam and majbyimp == 60200:
        xmimpflag = range_id(yearam, 104, [1700, 1801])
    if yearam and majbyimp == 60300 and safe_ge(yearam, 1700):
        xmimpflag = range_id(yearam, 120, [1801])
    if yearam and majbyimp == 60400 and safe_lt(yearam, 1801):
        xmimpflag = range_id(yearam, 107, [1700])
    if yearam and majbyimp == 60500:
        xmimpflag = range_id(yearam, 110, [1700, 1801])
    if yearam and majbyimp == 60600:
        xmimpflag = range_id(yearam, 113, [1700, 1801])
    if yearam and majbyimp == 60700:
        xmimpflag = range_id(yearam, 116, [1700, 1801])
    if yearam and safe_lt(yearam, 1700) and majbyimp == 60800:
        xmimpflag = range_id(yearam, 122, [1700, 1801])
    if yearam and safe_lt(yearam, 1627):
        xmimpflag = 1
    if safe_in_range(yearam, 1626, 1642) and (
            mjselimp1 == 40000 or (
                safe_in_range(mjselimp, 31100, 32000) or mjselimp == 80400)):
        xmimpflag = 2
    if yearam and safe_lt(yearam, 1716) and safe_in_range(mjselimp, 36100, 37000):
        xmimpflag = 3
    if yearam and mjselimp == 50300:
        xmimpflag = range_id(yearam, 4, [1701, 1800])
    if yearam and natinimp == 8:
        xmimpflag = range_id(yearam, 7, [1650, 1674, 1731])
    if yearam and mjselimp == 50200:
        xmimpflag = range_id(yearam, 11, [1751, 1776, 1801, 1826])
    if yearam and safe_in_range(yearam, 1642, 1663) and ((
            safe_in_range(mjselimp, 31100, 32000)
    ) or mjselimp1 == 40000 or mjselimp == 80400):
        xmimpflag = 16
    if yearam and safe_in_range(yearam, 1794, 1807) and natinimp == 15:
        xmimpflag = 157
    if yearam and safe_lt(yearam, 1794) and natinimp == 15:
        xmimpflag = 159
    if yearam and natinimp == 9 and safe_lt(yearam, 1876):
        xmimpflag = range_id(yearam, 99, [1851])
    if yearam and rig == 1 and safe_lt(yearam, 1876):
        xmimpflag = 98 if safe_in_range(yearam, 1751, 1776) else range_id(
            yearam, 17, [1751, 1801, 1826, 1851])
    if yearam and rig == 2 and safe_lt(yearam, 1876):
        xmimpflag = range_id(yearam, 22, [1776, 1801, 1826, 1851])
    if yearam and rig == 3 and safe_lt(yearam, 1876):
        xmimpflag = range_id(yearam, 27, [1751, 1776, 1801])
    if yearam and rig == 4 and safe_lt(yearam, 1876):
        xmimpflag = range_id(yearam, 31, [1726, 1751, 1776, 1801, 1826, 1851])
    if rig == 5:
        xmimpflag = 38
    if rig == 6:
        xmimpflag = 39
    if rig == 7:
        xmimpflag = 40
    if yearam and rig == 8 and safe_lt(yearam, 1876):
        xmimpflag = range_id(yearam, 41, [1776, 1801, 1826, 1851])
    if yearam and rig in (9, 31) and safe_lt(yearam, 1876):
        xmimpflag = range_id(yearam, 46, [1826, 1851])
    if rig in (10, 24):
        xmimpflag = 49
    if rig in (11, 12):
        xmimpflag = 50
    if yearam and rig == 13 and safe_lt(yearam, 1877):
        xmimpflag = range_id(yearam, 51, [1751, 1776, 1801, 1826])
    if rig == 15:
        xmimpflag = 56
    if rig == 20:
        xmimpflag = 57
    if rig == 21:
        xmimpflag = 58
    if rig == 23:
        xmimpflag = 59
    if yearam and rig == 25 and safe_lt(yearam, 1877):
        xmimpflag = 160 if safe_in_range(yearam, 1826, 1851) else range_id(
            yearam, 60, [1751, 1776, 1801, 1826])
    if yearam and rig == 27 and safe_lt(yearam, 1877):
        xmimpflag = range_id(yearam, 65, [1751, 1776, 1801])
    if rig == 28:
        xmimpflag = 69
    if yearam and rig in (30, 45, 63) and safe_lt(yearam, 1876):
        xmimpflag = 97 if safe_in_range(yearam, 1776, 1801) else (
            85 if safe_in_range(yearam, 1826, 1876) else range_id(
                yearam, 70, [1726, 1776, 1826]))
    if rig in (32, 39):
        xmimpflag = 73
    if yearam and rig == 35 and safe_lt(yearam, 1877):
        xmimpflag = range_id(yearam, 74, [1726, 1751, 1776, 1801])
    if yearam and rig == 40 and safe_lt(yearam, 1876):
        xmimpflag = range_id(yearam, 79, [1776, 1801, 1826])
    if rig in (41, 57):
        xmimpflag = 83
    if rig == 44:
        xmimpflag = 84
    if rig == 47:
        xmimpflag = 86
    if rig == 48:
        xmimpflag = 87
    if yearam and rig in (14, 36, 49) and safe_lt(yearam, 1876):
        xmimpflag = range_id(yearam, 88, [1826])
    if yearam and rig in (16, 51) and safe_lt(yearam, 1876):
        xmimpflag = range_id(yearam, 90, [1826, 1851])
    if rig in (17, 19, 52, 53):
        xmimpflag = 93
    if yearam and rig == 60 and safe_lt(yearam, 1876):
        xmimpflag = range_id(yearam, 94, [1726, 1826])
    if yearam and rig == 1 and natinimp == 9:
        xmimpflag = range_id(yearam, 137, [1776, 1801, 1826])
    if yearam and rig in (2, 5) and natinimp == 9 and safe_lt(yearam, 1801):
        xmimpflag = range_id(yearam, 141, [1776])
    if yearam and rig == 5 and natinimp == 9 and safe_in_range(yearam, 1801, 1826):
        xmimpflag = 143
    if yearam and rig in (2, 5) and natinimp == 9 and safe_lt(1825, yearam):
        xmimpflag = 145
    if yearam and rig == 4 and natinimp == 9:
        xmimpflag = range_id(yearam, 146, [1776, 1801, 1826])
    if yearam and rig == 8 and natinimp == 9:
        xmimpflag = range_id(yearam, 150, [1776, 1826])
    if yearam and safe_in_range(yearam, 1826, 1876) and rig == 9 and natinimp == 9:
        xmimpflag = 154
    if rig == 27 and natinimp == 9:
        xmimpflag = 155
    if rig == 35 and natinimp == 9:
        xmimpflag = 156

    # slaximp - Imputed number of slaves embarked
    # slamimp - Imputed number of slaves disembarked

    captive_threshold = 0 if is_iam else 50
    slam_unknown = not slaarriv and not slastot
    if safe_ge(tslavesd, 1):
        slaximp = tslavesd
    elif safe_ge(tslavesp, 1):
        slaximp = tslavesp
    else:
        slaximp = None
    if tslaves_unknown:
        if slam_unknown and safe_lt(ncartot, captive_threshold):
            ncartot = None
        slaximp = (
            ncartot
            if (safe_lt(slaarriv, ncartot) or
                (slastot and not slaarriv and safe_lt(slastot, ncartot)) or
                (slam_unknown and safe_ge(ncartot, captive_threshold)))
            else slaximp)

    if safe_ge(slaarriv, 1):
        slamimp = slaarriv
    else:
        if not (tslaves_unknown or ncartot or safe_ge(slastot, captive_threshold)):
            slastot = None
        slamimp = slastot if (
            not tslavesd and not ncartot and safe_ge(slastot, captive_threshold)) or (
                tslaves_unknown and safe_ge(ncartot, slastot)) or (
                    not tslavesd and safe_ge(tslavesp, slastot)) or (
                        safe_ge(tslavesd, slastot)) else None
    slax_unknown = tslaves_unknown and not ncartot
    if slam_unknown or slax_unknown:
        (mortality, population, backup_slam) = {
            1: (0.255634697158707, 166.401374570447, True),
            2: (0.173114449095158, 152.863945578231, True),
            3: (0.191426939591589, 250.179245283019, True),
            4: (0.143739162059858, 273.896226415094, False),
            5: (0.0703329947332674, 380.04854368932, False),
            6: (0.117444418143106, 305.868020304568, True),
            7: (0.126779394689057, 265.88, False),
            8: (0.189011301766662, 281.325, True),
            9: (0.140365224720275, 402.502202643172, True),
            10: (0.107188743129005, 277.059842519684, True),
            11: (0.126901348540731, 355.810945273632, True),
            12: (0.0655772248600899, 309.533898305085, True),
            13: (0.0778021073375869, 305.812154696132, True),
            14: (0.0654921908875572, 285.054112554113, True),
            15: (0.0671696102131247, 361.638059701493, True),
            16: (0.371414750110571, 239.9, True),
            17: (0.0557746478873239, 148.882352941176, True),
            18: (0.093544030879478, 184.486013986014, True),
            19: (0.0985982521761244, 230.298469387755, True),
            20: (0.0944678720322908, 444.290145985401, True),
            21: (0.167379623404603, 492.946428571429, True),
            22: (0.183801786070534, 91.9594594594595, True),
            23: (0.102358180948044, 95.972972972973, True),
            24: (0.122708750828674, 146.31, True),
            25: (0.101742168136026, 279.357142857143, True),
            26: (0.0830808603000646, 341.5, True),
            27: (0.0951735364832193, 335.546666666667, False),
            28: (0.0599984615282753, 348.926267281106, False),
            29: (0.0849037398486349, 323.539358600583, True),
            30: (0.0831292966753462, 435.738461538461, True),
            31: (0.154603810637904, 221.279220779221, True),
            32: (0.169381440464976, 296.593103448276, True),
            33: (0.183684529291394, 281.452966714906, True),
            34: (0.0864964921326426, 325.652360515021, True),
            35: (0.176037224384829, 272.474358974359, True),
            36: (0.116937605450612, 556.677419354839, True),
            37: (0.172812495199871, 890.470588235294, True),
            38: (0.105087524949968, 335.813953488372, True),
            39: (0.0856667000685018, 257.263157894737, True),
            40: (0.0865650987499053, 328.195266272189, True),
            41: (0.171814252005436, 129.145454545455, True),
            42: (0.0610387045813586, 158.1, True),
            43: (0.159823459162871, 247.759689922481, True),
            44: (0.0988853555387519, 363, True),
            45: (0.0904513085721602, 466.25641025641, True),
            46: (0.082310278477633, 159.810810810811, True),
            47: (0.104714300552102, 638.25, True),
            48: (0.193439630544956, 608.392156862745, True),
            49: (0.145583038352611, 428.888888888889, True),
            50: (0.233333333333333, 270.846153846154, True),
            51: (0.179223522528989, 229.64, True),
            52: (0.0819156347249732, 290.164383561644, False),
            53: (0.0540922242825536, 256.548387096774, True),
            54: (0.0913651933726713, 216.907894736842, True),
            55: (0.0604022380426763, 241.461538461538, True),
            56: (0.0542026549646127, 340.230769230769, True),
            57: (0.0974564330758702, 516.45, True),
            58: (0.162886379968412, 447.518072289157, False),
            59: (0.0561646667118922, 152.923076923077, True),
            60: (0.133468501803896, 403.292993630573, True),
            61: (0.106708705390018, 285.644444444444, True),
            62: (0.0785278768682708, 335.658227848101, True),
            63: (0.107782269167156, 472.267857142857, True),
            65: (0.115409873680179, 103.376146788991, True),
            66: (0.207088877726936, 68.1506849315068, True),
            67: (0.110922605367631, 80.0491803278688, True),
            68: (0.127935729778166, 84, False),
            69: (0.206358225584424, 1004.47058823529, True),
            70: (0.142775407154303, 311.222222222222, True),
            71: (0.106323148232566, 310.39837398374, True),
            72: (0.169436742362705, 265.325842696629, True),
            73: (0.129605450439467, 407.289473684211, True),
            74: (0.0794384325299229, 117.137931034483, True),
            75: (0.189369734252207, 192.772020725389, True),
            76: (0.131187789757565, 199.041666666667, True),
            77: (0.136342992788614, 186.407894736842, True),
            78: (0.103049659988616, 155.470588235294, True),
            79: (0.35, 193.74358974359, True),
            80: (0.0732085200996002, 249.692307692308, True),
            81: (0.0934359066589073, 352.952806122449, True),
            82: (0.07182740558555, 419.619047619047, True),
            83: (0.0956449943871365, 304.5625, False),
            84: (0.163929225997462, 319.285714285714, True),
            85: (0.339905284604731, 563.333333333333, True),
            86: (0.112733293827202, 129.277777777778, True),
            87: (0.0655504344628028, 211, True),
            88: (0.198929221794951, 296.473684210526, False),
            89: (0.107517933823928, 281.958333333333, True),
            90: (0.028250184258012, 208.341176470588, True),
            91: (0.0487771272192143, 267.896551724138, True),
            92: (0.111975986975987, 328.555555555556, True),
            93: (0.0979648763988006, 101.111111111111, True),
            94: (0.297737659966491, 319.733333333333, True),
            95: (0.0220048899755501, 220.428571428571, True),
            96: (0, 433, True),
            97: (0.138965456634756, 259.21875, True),
            98: (0.126563817175912, 132.596685082873, True),
            99: (0.166050441674744, 125.619750283768, True),
            100: (0.178717812379779, 565.645161290322, True),
            101: (0.142415261804064, 163.80243902439, True),
            102: (0.104951847967976, 153.265497076023, True),
            103: (0.0794334443169517, 138.094017094017, True),
            104: (0.125269157905197, 107.64, False),
            105: (0.0887057111704602, 191.988789237668, True),
            106: (0.0985396051230542, 188.140969162996, True),
            107: (0.199714956235816, 239.363636363636, True),
            108: (0.116764553914052, 241.066480055983, True),
            110: (0.217817105373686, 321.139784946236, True),
            111: (0.134584278813695, 320.396527777777, True),
            112: (0.0649564900465187, 302.919243986254, True),
            113: (0.294943293777566, 178.191780821918, True),
            114: (0.190466263797331, 268.709993468321, True),
            115: (0.165262209695588, 265.480215827338, True),
            116: (0.250590294065011, 216.026607538803, True),
            117: (0.0862116624182079, 341.979498861048, True),
            118: (0.0795782666543268, 382.444580777097, True),
            120: (0.100542298212489, 191.62583518931, True),
            121: (0.0690791392436498, 162.041666666667, True),
            122: (0.274602006426542, 173.454545454545, True),
            123: (0.274602006426542, 255.028571428571, True),
            124: (0.181330570603409, 447.532008830022, True),
            127: (0.165107561642471, 163.181286549708, True),
            128: (0.230972326367458, 241.774647887324, True),
            129: (0.218216262481124, 249.141527001862, True),
            130: (0.164154067860228, 227.680034129693, True),
            131: (0.153670852602567, 272.60549132948, True),
            132: (0.120410468186061, 268.071314102564, True),
            133: (0.126821090786133, 290.826654240447, True),
            134: (0.105799354866935, 225.932515337423, True),
            135: (0.114160782328086, 391.452674897119, True),
            136: (0.170755559662484, 480.734042553191, True),
            137: (0.12659407459354, 104.986301369863, True),
            138: (0.179201806454531, 108.37037037037, False),
            139: (0.162003845923261, 128.438775510204, True),
            140: (0.171264386321147, 557.6, True),
            141: (0.213152374545978, 74, True),
            142: (0.190548809128441, 80.5625, False),
            145: (0.0577485174550083, 376.928571428571, True),
            146: (0.153749295952981, 154.307692307692, True),
            147: (0.143606923731731, 165.903225806452, False),
            148: (0.254317624200109, 199.730769230769, True),
            149: (0.136559928551299, 1003, True),
            150: (0.182187702624498, 100.090909090909, True),
            151: (0.00833333333333333, 127.103448275862, True),
            152: (0.100333848361108, 436.5, True),
            154: (0.235321405225611, 580.060606060606, True),
            155: (0.157476046121814, 70.0833333333334, True),
            156: (0.17641709128796, 118.333333333333, True),
            157: (0.230610260687796, 139.029411764706, True),
            159: (0.154487726688789, 245.12676056338, True),
            160: (0.0779281672325541, 536.842857142857, True),
        }[xmimpflag]
        if slam_unknown and slax_unknown:
            if backup_slam:
                slamimp = population
            else:
                slaximp = population
        if slam_unknown:
            if safe_ge(slaximp, 1):
                slamimp = slaximp * (1 - mortality)
        elif safe_ge(slamimp, 1):
            slaximp = slamimp / (1 - mortality)
    sladvoy = _numbers.get('SLADVOY')
    if safe_lt(0, sladvoy) and not slaarriv and slax_unknown and safe_ge(slastot, 50):
        slaximp = slastot + sladvoy
    if safe_lt(0, sladvoy) and slax_unknown and safe_lt(1, slaarriv):
        slaximp = slaarriv + sladvoy
    if safe_lt(0, sladvoy) and slam_unknown and slax_unknown:
        slaximp = slamimp + sladvoy

    slaximp = round(slaximp) if slaximp else None
    slamimp = round(slamimp) if slamimp else None

    # tslmtimp - Imputed total of slaves embarked for mortality calculation
    # vymrtimp - Imputed number of slaves died in middle passage
    # vymrtrat - Slaves died on voyage / Slaves embarked

    slaarriv = _numbers.get('SLAARRIV')
    if sladvoy is None and slaarriv is not None and safe_ge(tslavesd, slaarriv):
        vymrtimp = tslavesd - slaarriv
    else:
        vymrtimp = sladvoy
    if safe_lt(vymrtimp, 0):
        tslmtimp = None
    elif not tslavesd and safe_ge(slaarriv, 1):
        tslmtimp = slaarriv + vymrtimp
    else:
        tslmtimp = tslavesd
    vymrtrat = vymrtimp / tslmtimp if vymrtimp and tslmtimp else None

    # AGE AND GENDER VARIABLES INCORPORATING INFORMATION FROM VARIABLES 4,5,6

    # adlt1imp - Imputed number of adults among embarked slaves
    # chil1imp - Imputed number of children among embarked slaves
    # male1imp - Imputed number of males among embarked slaves
    # feml1imp - Imputed number of females among embarked slaves
    # slavema1 - Number of embarked slaves with age identified
    # slavemx1 - Number of embarkedslaves with sex identified
    # slavmax1 - Number of embarked slaves identified by age and sex
    # menrat1 - Ratio of men among embarked slaves
    # womrat1 - Ratio of women among embarked slaves
    # boyrat1 - Ratio of boys among embarked slaves
    # girlrat1 - Ratio of girls among embarked slaves
    # chilrat1 - Child ratio among embarked slaves
    # malrat1 - Male ratio among embarked slaves

    # adlt4imp - Imputed number of adults embarked at second port of purchase
    # chil4imp - Imputed number of children embarked at second port of purchase
    # male4imp - Imputed number of males embarked at second port of purchase
    # feml4imp - Imputed number of females embarked at second port of purchase

    men1 = _numbers.get('MEN1', 0)
    men4 = _numbers.get('MEN4', 0)
    men5 = _numbers.get('MEN5', 0)

    women1 = _numbers.get('WOMEN1', 0)
    women4 = _numbers.get('WOMEN4', 0)
    women5 = _numbers.get('WOMEN5', 0)

    adult1 = _numbers.get('ADULT1', 0)
    adult4 = _numbers.get('ADULT4', 0)
    adult5 = _numbers.get('ADULT5', 0)

    girl1 = _numbers.get('GIRL1', 0)
    girl4 = _numbers.get('GIRL4', 0)
    girl5 = _numbers.get('GIRL5', 0)

    boy1 = _numbers.get('BOY1', 0)
    boy4 = _numbers.get('BOY4', 0)
    boy5 = _numbers.get('BOY5', 0)

    child1 = _numbers.get('CHILD1', 0)
    child4 = _numbers.get('CHILD4', 0)
    child5 = _numbers.get('CHILD5', 0)

    infant1 = _numbers.get('INFANT1', 0)
    infant4 = _numbers.get('INFANT4', 0)

    male1 = _numbers.get('MALE1', 0)
    male4 = _numbers.get('MALE4', 0)
    male5 = _numbers.get('MALE5', 0)

    female1 = _numbers.get('FEMALE1', 0)
    female4 = _numbers.get('FEMALE4', 0)
    female5 = _numbers.get('FEMALE5', 0)

    adlt1imp = men1 + women1 + adult1 + \
        men4 + women4 + adult4 + men5 + women5 + adult5
    chil1imp = boy1 + girl1 + child1 + infant1 + boy4 + \
        girl4 + child4 + infant4 + boy5 + girl5 + child5
    malemax1 = men1 + boy1 + men4 + boy4 + men5 + boy5
    femmax1 = women1 + girl1 + women4 + girl4 + women5 + girl5
    slavmax1 = threshold(malemax1 + femmax1, 20)
    male1imp = male1 + male4 + male5
    feml1imp = female1 + female4 + female5
    if not male1imp:
        male1imp = malemax1
    if not feml1imp:
        feml1imp = femmax1
    slavema1 = threshold(adlt1imp + chil1imp, 20)
    slavemx1 = threshold(male1imp + feml1imp, 20)
    if slavema1 is None:
        adlt1imp = None
        chil1imp = None
    if slavemx1 is None:
        feml1imp = None
        male1imp = None
    chilrat1 = chil1imp / slavema1 if slavema1 else None
    malrat1 = male1imp / slavemx1 if slavemx1 else None
    menrat1 = None
    womrat1 = None
    boyrat1 = None
    girlrat1 = None
    if safe_ge(slavmax1, 20):
        menrat1 = (men1 + men4 + men5) / slavmax1
    if safe_ge(slavmax1, 20):
        womrat1 = (women1 + women4 + women5) / slavmax1
    if safe_ge(slavmax1, 20):
        boyrat1 = (boy1 + boy4 + boy5) / slavmax1
    if safe_ge(slavmax1, 20):
        girlrat1 = (girl1 + girl4 + girl5) / slavmax1

    # adlt3imp - Imputed number of adults among disembarked slaves
    # chil3imp - Imputed number of children among disembarked slaves
    # male3imp - Imputed number of males among disembarked slaves
    # feml3imp - Imputed number of females among disembarked slaves
    # slavema3 - Number of disembarked slaves with age identified
    # slavemx3 - Number of disembarked slaves with sex identIfied
    # slavmax3 - Number of disembarked slaves identIfied by age and sex
    # menrat3 - Ratio of men among disembarked slaves
    # womrat3 - Ratio of women among disembarked slaves
    # boyrat3 - Ratio of boys among disembarked slaves
    # girlrat3 - Ratio of girls among disembarked slaves
    # chilrat3 - Child ratio among disembarked slaves
    # malrat3 - Male ratio among disembarked slaves

    men3 = _numbers.get('MEN3', 0)
    men6 = _numbers.get('MEN6', 0)

    women3 = _numbers.get('WOMEN3', 0)
    women6 = _numbers.get('WOMEN6', 0)

    adult3 = _numbers.get('ADULT3', 0)
    adult6 = _numbers.get('ADULT6', 0)

    girl3 = _numbers.get('GIRL3', 0)
    girl6 = _numbers.get('GIRL6', 0)

    boy3 = _numbers.get('BOY3', 0)
    boy6 = _numbers.get('BOY6', 0)

    child3 = _numbers.get('CHILD3', 0)
    child6 = _numbers.get('CHILD6', 0)

    infant3 = _numbers.get('INFANT3', 0)

    male3 = _numbers.get('MALE3', 0)
    male6 = _numbers.get('MALE6', 0)

    female3 = _numbers.get('FEMALE3', 0)
    female6 = _numbers.get('FEMALE6', 0)

    adlt3imp = men3 + women3 + adult3 + men6 + women6 + adult6
    chil3imp = boy3 + girl3 + child3 + infant3 + boy6 + girl6 + child6

    male3imp = male3 + male6
    feml3imp = female3 + female6
    if male3imp == 0:
        male3imp = men3 + boy3 + men6 + boy6
    if feml3imp == 0:
        feml3imp = women3 + girl3 + women6 + girl6

    slavema3 = threshold(adlt3imp + chil3imp, 20)
    slavemx3 = threshold(male3imp + feml3imp, 20)
    slavmax3 = threshold(
        men3 + women3 + boy3 + girl3 + men6 + women6 + boy6 + girl6, 20)

    if slavema3 is None:
        adlt3imp = None
        chil3imp = None
    if slavemx3 is None:
        feml3imp = None
        male3imp = None

    chilrat3 = chil3imp / slavema3 if slavema3 else None
    malrat3 = male3imp / slavemx3 if slavemx3 else None
    menrat3 = None
    womrat3 = None
    boyrat3 = None
    girlrat3 = None
    if safe_ge(slavmax3, 20):
        menrat3 = (men3 + men6) / slavmax3
    if safe_ge(slavmax3, 20):
        womrat3 = (women3 + women6) / slavmax3
    if safe_ge(slavmax3, 20):
        boyrat3 = (boy3 + boy6) / slavmax3
    if safe_ge(slavmax3, 20):
        girlrat3 = (girl3 + girl6) / slavmax3

    # men7 - Imputed men when leaving Africa or arriving at ports of landing
    # women7 - Imputed women when leaving Africa or arriving at ports of
    # landing
    # boy7 - Imputed boys when leaving Africa or arriving at ports of landing
    # girl7 - Imputed girls when leaving Africa or arriving at ports of landing
    # adult7 - Imputed adults when leaving Africa or arriving at ports of
    # landing
    # child7 - Imputed children when leaving Africa or arriving at ports of
    # lading
    # male7 - Imputed males when leaving Africa or arriving at ports of landing
    # female7 - Imputed females when leaving Africa or arriving at ports of
    # landing
    # slavema7 - Number of slaves with age identIfied, Africa or ports of
    # lading
    # slavemx7 - Number of slaves with sex identIfied, Africa or ports of
    # landing
    # slavmax7 - Number of slaves identIfied by both age and sex
    # menrat7 - Imputed ratio of men when leaving Africa or arriving at ports
    # of landing
    # womrat7 - Imputed ratio of women when leaving Africa or arriving at ports
    # of landing
    # boyrat7 - Imputed ratio of boys when leaving Africa or arriving at ports
    # of landing
    # girlrat7 - Imputed ratio of girls when leaving Africa or arriving at
    # ports of landing
    # chilrat7 - Imputed ratio of children when leaving Africa or arriving at
    # ports of landing
    # malrat7 - Imputed ratio of males when leaving Africa or arriving at ports
    # of landing
    men7 = None
    women7 = None
    boy7 = None
    girl7 = None
    adult7 = None
    child7 = None
    male7 = None
    female7 = None
    slavema7 = None
    slavemx7 = None
    slavmax7 = None
    menrat7 = None
    womrat7 = None
    boyrat7 = None
    girlrat7 = None
    chilrat7 = None
    malrat7 = None

    if safe_ge(slavema3, 20):
        slavema7 = slavema3
    if safe_ge(slavemx3, 20):
        slavemx7 = slavemx3
    if safe_ge(slavmax3, 20):
        slavmax7 = slavmax3
    if safe_ge(slavmax7, 20):
        men7 = men3 + men6
    if safe_ge(slavmax7, 20):
        women7 = women3 + women6
    if safe_ge(slavmax7, 20):
        boy7 = boy3 + boy6
    if safe_ge(slavmax7, 20):
        girl7 = girl3 + girl6
    if safe_ge(slavema7, 20):
        adult7 = adlt3imp
    if safe_ge(slavema7, 20):
        child7 = chil3imp
    if safe_ge(slavemx7, 20):
        male7 = male3imp
    if safe_ge(slavemx7, 20):
        female7 = feml3imp
    if safe_ge(menrat3, 0):
        menrat7 = menrat3
    if safe_ge(womrat3, 0):
        womrat7 = womrat3
    if safe_ge(boyrat3, 0):
        boyrat7 = boyrat3
    if safe_ge(girlrat3, 0):
        girlrat7 = girlrat3
    if safe_ge(malrat3, 0):
        malrat7 = malrat3
    if safe_ge(chilrat3, 0):
        chilrat7 = chilrat3

    if slavema3 is None and safe_ge(slavema1, 20):
        slavema7 = slavema1
    if slavemx3 is None and safe_ge(slavemx1, 20):
        slavemx7 = slavemx1
    if slavmax3 is None and safe_ge(slavmax1, 20):
        slavmax7 = slavmax1
    if slavmax3 is None and safe_ge(slavmax1, 20):
        men7 = men1 + men4 + men5
    if slavmax3 is None and safe_ge(slavmax1, 20):
        women7 = women1 + women4 + women5
    if slavmax3 is None and safe_ge(slavmax1, 20):
        boy7 = boy1 + boy4 + boy5
    if slavmax3 is None and safe_ge(slavmax1, 20):
        girl7 = girl1 + girl4 + girl5
    if slavema3 is None and safe_ge(slavema1, 20):
        adult7 = adlt1imp
    if slavema3 is None and safe_ge(slavema1, 20):
        child7 = chil1imp
    if slavemx3 is None and safe_ge(slavemx1, 20):
        male7 = male1imp
    if slavemx3 is None and safe_ge(slavemx1, 20):
        female7 = feml1imp
    if menrat3 is None and safe_ge(menrat1, 0):
        menrat7 = menrat1
    if womrat3 is None and safe_ge(womrat1, 0):
        womrat7 = womrat1
    if boyrat3 is None and safe_ge(boyrat1, 0):
        boyrat7 = boyrat1
    if girlrat3 is None and safe_ge(girlrat1, 0):
        girlrat7 = girlrat1
    if malrat3 is None and safe_ge(malrat1, 0):
        malrat7 = malrat1
    if chilrat3 is None and safe_ge(chilrat1, 0):
        chilrat7 = chilrat1

    # adlt2imp - Imputed number of adults who died on middle passage
    # chil2imp - Imputed number of children who died on middle passage
    # male2imp - Imputed number of males who died on middle passage
    # feml2imp - Imputed number of females who died on middle passage
    men2 = _numbers.get('MEN2', 0)
    women2 = _numbers.get('WOMEN2', 0)
    adult2 = _numbers.get('ADULT2', 0)
    girl2 = _numbers.get('GIRL2', 0)
    boy2 = _numbers.get('BOY2', 0)
    child2 = _numbers.get('CHILD2', 0)
    male2 = _numbers.get('MALE2', 0)
    female2 = _numbers.get('FEMALE2', 0)

    adlt2imp = men2 + women2 + adult2
    chil2imp = boy2 + girl2 + child2

    male2imp = male2
    feml2imp = female2
    if not male2imp:
        male2imp = men2 + boy2
    if not feml2imp:
        feml2imp = women2 + girl2

    if safe_in_range(sladvoy, 1, chil2imp) and adlt2imp == 0 and chil2imp:
        adlt2imp = sladvoy - chil2imp
    if safe_in_range(sladvoy, 1, adlt2imp) and chil2imp == 0 and adlt2imp:
        chil2imp = sladvoy - adlt2imp
    if safe_in_range(sladvoy, 1, feml2imp) and male2imp == 0 and feml2imp:
        male2imp = sladvoy - feml2imp
    if safe_in_range(sladvoy, 1, male2imp) and feml2imp == 0 and male2imp:
        feml2imp = sladvoy - male2imp

    local_vars = locals()
    local_vars = {
        k: v for k, v in list(local_vars.items()) if not k.startswith('_')
    }

    # Recode zero numerical values to None and vice versa with an 'all or
    # nothing' logic.
    _recode_var_names = [
        'men1', 'women1', 'boy1', 'girl1', 'child1', 'infant1', 'adult1',
        'men4', 'women4', 'boy4', 'girl4', 'child4', 'infant4', 'adult4',
        'men5', 'women5', 'boy5', 'girl5', 'child5', 'adult5'
    ]
    all_or_nothing(_recode_var_names, local_vars)

    _recode_var_names = [
        'male1', 'female1', 'male4', 'female4', 'male5', 'female5'
    ]
    all_or_nothing(_recode_var_names, local_vars)

    _recode_var_names = ['men2', 'women2', 'boy2', 'girl2', 'child2', 'adult2']
    all_or_nothing(_recode_var_names, local_vars)

    _recode_var_names = ['male2', 'female2']
    all_or_nothing(_recode_var_names, local_vars)

    _recode_var_names = [
        'men3', 'women3', 'boy3', 'girl3', 'child3', 'infant3', 'adult3',
        'men6', 'women6', 'boy6', 'girl6', 'child6', 'adult6'
    ]
    all_or_nothing(_recode_var_names, local_vars)

    _recode_var_names = ['male3', 'female3', 'male6', 'female6']
    all_or_nothing(_recode_var_names, local_vars)

    _recode_var_names = ['ncar13', 'ncar15', 'ncar17', 'ncartot']
    all_or_nothing(_recode_var_names, local_vars)

    _recode_var_names = ['slas32', 'slas36', 'slas39', 'slastot']
    all_or_nothing(_recode_var_names, local_vars)

    _no_zeros = ['pctdis', 'adlt2imp', 'chil2imp', 'male2imp', 'feml2imp']
    for k in _no_zeros:
        if not local_vars.get(k):
            local_vars[k] = None

    # Generate model field values.
    imputed_field_values = {
        v[0]: v[1](local_vars[k])
        for k, v in list(imputed_vars_model_map.items())
    }
    # Generate imputed number values.
    imputed_numbers = {
        k: float(local_vars[k]) if local_vars[k] else None
        for k in slave_number_var_names
    }

    # Fields that are not available/present in I-Am and should be removed from
    # the output.
    iam_rem = [
        'yeardep', 'yearaf', 'voy1imp', 'tonmod', 'ptdepimp', 'deptregimp',
        'deptregimp1', 'retrnreg1', 'embport', 'embport2', 'embreg', 'embreg2',
        'plac3tra', 'regem3', 'arrport2', 'regarr2', 'portret', 'retrnreg',
        'xmimpflag'
    ]
    iam_sex_rem = [
        'men$', 'women$', 'adult$', 'girl$', 'boy$', 'child$', 'male$',
        'female$', 'adlt$imp', 'chil$imp', 'male$imp', 'feml$imp'
    ]

    if is_iam:
        for d in [imputed_field_values, imputed_numbers, local_vars]:
            for k in iam_rem:
                d.pop(k, None)
            for k in iam_sex_rem:
                for num in ['2', '4', '5', '6']:
                    d.pop(k.replace('$', num), None)

    return (imputed_field_values, imputed_numbers, local_vars)
