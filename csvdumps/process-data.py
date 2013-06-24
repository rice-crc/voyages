from voyages.apps.voyage.models import *
from datetime import datetime

input_file = open('voyage-database.csv', 'r')

first_line = input_file.readline()
data = first_line.split(',')
varNameDict = {}
NULL_VAL = "\N"


for index, term in enumerate(data):
    varNameDict[term] = index

def isNotBlank(fieldname):
    return data[varNameDict[fieldname]] != NULL_VAL

def getFieldValue(fieldname):
    return data[varNameDict[fieldname]]

def getIntFieldValue(fieldname):
    try:
        if not isNotBlank(fieldname):
            return None
        return int(getFieldValue(fieldname))
    except ValueError:
        return None

for line in input_file:
    data = line.split(',')

    # voyage
    voyageObj = Voyage(voyage_id=data[varNameDict['voyageid']])
    voyageObj.voyage_ship = VoyageShip()
    voyageObj.voyage_ship.ship_name = data[varNameDict['shipname']]

    # crew section
    crew = VoyageCaptainCrew()
    if isNotBlank('captaina'):
        crew.first_captain = VoyageCaptainCrew.Captain.objects.get_or_create(name=getFieldValue('captaina'))
    if isNotBlank('captainb'):
        crew.second_captain = VoyageCaptainCrew.Captain.objects.get_or_create(name=getFieldValue('captainb'))
    if isNotBlank('captainc'):
        crew.third_captain = VoyageCaptainCrew.Captain.objects.get_or_create(name=getFieldValue('captainc'))

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

    voyageObj.voyage_captain_crew = crew

    # Voyage numbers and characteristics
    characteristics = VoyageSlavesCharacteristics()

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

    tempCharacteristics = []
    for idx in range(1, 6):
        tmpGroup = VoyageSlavesCharacteristics.GroupComposition()
        tmpGroup.num_men = getIntFieldValue("men" + str(idx))
        tmpGroup.num_women = getIntFieldValue("women" + str(idx))
        tmpGroup.num_boy = getIntFieldValue("boy" + str(idx))
        tmpGroup.num_girl = getIntFieldValue("girl" + str(idx))
        tmpGroup.num_males = getIntFieldValue("male" + str(idx))
        tmpGroup.num_females = getIntFieldValue("female" + str(idx))
        tmpGroup.num_adult = getIntFieldValue("adult" + str(idx))
        tmpGroup.num_child = getIntFieldValue("child" + str(idx))
        tmpGroup.num_infant = getIntFieldValue("infant" + str(idx))

        tempCharacteristics.append(tmpGroup)

    characteristics.embarked_first_port_purchase = tempCharacteristics[0]
    characteristics.died_on_middle_passage = tempCharacteristics[1]
    characteristics.disembarked_first_place = tempCharacteristics[2]
    characteristics.embarked_second_port_purchase = tempCharacteristics[3]
    characteristics.embarked_third_port_purchase = tempCharacteristics[4]
    characteristics.disembarked_third_place = tempCharacteristics[5]

    voyageObj.voyage_slave_characteristics = characteristics

    # In progress - might need to change
    voyage_dates = VoyageDates()
    try:
        voyage_dates.departure_last_place_of_landing = datetime.strptime(data[varNameDict["datedep"]])
    except ValueError:
        voyage_dates.departure_last_place_of_landing = None

    voyageObj.voyage_dates = voyage_dates

    characteristics.voyageObj.save()