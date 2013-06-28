import sys
from voyages.apps.voyage.models import *

# Load the source csv to the database
if len(sys.argv) > 0:
    input_file = open(sys.argv[0], 'r')
else:
    input_file = open('tontype.csv', 'r')

NULL_VAL = "\N"
DELIMITER = ','
first_line = input_file.readline()
data = first_line.split(DELIMITER)
varNameDict = {}

for index, term in enumerate(data):
    varNameDict[term] = index


def getFieldValue(fieldname):
    return data[varNameDict[fieldname]]

for line in input_file:
    data = line.split(DELIMITER)

    ton_type = VoyageShip.TonType()
    ton_type.code = getFieldValue('id')
    ton_type.ton_type = getFieldValue('name')

    ton_type.save()
