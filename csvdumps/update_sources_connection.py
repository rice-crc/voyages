from voyages.apps.voyage.models import *
input_file = open('voyage_extra_voyage.txt', 'r')

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

listSources = VoyageSources.objects.all()
counter = 0

for line in input_file:
    data = line[0:-2].split(DELIMITER)

    if getFieldValue('suggestion') != "f" or getIntFieldValue('revision') != 1:
        continue

    counter += 1
    print counter

    voyageObj = Voyage.objects.get(voyage_id=getIntFieldValue('voyageid'))
    # Voyage sources
    # Potentially has a bug!!!!!!!!
    def findBestMachingSource(matchstring):
        # Base case if the string is too short
        if len(matchstring) <= 1:
            return None

        for source in listSources:
            if source.short_ref is None:
                continue
            if len(source.short_ref) < len(matchstring):
                continue
            #sourcestr = source.short_ref.decode('utf-8')
            sourcestr = source.short_ref

            if sourcestr.startswith(matchstring):
                return source

        # Find the best matching/contains the substring
        # : should be the last delimiter, then
        tmpPos = max(matchstring.rfind(':'), matchstring.rfind(","), matchstring.rfind("-"))
        if tmpPos > -1:
            return findBestMachingSource(matchstring[: tmpPos])
        else:
            return None

    def insertSource(fieldname, order):
        if isNotBlank(fieldname):
            to_be_matched = getFieldValue(fieldname).decode('utf-8')
            src = findBestMachingSource(to_be_matched)
            if src is not None:
                VoyageSourcesConnection.objects.create(source=src, source_order=order,
                                                       text_ref=getFieldValue(fieldname),
                                                       group=voyageObj)
                print "Found match"
            else :
                #print "No match found for %s" % getFieldValue(fieldname)
                VoyageSourcesConnection.objects.create(source_order=order,
                                                       text_ref=getFieldValue(fieldname),
                                                       group=voyageObj)
                print "Not found"

    # Alphabetical letters between a and r
    letters = map(chr, range(97, 97 + 18))
    for idx, letter in enumerate(letters):
        # Inserting sourcea, sourceb. .. sourcer
        insertSource('source' + letter, (idx + 1))

