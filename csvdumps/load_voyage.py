import sys
from voyages.apps.voyage.models import *
from datetime import datetime

# Load the source csv to the database
if len(sys.argv) > 0:
    input_file = open(sys.argv[0], 'r')
else:
    input_file = open('voyage-database.csv', 'r')

# Load the voyage csv to the database
# Requires loading sources.csv first
NULL_VAL = "\N"
DELIMITER = ','
first_line = input_file.readline()
data = first_line.split(DELIMITER)
varNameDict = {}

listSources = VoyageSources.objects.all()

for index, term in enumerate(data):
    varNameDict[term] = index


def isNotBlank(field_name):
    return data[varNameDict[field_name]] != NULL_VAL


def getFieldValue(field_name):
    return data[varNameDict[field_name]]


def getIntFieldValue(field_name):
    try:
        if not isNotBlank(field_name):
            return None
        return int(getFieldValue(field_name))
    except ValueError:
        return None

for line in input_file:
    data = line.split(DELIMITER)

    if getFieldValue('suggestion') != "t" or getFieldValue('revision') != 1:
        continue

    voyageObj = Voyage(voyage_id=data[varNameDict['voyageid']])

    # A: voyage ship, nation and owner
    ship = VoyageShip.objects.create()
    ship.ship_name = data[varNameDict['shipname']]
    if isNotBlank('national'):
        ship.nationality_ship = VoyageShip.Nationality.objects.filter(code=getIntFieldValue('national'))[0]
    ship.tonnage = getIntFieldValue('tonnage')
    ship.ton_type = VoyageShip.TonType.objects.filter(code=getIntFieldValue('tontype'))[0]
    ship.rig_of_vessel = VoyageShip.RigOfVessel.objects.filter(code=getIntFieldValue('rig'))[0]
    ship.guns_mounted = getIntFieldValue('guns')
    ship.year_of_construction = getIntFieldValue('yrcons')
    ship.vessel_construction_place = Place.objects.filter(code=)

    voyageObj.voyage_ship = ship

    # Captain and Crew section
    crew = VoyageCrew.objects.create()
    crew.crew_voyage_outset = getIntFieldValue('crew1')
    crew.crew_departure_last_port = getIntFieldValue('crew2')
    crew.crew_first_landing = getIntFieldValue('crew3')
    crew.crew_return_begin = getIntFieldValue('crew4')
    crew.crew_end_voyage = getIntFieldValue('crew5')
    crew.unspecified_crew = getIntFieldValue('crew')
    crew.crew_died_before_first_trade = getIntFieldValue('saild1')
    crew.crew_died_while_ship_african = getIntFieldValue('saild2')
    crew.crew_died_middle_passge = getIntFieldValue('saild3')
    crew.crew_died_in_americas = getIntFieldValue('saild4')
    crew.crew_died_on_return_voyage = getIntFieldValue('saild5')
    crew.crew_died_complete_voyage = getIntFieldValue('crewdied')
    crew.crew_deserted = getIntFieldValue('ndesert')
    # crew.save()

    voyageObj.voyage_captain_crew = crew

    if isNotBlank('captaina'):
        first_captain = VoyageCaptain.Captain.objects.get_or_create(
            name=getFieldValue('captaina'))
        VoyageCaptainConnection.objects.create(
            captain_order=1, captain=first_captain, voyage=voyageObj)

    if isNotBlank('captainb'):
        second_captain = VoyageCaptain.Captain.objects.get_or_create(
            name=getFieldValue('captainb'))
        VoyageCaptainConnection.objects.create(
            captain_order=2, captain=second_captain, voyage=voyageObj)

    if isNotBlank('captainc'):
        third_captain = VoyageCaptain.Captain.objects.get_or_create(
            name=getFieldValue('captainc'))
        VoyageCaptainConnection.objects.create(
            captain_order=3, captain=third_captain, voyage=voyageObj)

    # Voyage numbers and characteristics
    characteristics = VoyageSlavesNumbers.objects.create()

    characteristics.num_slaves_intended_first_port = getIntFieldValue("slintend")
    characteristics.num_slaves_intended_second_port = getIntFieldValue("slintend2")
    characteristics.num_slaves_carried_first_port = getIntFieldValue("ncar13")
    characteristics.num_slaves_carried_second_port = getIntFieldValue("ncar15")
    characteristics.num_slaves_carried_third_port = getIntFieldValue("ncar17")
    characteristics.total_num_slaves_purchased = getIntFieldValue("tslavesp")
    characteristics.total_num_slaves_dep_last_slaving_port = getIntFieldValue("tslavesd")
    characteristics.total_num_slaves_arr_first_port_embark = getIntFieldValue("slaarrive")
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
    characteristics.num_women_embark_third_port_purchase = getIntFieldValue("women")
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

    characteristics.voyage = voyageObj

    # In progress - might need to change
    voyage_dates = VoyageDates()
    try:
        voyage_dates.departure_last_place_of_landing = datetime.strptime(data[varNameDict["datedep"]])
    except ValueError:
        voyage_dates.departure_last_place_of_landing = None

    voyageObj.voyage_dates = voyage_dates

    # Voyage sources
    # Potentially has a bug!!!!!!!!
    def findBestMachingSource(matchstring):
        # Base case if the string is too short
        if len(matchstring) <= 2:
            return None

        for source in listSources:
            if source.short_ref.find(matchstring) > -1:
                return source

        # Find the best matching/contains the substring
        # : should be the last delimiter, then
        tmpPos = max(matchstring.rfind(':'), matchstring.rfind(","))
        if tmpPos > -1:
            return findBestMachingSource(matchstring[: tmpPos])
        else:
            return None

    def insertSource(fieldname, order):
        if isNotBlank(fieldname):
            src = findBestMachingSource(getFieldValue(fieldname))
            if src is not None:
                VoyageSourcesConnection.objects.create(source=src, source_order=order,
                                                      text_ref=getFieldValue(fieldname),
                                                      group=voyageObj)
            else :
                print "Error finding matching source %s" % getFieldValue(fieldname)

    # Alphabetical letters between a and r
    letters = map(chr, range(97, 115))
    for idx, letter in letters:
        # Inserting sourcea, sourceb. .. sourcer
        insertSource('source' + letter, (idx + 1))

