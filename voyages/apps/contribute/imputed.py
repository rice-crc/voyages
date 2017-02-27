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
    
def get_imputed_vars(interim):
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
    
    natinimp = interim.ship_registration_place__value
    tonnage = interim.tonnage_of_vessel
    if tonnage:
        tontype = interim.ton_type__id
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
    
    fate2 = None
    fate3 = None
    fate4 = None
    if interim.voyage_outcome:
        # fate2 - Outcome of voyage for slaves
        fate2 = recode_var(
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
        interim.imputed_outcome_of_voyage_for_slaves = SlavesOutcome.objects.get(value=fate2)
        # fate3 - Outcome of voyage If vessel captured
        fate3 = recode_var(
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
        interim.imputed_outcome_of_voyage_if_ship_captured = VesselCapturedOutcome.objects.get(value=fate3)
        # fate4 - Outcome of voyage for owner
        fate4 = recode_var(
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
        interim.imputed_outcome_of_voyage_for_owner = OwnerOutcome.objects.get(value=fate4)
        
    # At the equivalent point in SPSS, regions are infered from places.
    # This is probably redundant given our models already connect places
    # to regions, so lines 293-406 of the SPSS script are skipped.
    
    # what to do with 410-420?
    
    embport = interim.first_port_intended_embarkation__value
    embport2 = interim.second_port_intended_embarkation__value
    regem1 = interim.imputed_first_region_of_embarkation_of_slaves__value
    regem2= interim.imputed_second_region_of_embarkation_of_slaves__value
    regem3 = interim.imputed_third_region_of_embarkation_of_slaves__value
    
    numbers = {n.var_name: n.number for n in interim.slave_numbers.all()}
    
    # mjbyptimp - Principal port of slave purchase (replaces majbuypt as imputed variable)
    
    ncar13 = numbers.get('NCAR13', 0)
    ncar15 = numbers.get('NCAR15', 0)
    ncar17 = numbers.get('NCAR17', 0)
    ncartot = ncar13 + ncar15 + ncar17
    tslavesd = numbers.get('TSLAVESD')
    tslavesp = numbers.get('TSLAVESP')
    pctemb = ncartot / tslavesd if tslavesd
    if pctemb == None and tslavesp:
        pctemb = ncartot / tslavesp
    
    places = [
        interim.first_place_of_slave_purchase,
        interim.second_place_of_slave_purchase,
        interim.third_place_of_slave_purchase
    ]
    mjbyptimp = places[0]
    if not mjbyptimp: mjbyptimp = places[1]
    if not mjbyptimp: mjbyptimp = places[2]
    if places[1] and places[1] == places[2]: mjbyptimp = places[1]

    if ncar13 > ncar15 and ncar13 > ncar17: mjbyptimp = places[0]
    if ncar15 > ncar13 and ncar15 > ncar17: mjbyptimp = places[1]
    if ncar17 > ncar13 and ncar17 > ncar15: mjbyptimp = places[2]
    
    if (pctemb and pctemb < 0.5) or (ncartot < 50 and tslavesd is None and tslavesp is None):
        if ncar13 == 0 and ncar15 > 0 and ncar17 > 0: mjbyptimp = places[0]
        if ncar13 > 0 and ncar15 == 0 and ncar17 > 0: mjbyptimp = places[1]
        if ncar13 > 0 and ncar15 > 0 and ncar17 == 0: mjbyptimp = places[2]
        if ncar13 == 0 and ncar15 > 0 and ncar17 == 0 and places[2] is None: mjbyptimp = places[0]
        if ncar13 > 0 and ncar15 == 0 and ncar17 == 0 and places[1] and places[2] is None: mjbyptimp = places[1]
        if ncar13 == 0 and ncar15 == 0 and ncar17 > 0 and regem1 == regem2: mjbyptimp = regem1 + 99
        if ncar13 == 0 and ncar15 > 0 and ncar17 == 0 and regem1 == regem3: mjbyptimp = regem1 + 99
        if ncar13 > 0 and ncar15 == 0 and ncar17 == 0 and regem2 == regem3: mjbyptimp = regem2 + 99
        if ncar13 == 0 and ncar15 == 0 and ncar17 > 0 and regem1 != regem2: mjbyptimp = 60999
        if ncar13 == 0 and ncar15 > 0 and ncar17 == 0 and regem1 != regem3: mjbyptimp = 60999
        if ncar13 > 0 and ncar15 == 0 and ncar17 == 0 and regem2 != regem3: mjbyptimp = 60999

    if not ncartot:
        if places[0] >=1 and places[1] >=1 and places[2] is None and regem1 == regem2: mjbyptimp = regem1 + 99
        if places[0] >=1 and places[2] >=1 and places[1] is None and regem1 == regem3: mjbyptimp = regem1 + 99
        if places[1] >=1 and places[2] >=1 and places[0] is None and regem2 == regem3: mjbyptimp = regem2 + 99
        if places[0] >=1 and places[1] >=1 and places[2] is None and regem1 != regem2: mjbyptimp = 60999
        if places[0] >=1 and places[2] >=1 and places[1] is None and regem1 != regem3: mjbyptimp = 60999
        if places[1] >=1 and places[2] >=1 and places[0] is None and regem2 != regem3: mjbyptimp = 60999
        if places[0] >=1 and places[1] >=1 and places[2] >= 1 and regem1 == regem2: mjbyptimp = regem1 + 99
        if places[0] >=1 and places[1] >=1 and places[2] >= 1 and regem1 == regem3: mjbyptimp = regem1 + 99
        if places[0] >=1 and places[1] >=1 and places[2] >= 1 and regem2 == regem3: mjbyptimp = regem2 + 99
        if places[0] >=1 and places[1] >=1 and places[2] >= 1 and regem1 != regem2 and regem1 != regem3 and regem2 != regem3: mjbyptimp = 60999
    
    no_places = place[0] is None and place[1] is None place[2] is None
    if embport and embport2 is None and no_places:
        mjbyptimp = embport
    if embport2 and no_places:
        mjbyptimp = embport2
    if not mjbyptimp and interim.imputed_outcome_of_voyage_for_slaves__value != 2 and (embport or embport2 or ncartot > 0 or not place):
        mjbyptimp = 60999
    
    interim.imputed_principal_place_of_slave_purchase = Place.objects.get(value=mjbyptimp)
    
    # mjslptimp - Principal port of slave disembarkation
    
    sla1port = interim.first_place_of_slave_purchase__value
    adpsale1 = interim.second_place_of_slave_purchase__value
    adpsale2 = interim.third_place_of_slave_purchase__value
    arrport = interim.first_port_intended_disembarkation__value
    arrport2 = interim.second_port_intended_disembarkation__value
    mjslptimp = None
    if sla1port and not adpsale1 and not adpsale2: mjslptimp = sla1port
    if adpsale1 and not sla1port and not adpsale2: mjslptimp = adpsale1
    if adpsale2 and not sla1port and not adpsale1: mjslptimp = adpsale2
    if arrport and not sla1port and not adpsale1 and not adpsale2: mjslptimp = arrport
    
    # TODO: check if we are really suppose to set the variable to
    # None if both sides are equal to None.
    if sla1port == adpsale1: mjslptimp = sla1port
    if sla1port == adpsale2: mjslptimp = sla1port
    if adpsale1 == adpsale2: mjslptimp = adpsale1
    
    slas32 = numbers.get('SLAS32', 0)
    slas36 = numbers.get('SLAS36', 0)
    slas39 = numbers.get('SLAS39', 0)
    
    if slas32 > slas36 and slas32 > slas39: mjslptimp = sla1port
    if slas36 > slas32 and slas36 > slas39: mjslptimp = adpsale1
    if slas39 > slas32 and slas39 > slas36: mjslptimp = adpsale2
    
    slaarriv = numbers.get('SLAARRIV', 0)
    slastot = slas32 + slas36 + slas39
    pctdis = slastot / slaarriv
    if pctdis < 0.5 or (slastot < 50 and not slaarriv) and sla1port and adpsale1:
        if adpsale2:
            mjslptimp = 99801
        else:
            if slas32 == 0 and slas36 >= 1: mjslptimp = sla1port
            if slas36 == 0 and slas32 >= 1: mjslptimp = adpsale1
            if slas36 >= 1 and slas32 >= 1 & regdis1 == regdis2: mjslptimp = regdis1 + 99
            if slas36 >= 1 and slas32 >= 1 & regdis1 != regdis2: mjslptimp = 99801
    
    if not slastot:
        if sla1port and adpsale1 and not adpsale2 and regdis1 == regdis2: mjslptimp = regdis1 + 99
        if sla1port and adpsale2 and not adpsale1 and regdis1 == regdis3: mjslptimp = regdis1 + 99
        if adpsale1 and adpsale2 and not sla1port and regdis2 == regdis3: mjslptimp = regdis2 + 99
        if sla1port and adpsale1 and not adpsale2 and regdis1 != regdis2: mjslptimp = 99801
        if sla1port and adpsale2 and not adpsale1 and regdis1 != regdis3: mjslptimp = 99801
        if adpsale1 and adpsale2 and not sla1port and regdis2 != regdis3: mjslptimp = 99801
        if sla1port and adpsale1 and adpsale2 and regdis1 == regdis2: mjslptimp = regdis1 + 99
        if sla1port and adpsale1 and adpsale2 and regdis1 == regdis3: mjslptimp = regdis1 + 99
        if sla1port and adpsale1 and adpsale2 and regdis2 == regdis3: mjslptimp = regdis2 + 99
        if sla1port and adpsale1 and adpsale2 and regdis1 != regdis2 and regdis1 != regdis3 and regdis2 != regdis3: mjslptimp = 99801
        
    if arrport and not sla1port and not adpsale1 and not adpsale2: mjslptimp = arrport
    
    if not mjslptimp and (fate2 == 1 or fate2 == 3 or fate2 == 5) and \
       (arrport or arrport2 or sla1port or adpsale1 or adpsale2 or slastot > 0): mjslptimp = 99801
       
    interim.imputed_principal_port_of_slave_disembarkation = Place.objects.get(value=mjslptimp)

    # ptdepimp - Imputed port where voyage began
    portdep = interim.port_of_departure__value
    ptdepimp = portdepf
    if mjslptimp >= 50200 and mjslptimp < 50300 and portdep is None: ptdepimp=50299
    if mjslptimp >= 50300 and mjslptimp < 50400 and portdep is None: ptdepimp=50399
    if mjslptimp >= 50400 and mjslptimp < 50500 and portdep is None: ptdepimp=50422

    interim.imputed_port_where_voyage_began = Place.objects.get(value=ptdepimp)
    
    def get_region(place):
        return place.region if place is not None else None
    
    interim.imputed_region_where_voyage_began = get_region(interim.imputed_port_where_voyage_began)
    
    interim.imputed_first_region_of_slave_landing = get_region(interim.first_place_of_landing)
    interim.imputed_second_region_of_slave_landing = get_region(interim.second_place_of_landing)
    interim.imputed_third_region_of_slave_landing = get_region(interim.third_place_of_landing)
    
    def clear_mod(x, mod):
        return x - (x % mod)
    broad_mod = 10000
    deptregimp1 = clear_mod(ptdepimp, broad_mod)
    majbyimp1 = clear_mod(mjbyptimp, broad_mod)
    mjselimp1 = clear_mod(mjslptimp, broad_mod)
    portret = interim.port_voyage_ended__value
    retrnreg1 = clear_mod(portret, broad_mod)    
    
    # xmimpflag - Voyage groupings for estimating imputed slaves
    xmimpflag = None
    rig = interim.rig_of_vessel__value
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or rig is None) and yearam >= 1626 and yearam < 1651: xmimpflag = 127 
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or rig is None) and yearam >= 1651 and yearam < 1676: xmimpflag = 128 
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or rig is None) and yearam >= 1676 and yearam < 1701: xmimpflag = 129 
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or rig is None) and yearam >= 1701 and yearam < 1726: xmimpflag = 130 
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or rig is None) and yearam >= 1726 and yearam < 1751: xmimpflag = 131 
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or rig is None) and yearam >= 1751 and yearam < 1776: xmimpflag = 132 
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or rig is None) and yearam >= 1776 and yearam < 1801: xmimpflag = 133 
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or rig is None) and yearam >= 1801 and yearam < 1826: xmimpflag = 134 
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or rig is None) and yearam >= 1826 and yearam < 1851: xmimpflag = 135 
    if (rig == 26 or rig == 29 or rig == 42 or rig == 43 or rig == 54 or rig == 59 or rig == 61 or rig == 65 or rig == 80 or rig == 86 or rig is None) and yearam >= 1851 and yearam < 1876: xmimpflag = 136 
    if yearam < 1700 and majbyimp == 60100: xmimpflag = 101 
    if yearam >= 1700 and yearam < 1801 and majbyimp == 60100: xmimpflag = 102 
    if yearam >=1800 and majbyimp == 60100: xmimpflag = 103 
    if yearam < 1700 and majbyimp == 60200: xmimpflag = 104 
    if yearam >= 1700 and yearam < 1801 and majbyimp == 60200: xmimpflag = 105 
    if yearam >=1800 and majbyimp == 60200: xmimpflag = 106 
    if yearam < 1700 and majbyimp == 60400: xmimpflag = 107 
    if yearam >= 1700 and yearam < 1801 and majbyimp == 60400: xmimpflag = 108 
    if yearam < 1700 and majbyimp == 60500: xmimpflag = 110 
    if yearam >= 1700 and yearam < 1801 and majbyimp == 60500: xmimpflag = 111 
    if yearam >=1800 and majbyimp == 60500: xmimpflag = 112 
    if yearam < 1700 and majbyimp == 60600: xmimpflag = 113 
    if yearam >= 1700 and yearam < 1801 and majbyimp == 60600: xmimpflag = 114 
    if yearam >=1800 and majbyimp == 60600: xmimpflag = 115 
    if yearam < 1700 and majbyimp == 60700: xmimpflag = 116 
    if yearam >= 1700 and yearam < 1801 and majbyimp == 60700: xmimpflag = 117 
    if yearam >=1800 and majbyimp == 60700: xmimpflag = 118 
    if yearam >= 1700 and yearam < 1801 and majbyimp == 60300: xmimpflag = 120 
    if yearam >=1800 and majbyimp == 60300: xmimpflag = 121 
    if yearam < 1700 and majbyimp == 60800: xmimpflag = 122 
    if yearam >= 1700 and yearam < 1801 and majbyimp == 60800: xmimpflag = 123 
    if yearam >=1800 and majbyimp == 60800: xmimpflag = 124 
    if yearam < 1627: xmimpflag = 1 
    if (yearam >= 1626 and yearam < 1642) and ((mjselimp >= 31100 and mjselimp < 32000) or mjselimp1 == 40000 or mjselimp == 80400): xmimpflag = 2 
    if yearam < 1716 and mjselimp >= 36100 and mjselimp < 37000: xmimpflag = 3 
    if yearam < 1701 and mjselimp == 50300: xmimpflag = 4 
    if yearam >= 1700 and yearam < 1800 and mjselimp == 50300: xmimpflag = 5 
    if yearam > 1799 and mjselimp == 50300: xmimpflag = 6 
    if yearam < 1650 and natinimp == 8: xmimpflag = 7 
    if yearam >= 1650 and yearam < 1674 and natinimp == 8: xmimpflag = 8 
    if yearam >= 1674 and yearam < 1731 and natinimp == 8: xmimpflag = 9 
    if yearam > 1730 and natinimp == 8: xmimpflag = 10 
    if yearam < 1751 and mjselimp == 50200: xmimpflag = 11 
    if yearam >= 1751 and yearam < 1776 and mjselimp == 50200: xmimpflag = 12 
    if yearam >= 1776 and yearam < 1801 and mjselimp == 50200: xmimpflag = 13 
    if yearam >= 1801 and yearam < 1826 and mjselimp == 50200: xmimpflag = 14 
    if yearam > 1825 and mjselimp == 50200: xmimpflag = 15 
    if yearam >= 1642 and yearam < 1663 and ((mjselimp >= 31100 and mjselimp < 32000) or mjselimp1 == 40000 or mjselimp == 80400): xmimpflag = 16 
    if yearam >= 1794 and yearam < 1807 and natinimp == 15: xmimpflag = 157 
    if yearam < 1794 and natinimp == 15: xmimpflag = 159 
    if yearam < 1851 and natinimp == 9: xmimpflag = 99 
    if yearam >= 1851 and yearam < 1876 and natinimp =9: xmimpflag = 100 
    if yearam < 1751 and rig == 1: xmimpflag = 17 
    if yearam >= 1751 and yearam < 1776 and rig == 1: xmimpflag = 98 
    if yearam >= 1776 and yearam < 1801 and rig == 1: xmimpflag = 18 
    if yearam >= 1801 and yearam < 1826 and rig == 1: xmimpflag = 19 
    if yearam >= 1826 and yearam < 1851 and rig == 1: xmimpflag = 20 
    if yearam >= 1851 and yearam < 1876 and rig == 1: xmimpflag = 21 
    if yearam < 1776 and rig == 2: xmimpflag = 22 
    if yearam >= 1776 and yearam < 1801 and rig == 2: xmimpflag = 23 
    if yearam >= 1801 and yearam < 1826 and rig == 2: xmimpflag = 24 
    if yearam >= 1826 and yearam < 1851 and rig == 2: xmimpflag = 25 
    if yearam >= 1851 and yearam < 1876 and rig == 2: xmimpflag = 26 
    if yearam < 1751 and rig == 3: xmimpflag = 27 
    if yearam >= 1751 and yearam < 1776 and rig == 3: xmimpflag = 28 
    if yearam >= 1776 and yearam < 1801 and rig == 3: xmimpflag = 29 
    if yearam >= 1801 and yearam < 1876 and rig == 3: xmimpflag = 30 
    if yearam < 1726 and rig == 4: xmimpflag = 31 
    if yearam >= 1726 and yearam < 1751 and rig == 4: xmimpflag = 32 
    if yearam >= 1751 and yearam < 1776 and rig == 4: xmimpflag = 33 
    if yearam >= 1776 and yearam < 1801 and rig == 4: xmimpflag = 34 
    if yearam >= 1801 and yearam < 1826 and rig == 4: xmimpflag = 35 
    if yearam >= 1826 and yearam < 1851 and rig == 4: xmimpflag = 36 
    if yearam >= 1851 and yearam < 1876 and rig == 4: xmimpflag = 37 
    if rig == 5: xmimpflag = 38 
    if rig == 6: xmimpflag = 39 
    if rig == 7: xmimpflag = 40 
    if yearam < 1776 and rig == 8: xmimpflag = 41 
    if yearam >= 1776 and yearam < 1801 and rig == 8: xmimpflag = 42 
    if yearam >= 1801 and yearam < 1826 and rig == 8: xmimpflag = 43 
    if yearam >= 1826 and yearam < 1851 and rig == 8: xmimpflag = 44 
    if yearam >= 1851 and yearam < 1876 and rig == 8: xmimpflag = 45 
    if yearam < 1826 and (rig == 9 or rig == 31): xmimpflag = 46 
    if yearam >= 1826 and yearam < 1851 and (rig == 9 or rig == 31): xmimpflag = 47 
    if yearam >= 1851 and yearam < 1876 and (rig == 9 or rig == 31): xmimpflag = 48 
    if rig == 10 or rig == 24: xmimpflag = 49 
    if rig == 11 or rig == 12: xmimpflag = 50 
    if yearam < 1751 and rig == 13: xmimpflag = 51 
    if yearam >= 1751 and yearam < 1776 and rig == 13: xmimpflag = 52 
    if yearam >= 1776 and yearam < 1801 and rig == 13: xmimpflag = 53 
    if yearam >= 1801 and yearam < 1826 and rig == 13: xmimpflag = 54 
    if yearam >= 1826 and yearam < 1877 and rig == 13: xmimpflag = 55 
    if rig == 15: xmimpflag = 56 
    if rig == 20: xmimpflag = 57 
    if rig == 21: xmimpflag = 58 
    if rig == 23: xmimpflag = 59 
    if yearam < 1751 and rig == 25: xmimpflag = 60 
    if yearam >= 1751 and yearam < 1776 and rig == 25: xmimpflag = 61 
    if yearam >= 1776 and yearam < 1801 and rig == 25: xmimpflag = 62 
    if yearam >= 1801 and yearam < 1826 and rig == 25: xmimpflag = 63 
    if yearam >= 1826 and yearam < 1851 and rig == 25: xmimpflag = 160 
    if yearam >= 1851 and yearam < 1877 and rig == 25: xmimpflag = 64 
    if yearam < 1751 and rig == 27: xmimpflag = 65 
    if yearam >= 1751 and yearam < 1776 and rig == 27: xmimpflag = 66 
    if yearam >= 1776 and yearam < 1801 and rig == 27: xmimpflag = 67 
    if yearam >= 1801 and yearam < 1877 and rig == 27: xmimpflag = 68 
    if rig == 28: xmimpflag = 69 
    if yearam < 1726 and (rig == 30 or rig == 45 or rig == 63): xmimpflag = 70 
    if yearam >= 1726 and yearam < 1776 and (rig == 30 or rig == 45 or rig == 63): xmimpflag = 71 
    if yearam >= 1776 and yearam < 1801 and (rig == 30 or rig == 45 or rig == 63): xmimpflag = 97 
    if yearam >= 1801 and yearam < 1826 and (rig == 30 or rig == 45 or rig == 63): xmimpflag = 72 
    if yearam >= 1826 and yearam < 1876 and (rig == 30 or rig == 45 or rig == 63): xmimpflag = 85 
    if rig == 32 or rig == 39: xmimpflag = 73 
    if yearam < 1726 and rig == 35: xmimpflag = 74 
    if yearam >= 1726 and yearam < 1751 and rig == 35: xmimpflag = 75 
    if yearam >= 1751 and yearam < 1776 and rig == 35: xmimpflag = 76 
    if yearam >= 1776 and yearam < 1801 and rig == 35: xmimpflag = 77 
    if yearam >= 1801 and yearam < 1877 and rig == 35: xmimpflag = 78 
    if yearam < 1776 and rig == 40: xmimpflag = 79 
    if yearam >= 1776 and yearam < 1801 and rig == 40: xmimpflag = 80 
    if yearam >= 1801 and yearam < 1826 and rig == 40: xmimpflag = 81 
    if yearam >= 1826 and yearam < 1876 and rig == 40: xmimpflag = 82 
    if rig == 41 or rig == 57: xmimpflag = 83 
    if rig == 44: xmimpflag = 84 
    if rig == 47: xmimpflag = 86 
    if rig == 48: xmimpflag = 87 
    if yearam < 1826 and (rig == 14 or rig == 36 or rig == 49): xmimpflag = 88 
    if yearam >= 1826 and yearam < 1876 and (rig == 14 or rig == 36 or rig == 49): xmimpflag = 89 
    if yearam < 1826 and (rig == 16 or rig == 51): xmimpflag = 90 
    if yearam >= 1826 and yearam < 1851 and (rig == 16 or rig == 51): xmimpflag = 91 
    if yearam >= 1851 and yearam < 1876 and (rig == 16 or rig == 51): xmimpflag = 92 
    if rig == 17 or rig == 19 or rig == 52 or rig == 53: xmimpflag = 93 
    if yearam < 1726 and rig == 60: xmimpflag = 94 
    if yearam >= 1726 and yearam < 1826 and rig == 60: xmimpflag = 95 
    if yearam >= 1826 and yearam < 1876 and rig == 60: xmimpflag = 96 
    if yearam < 1776 and rig == 1 and natinimp == 9: xmimpflag = 137 
    if yearam >= 1776 and yearam < 1801 and rig == 1 and natinimp == 9: xmimpflag = 138 
    if yearam >= 1801 and yearam < 1826 and rig == 1 and natinimp == 9: xmimpflag = 139 
    if yearam > 1825 and rig == 1 and natinimp == 9: xmimpflag = 140 
    if yearam < 1776 and (rig == 2 or rig == 5) and natinimp == 9: xmimpflag = 141 
    if yearam >= 1776 and yearam < 1801 and (rig == 2 or rig == 5) and natinimp == 9: xmimpflag = 142 
    if yearam >= 1801 and yearam < 1826 and rig == 5 and natinimp == 9: xmimpflag = 143 
    if yearam > 1825 and (rig == 2 or rig == 5) and natinimp == 9: xmimpflag = 145 
    if yearam < 1776 and rig == 4 and natinimp == 9: xmimpflag = 146 
    if yearam >= 1776 and yearam < 1801 and rig == 4 and natinimp == 9: xmimpflag = 147 
    if yearam >= 1801 and yearam < 1826 and rig == 4 and natinimp == 9: xmimpflag = 148 
    if yearam > 1825 and rig == 4 and natinimp == 9: xmimpflag = 149 
    if yearam < 1776 and rig == 8 and natinimp == 9: xmimpflag = 150 
    if yearam >= 1776 and yearam < 1826 and rig == 8 and natinimp == 9: xmimpflag = 151 
    if yearam > 1825 and rig == 8 and natinimp == 9: xmimpflag = 152 
    if yearam >= 1826 and yearam < 1876 and rig == 9 and natinimp == 9: xmimpflag = 154 
    if rig == 27 and natinimp == 9: xmimpflag = 155 
    if rig == 35 and natinimp == 9: xmimpflag = 156
    interim.imputed_voyage_groupings_for_estimating_imputed_slaves = VoyageGroupings.objects.get(value=xmimpflag)
    
    
    # slaximp - Imputed number of slaves embarked
    # slamimp - Imputed number of slaves disembarked
    if tslavesd >= 1: slaximp = tslavesd
    if tslavesd is None and tslavesp >= 1: slaximp = tslavesp
    if tslavesd is None and tslavesp is None and ncartot > slaarriv: slaximp=ncartot
    if tslavesd is None and tslavesp is None and slaarriv is None and ncartot > slastot: slaximp = ncartot
    if tslavesd is None and tslavesp is None and slaarriv is None and slastot is None and ncartot >= 50: slaximp = ncartot
    if slaarriv >= 1: slamimp = slaarriv
    if slaarriv is None and slastot <= tslavesd: slamimp=slastot
    if slaarriv is None and tslavesd is None and slastot <= tslavesp: slamimp = slastot
    if slaarriv is None and tslavesd is None and tslavesp is None and slastot <= ncartot: slamimp = slastot
    if slaarriv is None and tslavesd is None and tslavesd is None and ncartot is None and slastot >= 50: slamimp=slastot
    # LOT OF CODE
    interim.imputed_total_slaves_embarked = slaximp
    interim.imputed_total_slaves_disembarked = slamimp