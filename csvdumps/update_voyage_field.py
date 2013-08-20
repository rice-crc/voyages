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

    voyageObj = Voyage.objects.filter(voyage_id=getIntFieldValue('voyageid'))[0]
    count += 1
    print count

    date_obj = voyageObj.voyage_dates
    if isNotBlank('dateleftafr'):
        tmp = getFieldValue('dateleftafr')
        # MM,DD,YYYY
        date_obj.date_departed_africa = tmp[5:7] + "," + tmp[8:10] + "," + tmp[0:4]
        date_obj.save()
