from voyages.apps.voyage.models import *
input_file = open('source.txt', 'r')

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

##### End of Common section to all files #####

obj0 = VoyageSourcesType()
obj0.group_id = 0
obj0.group_name = 'Documentary source'
obj0.save()


obj1 = VoyageSourcesType()
obj1.group_id = 0
obj1.group_name = 'Newspaper'
obj1.save()

obj2 = VoyageSourcesType()
obj2.group_id = 1
obj2.group_name = 'Published source'
obj2.save()

obj3 = VoyageSourcesType()
obj3.group_id = 2
obj3.group_name = 'Unpublished secondary source'
obj3.save()

obj0 = VoyageSourcesType()
obj0.group_id = 3
obj0.group_name = 'Documentary source'
obj0.save()


obj4 = VoyageSourcesType()
obj4.group_id = 4
obj4.group_name = 'Private note or collection'
obj4.save()

counter = 0

for line in input_file:
    data = line[0:-2].split(DELIMITER)

    counter += 1

    source = VoyageSources.objects.get(pk=counter)
    if isNotBlank('type'):
        source.source_type = VoyageSourcesType.objects.get(group_id=getIntFieldValue('type'))

    source.save()
