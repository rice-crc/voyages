from decimal import *
from voyages.apps.voyage.models import *

input_file = open('csvdumps/voyage.txt', 'r')

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

count = 0
nonCount = 0


for line in input_file:
    data = line[0:-2].split(DELIMITER)

    if isNotBlank('voyageid'):
        if getIntFieldValue('voyageid') == 51655:

            print len(data)
            print getFieldValue('suggestion')
            print getFieldValue('revision')
            if getFieldValue('suggestion') != "f" or getIntFieldValue('revision') != 1:
                print "skipped"


