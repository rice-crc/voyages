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
    if slaarriv is None and tslavesd is None and tslavesd is None and ncartot is None and slastot >= 50: slamimp = slastot
    
    if xmimpflag == 127 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.165107561642471)
    if xmimpflag == 127 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.165107561642471)
    if xmimpflag == 127 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 163.181286549708
    if xmimpflag == 127 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 163.181286549708 / (1 - 0.165107561642471 )
    if xmimpflag == 128 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.230972326367458)
    if xmimpflag == 128 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.230972326367458)
    if xmimpflag == 128 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 241.774647887324
    if xmimpflag == 128 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 241.774647887324 / (1 - 0.230972326367458 )
    if xmimpflag == 129 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.218216262481124)
    if xmimpflag == 129 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.218216262481124)
    if xmimpflag == 129 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 249.141527001862
    if xmimpflag == 129 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 249.141527001862 / (1 - 0.218216262481124 )
    if xmimpflag == 130 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.164154067860228)
    if xmimpflag == 130 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.164154067860228)
    if xmimpflag == 130 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 227.680034129693
    if xmimpflag == 130 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 227.680034129693 / (1 - 0.164154067860228 )
    if xmimpflag == 131 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.153670852602567)
    if xmimpflag == 131 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.153670852602567)
    if xmimpflag == 131 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 272.60549132948
    if xmimpflag == 131 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 272.60549132948 / (1 - 0.153670852602567 )
    if xmimpflag == 132 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.120410468186061)
    if xmimpflag == 132 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.120410468186061)
    if xmimpflag == 132 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 268.071314102564
    if xmimpflag == 132 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 268.071314102564 / (1 - 0.120410468186061 )
    if xmimpflag == 133 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.126821090786133)
    if xmimpflag == 133 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.126821090786133)
    if xmimpflag == 133 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 290.826654240447
    if xmimpflag == 133 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 290.826654240447 / (1 - 0.126821090786133 )
    if xmimpflag == 134 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.105799354866935)
    if xmimpflag == 134 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.105799354866935)
    if xmimpflag == 134 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 225.932515337423
    if xmimpflag == 134 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 225.932515337423 / (1 - 0.105799354866935 )
    if xmimpflag == 135 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.114160782328086)
    if xmimpflag == 135 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.114160782328086)
    if xmimpflag == 135 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 391.452674897119
    if xmimpflag == 135 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 391.452674897119 / (1 - 0.114160782328086 )
    if xmimpflag == 136 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.170755559662484)
    if xmimpflag == 136 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.170755559662484)
    if xmimpflag == 136 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 480.734042553191
    if xmimpflag == 136 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 480.734042553191 / (1 - 0.170755559662484 )
    if xmimpflag == 101 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.142415261804064)
    if xmimpflag == 101 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.142415261804064)
    if xmimpflag == 101 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 163.80243902439
    if xmimpflag == 101 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 163.80243902439 / (1 - 0.142415261804064 )
    if xmimpflag == 102 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.104951847967976)
    if xmimpflag == 102 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.104951847967976)
    if xmimpflag == 102 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 153.265497076023
    if xmimpflag == 102 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 153.265497076023 / (1 - 0.104951847967976 )
    if xmimpflag == 103 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0794334443169517)
    if xmimpflag == 103 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0794334443169517)
    if xmimpflag == 103 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 138.094017094017
    if xmimpflag == 103 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 138.094017094017 / (1 - 0.0794334443169517 )
    if xmimpflag == 104 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.125269157905197)
    if xmimpflag == 104 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.125269157905197)
    if xmimpflag == 104 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 107.64
    if xmimpflag == 104 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 107.64 - (107.64 * 0.125269157905197 )
    if xmimpflag == 105 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0887057111704602)
    if xmimpflag == 105 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0887057111704602)
    if xmimpflag == 105 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 191.988789237668
    if xmimpflag == 105 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 191.988789237668 / (1 - 0.0887057111704602 )
    if xmimpflag == 106 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0985396051230542)
    if xmimpflag == 106 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0985396051230542)
    if xmimpflag == 106 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 188.140969162996
    if xmimpflag == 106 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 188.140969162996 / (1 - 0.0985396051230542 )
    if xmimpflag == 107 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.199714956235816)
    if xmimpflag == 107 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.199714956235816)
    if xmimpflag == 107 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 239.363636363636
    if xmimpflag == 107 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 239.363636363636 / (1 - 0.199714956235816 )
    if xmimpflag == 108 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.116764553914052)
    if xmimpflag == 108 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.116764553914052)
    if xmimpflag == 108 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 241.066480055983
    if xmimpflag == 108 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 241.066480055983 / (1 - 0.116764553914052 )
    if xmimpflag == 110 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.217817105373686)
    if xmimpflag == 110 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.217817105373686)
    if xmimpflag == 110 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 321.139784946236
    if xmimpflag == 110 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 321.139784946236 / (1 - 0.217817105373686 )
    if xmimpflag == 111 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.134584278813695)
    if xmimpflag == 111 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.134584278813695)
    if xmimpflag == 111 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 320.396527777777
    if xmimpflag == 111 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 320.396527777777 / (1 - 0.134584278813695 )
    if xmimpflag == 112 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0649564900465187)
    if xmimpflag == 112 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0649564900465187)
    if xmimpflag == 112 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 302.919243986254
    if xmimpflag == 112 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 302.919243986254 / (1 - 0.0649564900465187 )
    if xmimpflag == 113 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.294943293777566)
    if xmimpflag == 113 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.294943293777566)
    if xmimpflag == 113 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 178.191780821918
    if xmimpflag == 113 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 178.191780821918 / (1 - 0.294943293777566 )
    if xmimpflag == 114 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.190466263797331)
    if xmimpflag == 114 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.190466263797331)
    if xmimpflag == 114 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 268.709993468321
    if xmimpflag == 114 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 268.709993468321 / (1 - 0.190466263797331 )
    if xmimpflag == 115 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.165262209695588)
    if xmimpflag == 115 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.165262209695588)
    if xmimpflag == 115 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 265.480215827338
    if xmimpflag == 115 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 265.480215827338 / (1 - 0.165262209695588 )
    if xmimpflag == 116 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.250590294065011)
    if xmimpflag == 116 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.250590294065011)
    if xmimpflag == 116 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 216.026607538803
    if xmimpflag == 116 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 216.026607538803 / (1 - 0.250590294065011 )
    if xmimpflag == 117 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0862116624182079)
    if xmimpflag == 117 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0862116624182079)
    if xmimpflag == 117 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 341.979498861048
    if xmimpflag == 117 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 341.979498861048 / (1 - 0.0862116624182079 )
    if xmimpflag == 118 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0795782666543268)
    if xmimpflag == 118 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0795782666543268)
    if xmimpflag == 118 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 382.444580777097
    if xmimpflag == 118 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 382.444580777097 / (1 - 0.0795782666543268 )
    if xmimpflag == 120 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.100542298212489)
    if xmimpflag == 120 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.100542298212489)
    if xmimpflag == 120 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 191.62583518931
    if xmimpflag == 120 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 191.62583518931 / (1 - 0.100542298212489 )
    if xmimpflag == 121 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0690791392436498)
    if xmimpflag == 121 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0690791392436498)
    if xmimpflag == 121 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 162.041666666667
    if xmimpflag == 121 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 162.041666666667 / (1 - 0.0690791392436498 )
    if xmimpflag == 122 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.274602006426542)
    if xmimpflag == 122 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.274602006426542)
    if xmimpflag == 122 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 173.454545454545
    if xmimpflag == 122 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 173.454545454545 / (1 - 0.274602006426542 )
    if xmimpflag == 123 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.274602006426542)
    if xmimpflag == 123 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.274602006426542)
    if xmimpflag == 123 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 255.028571428571
    if xmimpflag == 123 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 255.028571428571 / (1 - 0.274602006426542 )
    if xmimpflag == 124 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.181330570603409)
    if xmimpflag == 124 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.181330570603409)
    if xmimpflag == 124 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 447.532008830022
    if xmimpflag == 124 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 447.532008830022 / (1 - 0.181330570603409 )
    if xmimpflag == 1 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.255634697158707)
    if xmimpflag == 1 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.255634697158707)
    if xmimpflag == 1 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 166.401374570447
    if xmimpflag == 1 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 166.401374570447 / (1 - 0.255634697158707 )
    if xmimpflag == 2 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.173114449095158)
    if xmimpflag == 2 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.173114449095158)
    if xmimpflag == 2 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 152.863945578231
    if xmimpflag == 2 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 152.863945578231 / (1 - 0.173114449095158 )
    if xmimpflag == 3 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.191426939591589)
    if xmimpflag == 3 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.191426939591589)
    if xmimpflag == 3 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 250.179245283019
    if xmimpflag == 3 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 250.179245283019 / (1 - 0.191426939591589 )
    if xmimpflag == 4 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.143739162059858)
    if xmimpflag == 4 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.143739162059858)
    if xmimpflag == 4 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 273.896226415094
    if xmimpflag == 4 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 273.896226415094 - (273.896226415094 * 0.143739162059858 )
    if xmimpflag == 5 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0703329947332674)
    if xmimpflag == 5 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0703329947332674)
    if xmimpflag == 5 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 380.04854368932
    if xmimpflag == 5 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 380.04854368932 - (380.04854368932 * 0.0703329947332674 )
    if xmimpflag == 6 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.117444418143106)
    if xmimpflag == 6 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.117444418143106)
    if xmimpflag == 6 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 305.868020304568
    if xmimpflag == 6 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 305.868020304568 / (1 - 0.117444418143106 )
    if xmimpflag == 7 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.126779394689057)
    if xmimpflag == 7 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.126779394689057)
    if xmimpflag == 7 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 265.88
    if xmimpflag == 7 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 265.88 - (265.88 * 0.126779394689057 )
    if xmimpflag == 8 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.189011301766662)
    if xmimpflag == 8 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.189011301766662)
    if xmimpflag == 8 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 281.325
    if xmimpflag == 8 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 281.325 / (1 - 0.189011301766662 )
    if xmimpflag == 9 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.140365224720275)
    if xmimpflag == 9 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.140365224720275)
    if xmimpflag == 9 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 402.502202643172
    if xmimpflag == 9 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 402.502202643172 / (1 - 0.140365224720275 )
    if xmimpflag == 10 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.107188743129005)
    if xmimpflag == 10 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.107188743129005)
    if xmimpflag == 10 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 277.059842519684
    if xmimpflag == 10 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 277.059842519684 / (1 - 0.107188743129005 )
    if xmimpflag == 11 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.126901348540731)
    if xmimpflag == 11 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.126901348540731)
    if xmimpflag == 11 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 355.810945273632
    if xmimpflag == 11 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 355.810945273632 / (1 - 0.126901348540731 )
    if xmimpflag == 12 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0655772248600899)
    if xmimpflag == 12 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0655772248600899)
    if xmimpflag == 12 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 309.533898305085
    if xmimpflag == 12 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 309.533898305085 / (1 - 0.0655772248600899 )
    if xmimpflag == 13 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0778021073375869)
    if xmimpflag == 13 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0778021073375869)
    if xmimpflag == 13 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 305.812154696132
    if xmimpflag == 13 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 305.812154696132 / (1 - 0.0778021073375869 )
    if xmimpflag == 14 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0654921908875572)
    if xmimpflag == 14 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0654921908875572)
    if xmimpflag == 14 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 285.054112554113
    if xmimpflag == 14 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 285.054112554113 / (1 - 0.0654921908875572 )
    if xmimpflag == 15 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0671696102131247)
    if xmimpflag == 15 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0671696102131247)
    if xmimpflag == 15 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 361.638059701493
    if xmimpflag == 15 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 361.638059701493 / (1 - 0.0671696102131247 )
    if xmimpflag == 16 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.371414750110571)
    if xmimpflag == 16 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.371414750110571)
    if xmimpflag == 16 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 239.9
    if xmimpflag == 16 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 239.9 / (1 - 0.371414750110571 )
    if xmimpflag == 157 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.230610260687796)
    if xmimpflag == 157 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.230610260687796)
    if xmimpflag == 157 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 139.029411764706
    if xmimpflag == 157 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 139.029411764706 / (1 - 0.230610260687796 )
    if xmimpflag == 159 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.154487726688789)
    if xmimpflag == 159 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.154487726688789)
    if xmimpflag == 159 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 245.12676056338
    if xmimpflag == 159 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 245.12676056338 / (1 - 0.154487726688789 )
    if xmimpflag == 99 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.166050441674744)
    if xmimpflag == 99 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.166050441674744)
    if xmimpflag == 99 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 125.619750283768
    if xmimpflag == 99 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 125.619750283768 / (1 - 0.166050441674744 )
    if xmimpflag == 100 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.178717812379779)
    if xmimpflag == 100 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.178717812379779)
    if xmimpflag == 100 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 565.645161290322
    if xmimpflag == 100 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 565.645161290322 / (1 - 0.178717812379779 )
    if xmimpflag == 17 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0557746478873239)
    if xmimpflag == 17 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0557746478873239)
    if xmimpflag == 17 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 148.882352941176
    if xmimpflag == 17 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 148.882352941176 / (1 - 0.0557746478873239 )
    if xmimpflag == 98 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.126563817175912)
    if xmimpflag == 98 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.126563817175912)
    if xmimpflag == 98 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 132.596685082873
    if xmimpflag == 98 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 132.596685082873 / (1 - 0.126563817175912 )
    if xmimpflag == 18 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.093544030879478)
    if xmimpflag == 18 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.093544030879478)
    if xmimpflag == 18 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 184.486013986014
    if xmimpflag == 18 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 184.486013986014 / (1 - 0.093544030879478 )
    if xmimpflag == 19 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0985982521761244)
    if xmimpflag == 19 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0985982521761244)
    if xmimpflag == 19 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 230.298469387755
    if xmimpflag == 19 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 230.298469387755 / (1 - 0.0985982521761244 )
    if xmimpflag == 20 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0944678720322908)
    if xmimpflag == 20 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0944678720322908)
    if xmimpflag == 20 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 444.290145985401
    if xmimpflag == 20 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 444.290145985401 / (1 - 0.0944678720322908 )
    if xmimpflag == 21 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.167379623404603)
    if xmimpflag == 21 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.167379623404603)
    if xmimpflag == 21 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 492.946428571429
    if xmimpflag == 21 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 492.946428571429 / (1 - 0.167379623404603 )
    if xmimpflag == 22 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.183801786070534)
    if xmimpflag == 22 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.183801786070534)
    if xmimpflag == 22 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 91.9594594594595
    if xmimpflag == 22 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 91.9594594594595 / (1 - 0.183801786070534 )
    if xmimpflag == 23 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.102358180948044)
    if xmimpflag == 23 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.102358180948044)
    if xmimpflag == 23 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 95.972972972973
    if xmimpflag == 23 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 95.972972972973 / (1 - 0.102358180948044 )
    if xmimpflag == 24 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.122708750828674)
    if xmimpflag == 24 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.122708750828674)
    if xmimpflag == 24 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 146.31
    if xmimpflag == 24 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 146.31 / (1 - 0.122708750828674 )
    if xmimpflag == 25 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.101742168136026)
    if xmimpflag == 25 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.101742168136026)
    if xmimpflag == 25 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 279.357142857143
    if xmimpflag == 25 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 279.357142857143 / (1 - 0.101742168136026 )
    if xmimpflag == 26 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0830808603000646)
    if xmimpflag == 26 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0830808603000646)
    if xmimpflag == 26 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 341.5
    if xmimpflag == 26 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 341.5 / (1 - 0.0830808603000646 )
    if xmimpflag == 27 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0951735364832193)
    if xmimpflag == 27 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0951735364832193)
    if xmimpflag == 27 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 335.546666666667
    if xmimpflag == 27 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 335.546666666667 - (335.546666666667 * 0.0951735364832193 )
    if xmimpflag == 28 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0599984615282753)
    if xmimpflag == 28 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0599984615282753)
    if xmimpflag == 28 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 348.926267281106
    if xmimpflag == 28 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 348.926267281106 - (348.926267281106 * 0.0599984615282753 )
    if xmimpflag == 29 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0849037398486349)
    if xmimpflag == 29 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0849037398486349)
    if xmimpflag == 29 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 323.539358600583
    if xmimpflag == 29 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 323.539358600583 / (1 - 0.0849037398486349 )
    if xmimpflag == 30 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0831292966753462)
    if xmimpflag == 30 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0831292966753462)
    if xmimpflag == 30 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 435.738461538461
    if xmimpflag == 30 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 435.738461538461 / (1 - 0.0831292966753462 )
    if xmimpflag == 31 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.154603810637904)
    if xmimpflag == 31 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.154603810637904)
    if xmimpflag == 31 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 221.279220779221
    if xmimpflag == 31 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 221.279220779221 / (1 - 0.154603810637904 )
    if xmimpflag == 32 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.169381440464976)
    if xmimpflag == 32 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.169381440464976)
    if xmimpflag == 32 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 296.593103448276
    if xmimpflag == 32 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 296.593103448276 / (1 - 0.169381440464976 )
    if xmimpflag == 33 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.183684529291394)
    if xmimpflag == 33 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.183684529291394)
    if xmimpflag == 33 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 281.452966714906
    if xmimpflag == 33 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 281.452966714906 / (1 - 0.183684529291394 )
    if xmimpflag == 34 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0864964921326426)
    if xmimpflag == 34 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0864964921326426)
    if xmimpflag == 34 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 325.652360515021
    if xmimpflag == 34 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 325.652360515021 / (1 - 0.0864964921326426 )
    if xmimpflag == 35 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.176037224384829)
    if xmimpflag == 35 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.176037224384829)
    if xmimpflag == 35 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 272.474358974359
    if xmimpflag == 35 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 272.474358974359 / (1 - 0.176037224384829 )
    if xmimpflag == 36 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.116937605450612)
    if xmimpflag == 36 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.116937605450612)
    if xmimpflag == 36 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 556.677419354839
    if xmimpflag == 36 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 556.677419354839 / (1 - 0.116937605450612 )
    if xmimpflag == 37 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.172812495199871)
    if xmimpflag == 37 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.172812495199871)
    if xmimpflag == 37 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 890.470588235294
    if xmimpflag == 37 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 890.470588235294 / (1 - 0.172812495199871 )
    if xmimpflag == 38 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.105087524949968)
    if xmimpflag == 38 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.105087524949968)
    if xmimpflag == 38 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 335.813953488372
    if xmimpflag == 38 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 335.813953488372 / (1 - 0.105087524949968 )
    if xmimpflag == 39 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0856667000685018)
    if xmimpflag == 39 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0856667000685018)
    if xmimpflag == 39 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 257.263157894737
    if xmimpflag == 39 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 257.263157894737 / (1 - 0.0856667000685018 )
    if xmimpflag == 40 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0865650987499053)
    if xmimpflag == 40 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0865650987499053)
    if xmimpflag == 40 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 328.195266272189
    if xmimpflag == 40 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 328.195266272189 / (1 - 0.0865650987499053 )
    if xmimpflag == 41 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.171814252005436)
    if xmimpflag == 41 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.171814252005436)
    if xmimpflag == 41 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 129.145454545455
    if xmimpflag == 41 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 129.145454545455 / (1 - 0.171814252005436 )
    if xmimpflag == 42 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0610387045813586)
    if xmimpflag == 42 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0610387045813586)
    if xmimpflag == 42 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 158.1
    if xmimpflag == 42 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 158.1 / (1 - 0.0610387045813586 )
    if xmimpflag == 43 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.159823459162871)
    if xmimpflag == 43 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.159823459162871)
    if xmimpflag == 43 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 247.759689922481
    if xmimpflag == 43 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 247.759689922481 / (1 - 0.159823459162871 )
    if xmimpflag == 44 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0988853555387519)
    if xmimpflag == 44 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0988853555387519)
    if xmimpflag == 44 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 363
    if xmimpflag == 44 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 363 / (1 - 0.0988853555387519 )
    if xmimpflag == 45 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0904513085721602)
    if xmimpflag == 45 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0904513085721602)
    if xmimpflag == 45 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 466.25641025641
    if xmimpflag == 45 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 466.25641025641 / (1 - 0.0904513085721602 )
    if xmimpflag == 46 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.082310278477633)
    if xmimpflag == 46 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.082310278477633)
    if xmimpflag == 46 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 159.810810810811
    if xmimpflag == 46 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 159.810810810811 / (1 - 0.082310278477633 )
    if xmimpflag == 47 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.104714300552102)
    if xmimpflag == 47 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.104714300552102)
    if xmimpflag == 47 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 638.25
    if xmimpflag == 47 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 638.25 / (1 - 0.104714300552102 )
    if xmimpflag == 48 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.193439630544956)
    if xmimpflag == 48 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.193439630544956)
    if xmimpflag == 48 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 608.392156862745
    if xmimpflag == 48 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 608.392156862745 / (1 - 0.193439630544956 )
    if xmimpflag == 49 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.145583038352611)
    if xmimpflag == 49 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.145583038352611)
    if xmimpflag == 49 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 428.888888888889
    if xmimpflag == 49 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 428.888888888889 / (1 - 0.145583038352611 )
    if xmimpflag == 50 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.233333333333333)
    if xmimpflag == 50 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.233333333333333)
    if xmimpflag == 50 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 270.846153846154
    if xmimpflag == 50 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 270.846153846154 / (1 - 0.233333333333333 )
    if xmimpflag == 51 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.179223522528989)
    if xmimpflag == 51 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.179223522528989)
    if xmimpflag == 51 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 229.64
    if xmimpflag == 51 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 229.64 / (1 - 0.179223522528989 )
    if xmimpflag == 52 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0819156347249732)
    if xmimpflag == 52 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0819156347249732)
    if xmimpflag == 52 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 290.164383561644
    if xmimpflag == 52 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 290.164383561644 - (290.164383561644 * 0.0819156347249732 )
    if xmimpflag == 53 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0540922242825536)
    if xmimpflag == 53 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0540922242825536)
    if xmimpflag == 53 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 256.548387096774
    if xmimpflag == 53 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 256.548387096774 / (1 - 0.0540922242825536 )
    if xmimpflag == 54 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0913651933726713)
    if xmimpflag == 54 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0913651933726713)
    if xmimpflag == 54 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 216.907894736842
    if xmimpflag == 54 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 216.907894736842 / (1 - 0.0913651933726713 )
    if xmimpflag == 55 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0604022380426763)
    if xmimpflag == 55 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0604022380426763)
    if xmimpflag == 55 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 241.461538461538
    if xmimpflag == 55 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 241.461538461538 / (1 - 0.0604022380426763 )
    if xmimpflag == 56 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0542026549646127)
    if xmimpflag == 56 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0542026549646127)
    if xmimpflag == 56 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 340.230769230769
    if xmimpflag == 56 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 340.230769230769 / (1 - 0.0542026549646127 )
    if xmimpflag == 57 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0974564330758702)
    if xmimpflag == 57 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0974564330758702)
    if xmimpflag == 57 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 516.45
    if xmimpflag == 57 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 516.45 / (1 - 0.0974564330758702 )
    if xmimpflag == 58 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.162886379968412)
    if xmimpflag == 58 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.162886379968412)
    if xmimpflag == 58 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 447.518072289157
    if xmimpflag == 58 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 447.518072289157 - (447.518072289157 * 0.162886379968412 )
    if xmimpflag == 59 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0561646667118922)
    if xmimpflag == 59 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0561646667118922)
    if xmimpflag == 59 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 152.923076923077
    if xmimpflag == 59 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 152.923076923077 / (1 - 0.0561646667118922 )
    if xmimpflag == 60 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.133468501803896)
    if xmimpflag == 60 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.133468501803896)
    if xmimpflag == 60 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 403.292993630573
    if xmimpflag == 60 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 403.292993630573 / (1 - 0.133468501803896 )
    if xmimpflag == 61 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.106708705390018)
    if xmimpflag == 61 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.106708705390018)
    if xmimpflag == 61 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 285.644444444444
    if xmimpflag == 61 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 285.644444444444 / (1 - 0.106708705390018 )
    if xmimpflag == 62 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0785278768682708)
    if xmimpflag == 62 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0785278768682708)
    if xmimpflag == 62 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 335.658227848101
    if xmimpflag == 62 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 335.658227848101 / (1 - 0.0785278768682708 )
    if xmimpflag == 63 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.107782269167156)
    if xmimpflag == 63 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.107782269167156)
    if xmimpflag == 63 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 472.267857142857
    if xmimpflag == 63 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 472.267857142857 / (1 - 0.107782269167156 )
    if xmimpflag == 160 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0779281672325541)
    if xmimpflag == 160 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0779281672325541)
    if xmimpflag == 160 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 536.842857142857
    if xmimpflag == 160 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 536.842857142857 / (1 - 0.0779281672325541 )
    if xmimpflag == 65 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.115409873680179)
    if xmimpflag == 65 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.115409873680179)
    if xmimpflag == 65 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 103.376146788991
    if xmimpflag == 65 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 103.376146788991 / (1 - 0.115409873680179 )
    if xmimpflag == 66 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.207088877726936)
    if xmimpflag == 66 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.207088877726936)
    if xmimpflag == 66 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 68.1506849315068
    if xmimpflag == 66 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 68.1506849315068 / (1 - 0.207088877726936 )
    if xmimpflag == 67 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.110922605367631)
    if xmimpflag == 67 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.110922605367631)
    if xmimpflag == 67 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 80.0491803278688
    if xmimpflag == 67 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 80.0491803278688 / (1 - 0.110922605367631 )
    if xmimpflag == 68 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.127935729778166)
    if xmimpflag == 68 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.127935729778166)
    if xmimpflag == 68 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 84
    if xmimpflag == 68 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 84 - (84 * 0.127935729778166 )
    if xmimpflag == 69 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.206358225584424)
    if xmimpflag == 69 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.206358225584424)
    if xmimpflag == 69 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 1004.47058823529
    if xmimpflag == 69 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 1004.47058823529 / (1 - 0.206358225584424 )
    if xmimpflag == 70 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.142775407154303)
    if xmimpflag == 70 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.142775407154303)
    if xmimpflag == 70 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 311.222222222222
    if xmimpflag == 70 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 311.222222222222 / (1 - 0.142775407154303 )
    if xmimpflag == 71 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.106323148232566)
    if xmimpflag == 71 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.106323148232566)
    if xmimpflag == 71 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 310.39837398374
    if xmimpflag == 71 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 310.39837398374 / (1 - 0.106323148232566 )
    if xmimpflag == 97 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.138965456634756)
    if xmimpflag == 97 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.138965456634756)
    if xmimpflag == 97 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 259.21875
    if xmimpflag == 97 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 259.21875 / (1 - 0.138965456634756 )
    if xmimpflag == 72 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.169436742362705)
    if xmimpflag == 72 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.169436742362705)
    if xmimpflag == 72 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 265.325842696629
    if xmimpflag == 72 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 265.325842696629 / (1 - 0.169436742362705 )
    if xmimpflag == 85 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.339905284604731)
    if xmimpflag == 85 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.339905284604731)
    if xmimpflag == 85 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 563.333333333333
    if xmimpflag == 85 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 563.333333333333 / (1 - 0.339905284604731 )
    if xmimpflag == 73 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.129605450439467)
    if xmimpflag == 73 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.129605450439467)
    if xmimpflag == 73 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 407.289473684211
    if xmimpflag == 73 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 407.289473684211 / (1 - 0.129605450439467 )
    if xmimpflag == 74 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0794384325299229)
    if xmimpflag == 74 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0794384325299229)
    if xmimpflag == 74 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 117.137931034483
    if xmimpflag == 74 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 117.137931034483 / (1 - 0.0794384325299229 )
    if xmimpflag == 75 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.189369734252207)
    if xmimpflag == 75 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.189369734252207)
    if xmimpflag == 75 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 192.772020725389
    if xmimpflag == 75 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 192.772020725389 / (1 - 0.189369734252207 )
    if xmimpflag == 76 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.131187789757565)
    if xmimpflag == 76 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.131187789757565)
    if xmimpflag == 76 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 199.041666666667
    if xmimpflag == 76 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 199.041666666667 / (1 - 0.131187789757565 )
    if xmimpflag == 77 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.136342992788614)
    if xmimpflag == 77 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.136342992788614)
    if xmimpflag == 77 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 186.407894736842
    if xmimpflag == 77 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 186.407894736842 / (1 - 0.136342992788614 )
    if xmimpflag == 78 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.103049659988616)
    if xmimpflag == 78 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.103049659988616)
    if xmimpflag == 78 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 155.470588235294
    if xmimpflag == 78 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 155.470588235294 / (1 - 0.103049659988616 )
    if xmimpflag == 79 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.35)
    if xmimpflag == 79 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.35)
    if xmimpflag == 79 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 193.74358974359
    if xmimpflag == 79 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 193.74358974359 / (1 - 0.35 )
    if xmimpflag == 80 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0732085200996002)
    if xmimpflag == 80 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0732085200996002)
    if xmimpflag == 80 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 249.692307692308
    if xmimpflag == 80 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 249.692307692308 / (1 - 0.0732085200996002 )
    if xmimpflag == 81 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0934359066589073)
    if xmimpflag == 81 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0934359066589073)
    if xmimpflag == 81 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 352.952806122449
    if xmimpflag == 81 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 352.952806122449 / (1 - 0.0934359066589073 )
    if xmimpflag == 82 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.07182740558555)
    if xmimpflag == 82 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.07182740558555)
    if xmimpflag == 82 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 419.619047619047
    if xmimpflag == 82 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 419.619047619047 / (1 - 0.07182740558555 )
    if xmimpflag == 83 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0956449943871365)
    if xmimpflag == 83 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0956449943871365)
    if xmimpflag == 83 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 304.5625
    if xmimpflag == 83 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 304.5625 - (304.5625 * 0.0956449943871365 )
    if xmimpflag == 84 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.163929225997462)
    if xmimpflag == 84 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.163929225997462)
    if xmimpflag == 84 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 319.285714285714
    if xmimpflag == 84 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 319.285714285714 / (1 - 0.163929225997462 )
    if xmimpflag == 86 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.112733293827202)
    if xmimpflag == 86 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.112733293827202)
    if xmimpflag == 86 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 129.277777777778
    if xmimpflag == 86 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 129.277777777778 / (1 - 0.112733293827202 )
    if xmimpflag == 87 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0655504344628028)
    if xmimpflag == 87 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0655504344628028)
    if xmimpflag == 87 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 211
    if xmimpflag == 87 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 211 / (1 - 0.0655504344628028 )
    if xmimpflag == 88 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.198929221794951)
    if xmimpflag == 88 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.198929221794951)
    if xmimpflag == 88 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 296.473684210526
    if xmimpflag == 88 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 296.473684210526 - (296.473684210526 * 0.198929221794951 )
    if xmimpflag == 89 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.107517933823928)
    if xmimpflag == 89 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.107517933823928)
    if xmimpflag == 89 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 281.958333333333
    if xmimpflag == 89 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 281.958333333333 / (1 - 0.107517933823928 )
    if xmimpflag == 90 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.028250184258012)
    if xmimpflag == 90 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.028250184258012)
    if xmimpflag == 90 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 208.341176470588
    if xmimpflag == 90 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 208.341176470588 / (1 - 0.028250184258012 )
    if xmimpflag == 91 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0487771272192143)
    if xmimpflag == 91 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0487771272192143)
    if xmimpflag == 91 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 267.896551724138
    if xmimpflag == 91 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 267.896551724138 / (1 - 0.0487771272192143 )
    if xmimpflag == 92 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.111975986975987)
    if xmimpflag == 92 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.111975986975987)
    if xmimpflag == 92 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 328.555555555556
    if xmimpflag == 92 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 328.555555555556 / (1 - 0.111975986975987 )
    if xmimpflag == 93 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0979648763988006)
    if xmimpflag == 93 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0979648763988006)
    if xmimpflag == 93 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 101.111111111111
    if xmimpflag == 93 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 101.111111111111 / (1 - 0.0979648763988006 )
    if xmimpflag == 94 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.297737659966491)
    if xmimpflag == 94 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.297737659966491)
    if xmimpflag == 94 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 319.733333333333
    if xmimpflag == 94 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 319.733333333333 / (1 - 0.297737659966491 )
    if xmimpflag == 95 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0220048899755501)
    if xmimpflag == 95 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0220048899755501)
    if xmimpflag == 95 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 220.428571428571
    if xmimpflag == 95 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 220.428571428571 / (1 - 0.0220048899755501 )
    if xmimpflag == 96 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0)
    if xmimpflag == 96 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0)
    if xmimpflag == 96 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 433
    if xmimpflag == 96 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 433 / (1 - 0 )
    if xmimpflag == 137 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.12659407459354)
    if xmimpflag == 137 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.12659407459354)
    if xmimpflag == 137 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 104.986301369863
    if xmimpflag == 137 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 104.986301369863 / (1 - 0.12659407459354 )
    if xmimpflag == 138 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.179201806454531)
    if xmimpflag == 138 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.179201806454531)
    if xmimpflag == 138 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 108.37037037037
    if xmimpflag == 138 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 108.37037037037 - (108.37037037037 * 0.179201806454531 )
    if xmimpflag == 139 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.162003845923261)
    if xmimpflag == 139 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.162003845923261)
    if xmimpflag == 139 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 128.438775510204
    if xmimpflag == 139 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 128.438775510204 / (1 - 0.162003845923261 )
    if xmimpflag == 140 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.171264386321147)
    if xmimpflag == 140 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.171264386321147)
    if xmimpflag == 140 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 557.6
    if xmimpflag == 140 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 557.6 / (1 - 0.171264386321147 )
    if xmimpflag == 141 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.213152374545978)
    if xmimpflag == 141 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.213152374545978)
    if xmimpflag == 141 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 74
    if xmimpflag == 141 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 74 / (1 - 0.213152374545978 )
    if xmimpflag == 142 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.190548809128441)
    if xmimpflag == 142 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.190548809128441)
    if xmimpflag == 142 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 80.5625
    if xmimpflag == 142 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 80.5625 - (80.5625 * 0.190548809128441 )
    if xmimpflag == 145 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.0577485174550083)
    if xmimpflag == 145 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.0577485174550083)
    if xmimpflag == 145 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 376.928571428571
    if xmimpflag == 145 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 376.928571428571 / (1 - 0.0577485174550083 )
    if xmimpflag == 146 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.153749295952981)
    if xmimpflag == 146 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.153749295952981)
    if xmimpflag == 146 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 154.307692307692
    if xmimpflag == 146 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 154.307692307692 / (1 - 0.153749295952981 )
    if xmimpflag == 147 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.143606923731731)
    if xmimpflag == 147 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.143606923731731)
    if xmimpflag == 147 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 165.903225806452
    if xmimpflag == 147 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 165.903225806452 - (165.903225806452 * 0.143606923731731 )
    if xmimpflag == 148 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.254317624200109)
    if xmimpflag == 148 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.254317624200109)
    if xmimpflag == 148 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 199.730769230769
    if xmimpflag == 148 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 199.730769230769 / (1 - 0.254317624200109 )
    if xmimpflag == 149 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.136559928551299)
    if xmimpflag == 149 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.136559928551299)
    if xmimpflag == 149 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 1003
    if xmimpflag == 149 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 1003 / (1 - 0.136559928551299 )
    if xmimpflag == 150 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.182187702624498)
    if xmimpflag == 150 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.182187702624498)
    if xmimpflag == 150 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 100.090909090909
    if xmimpflag == 150 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 100.090909090909 / (1 - 0.182187702624498 )
    if xmimpflag == 151 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.00833333333333333)
    if xmimpflag == 151 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.00833333333333333)
    if xmimpflag == 151 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 127.103448275862
    if xmimpflag == 151 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 127.103448275862 / (1 - 0.00833333333333333)
    if xmimpflag == 152 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.100333848361108)
    if xmimpflag == 152 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.100333848361108)
    if xmimpflag == 152 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 436.5
    if xmimpflag == 152 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 436.5 / (1 - 0.100333848361108 )
    if xmimpflag == 154 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.235321405225611)
    if xmimpflag == 154 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.235321405225611)
    if xmimpflag == 154 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 580.060606060606
    if xmimpflag == 154 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 580.060606060606 / (1 - 0.235321405225611 )
    if xmimpflag == 155 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.157476046121814)
    if xmimpflag == 155 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.157476046121814)
    if xmimpflag == 155 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 70.0833333333334
    if xmimpflag == 155 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 70.0833333333334 / (1 - 0.157476046121814 )
    if xmimpflag == 156 and slaximp >= 1 and slaarriv is None and slastot is None: slamimp = slaximp - (slaximp * 0.17641709128796)
    if xmimpflag == 156 and slamimp >= 1 and tslavesd is None and tslavesp is None and ncartot is None: slaximp = slamimp / (1 - 0.17641709128796)
    if xmimpflag == 156 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slamimp = 118.333333333333
    if xmimpflag == 156 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = 118.333333333333 / (1 - 0.17641709128796 )
    
    sladvoy = numbers.get('SLADVOY')
    if sladvoy > 0 and slaarriv is None and tslavesd is None and tslavesp is None and ncartot is None and slastot >= 50: slaximp = slastot + sladvoy
    if sladvoy > 0 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv > 1: slaximp = slaarriv + sladvoy
    if sladvoy > 0 and tslavesd is None and tslavesp is None and ncartot is None and slaarriv is None and slastot is None: slaximp = slamimp + sladvoy

    slaximp = round(slaximp)
    slamimp = round(slamimp)
    
    interim.imputed_total_slaves_embarked = slaximp
    interim.imputed_total_slaves_disembarked = slamimp
    
    # tslmtimp - Imputed total of slaves embarked for mortality calculation
    # vymrtimp - Imputed number of slaves died in middle passage
    # vymrtrat - Slaves died on voyage / Slaves embarked
        
    if sladvoy is None and slaarriv <= tslavesd: vymrtimp = tslavesd - slaarriv
    if vymrtimp >= 0: tslmtimp = tslavesd
    if (tslavesd is None and vymrtimp >= 0) and slaarriv >= 1: tslmtimp = slaarriv + vymrtimp
    vymrtrat = vymrtimp / tslmtimp
    
    interim.imputed_number_of_slaves_embarked_for_mortality_calculation = tslmtimp
    interim.imputed_total_slave_deaths_during_middle_passage = vymrtimp
    interim.imputed_mortality_rate = vymrtrat
    
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
    
    # TODO: write first into local variables men1, women1... then reuse them
    adlt1imp = numbers.get('MEN1', 0) + 
        numbers.get('WOMEN1', 0) + 
        numbers.get('ADULT1', 0) +
        numbers.get('MEN4', 0) + 
        numbers.get('WOMEN4', 0) + 
        numbers.get('ADULT4', 0) + 
        numbers.get('MEN5', 0) + 
        numbers.get('WOMEN5', 0) + 
        numbers.get('ADULT5', 0)
    chil1imp = numbers.get('BOY1', 0) + 
        numbers.get('GIRL1', 0) + 
        numbers.get('CHILD1', 0) + 
        numbers.get('INFANT1', 0) + 
        numbers.get('BOY4', 0) + 
        numbers.get('GIRL4', 0) + 
        numbers.get('CHILD4', 0) + 
        numbers.get('INFANT4', 0) + 
        numbers.get('BOY5', 0) + 
        numbers.get('GIRL5', 0) + 
        numbers.get('CHILD5', 0)
    male1imp = numbers.get('MALE1', 0) + 
        numbers.get('MALE4', 0) + 
        numbers.get('MALE5', 0)
    feml1imp = numbers.get('FEMALE1', 0) + 
        numbers.get('FEMALE4', 0) + 
        numbers.get('FEMALE5', 0)
    if not male1imp: 
        male1imp = numbers.get('MEN1', 0) + 
            numbers.get('BOY1', 0) + 
            numbers.get('MEN4', 0) + 
            numbers.get('BOY4', 0) + 
            numbers.get('MEN5', 0) + 
            numbers.get('BOY5', 0)
    if not feml1imp:
        feml1imp = numbers.get('WOMEN1', 0) + 
            numbers.get('GIRL1', 0) + 
            numbers.get('WOMEN4', 0) + 
            numbers.get('GIRL4', 0) + 
            numbers.get('WOMEN5', 0) + 
            numbers.get('GIRL5', 0)
    slavema1 = adlt1imp + chil1imp
    slavemx1 = male1imp + feml1imp
    slavmax1 = numbers.get('MEN1', 0) +
		numbers.get('WOMEN1', 0) +
		numbers.get('BOY1', 0) +
		numbers.get('GIRL1', 0) +
		numbers.get('MEN4', 0) +
		numbers.get('WOMEN4', 0) +
		numbers.get('BOY4', 0) +
		numbers.get('GIRL4', 0) +
		numbers.get('MEN5', 0) +
		numbers.get('WOMEN5', 0) +
		numbers.get('BOY5', 0) +
		numbers.get('GIRL5', 0)
    if slavema1 <= 19: slavema1 = None
    if slavemx1 <= 19: slavemx1 = None
    if slavmax1 <= 19: slavmax1 = None
    if slavema1 is None:
        adlt1imp = None
        chil1imp = None
    if slavemx1 is None:
        feml1imp = None
        male1imp = None
    chilrat1 = chil1imp / slavema1
    malrat1 = male1imp / slavemx1
    if slavmax1 >= 20: menrat1 = (men1 + men4 + men5) / slavmax1
    if slavmax1 >= 20: womrat1 = (women1 + women4 + women5) / slavmax1
    if slavmax1 >= 20: boyrat1 = (boy1 + boy4 + boy5) / slavmax1
    if slavmax1 >= 20: girlrat1 = (girl1 + girl4 + girl5) / slavmax1

    # @ original script line 1530