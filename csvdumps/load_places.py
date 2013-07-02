from voyages.apps.voyage.models import *

input_file = open('places.csv', 'r')

##### Common section to all files #####
NULL_VAL = "\N"
DELIMITER = ','

first_line = input_file.readline()
data = first_line[0:-2].split(DELIMITER)
print len(data)

varNameDict = {}
for index, term in enumerate(data):
    varNameDict[term[1:-1]] = index


def isNotBlank(field_name):
    return data[varNameDict[field_name]][1:-1] != NULL_VAL


def getFieldValue(field_name):
    print field_name
    return data[varNameDict[field_name]][1:-1]


def getIntFieldValue(field_name):
    try:
        if not isNotBlank(field_name):
            return None
        return int(getFieldValue(field_name))
    except ValueError:
        return None


def getDecimalFieldValue(field_name):
    try:
        if not isNotBlank(field_name):
            return None
        return float(getFieldValue(field_name))
    except ValueError:
        return None
##### End of Common section to all files #####

for line in input_file:
    data = line.split(DELIMITER)

    location = Place()
    location.name = getFieldValue('name')
    location.code = getFieldValue('id')
    location.longitude = getDecimalFieldValue('longitude')
    location.latitude = getDecimalFieldValue('latitude')
    if isNotBlank('region_id'):
        location.region = Region.objects.filter(code=getIntFieldValue('region_id'))

    location.save()
