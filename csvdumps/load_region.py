from voyages.apps.voyage.models import *
from decimal import *

input_file = open('region.txt', 'r')

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


def getDecimalFieldValue(field_name):
    try:
        if not isNotBlank(field_name):
            return None
        return Decimal(getFieldValue(field_name))
    except ValueError:
        return None
##### End of Common section to all files #####

for line in input_file:
    data = line[0:-2].split(DELIMITER)

    region = Region()
    region.name = getFieldValue('name')
    region.code = getIntFieldValue('order_num')

    if getFieldValue('show_on_map') == "t":
        region.show_on_map = True
    else:
        region.show_on_map = False

    if getFieldValue('show_on_main_map') == "t":
        region.show_on_main_map = True
    else:
        region.show_on_main_map = False

    if isNotBlank('area_id'):
        region.broad_region = BroadRegion.objects.filter(code=getIntFieldValue('area_id'))[0]

    region.save()
