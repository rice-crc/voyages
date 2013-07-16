from voyages.apps.voyage.models import *

# Load the source csv to the database
count = 0
for voyageObj in Voyage.objects.all():
    count = count + 1
    print count

    ship_list = VoyageShip.objects.filter(voyage=voyageObj)
    if len(ship_list) >= 1:
        voyageObj.voyage_ship = ship_list[0]

    date_list = VoyageDates.objects.filter(voyage=voyageObj)
    if len(date_list) >= 1:
        voyageObj.voyage_dates = date_list[0]

    itin_list = VoyageItinerary.objects.filter(voyage=voyageObj)
    if len(itin_list) >= 1:
        voyageObj.voyage_itinerary = itin_list[0]

    slnumber_list = VoyageSlavesNumbers.objects.filter(voyage=voyageObj)
    if len(slnumber_list) >= 1:
        voyageObj.voyage_slaves_numbers = slnumber_list[0]

    crew_list = VoyageCrew.objects.filter(voyage=voyageObj)
    if len(crew_list) >= 1:
        voyageObj.voyage_crew = crew_list[0]

    voyageObj.save()