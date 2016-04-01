# Calculation of imputed variables
# Python code based on original SPSS script.

from datetime import datetime

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
    if len(split) != 3 or len(split[2]) != 4 or len(split[1]) == 0 or len(split[0]) == 0:
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

def get_imputed_vars(interim):
    """
    Extract all imputed variables from the interim model.
    :param interim: the interim model (contribute.models.InterimVoyage)
    """
    dict = get_date_vars(interim)

def recode_var(dict, value):
    """
    Recode a variable based on groups of values.
    :param dict: a dictionary of (key, [list]) which
                 each lists are pairwise disjoint and
                 one of them should contain the parameter
                 value.
    :param value: the value to search on the lists indexed by dict
    """
    for key, lst in dict.items():
        if value in lst:
            return key
    return None
    
def get_date_vars(interim):
    """
    The date variables in the interim model are usually comma separated.
    This function will search through a list of ordered date fields and
    take the first non-null year value from the list for the imputed year
    variable.
    """
    named_sources = {
        'd1slatrc': interim.date_slave_purchase_began,
        'datarr34': interim.date_first_slave_disembarkation,
        'datarr45': interim.date_voyage_completed,
        'datedepc': interim.date_departure,
        'dlslatrc': interim.date_vessel_left_last_slaving_port,
        'ddepamc': interim.date_return_departure,
    }
    
    def extract_year_from_sources(sources):
        return first_valid(map(extract_year, [named_sources.get(var_name) for var_name in sources]))
    
    # WARNING: ddepamc IS MISSING from our model
    
    # YEARDEP - Year voyage began (imputed)
    yeardep_sources = ['datedepc', 'd1slatrc', 'dlslatrc', 'datarr34', 'ddepamc', 'datarr45']
    interim.imputed_year_voyage_began = extract_year_from_sources(yeardep_sources)
    
    # YEARAF - Year departed Africa (imputed)
    yearaf_sources = ['dlslatrc', 'd1slatrc', 'datedepc', 'datarr34', 'ddepamc', 'datarr45]
    interim.imputed_year_departed_africa = extract_year_from_sources(yearaf_sources)
    
    # YEARAM Year of arrival at port of disembarkation (imputed)
    yearam_sources = ['datarr34', 'dlslatrc', 'd1slatrc', 'datedepc', 'ddepamc', 'datedepc', 'datarr45']
    yearam = extract_year_from_sources(yearam_sources)
    interim.imputed_year_arrived_at_port_of_disembarkation = yearam
    
    def year_mod(the_year, mod, start):
        return 1 + ((the_year - start - 1) // mod)
    
    # YEAR5
    interim.imputed_quinquennium_in_which_voyage_occurred = year_mod(yearam, 5, 1525)
    # YEAR10
    interim.imputed_decade_in_which_voyage_occurred = year_mod(yearam, 10, 1500)
    # YEAR25
    interim.imputed_quarter_century_in_which_voyage_occurred = year_mod(yearam, 25, 1500)
    # YEAR100
    interim.imputed_century_in_which_voyage_occurred = ((yearam - 1) // 100) * 100
    # VOY1IMP = DATEDIF(DATE_LAND1, DATE_DEP, "days").
    voy1imp = date_diff(
        interim.date_first_slave_disembarkation,
        interim.date_departure
    )
    if voy1imp and voy1imp <= 10:
        voy1imp = None 
    interim.imputed_voyage_length_home_port_to_first_port_of_disembarkation = voy1imp
    # VOY2IMP = DATEDIF(DATE_LAND1, DATE_LEFTAFR, "days").
    voy2imp = date_diff(
        interim.date_first_slave_disembarkation,
        interim.date_vessel_left_last_slaving_port
    )
    interim_length = interim.length_of_middle_passage
    if voy2imp is None or (voy2imp < 20 and interim_length and interim_length - voy2imp > 10)):
        voy2imp = interim_length
    if voy2imp and voy2imp <= 38:
        voy2imp = None
    interim.imputed_voyage_length_home_port_to_first_port_of_disembarkation = voy2imp
    
    natinimp = interim.ship_registration_place
    tonnage = interim.tonnage_of_vessel
    if tonnage:
        tontype = interim.ton_type
        if tontype == 13:
            tonmod = tonnage
        if (tontype < 3 or tontype == 4 or tontype == 5) and yearam > 1773:
            tonmod = tonnage
        if (tontype < 3 or tontype == 4 or tontype == 5) and yearam < 1774 and tonnage > 250:
            tonmod = 13.1 + (1.1 * tonnage)
        if (tontype < 3 or tontype == 4 or tontype == 5) and yearam < 1774 and tonnage > 150 and tonnage < 251:
            tonmod = 65.3 + (1.2 * tonnage)
        if (tontype < 3 or tontype == 4 or tontype == 5) and yearam < 1774 and tonnage < 151:
            tonmod = 2.3 + (1.8 * tonnage)
        if tontype == 4 and yearam > 1783 and yearam < 1794:
            tonmod = None
        if tontype == 3 or tontype == 6 or tontype == 9 or tontype == 16:
            tonmod = 71 + (0.86 * tonnage)
        if (tontype == 3 or tontype == 6 or tontype == 9 or tontype == 16) and yearam < 1774 and tonmod > 250:
            tonmod = 13.1 + (1.1 * tonnage)
        if (tontype == 3 or tontype == 6 or tontype == 9 or tontype == 16) and yearam < 1774 and tonmod > 150 and tonmod < 251:
            tonmod = 65.3 + (1.2 * tonnage)
        if (tontype == 3 or tontype == 6 or tontype == 9 or tontype == 16) and yearam < 1774 and tonmod < 151:
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
        if tontype is None and yearam > 1714 and yearam < 1786 and tonnage > 0 and natinimp == 7:
            tontype = 22
        if tontype == 22 and tonnage > 250:
            tonmod = 13.1 + (1.1 * tonnage)
        if tontype == 22 and tonnage > 150 and tonnage < 251:
            tonmod = 65.3 + (1.2 * tonnage)
        if tontype == 22 and tonnage < 151:
            tonmod = 2.3 + (1.8 * tonnage)
        if tontype == 15 or tontype == 14 or tontype == 17:
            tonmod = 52.86 + (1.22 * tonnage)
        
        interim.imputed_standardized_tonnage = tonmod
    
    if interim.voyage_outcome:
        interim.imputed_outcome_of_voyage_for_slaves = recode_var(
            {
                1: [1, 4, 5, 7, 8, 9, 11, 12, 15, 16, 17, 19, 20, 24, 26, 29, 30, 39, 40, 46, 47, 48, 49,
                    51, 52, 54, 58, 68, 70, 71, 72, 76, 78, 79, 80, 81, 82, 85, 88, 92, 95, 97, 104, 108,
                    109, 122, 123, 124, 125, 132, 134, 135, 142, 144, 148, 154, 157, 159, 161, 162, 163,
                    170, 171,172,173, 174, 176,177, 178, 179, 180, 181, 182, 183, 184, 185, 187, 189, 201,
                    203, 205],
                2: [2, 6, 10, 14, 18, 22, 25, 27, 31, 41, 45, 50, 57, 74, 90, 93, 94, 96, 102, 103, 106,
                    110, 111, 112, 118, 121, 126, 127, 128, 130, 138, 141, 153, 155, 156, 160, 192, 193,
                    198, 202],
                3: [42, 44, 69, 73, 114, 120, 206, 207],
                4: [3, 66, 99],
                5: [13, 21, 23, 43, 53, 55, 56, 59, 67, 77, 86, 87, 113, 164, 165, 166, 188, 191, 194, 195,
                    196, 199],
                6: [208],
                7: [28, 75, 89, 91, 98]
            }, 
            interim.voyage_outcome
        )
        interim.imputed_outcome_of_voyage_if_ship_captured = recode_var(
            {
                1: [2, 3, 4, 5, 27, 28, 29, 30, 75, 85, 86, 91, 94, 95, 97],
                2: [6, 7, 8, 9, 31, 48, 96, 159, 192, 193],
                3: [10, 11, 12, 13, 54, 58, 102, 103, 104, 106, 108, 109, 110, 111, 112, 113, 114, 118,
                    120, 121, 122, 123, 124, 125, 126, 127, 128, 130, 132, 134, 135, 138, 141, 144, 148,
                    155, 156, 194, 196, 198, 202, 203, 205],
                4: [14, 15, 16, 17],
                5: [18, 19, 20, 21, 187, 188, 189, 191, 195],
                6: [22, 23, 24, 25, 55],
                8: [43, 50, 51, 52, 53, 164, 165, 166, 170, 171, 172, 173, 174, 176, 177, 178, 179, 180,
                    181, 182, 183, 184],
                9: [160, 161, 162, 163, 185],
                10: [42, 56, 66, 69, 73, 76, 80, 81, 82, 87, 99],
                11: [57, 74, 79, 89, 90, 98],
                12: [142, 199],
                13: [26, 39, 45, 46, 47, 67, 71, 72, 78, 153, 154, 157],
                14: [1, 40,41,44,49, 59, 68, 70, 77, 88, 92, 93, 206, 207],
                15: [208],
                16: [201],
                17: [211],
                18: [212]
            }, 
            interim.voyage_outcome
        )
        interim.imputed_outcome_of_voyage_for_owner = recode_var(
            {
                1: [1, 49, 68, 77, 79, 88, 92, 135, 203, 205, 206, 207, 208],
                2: [2, 3, 4, 5, 27, 28, 29, 30, 54, 58, 59, 85, 86, 91, 94, 95, 97],
                3: [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 31,
                    39, 41, 42, 43, 44, 45, 46, 47, 48, 50, 51, 52, 53, 55, 56, 57, 66, 67, 69, 71, 72,
                    73, 74, 75, 76, 78, 80, 81, 82, 87, 89, 90, 93, 98, 99, 102, 103, 104, 106, 108, 109,
                    110, 111, 112, 113, 114, 118, 120, 121, 122, 123, 124, 125, 126, 127, 128, 130, 132,
                    134, 138, 141, 142, 144, 148, 153, 154, 155, 156, 157, 159, 160, 161, 162, 163, 164,
                    165, 166, 170, 171, 172, 173, 174, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185,
                    187, 188, 189, 191, 192, 193, 194, 195, 196, 198, 199, 201, 202],
                4: [40,70,96,208]
            }, 
            interim.voyage_outcome
        )
        
        