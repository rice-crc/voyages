from voyages.apps.resources.models import *
from decimal import *

input_file = open('images.txt', 'r')

##### Common section to all files #####
NULL_VAL = "\N"
DELIMITER = '\t'

first_line = input_file.readline()
data = first_line[0:-2].split(DELIMITER)

varNameDict = {}
for index, term in enumerate(data):
    varNameDict[term[1:-1]] = index


def isNotBlank(field_name):
    # Empty field

    if data[varNameDict[field_name]] == "":
        return False
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

count = 0

for line in input_file.read().split("\r\n"):
    data = line[0:-2].split(DELIMITER)

    if len(data) == 1:
        # Done with last line
        break

    img = Image()
    if isNotBlank('file_name'):
        img.file.name = 'images/' + getFieldValue('file_name')
    if isNotBlank('title'):
        img.title = getFieldValue('title')

    if isNotBlank('description'):
        img.description = getFieldValue('description')

    img.width = getIntFieldValue('width')
    img.height = getIntFieldValue('height')
    if isNotBlank('creator'):
        img.creator = getFieldValue('creator')
    if isNotBlank('language'):
        img.language = getFieldValue('language')
    if isNotBlank('source'):
        img.source = getFieldValue('source')

    if getFieldValue('ready_to_go') == "t":
        img.ready_to_go = True
    else:
        img.ready_to_go = False

    img.order_num = getIntFieldValue('order_num')
    if isNotBlank('category'):
        img.category = ImageCategory.objects.filter(value=getIntFieldValue('category'))[0]

    img.date = getIntFieldValue('date')

    img.save()
