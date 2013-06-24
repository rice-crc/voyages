from voyages.apps.voyage.models import *

# Load the source csv to the database
input_file = open('sources.csv', 'r')

first_line = input_file.readline()
data = first_line.split(',')
varNameDict = {}
NULL_VAL = "\N"

for index, term in enumerate(data):
    varNameDict[term] = index

def getFieldValue(fieldname):
    return data[varNameDict[fieldname]]

for line in input_file:
    data = line.split(',')

    source = VoyageSources()
    source.short_ref = getFieldValue('id')
    source.long_ref = getFieldValue('name')

    source.save()
