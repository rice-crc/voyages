from voyages.apps.voyage.models import Place, Region
import math
import unicodecsv

data = [(float(p.latitude), float(p.longitude), p.region_id) for p in Place.objects.all() if p.latitude and p.longitude]

regions = {r.pk: r for r in Region.objects.all()}

def norm(dx, dy):
    return math.sqrt(dx * dx + dy * dy)

def get_region(lat, lng):
    nearest = [t[1] for t in sorted([(norm(lat - x[0], lng - x[1]), x[2]) for x in data])[:10]]
    histogram = {}
    for region_id in nearest:
        histogram[region_id] = histogram.get(region_id, 0) + 1
    last = sorted([(v, k) for (k, v) in histogram.items()])[-1]
    return regions[last[1]]

def add_regions_to_csv(csv_in, csv_out):
    input_file = unicodecsv.DictReader(open(csv_in, 'rb'))
    rows = [r for r in input_file]
    our_cols = ['Region', 'RegionCode', 'MapView']
    columns = set()
    for row in rows:
        columns = columns.union(set(row.keys()))
        try:
            lat = float(row['Latitude'])
            lng = float(row['Longitude'])
            region = get_region(lat, lng)
            row['Region'] = region.region
            row['RegionCode'] = region.value
            row['MapView'] = "https://www.google.com/maps/@?api=1&map_action=map&center=" + str(lat) + "," + str(lng) + "&zoom=10"
        except:
            for k in our_cols:
                row[k] = ''
    columns = list(columns) + our_cols
    out_file = unicodecsv.DictWriter(open(csv_out, 'wb'), fieldnames=columns)
    out_file.writeheader()
    for row in rows:
        out_file.writerow(row)
    return rows

# PowerShell Script to fetch geo locations from Google Maps API.

# $key = "secret..."
# 
# $data = Import-Csv places.csv
# $places = $data.Place_Name | sort | uniq | Where-Object { $_.Length -gt 3 }
# 
# $data = $places | %{
# 	$geo = Invoke-WebRequest "https://maps.googleapis.com/maps/api/geocode/json?address=$($_)&key=$($key)" | ConvertFrom-Json
# 	if ($geo.results.Length -gt 0) {
# 		$m = $geo.results[0]
# 		$geo = @{ Original = $_; Match = $m.formatted_address; Latitude = $m.geometry.location.lat; Longitude = $m.geometry.location.lng; }
# 	} else {
# 		$geo = @{ Original = $_; Match = "None"; Latitude = ""; Longitude = ""; }
# 	}
# 	return New-Object pscustomobject -Property $geo
# }
#
# $data | Export-Csv "path"