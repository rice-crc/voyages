from voyages.apps.voyage.models import *

input_file = open('voyage-database.csv', 'r')

first_line = input_file.readline()
data = first_line.split(',')
varNameDict = {}

for index, term in enumerate(data):
    varNameDict[term] = index

for line in input_file:
    data = line.split(',')
    voyageObj = Voyage(voyage_id=data[varNameDict['voyageid']])
    voyageObj.voyage_ship = Voyage.VoyageShip()
    voyageObj.voyage_ship.ship_name = data[varNameDict['shipname']]


    voyageObj.save()