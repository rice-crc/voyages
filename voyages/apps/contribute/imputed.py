# Calculation of imputed variables
# Python code based on original SPSS script.

from __future__ import \
    division  # Make the / operator use floating point division.
from __future__ import print_function, unicode_literals

import inspect
from builtins import map, next, range, str
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

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


# Convenience id function


def id(x):
    return x


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


# Construct a dictionary that will map imputed variable names to
# _interimVoyage model fields, with an adapter function that converts
# the value to the expected type (e.g., from numerical code value to
# actual model from the database).
place_from_val = fn_from_value(Place)
region_from_val = fn_from_value(Region)
# Map between imputed SPSS variables and our model.
imputed_vars_model_map = {
    'natinimp': ('imputed_national_carrier', fn_from_value(Nationality)),
    'tonmod': ('imputed_standardized_tonnage', id),
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
    'yeardep': ('imputed_year_voyage_began', id),
    'yearaf': ('imputed_year_departed_africa', id),
    'yearam': ('imputed_year_arrived_at_port_of_disembarkation', id),
    'year5': ('imputed_quinquennium_in_which_voyage_occurred', id),
    'year10': ('imputed_decade_in_which_voyage_occurred', id),
    'year25': ('imputed_quarter_century_in_which_voyage_occurred', id),
    'year100': ('imputed_century_in_which_voyage_occurred', id),
    'voy1imp':
        ('imputed_voyage_length_home_port_to_first_port_of_disembarkation', id),
    'voy2imp': ('imputed_length_of_middle_passage', id),
    'xmimpflag': ('imputed_voyage_groupings_for_estimating_imputed_slaves',
                  fn_from_value(VoyageGroupings)),
    'slaximp': ('imputed_total_slaves_embarked', id),
    'slamimp': ('imputed_total_slaves_disembarked', id),
    'tslmtimp':
        ('imputed_number_of_slaves_embarked_for_mortality_calculation', id),
    'vymrtimp': ('imputed_total_slave_deaths_during_middle_passage', id),
    'vymrtrat': ('imputed_mortality_rate', id),
    # Manually imputed -- 'jamcaspr': ('imputed_standardized_price_of_slaves', id)
}


def clear_mod(x, mod):
    return x - (x % mod) if x is not None else None


def region_value(x):
    return clear_mod(x, 100)


def broad_value(x):
    return clear_mod(x, 10000) if x <= 80000 else 80000


def extract_year(csv_date):
    """
    Extract the four-digit year from a comma separated date in the format MM,DD,YYYY
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


def recode_var(dict, value):
    """
    Recode a variable based on groups of values.
    :param dict: a dictionary of (key, [list]) which
                 each lists are pairwise disjoint and
                 one of them should contain the parameter
                 value.
    :param value: the value to search on the lists indexed by dict
    """
    for key, lst in list(dict.items()):
        if value in lst:
            return key
    return None


def threshold(value, min):
    return None if (value is not None and value < min) else value


def year_mod(the_year, mod, start):
    if the_year is None:
        return None
    return 1 + ((the_year - start - 1) // mod)


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
    year100 = ((yearam - 1) // 100) * 100 if yearam else None
    # VOY1IMP = DATEDIF(DATE_LAND1, DATE_DEP, "days").
    voy1imp = date_diff(_interim.date_first_slave_disembarkation,
                        _interim.date_departure)
    voy1imp = threshold(voy1imp, 39)
    # VOY2IMP = DATEDIF(DATE_LAND1, DATE_LEFTAFR, "days").
    voy2imp = date_diff(_interim.date_first_slave_disembarkation,
                        _interim.date_vessel_left_last_slaving_port)
    try:
        _interim_length = int(_interim.length_of_middle_passage)
    except:
        _interim_length = 0
    if voy2imp is None or (voy2imp < (0 if is_iam else 20) and
                           _interim_length and _interim_length - voy2imp >
                           (0 if is_iam else 10)):
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
        tonnage = int(tonnage)
        tontype = get_obj_value(_interim.ton_type)
        tonmod = tonnage
        if tontype == 13:
            tonmod = tonnage
        if ((tontype and tontype < 3) or tontype == 4 or tontype == 5):
            if yearam > 1773:
                tonmod = tonnage
            if yearam and yearam < 1774 and tonnage > 250:
                tonmod = 13.1 + (1.1 * tonnage)
            if yearam and yearam < 1774 and tonnage > 150 and tonnage < 251:
                tonmod = 65.3 + (1.2 * tonnage)
            if yearam and yearam < 1774 and tonnage < 151:
                tonmod = 2.3 + (1.8 * tonnage)
        if tontype == 4 and yearam > 1783 and yearam and yearam < 1794:
            tonmod = None
        if tontype == 3 or tontype == 6 or tontype == 9 or tontype == 16:
            tonmod = 71 + (0.86 * tonnage)
            if yearam and yearam < 1774 and tonmod > 250:
                tonmod = 13.1 + (1.1 * tonnage)
            if yearam and yearam < 1774 and tonmod > 150 and tonmod < 251:
                tonmod = 65.3 + (1.2 * tonnage)
            if yearam and yearam < 1774 and tonmod < 151:
                tonmod = 2.3 + (1.8 * tonnage)
        if tontype == 7:
            tonmod = tonnage * 2
        if tontype == 7 and yearam > 1773 and tonmod > 250:
            tonmod = 13.1 + (1.1 * tonmod)
        if tontype == 7 and yearam > 1773 and tonmod > 150 and tonmod < 251:
            tonmod = 65.3 + (1.2 * tonmod)
        if tontype == 7 and yearam > 1773 and tonmod < 151:
            tonmod = 2.3 + (1.8 * tonmod)
        if tontype == 21:
            tonmod = -6.093 + (0.76155 * tonnage)
        if tontype == 21 and yearam > 1773 and tonmod > 250:
            tonmod = 13.1 + (1.1 * tonmod)
        if tontype == 21 and yearam > 1773 and tonmod > 150 and tonmod < 251:
            tonmod = 65.3 + (1.2 * tonmod)
        if tontype == 21 and yearam > 1773 and tonmod < 151:
            tonmod = 2.3 + (1.8 * tonmod)
        if tontype is None and yearam > 1714 and yearam and yearam < 1786 and tonnage > 0 and natinimp == 7:
            tontype = 22
        if tontype == 22 and tonnage > 250:
            tonmod = 13.1 + (1.1 * tonnage)
        if tontype == 22 and tonnage > 150 and tonnage < 251:
            tonmod = 65.3 + (1.2 * tonnage)
        if tontype == 22 and tonnage < 151:
            tonmod = 2.3 + (1.8 * tonnage)
        if tontype == 15 or tontype == 14 or tontype == 17:
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

    # mjbyptimp - Principal port of slave purchase (replaces majbuypt as imputed variable)

    ncar13 = _numbers.get('NCAR13', 0)
    ncar15 = _numbers.get('NCAR15', 0)
    ncar17 = _numbers.get('NCAR17', 0)
    if is_iam:
        ncar17 = 0
    ncartot = ncar13 + ncar15 + ncar17
    tslavesd = _numbers.get('TSLAVESD')
    tslavesp = _numbers.get('TSLAVESP')
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
    regem1 = region_value(_places[0])
    regem2 = region_value(_places[1])
    regem3 = region_value(_places[2])
    mjbyptimp = None
    if _places[0] and not _places[1] and not _places[2]:
        mjbyptimp = _places[0]
    if _places[1] and not _places[0] and not _places[2]:
        mjbyptimp = _places[1]
    if _places[2] and not _places[0] and not _places[1]:
        mjbyptimp = _places[2]

    embreg = region_value(embport)
    embreg2 = region_value(embport2)
    if not _places[0] and not _places[1] and not _places[2]:
        if embport >= 1 and not embport2:
            mjbyptimp = embport
        if not embport and embport2 >= 1:
            mjbyptimp = embport2
        if embport >= 1 and embport2 >= 1 and embreg == embreg2:
            mjbyptimp = embreg + 99
        if embport >= 1 and embport2 >= 1 and embreg != embreg2:
            mjbyptimp = 60999

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

    if ncar13 > ncar15 and ncar13 > ncar17:
        mjbyptimp = _places[0]
    if ncar15 > ncar13 and ncar15 > ncar17:
        mjbyptimp = _places[1]
    if ncar17 > ncar13 and ncar17 > ncar15:
        mjbyptimp = _places[2]

    if ncar13 == ncar15 and ncar13 > ncar17 and regem1 and regem1 == regem2:
        mjbyptimp = regem1 + 99
    if ncar13 == ncar15 and ncar13 > ncar17 and regem1 != regem2:
        mjbyptimp = 60999
    if ncar13 == ncar17 and ncar13 > ncar15 and regem1 and regem1 == regem3:
        mjbyptimp = regem1 + 99
    if ncar13 == ncar17 and ncar13 > ncar15 and regem1 != regem3:
        mjbyptimp = 60999
    if ncar15 == ncar17 and ncar15 > ncar13 and regem2 and regem2 == regem3:
        mjbyptimp = regem2 + 99
    if ncar15 == ncar17 and ncar15 > ncar17 and regem2 != regem3:
        mjbyptimp = 60999

    if (pctemb and pctemb < 0.5) or (ncartot < 50 and not tslavesd and
                                     not tslavesp):
        if ncar13 == 0 and ncar15 > 0 and ncar17 > 0:
            mjbyptimp = _places[0]
        if ncar13 > 0 and ncar15 == 0 and ncar17 > 0:
            mjbyptimp = _places[1]
        if ncar13 > 0 and ncar15 > 0 and ncar17 == 0:
            mjbyptimp = _places[2]
        if ncar13 == 0 and ncar15 > 0 and ncar17 == 0 and _places[2] is None:
            mjbyptimp = _places[0]
        if ncar13 > 0 and ncar15 == 0 and ncar17 == 0 and _places[
                1] and _places[2] is None:
            mjbyptimp = _places[1]
        if ncar13 == 0 and ncar15 == 0 and ncar17 > 0 and regem1 is not None and regem1 == regem2:
            mjbyptimp = regem1 + 99
        if ncar13 == 0 and ncar15 > 0 and ncar17 == 0 and regem1 is not None and regem1 == regem3:
            mjbyptimp = regem1 + 99
        if ncar13 > 0 and ncar15 == 0 and ncar17 == 0 and regem2 is not None and regem2 == regem3:
            mjbyptimp = regem2 + 99
        if ncar13 == 0 and ncar15 == 0 and ncar17 > 0 and regem1 != regem2 and regem1 and regem2:
            mjbyptimp = 60999
        if ncar13 == 0 and ncar15 > 0 and ncar17 == 0 and regem1 != regem3 and regem1 and regem3:
            mjbyptimp = 60999
        if ncar13 > 0 and ncar15 == 0 and ncar17 == 0 and regem2 != regem3 and regem2 and regem3:
            mjbyptimp = 60999

    if not ncartot:
        if _places[0] >= 1 and _places[1] >= 1 and _places[
                2] is None and regem1 is not None and regem1 and regem1 == regem2:
            mjbyptimp = regem1 + 99
        if _places[0] >= 1 and _places[2] >= 1 and _places[
                1] is None and regem1 is not None and regem1 and regem1 == regem3:
            mjbyptimp = regem1 + 99
        if _places[1] >= 1 and _places[2] >= 1 and _places[
                0] is None and regem2 is not None and regem2 and regem2 == regem3:
            mjbyptimp = regem2 + 99
        if _places[0] >= 1 and _places[1] >= 1 and _places[
                2] is None and regem1 != regem2:
            mjbyptimp = 60999
        if _places[0] >= 1 and _places[2] >= 1 and _places[
                1] is None and regem1 != regem3:
            mjbyptimp = 60999
        if _places[1] >= 1 and _places[2] >= 1 and _places[
                0] is None and regem2 != regem3:
            mjbyptimp = 60999
        if _places[0] >= 1 and _places[1] >= 1 and _places[
                2] >= 1 and regem1 and regem1 == regem2:
            mjbyptimp = regem1 + 99
        if _places[0] >= 1 and _places[1] >= 1 and _places[
                2] >= 1 and regem1 and regem1 == regem3:
            mjbyptimp = regem1 + 99
        if _places[0] >= 1 and _places[1] >= 1 and _places[
                2] >= 1 and regem2 and regem2 == regem3:
            mjbyptimp = regem2 + 99
        if _places[0] >= 1 and _places[1] >= 1 and _places[
                2] >= 1 and regem1 != regem2 and regem1 != regem3 and regem2 != regem3:
            mjbyptimp = 60999

    _no_places = _places[0] is None and _places[1] is None and _places[2] is None
    if embport and embport2 is None and _no_places:
        mjbyptimp = embport
    if embport2 and _no_places:
        mjbyptimp = embport2
    if not mjbyptimp and get_obj_value(
            _interim.imputed_outcome_of_voyage_for_slaves) != 2 and (
                embport or embport2 or ncartot > 0 or _places[0] >= 1 or
                _places[1] >= 1 or _places[2] >= 1):
        mjbyptimp = 60999

    majbuypt = get_obj_value(_interim.principal_place_of_slave_purchase)
    if not mjbyptimp and majbuypt >= 1:
        mjbyptimp = majbuypt

    if is_iam:
        # For I-Am use a simpler routine (Greg)
        plac1tra = get_obj_value(_interim.first_place_of_slave_purchase)
        plac2tra = get_obj_value(_interim.second_place_of_slave_purchase)
        if plac1tra >= 1 and (plac2tra is None or ncar13 > ncar15):
            mjbyptimp = plac1tra
        if ncar15 > ncar13:
            mjbyptimp = plac2tra
        if ncar13 == ncar15 and regem1 == regem2:
            mjbyptimp = regem1 + 99
        if ncar13 == ncar15 and regem1 != regem2:
            mjbyptimp = 80299
        if mjbyptimp is None and majbuypt >= 1:
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

    if not sla1port and not adpsale1 and not adpsale2:
        if arrport >= 1 and not arrport2:
            mjslptimp = arrport
        if not arrport and arrport2 >= 1:
            mjslptimp = arrport2
        if arrport >= 1 and arrport2 >= 1 and regarr and regarr == regarr2:
            mjslptimp = regarr + 99
        if arrport >= 1 and arrport2 >= 1 and regarr != regarr2:
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

    if slas32 > slas36 and slas32 > slas39:
        mjslptimp = sla1port
    if slas36 > slas32 and slas36 > slas39:
        mjslptimp = adpsale1
    if slas39 > slas32 and slas39 > slas36:
        mjslptimp = adpsale2

    if slas32 == slas36 and slas32 > slas39 and regdis1 and regdis1 == regdis2:
        mjslptimp = regdis1 + 99
    if slas32 == slas36 and slas32 > slas39 and regdis1 != regdis2:
        mjslptimp = 99801
    if slas32 == slas39 and slas32 > slas36 and regdis1 and regdis1 == regdis3:
        mjslptimp = regdis1 + 99
    if slas32 == slas39 and slas32 > slas36 and regdis1 != regdis3:
        mjslptimp = 99801
    if slas36 == slas39 and slas36 > slas32 and regdis2 and regdis2 == regdis3:
        mjslptimp = regdis2 + 99
    if slas36 == slas39 and slas36 > slas39 and regdis2 != regdis3:
        mjslptimp = 99801

    slaarriv = _numbers.get('SLAARRIV', 0)
    slastot = slas32 + slas36 + slas39
    pctdis = slastot / slaarriv if slaarriv else None
    if ((pctdis is not None and pctdis < 0.5) or
            (slastot < 50 and not slaarriv)) and sla1port and adpsale1:
        if adpsale2:
            mjslptimp = 99801
        else:
            if slas32 == 0 and slas36 >= 1:
                mjslptimp = sla1port
            if slas36 == 0 and slas32 >= 1:
                mjslptimp = adpsale1
            if slas36 >= 1 and slas32 >= 1 and regdis1 == regdis2:
                mjslptimp = regdis1 + 99
            if slas36 >= 1 and slas32 >= 1 and regdis1 != regdis2:
                mjslptimp = 99801

    if not slastot:
        if sla1port and adpsale1 and not adpsale2 and regdis1 == regdis2:
            mjslptimp = regdis1 + 99
        if sla1port and adpsale2 and not adpsale1 and regdis1 == regdis3:
            mjslptimp = regdis1 + 99
        if adpsale1 and adpsale2 and not sla1port and regdis2 == regdis3:
            mjslptimp = regdis2 + 99
        if sla1port and adpsale1 and not adpsale2 and regdis1 != regdis2:
            mjslptimp = 99801
        if sla1port and adpsale2 and not adpsale1 and regdis1 != regdis3:
            mjslptimp = 99801
        if adpsale1 and adpsale2 and not sla1port and regdis2 != regdis3:
            mjslptimp = 99801
        if sla1port and adpsale1 and adpsale2 and regdis1 == regdis2:
            mjslptimp = regdis1 + 99
        if sla1port and adpsale1 and adpsale2 and regdis1 == regdis3:
            mjslptimp = regdis1 + 99
        if sla1port and adpsale1 and adpsale2 and regdis2 == regdis3:
            mjslptimp = regdis2 + 99
        if sla1port and adpsale1 and adpsale2 and regdis1 != regdis2 and regdis1 != regdis3 and regdis2 != regdis3:
            mjslptimp = 99801

    if arrport and not sla1port and not adpsale1 and not adpsale2:
        mjslptimp = arrport

    if not mjslptimp and (fate2 == 1 or fate2 == 3 or fate2 == 5) and \
       (arrport or arrport2 or sla1port or adpsale1 or adpsale2 or slastot > 0):
        mjslptimp = 99801

    majselpt = get_obj_value(_interim.principal_place_of_slave_disembarkation)
    if not mjslptimp and majselpt >= 1:
        mjslptimp = majselpt

    # ptdepimp - Imputed port where voyage began
    portdep = get_obj_value(_interim.port_of_departure)
    ptdepimp = portdep
    if mjslptimp >= 50200 and mjslptimp < 50300 and portdep is None:
        ptdepimp = 50299
    if mjslptimp >= 50300 and mjslptimp < 50400 and portdep is None:
        ptdepimp = 50399
    if mjslptimp >= 50400 and mjslptimp < 50500 and portdep is None:
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
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or
            rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or
            rig is None) and yearam >= 1626 and yearam < 1651:
        xmimpflag = 127
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or
            rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or
            rig is None) and yearam >= 1651 and yearam < 1676:
        xmimpflag = 128
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or
            rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or
            rig is None) and yearam >= 1676 and yearam < 1701:
        xmimpflag = 129
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or
            rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or
            rig is None) and yearam >= 1701 and yearam < 1726:
        xmimpflag = 130
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or
            rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or
            rig is None) and yearam >= 1726 and yearam < 1751:
        xmimpflag = 131
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or
            rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or
            rig is None) and yearam >= 1751 and yearam < 1776:
        xmimpflag = 132
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or
            rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or
            rig is None) and yearam >= 1776 and yearam < 1801:
        xmimpflag = 133
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or
            rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or
            rig is None) and yearam >= 1801 and yearam < 1826:
        xmimpflag = 134
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or
            rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or
            rig is None) and yearam >= 1826 and yearam < 1851:
        xmimpflag = 135
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or
            rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or
            rig is None) and yearam >= 1851 and yearam < 1876:
        xmimpflag = 136
    if yearam and yearam < 1700 and majbyimp == 60100:
        xmimpflag = 101
    if yearam and yearam >= 1700 and yearam < 1801 and majbyimp == 60100:
        xmimpflag = 102
    if yearam and yearam >= 1800 and majbyimp == 60100:
        xmimpflag = 103
    if yearam and yearam < 1700 and majbyimp == 60200:
        xmimpflag = 104
    if yearam and yearam >= 1700 and yearam < 1801 and majbyimp == 60200:
        xmimpflag = 105
    if yearam and yearam >= 1800 and majbyimp == 60200:
        xmimpflag = 106
    if yearam and yearam < 1700 and majbyimp == 60400:
        xmimpflag = 107
    if yearam and yearam >= 1700 and yearam < 1801 and majbyimp == 60400:
        xmimpflag = 108
    if yearam and yearam < 1700 and majbyimp == 60500:
        xmimpflag = 110
    if yearam and yearam >= 1700 and yearam < 1801 and majbyimp == 60500:
        xmimpflag = 111
    if yearam and yearam >= 1800 and majbyimp == 60500:
        xmimpflag = 112
    if yearam and yearam < 1700 and majbyimp == 60600:
        xmimpflag = 113
    if yearam and yearam >= 1700 and yearam < 1801 and majbyimp == 60600:
        xmimpflag = 114
    if yearam and yearam >= 1800 and majbyimp == 60600:
        xmimpflag = 115
    if yearam and yearam < 1700 and majbyimp == 60700:
        xmimpflag = 116
    if yearam and yearam >= 1700 and yearam < 1801 and majbyimp == 60700:
        xmimpflag = 117
    if yearam and yearam >= 1800 and majbyimp == 60700:
        xmimpflag = 118
    if yearam and yearam >= 1700 and yearam < 1801 and majbyimp == 60300:
        xmimpflag = 120
    if yearam and yearam >= 1800 and majbyimp == 60300:
        xmimpflag = 121
    if yearam and yearam < 1700 and majbyimp == 60800:
        xmimpflag = 122
    if yearam and yearam >= 1700 and yearam < 1801 and majbyimp == 60800:
        xmimpflag = 123
    if yearam and yearam >= 1800 and majbyimp == 60800:
        xmimpflag = 124
    if yearam and yearam < 1627:
        xmimpflag = 1
    if (yearam >= 1626 and
            yearam < 1642) and ((mjselimp >= 31100 and mjselimp < 32000) or
                                mjselimp1 == 40000 or mjselimp == 80400):
        xmimpflag = 2
    if yearam and yearam < 1716 and mjselimp >= 36100 and mjselimp < 37000:
        xmimpflag = 3
    if yearam and yearam < 1701 and mjselimp == 50300:
        xmimpflag = 4
    if yearam and yearam >= 1700 and yearam < 1800 and mjselimp == 50300:
        xmimpflag = 5
    if yearam and yearam > 1799 and mjselimp == 50300:
        xmimpflag = 6
    if yearam and yearam < 1650 and natinimp == 8:
        xmimpflag = 7
    if yearam and yearam >= 1650 and yearam < 1674 and natinimp == 8:
        xmimpflag = 8
    if yearam and yearam >= 1674 and yearam < 1731 and natinimp == 8:
        xmimpflag = 9
    if yearam and yearam > 1730 and natinimp == 8:
        xmimpflag = 10
    if yearam and yearam < 1751 and mjselimp == 50200:
        xmimpflag = 11
    if yearam and yearam >= 1751 and yearam < 1776 and mjselimp == 50200:
        xmimpflag = 12
    if yearam and yearam >= 1776 and yearam < 1801 and mjselimp == 50200:
        xmimpflag = 13
    if yearam and yearam >= 1801 and yearam < 1826 and mjselimp == 50200:
        xmimpflag = 14
    if yearam and yearam > 1825 and mjselimp == 50200:
        xmimpflag = 15
    if yearam and yearam >= 1642 and yearam < 1663 and (
        (mjselimp >= 31100 and mjselimp < 32000) or mjselimp1 == 40000 or
            mjselimp == 80400):
        xmimpflag = 16
    if yearam and yearam >= 1794 and yearam < 1807 and natinimp == 15:
        xmimpflag = 157
    if yearam and yearam < 1794 and natinimp == 15:
        xmimpflag = 159
    if yearam and yearam < 1851 and natinimp == 9:
        xmimpflag = 99
    if yearam and yearam >= 1851 and yearam < 1876 and natinimp == 9:
        xmimpflag = 100
    if yearam and yearam < 1751 and rig == 1:
        xmimpflag = 17
    if yearam and yearam >= 1751 and yearam < 1776 and rig == 1:
        xmimpflag = 98
    if yearam and yearam >= 1776 and yearam < 1801 and rig == 1:
        xmimpflag = 18
    if yearam and yearam >= 1801 and yearam < 1826 and rig == 1:
        xmimpflag = 19
    if yearam and yearam >= 1826 and yearam < 1851 and rig == 1:
        xmimpflag = 20
    if yearam and yearam >= 1851 and yearam < 1876 and rig == 1:
        xmimpflag = 21
    if yearam and yearam < 1776 and rig == 2:
        xmimpflag = 22
    if yearam and yearam >= 1776 and yearam < 1801 and rig == 2:
        xmimpflag = 23
    if yearam and yearam >= 1801 and yearam < 1826 and rig == 2:
        xmimpflag = 24
    if yearam and yearam >= 1826 and yearam < 1851 and rig == 2:
        xmimpflag = 25
    if yearam and yearam >= 1851 and yearam < 1876 and rig == 2:
        xmimpflag = 26
    if yearam and yearam < 1751 and rig == 3:
        xmimpflag = 27
    if yearam and yearam >= 1751 and yearam < 1776 and rig == 3:
        xmimpflag = 28
    if yearam and yearam >= 1776 and yearam < 1801 and rig == 3:
        xmimpflag = 29
    if yearam and yearam >= 1801 and yearam < 1876 and rig == 3:
        xmimpflag = 30
    if yearam and yearam < 1726 and rig == 4:
        xmimpflag = 31
    if yearam and yearam >= 1726 and yearam < 1751 and rig == 4:
        xmimpflag = 32
    if yearam and yearam >= 1751 and yearam < 1776 and rig == 4:
        xmimpflag = 33
    if yearam and yearam >= 1776 and yearam < 1801 and rig == 4:
        xmimpflag = 34
    if yearam and yearam >= 1801 and yearam < 1826 and rig == 4:
        xmimpflag = 35
    if yearam and yearam >= 1826 and yearam < 1851 and rig == 4:
        xmimpflag = 36
    if yearam and yearam >= 1851 and yearam < 1876 and rig == 4:
        xmimpflag = 37
    if rig == 5:
        xmimpflag = 38
    if rig == 6:
        xmimpflag = 39
    if rig == 7:
        xmimpflag = 40
    if yearam and yearam < 1776 and rig == 8:
        xmimpflag = 41
    if yearam and yearam >= 1776 and yearam < 1801 and rig == 8:
        xmimpflag = 42
    if yearam and yearam >= 1801 and yearam < 1826 and rig == 8:
        xmimpflag = 43
    if yearam and yearam >= 1826 and yearam < 1851 and rig == 8:
        xmimpflag = 44
    if yearam and yearam >= 1851 and yearam < 1876 and rig == 8:
        xmimpflag = 45
    if yearam and yearam < 1826 and (rig == 9 or rig == 31):
        xmimpflag = 46
    if yearam and yearam >= 1826 and yearam < 1851 and (rig == 9 or rig == 31):
        xmimpflag = 47
    if yearam and yearam >= 1851 and yearam < 1876 and (rig == 9 or rig == 31):
        xmimpflag = 48
    if rig == 10 or rig == 24:
        xmimpflag = 49
    if rig == 11 or rig == 12:
        xmimpflag = 50
    if yearam and yearam < 1751 and rig == 13:
        xmimpflag = 51
    if yearam and yearam >= 1751 and yearam < 1776 and rig == 13:
        xmimpflag = 52
    if yearam and yearam >= 1776 and yearam < 1801 and rig == 13:
        xmimpflag = 53
    if yearam and yearam >= 1801 and yearam < 1826 and rig == 13:
        xmimpflag = 54
    if yearam and yearam >= 1826 and yearam < 1877 and rig == 13:
        xmimpflag = 55
    if rig == 15:
        xmimpflag = 56
    if rig == 20:
        xmimpflag = 57
    if rig == 21:
        xmimpflag = 58
    if rig == 23:
        xmimpflag = 59
    if yearam and yearam < 1751 and rig == 25:
        xmimpflag = 60
    if yearam and yearam >= 1751 and yearam < 1776 and rig == 25:
        xmimpflag = 61
    if yearam and yearam >= 1776 and yearam < 1801 and rig == 25:
        xmimpflag = 62
    if yearam and yearam >= 1801 and yearam < 1826 and rig == 25:
        xmimpflag = 63
    if yearam and yearam >= 1826 and yearam < 1851 and rig == 25:
        xmimpflag = 160
    if yearam and yearam >= 1851 and yearam < 1877 and rig == 25:
        xmimpflag = 64
    if yearam and yearam < 1751 and rig == 27:
        xmimpflag = 65
    if yearam and yearam >= 1751 and yearam < 1776 and rig == 27:
        xmimpflag = 66
    if yearam and yearam >= 1776 and yearam < 1801 and rig == 27:
        xmimpflag = 67
    if yearam and yearam >= 1801 and yearam < 1877 and rig == 27:
        xmimpflag = 68
    if rig == 28:
        xmimpflag = 69
    if yearam and yearam < 1726 and (rig == 30 or rig == 45 or rig == 63):
        xmimpflag = 70
    if yearam and yearam >= 1726 and yearam < 1776 and (rig == 30 or
                                                        rig == 45 or rig == 63):
        xmimpflag = 71
    if yearam and yearam >= 1776 and yearam < 1801 and (rig == 30 or
                                                        rig == 45 or rig == 63):
        xmimpflag = 97
    if yearam and yearam >= 1801 and yearam < 1826 and (rig == 30 or
                                                        rig == 45 or rig == 63):
        xmimpflag = 72
    if yearam and yearam >= 1826 and yearam < 1876 and (rig == 30 or
                                                        rig == 45 or rig == 63):
        xmimpflag = 85
    if rig == 32 or rig == 39:
        xmimpflag = 73
    if yearam and yearam < 1726 and rig == 35:
        xmimpflag = 74
    if yearam and yearam >= 1726 and yearam < 1751 and rig == 35:
        xmimpflag = 75
    if yearam and yearam >= 1751 and yearam < 1776 and rig == 35:
        xmimpflag = 76
    if yearam and yearam >= 1776 and yearam < 1801 and rig == 35:
        xmimpflag = 77
    if yearam and yearam >= 1801 and yearam < 1877 and rig == 35:
        xmimpflag = 78
    if yearam and yearam < 1776 and rig == 40:
        xmimpflag = 79
    if yearam and yearam >= 1776 and yearam < 1801 and rig == 40:
        xmimpflag = 80
    if yearam and yearam >= 1801 and yearam < 1826 and rig == 40:
        xmimpflag = 81
    if yearam and yearam >= 1826 and yearam < 1876 and rig == 40:
        xmimpflag = 82
    if rig == 41 or rig == 57:
        xmimpflag = 83
    if rig == 44:
        xmimpflag = 84
    if rig == 47:
        xmimpflag = 86
    if rig == 48:
        xmimpflag = 87
    if yearam and yearam < 1826 and (rig == 14 or rig == 36 or rig == 49):
        xmimpflag = 88
    if yearam and yearam >= 1826 and yearam < 1876 and (rig == 14 or
                                                        rig == 36 or rig == 49):
        xmimpflag = 89
    if yearam and yearam < 1826 and (rig == 16 or rig == 51):
        xmimpflag = 90
    if yearam and yearam >= 1826 and yearam < 1851 and (rig == 16 or rig == 51):
        xmimpflag = 91
    if yearam and yearam >= 1851 and yearam < 1876 and (rig == 16 or rig == 51):
        xmimpflag = 92
    if rig == 17 or rig == 19 or rig == 52 or rig == 53:
        xmimpflag = 93
    if yearam and yearam < 1726 and rig == 60:
        xmimpflag = 94
    if yearam and yearam >= 1726 and yearam < 1826 and rig == 60:
        xmimpflag = 95
    if yearam and yearam >= 1826 and yearam < 1876 and rig == 60:
        xmimpflag = 96
    if yearam and yearam < 1776 and rig == 1 and natinimp == 9:
        xmimpflag = 137
    if yearam and yearam >= 1776 and yearam < 1801 and rig == 1 and natinimp == 9:
        xmimpflag = 138
    if yearam and yearam >= 1801 and yearam < 1826 and rig == 1 and natinimp == 9:
        xmimpflag = 139
    if yearam and yearam > 1825 and rig == 1 and natinimp == 9:
        xmimpflag = 140
    if yearam and yearam < 1776 and (rig == 2 or rig == 5) and natinimp == 9:
        xmimpflag = 141
    if yearam and yearam >= 1776 and yearam < 1801 and (rig == 2 or rig
                                                        == 5) and natinimp == 9:
        xmimpflag = 142
    if yearam and yearam >= 1801 and yearam < 1826 and rig == 5 and natinimp == 9:
        xmimpflag = 143
    if yearam and yearam > 1825 and (rig == 2 or rig == 5) and natinimp == 9:
        xmimpflag = 145
    if yearam and yearam < 1776 and rig == 4 and natinimp == 9:
        xmimpflag = 146
    if yearam and yearam >= 1776 and yearam < 1801 and rig == 4 and natinimp == 9:
        xmimpflag = 147
    if yearam and yearam >= 1801 and yearam < 1826 and rig == 4 and natinimp == 9:
        xmimpflag = 148
    if yearam and yearam > 1825 and rig == 4 and natinimp == 9:
        xmimpflag = 149
    if yearam and yearam < 1776 and rig == 8 and natinimp == 9:
        xmimpflag = 150
    if yearam and yearam >= 1776 and yearam < 1826 and rig == 8 and natinimp == 9:
        xmimpflag = 151
    if yearam and yearam > 1825 and rig == 8 and natinimp == 9:
        xmimpflag = 152
    if yearam and yearam >= 1826 and yearam < 1876 and rig == 9 and natinimp == 9:
        xmimpflag = 154
    if rig == 27 and natinimp == 9:
        xmimpflag = 155
    if rig == 35 and natinimp == 9:
        xmimpflag = 156

    # slaximp - Imputed number of slaves embarked
    # slamimp - Imputed number of slaves disembarked

    slaximp = None
    slamimp = None
    captive_threshold = 0 if is_iam else 50
    if tslavesd >= 1:
        slaximp = tslavesd
    if not tslavesd and tslavesp >= 1:
        slaximp = tslavesp
    if not tslavesd and not tslavesp and ncartot > slaarriv and slaarriv:
        slaximp = ncartot
    if not tslavesd and not tslavesp and not slaarriv and ncartot > slastot and slastot:
        slaximp = ncartot
    if not tslavesd and not tslavesp and not slaarriv and not slastot and ncartot < captive_threshold:
        ncartot = None
    if not tslavesd and not tslavesp and not slaarriv and not slastot and ncartot >= captive_threshold:
        slaximp = ncartot

    if slaarriv >= 1:
        slamimp = slaarriv
    if not slaarriv and slastot <= tslavesd:
        slamimp = slastot
    if not slaarriv and not tslavesd and slastot <= tslavesp:
        slamimp = slastot
    if not slaarriv and not tslavesd and not tslavesp and slastot <= ncartot:
        slamimp = slastot
    if not tslavesd and not tslavesp and not slaarriv and not ncartot and slastot < captive_threshold:
        slastot = None
    if not slaarriv and not tslavesd and not tslavesd and not ncartot and slastot >= captive_threshold:
        slamimp = slastot

    if xmimpflag == 127 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.165107561642471)
    if xmimpflag == 127 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.165107561642471)
    if xmimpflag == 127 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 163.181286549708
    if xmimpflag == 127 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 163.181286549708 / (1 - 0.165107561642471)
    if xmimpflag == 128 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.230972326367458)
    if xmimpflag == 128 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.230972326367458)
    if xmimpflag == 128 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 241.774647887324
    if xmimpflag == 128 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 241.774647887324 / (1 - 0.230972326367458)
    if xmimpflag == 129 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.218216262481124)
    if xmimpflag == 129 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.218216262481124)
    if xmimpflag == 129 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 249.141527001862
    if xmimpflag == 129 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 249.141527001862 / (1 - 0.218216262481124)
    if xmimpflag == 130 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.164154067860228)
    if xmimpflag == 130 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.164154067860228)
    if xmimpflag == 130 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 227.680034129693
    if xmimpflag == 130 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 227.680034129693 / (1 - 0.164154067860228)
    if xmimpflag == 131 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.153670852602567)
    if xmimpflag == 131 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.153670852602567)
    if xmimpflag == 131 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 272.60549132948
    if xmimpflag == 131 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 272.60549132948 / (1 - 0.153670852602567)
    if xmimpflag == 132 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.120410468186061)
    if xmimpflag == 132 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.120410468186061)
    if xmimpflag == 132 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 268.071314102564
    if xmimpflag == 132 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 268.071314102564 / (1 - 0.120410468186061)
    if xmimpflag == 133 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.126821090786133)
    if xmimpflag == 133 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.126821090786133)
    if xmimpflag == 133 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 290.826654240447
    if xmimpflag == 133 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 290.826654240447 / (1 - 0.126821090786133)
    if xmimpflag == 134 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.105799354866935)
    if xmimpflag == 134 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.105799354866935)
    if xmimpflag == 134 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 225.932515337423
    if xmimpflag == 134 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 225.932515337423 / (1 - 0.105799354866935)
    if xmimpflag == 135 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.114160782328086)
    if xmimpflag == 135 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.114160782328086)
    if xmimpflag == 135 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 391.452674897119
    if xmimpflag == 135 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 391.452674897119 / (1 - 0.114160782328086)
    if xmimpflag == 136 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.170755559662484)
    if xmimpflag == 136 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.170755559662484)
    if xmimpflag == 136 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 480.734042553191
    if xmimpflag == 136 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 480.734042553191 / (1 - 0.170755559662484)
    if xmimpflag == 101 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.142415261804064)
    if xmimpflag == 101 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.142415261804064)
    if xmimpflag == 101 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 163.80243902439
    if xmimpflag == 101 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 163.80243902439 / (1 - 0.142415261804064)
    if xmimpflag == 102 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.104951847967976)
    if xmimpflag == 102 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.104951847967976)
    if xmimpflag == 102 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 153.265497076023
    if xmimpflag == 102 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 153.265497076023 / (1 - 0.104951847967976)
    if xmimpflag == 103 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0794334443169517)
    if xmimpflag == 103 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0794334443169517)
    if xmimpflag == 103 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 138.094017094017
    if xmimpflag == 103 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 138.094017094017 / (1 - 0.0794334443169517)
    if xmimpflag == 104 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.125269157905197)
    if xmimpflag == 104 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.125269157905197)
    if xmimpflag == 104 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 107.64
    if xmimpflag == 104 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 107.64 - (107.64 * 0.125269157905197)
    if xmimpflag == 105 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0887057111704602)
    if xmimpflag == 105 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0887057111704602)
    if xmimpflag == 105 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 191.988789237668
    if xmimpflag == 105 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 191.988789237668 / (1 - 0.0887057111704602)
    if xmimpflag == 106 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0985396051230542)
    if xmimpflag == 106 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0985396051230542)
    if xmimpflag == 106 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 188.140969162996
    if xmimpflag == 106 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 188.140969162996 / (1 - 0.0985396051230542)
    if xmimpflag == 107 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.199714956235816)
    if xmimpflag == 107 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.199714956235816)
    if xmimpflag == 107 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 239.363636363636
    if xmimpflag == 107 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 239.363636363636 / (1 - 0.199714956235816)
    if xmimpflag == 108 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.116764553914052)
    if xmimpflag == 108 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.116764553914052)
    if xmimpflag == 108 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 241.066480055983
    if xmimpflag == 108 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 241.066480055983 / (1 - 0.116764553914052)
    if xmimpflag == 110 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.217817105373686)
    if xmimpflag == 110 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.217817105373686)
    if xmimpflag == 110 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 321.139784946236
    if xmimpflag == 110 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 321.139784946236 / (1 - 0.217817105373686)
    if xmimpflag == 111 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.134584278813695)
    if xmimpflag == 111 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.134584278813695)
    if xmimpflag == 111 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 320.396527777777
    if xmimpflag == 111 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 320.396527777777 / (1 - 0.134584278813695)
    if xmimpflag == 112 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0649564900465187)
    if xmimpflag == 112 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0649564900465187)
    if xmimpflag == 112 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 302.919243986254
    if xmimpflag == 112 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 302.919243986254 / (1 - 0.0649564900465187)
    if xmimpflag == 113 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.294943293777566)
    if xmimpflag == 113 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.294943293777566)
    if xmimpflag == 113 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 178.191780821918
    if xmimpflag == 113 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 178.191780821918 / (1 - 0.294943293777566)
    if xmimpflag == 114 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.190466263797331)
    if xmimpflag == 114 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.190466263797331)
    if xmimpflag == 114 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 268.709993468321
    if xmimpflag == 114 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 268.709993468321 / (1 - 0.190466263797331)
    if xmimpflag == 115 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.165262209695588)
    if xmimpflag == 115 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.165262209695588)
    if xmimpflag == 115 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 265.480215827338
    if xmimpflag == 115 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 265.480215827338 / (1 - 0.165262209695588)
    if xmimpflag == 116 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.250590294065011)
    if xmimpflag == 116 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.250590294065011)
    if xmimpflag == 116 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 216.026607538803
    if xmimpflag == 116 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 216.026607538803 / (1 - 0.250590294065011)
    if xmimpflag == 117 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0862116624182079)
    if xmimpflag == 117 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0862116624182079)
    if xmimpflag == 117 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 341.979498861048
    if xmimpflag == 117 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 341.979498861048 / (1 - 0.0862116624182079)
    if xmimpflag == 118 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0795782666543268)
    if xmimpflag == 118 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0795782666543268)
    if xmimpflag == 118 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 382.444580777097
    if xmimpflag == 118 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 382.444580777097 / (1 - 0.0795782666543268)
    if xmimpflag == 120 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.100542298212489)
    if xmimpflag == 120 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.100542298212489)
    if xmimpflag == 120 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 191.62583518931
    if xmimpflag == 120 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 191.62583518931 / (1 - 0.100542298212489)
    if xmimpflag == 121 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0690791392436498)
    if xmimpflag == 121 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0690791392436498)
    if xmimpflag == 121 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 162.041666666667
    if xmimpflag == 121 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 162.041666666667 / (1 - 0.0690791392436498)
    if xmimpflag == 122 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.274602006426542)
    if xmimpflag == 122 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.274602006426542)
    if xmimpflag == 122 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 173.454545454545
    if xmimpflag == 122 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 173.454545454545 / (1 - 0.274602006426542)
    if xmimpflag == 123 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.274602006426542)
    if xmimpflag == 123 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.274602006426542)
    if xmimpflag == 123 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 255.028571428571
    if xmimpflag == 123 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 255.028571428571 / (1 - 0.274602006426542)
    if xmimpflag == 124 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.181330570603409)
    if xmimpflag == 124 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.181330570603409)
    if xmimpflag == 124 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 447.532008830022
    if xmimpflag == 124 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 447.532008830022 / (1 - 0.181330570603409)
    if xmimpflag == 1 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.255634697158707)
    if xmimpflag == 1 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.255634697158707)
    if xmimpflag == 1 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 166.401374570447
    if xmimpflag == 1 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 166.401374570447 / (1 - 0.255634697158707)
    if xmimpflag == 2 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.173114449095158)
    if xmimpflag == 2 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.173114449095158)
    if xmimpflag == 2 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 152.863945578231
    if xmimpflag == 2 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 152.863945578231 / (1 - 0.173114449095158)
    if xmimpflag == 3 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.191426939591589)
    if xmimpflag == 3 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.191426939591589)
    if xmimpflag == 3 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 250.179245283019
    if xmimpflag == 3 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 250.179245283019 / (1 - 0.191426939591589)
    if xmimpflag == 4 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.143739162059858)
    if xmimpflag == 4 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.143739162059858)
    if xmimpflag == 4 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 273.896226415094
    if xmimpflag == 4 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 273.896226415094 - (273.896226415094 * 0.143739162059858)
    if xmimpflag == 5 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0703329947332674)
    if xmimpflag == 5 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0703329947332674)
    if xmimpflag == 5 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 380.04854368932
    if xmimpflag == 5 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 380.04854368932 - (380.04854368932 * 0.0703329947332674)
    if xmimpflag == 6 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.117444418143106)
    if xmimpflag == 6 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.117444418143106)
    if xmimpflag == 6 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 305.868020304568
    if xmimpflag == 6 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 305.868020304568 / (1 - 0.117444418143106)
    if xmimpflag == 7 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.126779394689057)
    if xmimpflag == 7 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.126779394689057)
    if xmimpflag == 7 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 265.88
    if xmimpflag == 7 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 265.88 - (265.88 * 0.126779394689057)
    if xmimpflag == 8 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.189011301766662)
    if xmimpflag == 8 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.189011301766662)
    if xmimpflag == 8 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 281.325
    if xmimpflag == 8 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 281.325 / (1 - 0.189011301766662)
    if xmimpflag == 9 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.140365224720275)
    if xmimpflag == 9 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.140365224720275)
    if xmimpflag == 9 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 402.502202643172
    if xmimpflag == 9 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 402.502202643172 / (1 - 0.140365224720275)
    if xmimpflag == 10 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.107188743129005)
    if xmimpflag == 10 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.107188743129005)
    if xmimpflag == 10 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 277.059842519684
    if xmimpflag == 10 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 277.059842519684 / (1 - 0.107188743129005)
    if xmimpflag == 11 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.126901348540731)
    if xmimpflag == 11 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.126901348540731)
    if xmimpflag == 11 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 355.810945273632
    if xmimpflag == 11 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 355.810945273632 / (1 - 0.126901348540731)
    if xmimpflag == 12 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0655772248600899)
    if xmimpflag == 12 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0655772248600899)
    if xmimpflag == 12 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 309.533898305085
    if xmimpflag == 12 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 309.533898305085 / (1 - 0.0655772248600899)
    if xmimpflag == 13 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0778021073375869)
    if xmimpflag == 13 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0778021073375869)
    if xmimpflag == 13 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 305.812154696132
    if xmimpflag == 13 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 305.812154696132 / (1 - 0.0778021073375869)
    if xmimpflag == 14 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0654921908875572)
    if xmimpflag == 14 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0654921908875572)
    if xmimpflag == 14 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 285.054112554113
    if xmimpflag == 14 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 285.054112554113 / (1 - 0.0654921908875572)
    if xmimpflag == 15 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0671696102131247)
    if xmimpflag == 15 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0671696102131247)
    if xmimpflag == 15 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 361.638059701493
    if xmimpflag == 15 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 361.638059701493 / (1 - 0.0671696102131247)
    if xmimpflag == 16 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.371414750110571)
    if xmimpflag == 16 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.371414750110571)
    if xmimpflag == 16 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 239.9
    if xmimpflag == 16 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 239.9 / (1 - 0.371414750110571)
    if xmimpflag == 157 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.230610260687796)
    if xmimpflag == 157 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.230610260687796)
    if xmimpflag == 157 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 139.029411764706
    if xmimpflag == 157 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 139.029411764706 / (1 - 0.230610260687796)
    if xmimpflag == 159 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.154487726688789)
    if xmimpflag == 159 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.154487726688789)
    if xmimpflag == 159 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 245.12676056338
    if xmimpflag == 159 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 245.12676056338 / (1 - 0.154487726688789)
    if xmimpflag == 99 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.166050441674744)
    if xmimpflag == 99 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.166050441674744)
    if xmimpflag == 99 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 125.619750283768
    if xmimpflag == 99 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 125.619750283768 / (1 - 0.166050441674744)
    if xmimpflag == 100 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.178717812379779)
    if xmimpflag == 100 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.178717812379779)
    if xmimpflag == 100 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 565.645161290322
    if xmimpflag == 100 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 565.645161290322 / (1 - 0.178717812379779)
    if xmimpflag == 17 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0557746478873239)
    if xmimpflag == 17 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0557746478873239)
    if xmimpflag == 17 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 148.882352941176
    if xmimpflag == 17 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 148.882352941176 / (1 - 0.0557746478873239)
    if xmimpflag == 98 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.126563817175912)
    if xmimpflag == 98 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.126563817175912)
    if xmimpflag == 98 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 132.596685082873
    if xmimpflag == 98 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 132.596685082873 / (1 - 0.126563817175912)
    if xmimpflag == 18 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.093544030879478)
    if xmimpflag == 18 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.093544030879478)
    if xmimpflag == 18 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 184.486013986014
    if xmimpflag == 18 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 184.486013986014 / (1 - 0.093544030879478)
    if xmimpflag == 19 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0985982521761244)
    if xmimpflag == 19 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0985982521761244)
    if xmimpflag == 19 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 230.298469387755
    if xmimpflag == 19 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 230.298469387755 / (1 - 0.0985982521761244)
    if xmimpflag == 20 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0944678720322908)
    if xmimpflag == 20 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0944678720322908)
    if xmimpflag == 20 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 444.290145985401
    if xmimpflag == 20 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 444.290145985401 / (1 - 0.0944678720322908)
    if xmimpflag == 21 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.167379623404603)
    if xmimpflag == 21 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.167379623404603)
    if xmimpflag == 21 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 492.946428571429
    if xmimpflag == 21 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 492.946428571429 / (1 - 0.167379623404603)
    if xmimpflag == 22 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.183801786070534)
    if xmimpflag == 22 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.183801786070534)
    if xmimpflag == 22 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 91.9594594594595
    if xmimpflag == 22 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 91.9594594594595 / (1 - 0.183801786070534)
    if xmimpflag == 23 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.102358180948044)
    if xmimpflag == 23 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.102358180948044)
    if xmimpflag == 23 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 95.972972972973
    if xmimpflag == 23 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 95.972972972973 / (1 - 0.102358180948044)
    if xmimpflag == 24 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.122708750828674)
    if xmimpflag == 24 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.122708750828674)
    if xmimpflag == 24 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 146.31
    if xmimpflag == 24 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 146.31 / (1 - 0.122708750828674)
    if xmimpflag == 25 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.101742168136026)
    if xmimpflag == 25 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.101742168136026)
    if xmimpflag == 25 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 279.357142857143
    if xmimpflag == 25 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 279.357142857143 / (1 - 0.101742168136026)
    if xmimpflag == 26 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0830808603000646)
    if xmimpflag == 26 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0830808603000646)
    if xmimpflag == 26 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 341.5
    if xmimpflag == 26 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 341.5 / (1 - 0.0830808603000646)
    if xmimpflag == 27 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0951735364832193)
    if xmimpflag == 27 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0951735364832193)
    if xmimpflag == 27 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 335.546666666667
    if xmimpflag == 27 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 335.546666666667 - (335.546666666667 * 0.0951735364832193)
    if xmimpflag == 28 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0599984615282753)
    if xmimpflag == 28 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0599984615282753)
    if xmimpflag == 28 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 348.926267281106
    if xmimpflag == 28 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 348.926267281106 - (348.926267281106 * 0.0599984615282753)
    if xmimpflag == 29 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0849037398486349)
    if xmimpflag == 29 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0849037398486349)
    if xmimpflag == 29 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 323.539358600583
    if xmimpflag == 29 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 323.539358600583 / (1 - 0.0849037398486349)
    if xmimpflag == 30 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0831292966753462)
    if xmimpflag == 30 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0831292966753462)
    if xmimpflag == 30 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 435.738461538461
    if xmimpflag == 30 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 435.738461538461 / (1 - 0.0831292966753462)
    if xmimpflag == 31 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.154603810637904)
    if xmimpflag == 31 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.154603810637904)
    if xmimpflag == 31 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 221.279220779221
    if xmimpflag == 31 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 221.279220779221 / (1 - 0.154603810637904)
    if xmimpflag == 32 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.169381440464976)
    if xmimpflag == 32 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.169381440464976)
    if xmimpflag == 32 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 296.593103448276
    if xmimpflag == 32 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 296.593103448276 / (1 - 0.169381440464976)
    if xmimpflag == 33 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.183684529291394)
    if xmimpflag == 33 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.183684529291394)
    if xmimpflag == 33 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 281.452966714906
    if xmimpflag == 33 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 281.452966714906 / (1 - 0.183684529291394)
    if xmimpflag == 34 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0864964921326426)
    if xmimpflag == 34 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0864964921326426)
    if xmimpflag == 34 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 325.652360515021
    if xmimpflag == 34 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 325.652360515021 / (1 - 0.0864964921326426)
    if xmimpflag == 35 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.176037224384829)
    if xmimpflag == 35 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.176037224384829)
    if xmimpflag == 35 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 272.474358974359
    if xmimpflag == 35 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 272.474358974359 / (1 - 0.176037224384829)
    if xmimpflag == 36 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.116937605450612)
    if xmimpflag == 36 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.116937605450612)
    if xmimpflag == 36 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 556.677419354839
    if xmimpflag == 36 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 556.677419354839 / (1 - 0.116937605450612)
    if xmimpflag == 37 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.172812495199871)
    if xmimpflag == 37 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.172812495199871)
    if xmimpflag == 37 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 890.470588235294
    if xmimpflag == 37 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 890.470588235294 / (1 - 0.172812495199871)
    if xmimpflag == 38 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.105087524949968)
    if xmimpflag == 38 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.105087524949968)
    if xmimpflag == 38 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 335.813953488372
    if xmimpflag == 38 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 335.813953488372 / (1 - 0.105087524949968)
    if xmimpflag == 39 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0856667000685018)
    if xmimpflag == 39 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0856667000685018)
    if xmimpflag == 39 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 257.263157894737
    if xmimpflag == 39 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 257.263157894737 / (1 - 0.0856667000685018)
    if xmimpflag == 40 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0865650987499053)
    if xmimpflag == 40 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0865650987499053)
    if xmimpflag == 40 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 328.195266272189
    if xmimpflag == 40 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 328.195266272189 / (1 - 0.0865650987499053)
    if xmimpflag == 41 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.171814252005436)
    if xmimpflag == 41 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.171814252005436)
    if xmimpflag == 41 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 129.145454545455
    if xmimpflag == 41 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 129.145454545455 / (1 - 0.171814252005436)
    if xmimpflag == 42 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0610387045813586)
    if xmimpflag == 42 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0610387045813586)
    if xmimpflag == 42 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 158.1
    if xmimpflag == 42 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 158.1 / (1 - 0.0610387045813586)
    if xmimpflag == 43 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.159823459162871)
    if xmimpflag == 43 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.159823459162871)
    if xmimpflag == 43 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 247.759689922481
    if xmimpflag == 43 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 247.759689922481 / (1 - 0.159823459162871)
    if xmimpflag == 44 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0988853555387519)
    if xmimpflag == 44 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0988853555387519)
    if xmimpflag == 44 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 363
    if xmimpflag == 44 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 363 / (1 - 0.0988853555387519)
    if xmimpflag == 45 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0904513085721602)
    if xmimpflag == 45 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0904513085721602)
    if xmimpflag == 45 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 466.25641025641
    if xmimpflag == 45 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 466.25641025641 / (1 - 0.0904513085721602)
    if xmimpflag == 46 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.082310278477633)
    if xmimpflag == 46 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.082310278477633)
    if xmimpflag == 46 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 159.810810810811
    if xmimpflag == 46 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 159.810810810811 / (1 - 0.082310278477633)
    if xmimpflag == 47 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.104714300552102)
    if xmimpflag == 47 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.104714300552102)
    if xmimpflag == 47 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 638.25
    if xmimpflag == 47 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 638.25 / (1 - 0.104714300552102)
    if xmimpflag == 48 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.193439630544956)
    if xmimpflag == 48 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.193439630544956)
    if xmimpflag == 48 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 608.392156862745
    if xmimpflag == 48 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 608.392156862745 / (1 - 0.193439630544956)
    if xmimpflag == 49 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.145583038352611)
    if xmimpflag == 49 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.145583038352611)
    if xmimpflag == 49 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 428.888888888889
    if xmimpflag == 49 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 428.888888888889 / (1 - 0.145583038352611)
    if xmimpflag == 50 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.233333333333333)
    if xmimpflag == 50 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.233333333333333)
    if xmimpflag == 50 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 270.846153846154
    if xmimpflag == 50 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 270.846153846154 / (1 - 0.233333333333333)
    if xmimpflag == 51 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.179223522528989)
    if xmimpflag == 51 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.179223522528989)
    if xmimpflag == 51 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 229.64
    if xmimpflag == 51 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 229.64 / (1 - 0.179223522528989)
    if xmimpflag == 52 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0819156347249732)
    if xmimpflag == 52 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0819156347249732)
    if xmimpflag == 52 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 290.164383561644
    if xmimpflag == 52 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 290.164383561644 - (290.164383561644 * 0.0819156347249732)
    if xmimpflag == 53 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0540922242825536)
    if xmimpflag == 53 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0540922242825536)
    if xmimpflag == 53 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 256.548387096774
    if xmimpflag == 53 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 256.548387096774 / (1 - 0.0540922242825536)
    if xmimpflag == 54 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0913651933726713)
    if xmimpflag == 54 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0913651933726713)
    if xmimpflag == 54 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 216.907894736842
    if xmimpflag == 54 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 216.907894736842 / (1 - 0.0913651933726713)
    if xmimpflag == 55 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0604022380426763)
    if xmimpflag == 55 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0604022380426763)
    if xmimpflag == 55 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 241.461538461538
    if xmimpflag == 55 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 241.461538461538 / (1 - 0.0604022380426763)
    if xmimpflag == 56 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0542026549646127)
    if xmimpflag == 56 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0542026549646127)
    if xmimpflag == 56 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 340.230769230769
    if xmimpflag == 56 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 340.230769230769 / (1 - 0.0542026549646127)
    if xmimpflag == 57 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0974564330758702)
    if xmimpflag == 57 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0974564330758702)
    if xmimpflag == 57 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 516.45
    if xmimpflag == 57 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 516.45 / (1 - 0.0974564330758702)
    if xmimpflag == 58 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.162886379968412)
    if xmimpflag == 58 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.162886379968412)
    if xmimpflag == 58 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 447.518072289157
    if xmimpflag == 58 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 447.518072289157 - (447.518072289157 * 0.162886379968412)
    if xmimpflag == 59 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0561646667118922)
    if xmimpflag == 59 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0561646667118922)
    if xmimpflag == 59 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 152.923076923077
    if xmimpflag == 59 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 152.923076923077 / (1 - 0.0561646667118922)
    if xmimpflag == 60 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.133468501803896)
    if xmimpflag == 60 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.133468501803896)
    if xmimpflag == 60 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 403.292993630573
    if xmimpflag == 60 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 403.292993630573 / (1 - 0.133468501803896)
    if xmimpflag == 61 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.106708705390018)
    if xmimpflag == 61 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.106708705390018)
    if xmimpflag == 61 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 285.644444444444
    if xmimpflag == 61 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 285.644444444444 / (1 - 0.106708705390018)
    if xmimpflag == 62 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0785278768682708)
    if xmimpflag == 62 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0785278768682708)
    if xmimpflag == 62 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 335.658227848101
    if xmimpflag == 62 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 335.658227848101 / (1 - 0.0785278768682708)
    if xmimpflag == 63 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.107782269167156)
    if xmimpflag == 63 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.107782269167156)
    if xmimpflag == 63 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 472.267857142857
    if xmimpflag == 63 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 472.267857142857 / (1 - 0.107782269167156)
    if xmimpflag == 160 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0779281672325541)
    if xmimpflag == 160 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0779281672325541)
    if xmimpflag == 160 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 536.842857142857
    if xmimpflag == 160 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 536.842857142857 / (1 - 0.0779281672325541)
    if xmimpflag == 65 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.115409873680179)
    if xmimpflag == 65 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.115409873680179)
    if xmimpflag == 65 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 103.376146788991
    if xmimpflag == 65 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 103.376146788991 / (1 - 0.115409873680179)
    if xmimpflag == 66 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.207088877726936)
    if xmimpflag == 66 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.207088877726936)
    if xmimpflag == 66 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 68.1506849315068
    if xmimpflag == 66 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 68.1506849315068 / (1 - 0.207088877726936)
    if xmimpflag == 67 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.110922605367631)
    if xmimpflag == 67 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.110922605367631)
    if xmimpflag == 67 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 80.0491803278688
    if xmimpflag == 67 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 80.0491803278688 / (1 - 0.110922605367631)
    if xmimpflag == 68 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.127935729778166)
    if xmimpflag == 68 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.127935729778166)
    if xmimpflag == 68 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 84
    if xmimpflag == 68 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 84 - (84 * 0.127935729778166)
    if xmimpflag == 69 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.206358225584424)
    if xmimpflag == 69 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.206358225584424)
    if xmimpflag == 69 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 1004.47058823529
    if xmimpflag == 69 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 1004.47058823529 / (1 - 0.206358225584424)
    if xmimpflag == 70 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.142775407154303)
    if xmimpflag == 70 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.142775407154303)
    if xmimpflag == 70 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 311.222222222222
    if xmimpflag == 70 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 311.222222222222 / (1 - 0.142775407154303)
    if xmimpflag == 71 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.106323148232566)
    if xmimpflag == 71 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.106323148232566)
    if xmimpflag == 71 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 310.39837398374
    if xmimpflag == 71 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 310.39837398374 / (1 - 0.106323148232566)
    if xmimpflag == 97 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.138965456634756)
    if xmimpflag == 97 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.138965456634756)
    if xmimpflag == 97 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 259.21875
    if xmimpflag == 97 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 259.21875 / (1 - 0.138965456634756)
    if xmimpflag == 72 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.169436742362705)
    if xmimpflag == 72 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.169436742362705)
    if xmimpflag == 72 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 265.325842696629
    if xmimpflag == 72 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 265.325842696629 / (1 - 0.169436742362705)
    if xmimpflag == 85 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.339905284604731)
    if xmimpflag == 85 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.339905284604731)
    if xmimpflag == 85 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 563.333333333333
    if xmimpflag == 85 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 563.333333333333 / (1 - 0.339905284604731)
    if xmimpflag == 73 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.129605450439467)
    if xmimpflag == 73 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.129605450439467)
    if xmimpflag == 73 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 407.289473684211
    if xmimpflag == 73 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 407.289473684211 / (1 - 0.129605450439467)
    if xmimpflag == 74 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0794384325299229)
    if xmimpflag == 74 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0794384325299229)
    if xmimpflag == 74 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 117.137931034483
    if xmimpflag == 74 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 117.137931034483 / (1 - 0.0794384325299229)
    if xmimpflag == 75 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.189369734252207)
    if xmimpflag == 75 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.189369734252207)
    if xmimpflag == 75 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 192.772020725389
    if xmimpflag == 75 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 192.772020725389 / (1 - 0.189369734252207)
    if xmimpflag == 76 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.131187789757565)
    if xmimpflag == 76 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.131187789757565)
    if xmimpflag == 76 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 199.041666666667
    if xmimpflag == 76 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 199.041666666667 / (1 - 0.131187789757565)
    if xmimpflag == 77 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.136342992788614)
    if xmimpflag == 77 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.136342992788614)
    if xmimpflag == 77 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 186.407894736842
    if xmimpflag == 77 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 186.407894736842 / (1 - 0.136342992788614)
    if xmimpflag == 78 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.103049659988616)
    if xmimpflag == 78 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.103049659988616)
    if xmimpflag == 78 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 155.470588235294
    if xmimpflag == 78 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 155.470588235294 / (1 - 0.103049659988616)
    if xmimpflag == 79 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.35)
    if xmimpflag == 79 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.35)
    if xmimpflag == 79 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 193.74358974359
    if xmimpflag == 79 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 193.74358974359 / (1 - 0.35)
    if xmimpflag == 80 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0732085200996002)
    if xmimpflag == 80 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0732085200996002)
    if xmimpflag == 80 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 249.692307692308
    if xmimpflag == 80 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 249.692307692308 / (1 - 0.0732085200996002)
    if xmimpflag == 81 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0934359066589073)
    if xmimpflag == 81 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0934359066589073)
    if xmimpflag == 81 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 352.952806122449
    if xmimpflag == 81 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 352.952806122449 / (1 - 0.0934359066589073)
    if xmimpflag == 82 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.07182740558555)
    if xmimpflag == 82 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.07182740558555)
    if xmimpflag == 82 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 419.619047619047
    if xmimpflag == 82 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 419.619047619047 / (1 - 0.07182740558555)
    if xmimpflag == 83 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0956449943871365)
    if xmimpflag == 83 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0956449943871365)
    if xmimpflag == 83 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 304.5625
    if xmimpflag == 83 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 304.5625 - (304.5625 * 0.0956449943871365)
    if xmimpflag == 84 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.163929225997462)
    if xmimpflag == 84 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.163929225997462)
    if xmimpflag == 84 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 319.285714285714
    if xmimpflag == 84 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 319.285714285714 / (1 - 0.163929225997462)
    if xmimpflag == 86 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.112733293827202)
    if xmimpflag == 86 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.112733293827202)
    if xmimpflag == 86 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 129.277777777778
    if xmimpflag == 86 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 129.277777777778 / (1 - 0.112733293827202)
    if xmimpflag == 87 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0655504344628028)
    if xmimpflag == 87 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0655504344628028)
    if xmimpflag == 87 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 211
    if xmimpflag == 87 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 211 / (1 - 0.0655504344628028)
    if xmimpflag == 88 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.198929221794951)
    if xmimpflag == 88 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.198929221794951)
    if xmimpflag == 88 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 296.473684210526
    if xmimpflag == 88 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 296.473684210526 - (296.473684210526 * 0.198929221794951)
    if xmimpflag == 89 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.107517933823928)
    if xmimpflag == 89 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.107517933823928)
    if xmimpflag == 89 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 281.958333333333
    if xmimpflag == 89 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 281.958333333333 / (1 - 0.107517933823928)
    if xmimpflag == 90 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.028250184258012)
    if xmimpflag == 90 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.028250184258012)
    if xmimpflag == 90 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 208.341176470588
    if xmimpflag == 90 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 208.341176470588 / (1 - 0.028250184258012)
    if xmimpflag == 91 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0487771272192143)
    if xmimpflag == 91 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0487771272192143)
    if xmimpflag == 91 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 267.896551724138
    if xmimpflag == 91 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 267.896551724138 / (1 - 0.0487771272192143)
    if xmimpflag == 92 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.111975986975987)
    if xmimpflag == 92 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.111975986975987)
    if xmimpflag == 92 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 328.555555555556
    if xmimpflag == 92 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 328.555555555556 / (1 - 0.111975986975987)
    if xmimpflag == 93 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0979648763988006)
    if xmimpflag == 93 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0979648763988006)
    if xmimpflag == 93 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 101.111111111111
    if xmimpflag == 93 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 101.111111111111 / (1 - 0.0979648763988006)
    if xmimpflag == 94 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.297737659966491)
    if xmimpflag == 94 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.297737659966491)
    if xmimpflag == 94 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 319.733333333333
    if xmimpflag == 94 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 319.733333333333 / (1 - 0.297737659966491)
    if xmimpflag == 95 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0220048899755501)
    if xmimpflag == 95 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0220048899755501)
    if xmimpflag == 95 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 220.428571428571
    if xmimpflag == 95 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 220.428571428571 / (1 - 0.0220048899755501)
    if xmimpflag == 96 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0)
    if xmimpflag == 96 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0)
    if xmimpflag == 96 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 433
    if xmimpflag == 96 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 433 / (1 - 0)
    if xmimpflag == 137 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.12659407459354)
    if xmimpflag == 137 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.12659407459354)
    if xmimpflag == 137 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 104.986301369863
    if xmimpflag == 137 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 104.986301369863 / (1 - 0.12659407459354)
    if xmimpflag == 138 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.179201806454531)
    if xmimpflag == 138 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.179201806454531)
    if xmimpflag == 138 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 108.37037037037
    if xmimpflag == 138 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 108.37037037037 - (108.37037037037 * 0.179201806454531)
    if xmimpflag == 139 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.162003845923261)
    if xmimpflag == 139 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.162003845923261)
    if xmimpflag == 139 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 128.438775510204
    if xmimpflag == 139 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 128.438775510204 / (1 - 0.162003845923261)
    if xmimpflag == 140 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.171264386321147)
    if xmimpflag == 140 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.171264386321147)
    if xmimpflag == 140 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 557.6
    if xmimpflag == 140 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 557.6 / (1 - 0.171264386321147)
    if xmimpflag == 141 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.213152374545978)
    if xmimpflag == 141 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.213152374545978)
    if xmimpflag == 141 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 74
    if xmimpflag == 141 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 74 / (1 - 0.213152374545978)
    if xmimpflag == 142 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.190548809128441)
    if xmimpflag == 142 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.190548809128441)
    if xmimpflag == 142 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 80.5625
    if xmimpflag == 142 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 80.5625 - (80.5625 * 0.190548809128441)
    if xmimpflag == 145 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.0577485174550083)
    if xmimpflag == 145 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.0577485174550083)
    if xmimpflag == 145 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 376.928571428571
    if xmimpflag == 145 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 376.928571428571 / (1 - 0.0577485174550083)
    if xmimpflag == 146 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.153749295952981)
    if xmimpflag == 146 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.153749295952981)
    if xmimpflag == 146 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 154.307692307692
    if xmimpflag == 146 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 154.307692307692 / (1 - 0.153749295952981)
    if xmimpflag == 147 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.143606923731731)
    if xmimpflag == 147 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.143606923731731)
    if xmimpflag == 147 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 165.903225806452
    if xmimpflag == 147 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 165.903225806452 - (165.903225806452 * 0.143606923731731)
    if xmimpflag == 148 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.254317624200109)
    if xmimpflag == 148 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.254317624200109)
    if xmimpflag == 148 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 199.730769230769
    if xmimpflag == 148 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 199.730769230769 / (1 - 0.254317624200109)
    if xmimpflag == 149 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.136559928551299)
    if xmimpflag == 149 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.136559928551299)
    if xmimpflag == 149 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 1003
    if xmimpflag == 149 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 1003 / (1 - 0.136559928551299)
    if xmimpflag == 150 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.182187702624498)
    if xmimpflag == 150 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.182187702624498)
    if xmimpflag == 150 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 100.090909090909
    if xmimpflag == 150 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 100.090909090909 / (1 - 0.182187702624498)
    if xmimpflag == 151 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.00833333333333333)
    if xmimpflag == 151 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.00833333333333333)
    if xmimpflag == 151 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 127.103448275862
    if xmimpflag == 151 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 127.103448275862 / (1 - 0.00833333333333333)
    if xmimpflag == 152 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.100333848361108)
    if xmimpflag == 152 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.100333848361108)
    if xmimpflag == 152 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 436.5
    if xmimpflag == 152 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 436.5 / (1 - 0.100333848361108)
    if xmimpflag == 154 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.235321405225611)
    if xmimpflag == 154 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.235321405225611)
    if xmimpflag == 154 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 580.060606060606
    if xmimpflag == 154 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 580.060606060606 / (1 - 0.235321405225611)
    if xmimpflag == 155 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.157476046121814)
    if xmimpflag == 155 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.157476046121814)
    if xmimpflag == 155 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 70.0833333333334
    if xmimpflag == 155 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 70.0833333333334 / (1 - 0.157476046121814)
    if xmimpflag == 156 and slaximp >= 1 and not slaarriv and not slastot:
        slamimp = slaximp - (slaximp * 0.17641709128796)
    if xmimpflag == 156 and slamimp >= 1 and not tslavesd and not tslavesp and not ncartot:
        slaximp = slamimp / (1 - 0.17641709128796)
    if xmimpflag == 156 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slamimp = 118.333333333333
    if xmimpflag == 156 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = 118.333333333333 / (1 - 0.17641709128796)

    sladvoy = _numbers.get('SLADVOY')
    if sladvoy > 0 and not slaarriv and not tslavesd and not tslavesp and not ncartot and slastot >= 50:
        slaximp = slastot + sladvoy
    if sladvoy > 0 and not tslavesd and not tslavesp and not ncartot and slaarriv > 1:
        slaximp = slaarriv + sladvoy
    if sladvoy > 0 and not tslavesd and not tslavesp and not ncartot and not slaarriv and not slastot:
        slaximp = slamimp + sladvoy

    slaximp = round(slaximp) if slaximp else None
    slamimp = round(slamimp) if slamimp else None

    # tslmtimp - Imputed total of slaves embarked for mortality calculation
    # vymrtimp - Imputed number of slaves died in middle passage
    # vymrtrat - Slaves died on voyage / Slaves embarked

    vymrtimp = sladvoy
    tslmtimp = None
    slaarriv = _numbers.get('SLAARRIV')
    if sladvoy is None and slaarriv is not None and slaarriv <= tslavesd:
        vymrtimp = tslavesd - slaarriv
    if vymrtimp >= 0:
        tslmtimp = tslavesd
    if (not tslavesd and vymrtimp >= 0) and slaarriv >= 1:
        tslmtimp = slaarriv + vymrtimp
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

    adlt1imp = men1 + women1 + adult1 + men4 + \
        women4 + adult4 + men5 + women5 + adult5
    chil1imp = boy1 + girl1 + child1 + infant1 + boy4 + \
        girl4 + child4 + infant4 + boy5 + girl5 + child5
    male1imp = male1 + male4 + male5
    feml1imp = female1 + female4 + female5
    if not male1imp:
        male1imp = men1 + boy1 + men4 + boy4 + men5 + boy5
    if not feml1imp:
        feml1imp = women1 + girl1 + women4 + girl4 + women5 + girl5
    slavema1 = threshold(adlt1imp + chil1imp, 20)
    slavemx1 = threshold(male1imp + feml1imp, 20)
    slavmax1 = threshold(
        men1 + women1 + boy1 + girl1 + men4 + women4 + boy4 + girl4 + men5 +
        women5 + boy5 + girl5, 20)
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
    if slavmax1 >= 20:
        menrat1 = (men1 + men4 + men5) / slavmax1
    if slavmax1 >= 20:
        womrat1 = (women1 + women4 + women5) / slavmax1
    if slavmax1 >= 20:
        boyrat1 = (boy1 + boy4 + boy5) / slavmax1
    if slavmax1 >= 20:
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
    if slavmax3 >= 20:
        menrat3 = (men3 + men6) / slavmax3
    if slavmax3 >= 20:
        womrat3 = (women3 + women6) / slavmax3
    if slavmax3 >= 20:
        boyrat3 = (boy3 + boy6) / slavmax3
    if slavmax3 >= 20:
        girlrat3 = (girl3 + girl6) / slavmax3

    # men7 - Imputed men when leaving Africa or arriving at ports of landing
    # women7 - Imputed women when leaving Africa or arriving at ports of landing
    # boy7 - Imputed boys when leaving Africa or arriving at ports of landing
    # girl7 - Imputed girls when leaving Africa or arriving at ports of landing
    # adult7 - Imputed adults when leaving Africa or arriving at ports of landing
    # child7 - Imputed children when leaving Africa or arriving at ports of lading
    # male7 - Imputed males when leaving Africa or arriving at ports of landing
    # female7 - Imputed females when leaving Africa or arriving at ports of landing
    # slavema7 - Number of slaves with age identIfied, Africa or ports of lading
    # slavemx7 - Number of slaves with sex identIfied, Africa or ports of landing
    # slavmax7 - Number of slaves identIfied by both age and sex
    # menrat7 - Imputed ratio of men when leaving Africa or arriving at ports of landing
    # womrat7 - Imputed ratio of women when leaving Africa or arriving at ports of landing
    # boyrat7 - Imputed ratio of boys when leaving Africa or arriving at ports of landing
    # girlrat7 - Imputed ratio of girls when leaving Africa or arriving at ports of landing
    # chilrat7 - Imputed ratio of children when leaving Africa or arriving at ports of landing
    # malrat7 - Imputed ratio of males when leaving Africa or arriving at ports of landing
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

    if slavema3 >= 20:
        slavema7 = slavema3
    if slavemx3 >= 20:
        slavemx7 = slavemx3
    if slavmax3 >= 20:
        slavmax7 = slavmax3
    if slavmax7 >= 20:
        men7 = men3 + men6
    if slavmax7 >= 20:
        women7 = women3 + women6
    if slavmax7 >= 20:
        boy7 = boy3 + boy6
    if slavmax7 >= 20:
        girl7 = girl3 + girl6
    if slavema7 >= 20:
        adult7 = adlt3imp
    if slavema7 >= 20:
        child7 = chil3imp
    if slavemx7 >= 20:
        male7 = male3imp
    if slavemx7 >= 20:
        female7 = feml3imp
    if menrat3 >= 0:
        menrat7 = menrat3
    if womrat3 >= 0:
        womrat7 = womrat3
    if boyrat3 >= 0:
        boyrat7 = boyrat3
    if girlrat3 >= 0:
        girlrat7 = girlrat3
    if malrat3 >= 0:
        malrat7 = malrat3
    if chilrat3 >= 0:
        chilrat7 = chilrat3

    if slavema3 is None and slavema1 >= 20:
        slavema7 = slavema1
    if slavemx3 is None and slavemx1 >= 20:
        slavemx7 = slavemx1
    if slavmax3 is None and slavmax1 >= 20:
        slavmax7 = slavmax1
    if slavmax3 is None and slavmax1 >= 20:
        men7 = men1 + men4 + men5
    if slavmax3 is None and slavmax1 >= 20:
        women7 = women1 + women4 + women5
    if slavmax3 is None and slavmax1 >= 20:
        boy7 = boy1 + boy4 + boy5
    if slavmax3 is None and slavmax1 >= 20:
        girl7 = girl1 + girl4 + girl5
    if slavema3 is None and slavema1 >= 20:
        adult7 = adlt1imp
    if slavema3 is None and slavema1 >= 20:
        child7 = chil1imp
    if slavemx3 is None and slavemx1 >= 20:
        male7 = male1imp
    if slavemx3 is None and slavemx1 >= 20:
        female7 = feml1imp
    if menrat3 is None and menrat1 >= 0:
        menrat7 = menrat1
    if womrat3 is None and womrat1 >= 0:
        womrat7 = womrat1
    if boyrat3 is None and boyrat1 >= 0:
        boyrat7 = boyrat1
    if girlrat3 is None and girlrat1 >= 0:
        girlrat7 = girlrat1
    if malrat3 is None and malrat1 >= 0:
        malrat7 = malrat1
    if chilrat3 is None and chilrat1 >= 0:
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

    if sladvoy >= 1 and chil2imp >= 1 and adlt2imp == 0 and sladvoy > chil2imp and chil2imp:
        adlt2imp = sladvoy - chil2imp
    if sladvoy >= 1 and adlt2imp >= 1 and chil2imp == 0 and sladvoy > adlt2imp and adlt2imp:
        chil2imp = sladvoy - adlt2imp
    if sladvoy >= 1 and feml2imp >= 1 and male2imp == 0 and sladvoy > feml2imp and feml2imp:
        male2imp = sladvoy - feml2imp
    if sladvoy >= 1 and male2imp >= 1 and feml2imp == 0 and sladvoy > male2imp and male2imp:
        feml2imp = sladvoy - male2imp

    local_vars = locals()
    local_vars = {
        k: v for k, v in list(local_vars.items()) if not k.startswith('_')
    }

    # Recode zero numerical values to None and vice versa with an 'all or nothing' logic.
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

    # Fields that are not available/present in I-Am and should be removed from the output.
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
