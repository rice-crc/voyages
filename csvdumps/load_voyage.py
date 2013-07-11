from decimal import *
from voyages.apps.voyage.models import *

input_file = open('voyage.txt', 'r')

##### Common section to all files #####
NULL_VAL = "\N"
DELIMITER = '\t'

first_line = input_file.readline()
data = first_line[0:-2].split(DELIMITER)

varNameDict = {}
for index, term in enumerate(data):
    varNameDict[term[1:-1]] = index


def isNotBlank(field_name):
    return data[varNameDict[field_name]][1:-1] != NULL_VAL


def getFieldValue(field_name):
    return data[varNameDict[field_name]][1:-1]


def getIntFieldValue(field_name):
    try:
        if not isNotBlank(field_name):
            return None
        return int(getFieldValue(field_name))
    except ValueError:
        return None


def getIntFieldValuePlace(field_name):
    try:
        if not isNotBlank(field_name):
            return None
        tmpValue = int(getFieldValue(field_name))
        if tmpValue > 90000:
            tmpValue = 99801
        return tmpValue
    except ValueError:
        return None


def getDecimalFieldValue(field_name):
    try:
        if not isNotBlank(field_name):
            return None
        return Decimal(getFieldValue(field_name))
    except ValueError:
        return None

##### End of Common section to all files #####

listSources = VoyageSources.objects.all()

count = 0

for line in input_file:
    data = line[0:-2].split(DELIMITER)

    if getFieldValue('suggestion') != "f" or getIntFieldValue('revision') != 1:
        continue

    voyageObj = Voyage.objects.create()

    count = count + 1
    print count

    if isNotBlank('voyageid'):
        voyageObj.voyage_id = getIntFieldValue('voyageid')
        voyageObj.save()

    #print voyageObj.voyage_id

    # A: voyage ship, nation and owner
    ship = VoyageShip()

    ship.voyage = voyageObj

    if isNotBlank('shipname'):
        ship.ship_name = getFieldValue('shipname')

    if isNotBlank('national'):
        ship.nationality_ship = Nationality.objects.filter(value=getIntFieldValue('national'))[0]
    ship.tonnage = getIntFieldValue('tonnage')
    if isNotBlank('tontype'):
        ship.ton_type = TonType.objects.filter(value=getIntFieldValue('tontype'))[0]
    if isNotBlank('rig'):
        ship.rig_of_vessel = RigOfVessel.objects.filter(value=getIntFieldValue('rig'))[0]
    ship.guns_mounted = getIntFieldValue('guns')
    ship.year_of_construction = getIntFieldValue('yrcons')



    if isNotBlank('placcons'):
        ship.vessel_construction_place = Place.objects.filter(value=getIntFieldValuePlace('placcons'))[0]
    if isNotBlank('constreg'):
        ship.vessel_construction_region = Region.objects.filter(value=getIntFieldValue('constreg'))[0]

    ship.year_of_construction = getIntFieldValue('yrcons')

    ship.registered_year = getIntFieldValue('yrreg')
    if isNotBlank('placreg'):
        ship.registered_place = Place.objects.filter(value=getIntFieldValuePlace('placreg'))[0]
    if isNotBlank('regisreg'):
        ship.registered_region = Region.objects.filter(value=getIntFieldValue('regisreg'))[0]

    # Imputed variables in nationality
    if isNotBlank('natinimp'):
        ship.imputed_nationality = Nationality.objects.filter(value=getIntFieldValue('natinimp'))[0]
    if isNotBlank('tonmod'):
        ship.tonnage_mod = round(getDecimalFieldValue('tonmod'), 1)

    ship.save()

    if 1 == 1:
        continue

    # Owners section
    letters = map(chr, range(97, 97 + 16)) # from a to p
    for idx, letter in enumerate(letters):
        # Inserting ownera, ownerb, ..., ownerp
        if isNotBlank('owner' + letter):
            tmpOwner, created = VoyageShipOwner.objects.get_or_create(name=getFieldValue('owner' + letter))
            # Create a voyage-owner connection
            VoyageShipOwnerConnection.objects.create(owner=tmpOwner, voyage=voyageObj,
                                                     owner_order=(idx+1))

    # Voyage outcome
    outcome = VoyageOutcome.objects.create(voyage=voyageObj)
    if isNotBlank('fate'):
        outcome.particular_outcome = VoyageOutcome.ParticularOutcome.objects.filter(
                value=getIntFieldValue('fate'))[0]
    if isNotBlank('resistance'):
        outcome.resistance = VoyageOutcome.Resistance.objects.filter(
                value=getIntFieldValue('resistance'))[0]
    if isNotBlank('fate2'):
        outcome.outcome_slaves = VoyageOutcome.SlavesOutcome.objects.filter(
                value=getIntFieldValue('fate2'))[0]
    if isNotBlank('fate3'):
        outcome.vessel_captured_outcome = VoyageOutcome.VesselCapturedOutcome.objects.filter(
                value=getIntFieldValue('fate3'))[0]
    if isNotBlank('fate4'):
        outcome.outcome_owner = VoyageOutcome.OwnerOutcome.objects.filter(
                value=getIntFieldValue('fate4'))[0]

    itinerary = VoyageItinerary()

    itinerary.voyage = voyage=voyageObj
    # Voyage itinerary
    if isNotBlank('portdep'):
        itinerary.port_of_departure = Place.objects.filter(value=getIntFieldValuePlace('portdep'))[0]
    if isNotBlank('embport'):
        itinerary.int_first_port_emb = Place.objects.filter(value=getIntFieldValuePlace('embport'))[0]
    if isNotBlank('embport2'):
        itinerary.int_second_port_emb = Place.objects.filter(value=getIntFieldValuePlace('embport2'))[0]

    if isNotBlank('embreg'):
        itinerary.int_first_region_purchase_slaves = Region.objects.filter(value=getIntFieldValue('embreg'))[0]
    if isNotBlank('embreg2'):
        itinerary.int_second_region_purchase_slaves = Region.objects.filter(value=getIntFieldValue('embreg2'))[0]

    if isNotBlank('arrport'):
        itinerary.int_first_port_dis = Place.objects.filter(value=getIntFieldValuePlace('arrport'))[0]
    if isNotBlank('arrport2'):
        itinerary.int_second_port_dis = Place.objects.filter(value=getIntFieldValuePlace('arrport2'))[0]

    if isNotBlank('regarr'):
        itinerary.int_first_region_slave_landing = Region.objects.filter(value=getIntFieldValue('regarr'))[0]
    if isNotBlank('regarr2'):
        itinerary.int_second_region_slave_landing = Region.objects.filter(value=getIntFieldValue('regarr2'))[0]

    itinerary.ports_called_buying_slaves = getIntFieldValue('nppretra')

    if isNotBlank('plac1tra'):
        itinerary.first_place_slave_purchase = Place.objects.filter(value=getIntFieldValuePlace('plac1tra'))[0]
    if isNotBlank('plac2tra'):
        itinerary.second_place_slave_purchase = Place.objects.filter(value=getIntFieldValuePlace('plac2tra'))[0]
    if isNotBlank('plac3tra'):
        itinerary.third_place_slave_purchase = Place.objects.filter(value=getIntFieldValuePlace('plac3tra'))[0]

    if isNotBlank('regem1'):
        itinerary.first_region_slave_emb = Region.objects.filter(value=getIntFieldValue('regem1'))[0]
    if isNotBlank('regem2'):
        itinerary.second_region_slave_emb = Region.objects.filter(value=getIntFieldValue('regem2'))[0]
    if isNotBlank('regem3'):
        itinerary.third_region_slave_emb = Region.objects.filter(value=getIntFieldValue('regem3'))[0]
    if isNotBlank('npafttra'):
        itinerary.port_of_call_before_atl_crossing = Place.objects.filter(
                value=getIntFieldValuePlace('npafttra'))[0]

    itinerary.number_of_ports_of_call = getIntFieldValue('npprior')

    if isNotBlank('sla1port'):
        itinerary.first_landing_place = Place.objects.filter(value=getIntFieldValuePlace('sla1port'))[0]
    if isNotBlank('adpsale1'):
        itinerary.second_landing_place = Place.objects.filter(value=getIntFieldValuePlace('adpsale1'))[0]
    if isNotBlank('adpsale2'):
        itinerary.third_landing_place = Place.objects.filter(value=getIntFieldValuePlace('adpsale2'))[0]

    if isNotBlank('regdis1'):
        itinerary.first_landing_region = Region.objects.filter(value=getIntFieldValue('regdis1'))[0]
    if isNotBlank('regdis2'):
        itinerary.second_landing_region = Region.objects.filter(value=getIntFieldValue('regdis2'))[0]
    if isNotBlank('regdis3'):
        itinerary.third_landing_region = Region.objects.filter(value=getIntFieldValue('regdis3'))[0]

    if isNotBlank('portret'):
        itinerary.place_voyage_ended = Place.objects.filter(value=getIntFieldValuePlace('portret'))[0]
    if isNotBlank('retrnreg'):
        itinerary.region_of_return = Region.objects.filter(value=getIntFieldValue('retrnreg'))[0]
    if isNotBlank('retrnreg1'):
        itinerary.broad_region_of_return = BroadRegion.objects.filter(value=getIntFieldValue('retrnreg1'))[0]

    # Imputed itinerary variables
    if isNotBlank('ptdepimp'):
        itinerary.imp_port_voyage_begin = Place.objects.filter(value=getIntFieldValuePlace('ptdepimp'))[0]
    if isNotBlank('deptregimp'):
        itinerary.imp_region_voyage_begin = Region.objects.filter(value=getIntFieldValue('deptregimp'))[0]
    if isNotBlank('deptregimp1'):
        itinerary.imp_broad_region_voyage_begin = BroadRegion.objects.filter(value=getIntFieldValue('deptregimp1'))[0]
    if isNotBlank('majbuypt'):
        itinerary.principal_place_of_slave_purchase = Place.objects.filter(
                value=getIntFieldValuePlace('majbuypt'))[0]
    if isNotBlank('mjbyptimp'):
        itinerary.imp_principal_place_of_slave_purchase = Place.objects.filter(value=getIntFieldValuePlace('mjbyptimp'))[0]
    if isNotBlank('majbyimp'):
        itinerary.imp_principal_region_of_slave_purchase = Region.objects.filter(value=getIntFieldValue('majbyimp'))[0]
    if isNotBlank('majbyimp1'):
        itinerary.imp_broad_region_of_slave_purchase = BroadRegion.objects.filter(value=getIntFieldValue('majbyimp1'))[0]
    if isNotBlank('majselpt'):
        itinerary.principal_port_of_slave_dis = Place.objects.filter(value=getIntFieldValuePlace('majselpt'))[0]
    if isNotBlank('mjslptimp'):
        itinerary.imp_principal_port_slave_dis = Place.objects.filter(value=getIntFieldValuePlace('mjslptimp'))[0]
    if isNotBlank('mjselimp'):
        itinerary.imp_principal_region_slave_dis = Region.objects.filter(value=getIntFieldValue('mjselimp'))[0]
    if isNotBlank('mjselimp1'):
        itinerary.imp_broad_region_slave_dis = BroadRegion.objects.filter(value=getIntFieldValue('mjselimp1'))[0]

    itinerary.save()

    def construct_date_string(day_field, month_field, year_field):
        """
        :param day_field:
        :param month_field:
        :param year_field:
        :return "mm,dd, yyyy":
        """
        tmpStr = ""
        if isNotBlank(month_field):
            tmpStr += getFieldValue(month_field)
        tmpStr += ","
        if isNotBlank(day_field):
            tmpStr += getFieldValue(day_field)
        tmpStr += ","
        if isNotBlank(year_field):
            tmpStr += getFieldValue(year_field)
        if tmpStr == ',,':
            return None
        return tmpStr

    # Voyage dates
    date_info = VoyageDates()
    date_info.voyage = voyageObj
    date_info.voyage_began = construct_date_string('datedepa', 'datedepb', 'datedepc')
    date_info.slave_purchase_began = construct_date_string('d1slatra', 'd1slatrb', 'd1slatrc')
    date_info.vessel_left_port = construct_date_string('dlslatra', 'dlslatrb', 'dlslatrc')
    date_info.first_dis_of_slaves = construct_date_string('datarr32', 'datarr33', 'datarr34')
    date_info.arrival_at_second_place_landing = construct_date_string('datarr36', 'datarr37', 'datarr38')
    date_info.departure_last_place_of_landing = construct_date_string('ddepam', 'ddepamb', 'ddepamc')
    date_info.voyage_completed = construct_date_string('datarr43', 'datarr44', 'datarr45')
    if isNotBlank('yeardep'):
        date_info.imp_voyage_began = ",," + getFieldValue('yeardep')
    if isNotBlank('yearaf'):
        date_info.imp_departed_africa = ",," + getFieldValue('yearaf')
    if isNotBlank('yearam'):
        date_info.imp_arrival_at_port_of_dis = ",," + getFieldValue('yearam')

    date_info.imp_length_home_to_disembark = getIntFieldValue('voy1imp')
    date_info.imp_length_leaving_africa_to_disembark = getIntFieldValue('voy2imp')
    date_info.save()

    # Captain and Crew section
    crew = VoyageCrew()
    crew.voyage = voyageObj
    crew.crew_voyage_outset = getIntFieldValue('crew1')
    crew.crew_departure_last_port = getIntFieldValue('crew2')
    crew.crew_first_landing = getIntFieldValue('crew3')
    crew.crew_return_begin = getIntFieldValue('crew4')
    crew.crew_end_voyage = getIntFieldValue('crew5')
    crew.unspecified_crew = getIntFieldValue('crew')
    crew.crew_died_before_first_trade = getIntFieldValue('saild1')
    crew.crew_died_while_ship_african = getIntFieldValue('saild2')
    crew.crew_died_middle_passage = getIntFieldValue('saild3')
    crew.crew_died_in_americas = getIntFieldValue('saild4')
    crew.crew_died_on_return_voyage = getIntFieldValue('saild5')
    crew.crew_died_complete_voyage = getIntFieldValue('crewdied')
    crew.crew_deserted = getIntFieldValue('ndesert')

    if isNotBlank('captaina'):
        first_captain, created = VoyageCaptain.objects.get_or_create(
            name=getFieldValue('captaina'))
        VoyageCaptainConnection.objects.create(
            captain_order=1, captain=first_captain, voyage=voyageObj)

    if isNotBlank('captainb'):
        second_captain, created = VoyageCaptain.objects.get_or_create(
            name=getFieldValue('captainb'))
        VoyageCaptainConnection.objects.create(
            captain_order=2, captain=second_captain, voyage=voyageObj)

    if isNotBlank('captainc'):
        third_captain, created = VoyageCaptain.objects.get_or_create(
            name=getFieldValue('captainc'))
        VoyageCaptainConnection.objects.create(
            captain_order=3, captain=third_captain, voyage=voyageObj)
    crew.save()

    # Voyage numbers and characteristics
    characteristics = VoyageSlavesNumbers()
    characteristics.voyage = voyageObj

    characteristics.num_slaves_intended_first_port = getIntFieldValue("slintend")
    characteristics.num_slaves_intended_second_port = getIntFieldValue("slinten2")
    characteristics.num_slaves_carried_first_port = getIntFieldValue("ncar13")
    characteristics.num_slaves_carried_second_port = getIntFieldValue("ncar15")
    characteristics.num_slaves_carried_third_port = getIntFieldValue("ncar17")
    characteristics.total_num_slaves_purchased = getIntFieldValue("tslavesp")
    characteristics.total_num_slaves_dep_last_slaving_port = getIntFieldValue("tslavesd")
    characteristics.total_num_slaves_arr_first_port_embark = getIntFieldValue("slaarriv")
    characteristics.num_slaves_disembark_first_place = getIntFieldValue("slas32")
    characteristics.num_slaves_disembark_second_place = getIntFieldValue("slas36")
    characteristics.num_slaves_disembark_third_place = getIntFieldValue("slas39")

    characteristics.num_men_embark_first_port_purchase = getIntFieldValue("men1")
    characteristics.num_women_embark_first_port_purchase = getIntFieldValue("women1")
    characteristics.num_boy_embark_first_port_purchase = getIntFieldValue("boy1")
    characteristics.num_girl_embark_first_port_purchase = getIntFieldValue("girl1")
    characteristics.num_adult_embark_first_port_purchase = getIntFieldValue("adult1")
    characteristics.num_child_embark_first_port_purchase = getIntFieldValue("child1")
    characteristics.num_infant_embark_first_port_purchase = getIntFieldValue("infant1")
    characteristics.num_males_embark_first_port_purchase = getIntFieldValue("male1")
    characteristics.num_females_embark_first_port_purchase = getIntFieldValue("female1")

    characteristics.num_men_died_middle_passage = getIntFieldValue("men2")
    characteristics.num_women_died_middle_passage = getIntFieldValue("women2")
    characteristics.num_boy_died_middle_passage = getIntFieldValue("boy2")
    characteristics.num_girl_died_middle_passage = getIntFieldValue("girl2")
    characteristics.num_adult_died_middle_passage = getIntFieldValue("adult2")
    characteristics.num_child_died_middle_passage = getIntFieldValue("child2")
    characteristics.num_infant_died_middle_passage = getIntFieldValue("infant2")
    characteristics.num_males_died_middle_passage = getIntFieldValue("male2")
    characteristics.num_females_died_middle_passage = getIntFieldValue("female2")

    characteristics.num_men_disembark_first_landing = getIntFieldValue("men3")
    characteristics.num_women_disembark_first_landing = getIntFieldValue("women3")
    characteristics.num_boy_disembark_first_landing = getIntFieldValue("boy3")
    characteristics.num_girl_disembark_first_landing = getIntFieldValue("girl3")
    characteristics.num_adult_disembark_first_landing = getIntFieldValue("adult3")
    characteristics.num_child_disembark_first_landing = getIntFieldValue("child3")
    characteristics.num_infant_disembark_first_landing = getIntFieldValue("infant3")
    characteristics.num_males_disembark_first_landing = getIntFieldValue("male3")
    characteristics.num_females_disembark_first_landing = getIntFieldValue("female3")

    characteristics.num_men_embark_second_port_purchase = getIntFieldValue("men4")
    characteristics.num_women_embark_second_port_purchase = getIntFieldValue("women4")
    characteristics.num_boy_embark_second_port_purchase = getIntFieldValue("boy4")
    characteristics.num_girl_embark_second_port_purchase = getIntFieldValue("girl4")
    characteristics.num_adult_embark_second_port_purchase = getIntFieldValue("adult4")
    characteristics.num_child_embark_second_port_purchase = getIntFieldValue("child4")
    characteristics.num_infant_embark_second_port_purchase = getIntFieldValue("infant4")
    characteristics.num_males_embark_second_port_purchase = getIntFieldValue("male4")
    characteristics.num_females_embark_second_port_purchase = getIntFieldValue("female4")

    characteristics.num_men_embark_third_port_purchase = getIntFieldValue("men5")
    characteristics.num_women_embark_third_port_purchase = getIntFieldValue("women5")
    characteristics.num_boy_embark_third_port_purchase = getIntFieldValue("boy5")
    characteristics.num_girl_embark_third_port_purchase = getIntFieldValue("girl5")
    characteristics.num_adult_embark_third_port_purchase = getIntFieldValue("adult5")
    characteristics.num_child_embark_third_port_purchase = getIntFieldValue("child5")
    characteristics.num_infant_embark_third_port_purchase = getIntFieldValue("infant5")
    characteristics.num_males_embark_third_port_purchase = getIntFieldValue("male5")
    characteristics.num_females_embark_third_port_purchase = getIntFieldValue("female5")

    characteristics.num_men_disembark_second_landing = getIntFieldValue("men6")
    characteristics.num_women_embark_first_port_purchase = getIntFieldValue("women6")
    characteristics.num_boy_embark_first_port_purchase = getIntFieldValue("boy6")
    characteristics.num_girl_embark_first_port_purchase = getIntFieldValue("girl6")
    characteristics.num_adult_embark_first_port_purchase = getIntFieldValue("adult6")
    characteristics.num_child_embark_first_port_purchase = getIntFieldValue("child6")
    characteristics.num_infant_embark_first_port_purchase = getIntFieldValue("infant6")
    characteristics.num_males_embark_first_port_purchase = getIntFieldValue("male6")
    characteristics.num_females_embark_first_port_purchase = getIntFieldValue("female6")

    characteristics.save()

    # Voyage sources
    # Potentially has a bug!!!!!!!!
    def findBestMachingSource(matchstring):
        # Base case if the string is too short
        if len(matchstring) <= 2:
            return None

        for source in listSources:
            if source.short_ref is None:
                continue
            if len(source.short_ref) < len(matchstring):
                continue
            #sourcestr = source.short_ref.decode('utf-8')
            sourcestr = source.short_ref

            if sourcestr.find(matchstring) > -1:
                return source

        # Find the best matching/contains the substring
        # : should be the last delimiter, then
        tmpPos = max(matchstring.rfind(':'), matchstring.rfind(","), matchstring.rfind("-"))
        if tmpPos > -1:
            return findBestMachingSource(matchstring[: tmpPos])
        else:
            return None

    def insertSource(fieldname, order):
        if isNotBlank(fieldname):
            to_be_matched = getFieldValue(fieldname).decode('utf-8')
            src = findBestMachingSource(to_be_matched)
            if src is not None:
                VoyageSourcesConnection.objects.create(source=src, source_order=order,
                                                      text_ref=getFieldValue(fieldname),
                                                      group=voyageObj)
               # print "Found match %s" % to_be_matched
            else :
                #print "No match found for %s" % getFieldValue(fieldname)
                pass

    # Alphabetical letters between a and r
    letters = map(chr, range(97, 97 + 18))
    for idx, letter in enumerate(letters):
        # Inserting sourcea, sourceb. .. sourcer
        insertSource('source' + letter, (idx + 1))

    voyageObj.save()