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
    # Check validation for voy2imp, looks fishy in the SPSS script:
    # If (missing(voy2imp) | (voy2imp < 20 & (voyage - voy2imp > 10))) voy2imp=voyage.
    # the reference to voyage above does not make sense.
    if voy2imp and voy2imp <= 38:
        voy2imp = None
    interim.imputed_voyage_length_home_port_to_first_port_of_disembarkation = voy2imp
