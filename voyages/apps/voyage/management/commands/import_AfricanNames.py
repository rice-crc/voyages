# Script to import AfricanNames csv
# NOTE: the CSV must be UTF-8 without a BOM prefix otherwise
# the csv reader might choke on it. Use dos2unix utility to
# ensure that the file is kosher.

# Import models that will be used in this import script.
from django.core.management.base import BaseCommand
from django.db import transaction
from voyages.apps.resources.models import *
from voyages.apps.voyage.models import *
import csv

class Command(BaseCommand):
    help = 'Imports a CSV file with African Names into the database.'

    def add_arguments(self, parser):
        parser.add_argument('csv_path')

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, csv_path, *args, **options):
        def fuzzy_place_name(name):
            return name.lower().replace(' ', '').replace(',', '')

        names = {a.slave_id: a for a in AfricanName.objects.all()}
        sas = {s.name: s.sex_age_id for s in SexAge.objects.all()}
        countries = {fuzzy_place_name(c.name): c.country_id for c in Country.objects.all()}
        places = {fuzzy_place_name(p.place): p.value for p in Place.objects.all()}

        def add_blank(d):
            d[''] = None
            d[' '] = None

        add_blank(countries)
        add_blank(sas)
        add_blank(places)

        def get_fuzzy(d, name, source):
            original = name
            name = fuzzy_place_name(name)
            x = d.get(name)
            if not x:
                # Search for exact prefix match.
                namelen = len(name)
                for k, v in d.items():
                    length = min(len(k), namelen)
                    if k[0:length] == name[0:length]:
                        x = v
                        d[name] = v
                        break
            if not x and len(name): raise Exception(source + ' not found: "' + original + '"')
            return x

        def get_country(name):
            return get_fuzzy(countries, name, 'Country')

        def get_place(name):
            return get_fuzzy(places, name, 'Port')

        def is_blank(s):
            return len(s.strip()) == 0

        updated = []
        errors = {}
        with open(csv_path) as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for r in reader:
                pk = int(r['ID'])
                a = names.pop(pk, None) 
                if not a:
                    a = AfricanName()
                    a.slave_id = pk
                updated.append(a)
                # Fill fields of the record.
                count += 1
                try:
                    a.name = r['Name']
                    a.voyage_number = int(r['Voyage ID'])
                    a.age = None if is_blank(r['Age']) else int(float(r['Age']))
                    a.height = None if is_blank(r['Height (in)']) else float(r['Height (in)'])
                    a.ship_name = r['Ship name']
                    a.date_arrived = r['Arrival']
                    a.source = None # Missing field in CSV??
                    # Now we map Foreign Keys.
                    a.voyage_id = a.voyage_number # redundant field...
                    a.sex_age_id = sas[r['Sexage']]
                    a.country_id = get_country(r['Country of Origin'])
                    a.embarkation_port_id = get_place(r['Embarkation'])
                    a.disembarkation_port_id = get_place(r['Disembarkation'])
                except Exception as e:
                    errors.setdefault(e.message, []).append((count, r))

        if errors:
            # Display a summary of errors.
            for e, l in errors.items():
                failed = str([x[0] for x in l[0:3]])
                if len(l) > 3: failed += ' plus ' + str(len(l) - 3) + ' other rows'
                print(e + ": " + failed)
        else:
            # At this point any remaining elements in names is no longer present
            # in the CSV so we might delete them.
            delete = len(names) > 0 and raw_input('Delete pre-existing records without a match in the CSV? (y/N)').lower() == 'y'

            # Run all DB changes in a single transaction.
            with transaction.atomic():
                if delete:
                    for item in names.values():
                        item.delete()
                for a in updated:
                    a.save()
            print("Changes saved to the database, don't forget to run 'manage.py update_index resources.AfricanNames --remove' to update Solr")