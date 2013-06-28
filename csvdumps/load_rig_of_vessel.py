import sys
from voyages.apps.voyage.models import *

# Load the source csv to the database
if len(sys.argv) > 0:
    input_file = open(sys.argv[0], 'r')
else:
    input_file = open('rigofvessel.csv', 'r')

NULL_VAL = "\N"
DELIMITER = ','
first_line = input_file.readline()
data = first_line.split(DELIMITER)
varNameDict = {}

for index, term in enumerate(data):
    varNameDict[term] = index


def getFieldValue(field_name):
    return data[varNameDict[field_name]]

for line in input_file:
    data = line.split(DELIMITER)

    rov_obj = VoyageShip.RigOfVessel()
    rov_obj.code = getFieldValue('id')
    rov_obj.rig_of_vessel = getFieldValue('name')

    rov_obj.save()
