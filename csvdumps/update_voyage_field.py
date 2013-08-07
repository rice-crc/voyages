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

    if count > 200:
        break;

    characteristic = voyageObj.voyage_slaves_numbers
    characteristic.imp_total_num_slaves_embarked = getIntFieldValue('slaximp')
    characteristic.imp_num_adult_embarked = getIntFieldValue('adlt1imp')
    characteristic.imp_num_children_embarked = getIntFieldValue('chil1imp')
    characteristic.imp_num_male_embarked = getIntFieldValue('male1imp')
    characteristic.imp_num_female_embarked = getIntFieldValue('feml1imp')
    characteristic.total_slaves_embarked_age_identified = getIntFieldValue('slavema1')
    characteristic.total_slaves_embarked_gender_identified = getIntFieldValue('slavemx1')

    characteristic.imp_adult_death_middle_passage = getIntFieldValue('adlt2imp')
    characteristic.imp_child_death_middle_passage = getIntFieldValue('chil2imp')
    characteristic.imp_male_death_middle_passage = getIntFieldValue('male2imp')
    characteristic.imp_female_death_middle_passage = getIntFieldValue('feml2imp')
    characteristic.imp_num_adult_landed = getIntFieldValue('adlt3imp')
    characteristic.imp_num_child_landed = getIntFieldValue('chil3imp')
    characteristic.imp_num_male_landed = getIntFieldValue('male3imp')
    characteristic.imp_num_female_landed = getIntFieldValue('feml3imp')
    characteristic.total_slaves_landed_age_identified = getIntFieldValue('slavema3')
    characteristic.total_slaves_landed_gender_identified = getIntFieldValue('slavemx3')
    characteristic.total_slaves_dept_or_arr_age_identified = getIntFieldValue('slavema7')
    characteristic.total_slaves_dept_or_arr_gender_identified = getIntFieldValue('slavemx7')
    characteristic.imp_slaves_embarked_for_mortality = getIntFieldValue('tslmtimp')

    characteristic.save()
