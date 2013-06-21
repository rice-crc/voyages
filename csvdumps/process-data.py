from voyages.apps.voyage.models import *

input_file = open('voyage-database.csv', 'r')

first_line = input_file.readline()
data = first_line.split(',')
varNameDict = {}

for index, term in enumerate(data):
    varNameDict[term] = index

for line in input_file:
    data = line.split(',')

    # voyage
    voyageObj = Voyage(voyage_id=data[varNameDict['voyageid']])
    voyageObj.voyage_ship = VoyageShip()
    voyageObj.voyage_ship.ship_name = data[varNameDict['shipname']]

    crew = VoyageCaptainCrew()
    crew.first_captain = VoyageCaptainCrew.Captain.objects.get_or_create(name=data[varNameDict['captaina']])
    crew.second_captain = VoyageCaptainCrew.Captain.objects.get_or_create(name=data[varNameDict['captainb']])
    crew.third_captain = VoyageCaptainCrew.Captain.objects.get_or_create(name=data[varNameDict['captainc']])

    voyageObj.voyage_captain_crew = crew

    # Voyage numbers and characteristics
    characteristics = VoyageSlavesCharacteristics()

    tempCharacteristics = []

    for idx in range(1, 6):
        tmpGroup = VoyageSlavesCharacteristics.GroupComposition()
        try:
            tmpGroup.num_men = int(data[varNameDict["men" + str(idx)]])
        except ValueError:
            tmpGroup.num_men = None
        try:
            tmpGroup.num_women = int(data[varNameDict["women" + str(idx)]])
        except ValueError:
            tmpGroup.num_women = None
        try:
            tmpGroup.num_boy = int(data[varNameDict["boy" + str(idx)]])
        except ValueError:
            tmpGroup.num_boy = None
        try:
            tmpGroup.num_girl = int(data[varNameDict["girl" + str(idx)]])
        except ValueError:
            tmpGroup.num_girl = None
        try:
            tmpGroup.num_women = int(data[varNameDict["women" + str(idx)]])
        except ValueError:
            tmpGroup.num_women = None
        try:
            tmpGroup.num_adult = int(data[varNameDict["adult" + str(idx)]])
        except ValueError:
            tmpGroup.num_adult = None
        try:
            tmpGroup.num_child = int(data[varNameDict["child" + str(idx)]])
        except ValueError:
            tmpGroup.num_child = None
        try:
            tmpGroup.num_infant = int(data[varNameDict["infant" + str(idx)]])
        except ValueError:
            tmpGroup.num_infant = None
        tempCharacteristics.append(tmpGroup)

    characteristics.embarked_first_port_purchase = tempCharacteristics[0]
    characteristics.died_on_middle_passage = tempCharacteristics[1]
    characteristics.disembarked_first_place = tempCharacteristics[2]
    characteristics.embarked_second_port_purchase = tempCharacteristics[3]
    characteristics.embarked_third_port_purchase = tempCharacteristics[4]
    characteristics.disembarked_third_place = tempCharacteristics[5]


    characteristics.voyageObj.save()