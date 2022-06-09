from voyages.apps.common.utils import BulkImportationHelper, Trie
from voyages.apps.voyage.models import Place, Region
from django.db import transaction
from unidecode import unidecode
import math
import unicodecsv

data = [(float(p.latitude), float(p.longitude), p.region_id) for p in Place.objects.all() if p.latitude and p.longitude]

regions = {r.pk: r for r in Region.objects.all()}

def norm(dx, dy):
    return math.sqrt(dx * dx + dy * dy)

def get_region(lat, lng):
    """
    Use a nearest neighbors search to match lat-lng's to existing regions.
    
    Note: the distance is computed with Euclidean norm which *is not* a precise
    calculation but should be good enough for this feature. Use Haversine if
    this becomes an issue.
    """
    NEAREST_COUNT = 10
    nearest = [t[1] for t in sorted([(norm(lat - x[0], lng - x[1]), x[2]) for x in data])[:NEAREST_COUNT]]
    histogram = {}
    for region_id in nearest:
        histogram[region_id] = histogram.get(region_id, 0) + 1
    last = sorted([(v, k) for (k, v) in histogram.items()])[-1]
    return regions[last[1]]

def add_regions_to_csv(csv_in, csv_out):
    """
    Produce a CSV file that includes automated region matching and includes a
    Map URL link for visualization of the geo coordinates.
    """
    input_file = unicodecsv.DictReader(open(csv_in, 'rb'))
    rows = [r for r in input_file]
    our_cols = ['CodeValue', 'ShowOnMap', 'Region', 'RegionCode', 'MapView']
    columns = set()
    places_trie = Trie()
    for place in Place.objects.select_related('region').all():
        places_trie.add(unidecode(place.place).lower() + '*', place)
    for row in rows:
        columns = columns.union(set(row.keys()))
        for k in our_cols:
            row[k] = ''
        try:
            # First check if the Matching name is an entry or near an existing
            # Place entry.
            lat = float(row['Latitude'])
            lng = float(row['Longitude'])
            match_place = places_trie.get(unidecode(row['Match']).lower())
            if match_place is None:
                region = get_region(lat, lng)
            else:
                row['Match'] = match_place.place
                row['CodeValue'] = match_place.value
                region = match_place.region
            row['Region'] = region.region
            row['RegionCode'] = region.value
            row['MapView'] = f"=HYPERLINK(\"https://www.google.com/maps/@?api=1&map_action=map&center=" + str(lat) + "," + str(lng) + "&zoom=10\")"
        except:
            pass
    columns = list(sorted(columns)) + our_cols
    out_file = unicodecsv.DictWriter(open(csv_out, 'wb'), fieldnames=columns)
    out_file.writeheader()
    for row in rows:
        out_file.writerow(row)
    return rows

def import_places_from_csv(csv, skip_errors=True):
    """
    Given a CSV produced by add_regions_to_csv (and manually edited), import the
    places into the database in bulk.

    Note: the CodeValue column must be filled with values that are unique among
    all places.
    """
    rows = BulkImportationHelper.read_to_dict(open(csv, 'rb'))
    places = {p.value: p for p in Place.objects.all()}
    regions = {r.value: r.pk for r in Region.objects.all()}
    skipped = []
    idx_row = 1
    updates = {}
    for row in rows:
        idx_row += 1
        place_name = row['match'].strip()
        if place_name == '':
            skipped.append((idx_row, "Empty place name"))
            continue
        try:
            place_code = int(row['codevalue'])
        except:
            skipped.append((idx_row, "Bad place code value"))
            continue
        if place_code in updates:
            # Only log an error if the place name is different.
            if place_name != updates[place_code].place:
                skipped.append((idx_row, "Duplicate place code value"))
            continue
        # TODO: validate place code?
        place = places.get(place_code, Place())
        place.place = place_name
        try:
            place.region_id = regions[int(row['regioncode'])]
        except:
            skipped.append((idx_row, "Region id not found"))
            continue
        try:
            place.longitude = float(row['longitude'])
            place.latitude = float(row['latitude'])
        except:
            skipped.append((idx_row, "Bad geo coordinates"))
            continue
        place.value = place_code
        show = row['showonmap'].lower() == 'true'
        place.show_on_main_map = show
        place.show_on_voyage_map = show
        updates[place_code] = place
    if len(skipped) == 0 or skip_errors:
        with transaction.atomic():
            for place in updates.values():
                place.save()
    if len(skipped) > 0:
        for row_num, error in skipped:
            print(f"[{row_num}]: {error}")
    return updates

# Run the functions above on a shell, invoked by, say:
# docker exec -i voyages-django bash -c 'python3 manage.py shell'
# from tools.automation.geo_utils import *
# add_regions_to_csv('tmp/work/places_google.csv', 'tmp/work/places_processed.csv')
#
# After the CSV has been manually edited and is ready for import, invoke
# import_places_from_csv('csv path')

# PowerShell Script to fetch geo locations from Google Maps API.

# # Set the API key to Google Maps
# $key = "secret..."
# 
# $data = Import-Csv tmp/work/places.csv
# $places = $data.Place_Name | sort | uniq | Where-Object { $_.Length -gt 3 }
# 
# # Allow excluding certain countries from the results.
# $exclusion = @('US', 'Canada')
# 
# function Get-AddressComponent($item, $type) {
# 	ForEach ($component in $item.address_components) {
# 		if ($component.types.contains($type)) {
# 			return $component
# 		}
# 	}
# 	return $null
# }
# 
# if (!$key) {
#    Write-Error "Don't forget to set the API key!"
# }
# $out = @()
# $places | ForEach-Object {
#	$pct = (100.0 * $out.Length) / $places.Length
#	Write-Progress -Activity "Fetching Places on Google API" -Status "Searching $($_)" -PercentComplete $pct
# 	$geo = Invoke-RestMethod -ContentType "application/json; charset=utf-8" "https://maps.googleapis.com/maps/api/geocode/json?address=$($_)&key=$($key)"
# 	$results = $geo.results
# 	if ($exclusion -and $results) {
# 		try {
# 			$results = @($results) | Where-Object { 
# 				$rcountry = Get-AddressComponent $_ 'country'
# 				return !$rcountry -or (!$exclusion.Contains($rcountry.long_name) -and !$exclusion.Contains($rcountry.short_name))
# 			}
# 		} catch {
# 			Write-Host $_
# 		}
# 	}
# 	if ($results.Length -gt 0) {
# 		$m = $results[0]
# 		$locality = Get-AddressComponent $m 'locality'
# 		if ($locality) {
# 			$locality = $locality.long_name
# 		}
# 		if (!$locality) {
# 			$locality = $m.formatted_address
# 		}
# 		$geo = @{ Original = $_; Match = $locality; Latitude = $m.geometry.location.lat; Longitude = $m.geometry.location.lng; }
# 	} else {
# 		$geo = @{ Original = $_; Match = ""; Latitude = ""; Longitude = ""; }
# 	}
# 	$out += @(New-Object pscustomobject -Property $geo)
# }
# 
# $out | Export-Csv "/tmp/places_google.csv"