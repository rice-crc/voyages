from __future__ import print_function, unicode_literals

# Import models that will be used in this import script.
from builtins import input, str

from django.core.management.base import BaseCommand
from django.db import transaction
from unidecode import unidecode
import unicodecsv

from voyages.apps.resources.models import AfricanName, Country, SexAge
from voyages.apps.voyage.models import Place, Voyage

# Script to import AfricanNames csv
# NOTE: the CSV must be UTF-8 without a BOM prefix otherwise
# the csv reader might choke on it. Use dos2unix utility to
# ensure that the file is kosher.


class Command(BaseCommand):
    help = 'Imports a CSV file with African Names into the database.'

    def add_arguments(self, parser):
        parser.add_argument('csv_path')

    def __init__(self, *args, **kwargs):
        self.next_country_id = -1000000
        super().__init__(*args, **kwargs)

    def handle(self, csv_path, *args, **options):

        def fuzzy_name(name):
            return unidecode(name).lower().replace(' ', '').replace(',', '')

        voyage_ids = set(Voyage.objects.values_list('voyage_id', flat=True))
        names = {a.slave_id: a for a in AfricanName.objects.all()}
        sas = {s.name: s.sex_age_id for s in SexAge.objects.all()}
        countries = {fuzzy_name(c.name): c for c in Country.objects.all()}
        places = {fuzzy_name(p.place): p.value for p in Place.objects.all()}
        insert = []
        self.next_country_id = 1 + \
            max([c.country_id for c in list(countries.values())])

        def add_blank(d):
            d[''] = None
            d[' '] = None

        add_blank(countries)
        add_blank(sas)
        add_blank(places)

        def get_fuzzy(d, name, source, throws):
            original = name
            name = fuzzy_name(name)
            x = d.get(name)
            if x is None and len(name) > 0:
                # Search for exact prefix match.
                namelen = len(name)
                for k, v in list(d.items()):
                    length = min(len(k), namelen)
                    if k[0:length] == name[0:length]:
                        if x is not None:
                            # Duplicate prefix match... let us quit the search.
                            x = None
                            break
                        x = v
                # Update dict so that the next lookup is very fast.
                if x:
                    d[name] = x
            if throws and x is None and len(name) > 0:
                raise Exception(source + ' not found: "' + original + '"')
            return x

        def get_country(name):
            c = get_fuzzy(countries, name, 'Country', False)
            if not c:
                key = fuzzy_name(name)
                if len(key) > 0:
                    # We should create a new Country record.
                    c = Country()
                    c.name = name
                    c.country_id = self.next_country_id
                    insert.append(c)
                    countries[key] = c
                    self.next_country_id += 1
            return c

        def get_place_id(name):
            return get_fuzzy(places, name, 'Port', True)

        def is_blank(s):
            return len(s.strip()) == 0

        updated = []
        missing_voyage_ids = []
        errors = {}
        with open(csv_path) as csvfile:
            reader = unicodecsv.DictReader(csvfile)
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
                    voyage_id = int(r['Voyage ID'])
                    a.name = r['Name']
                    a.voyage_number = voyage_id
                    a.age = None if is_blank(
                        r['Age']) else int(float(r['Age']))
                    a.height = None if is_blank(r['Height (in)']) else float(
                        r['Height (in)'])
                    a.ship_name = r['Ship name']
                    a.date_arrived = r['Arrival']
                    a.source = None  # Missing field in CSV??
                    # Now we map Foreign Keys.
                    # Country is set as an object as it might be a new model.
                    a.country = get_country(r['Country of Origin'])
                    if voyage_id in voyage_ids:
                        a.voyage_id = voyage_id
                    else:
                        missing_voyage_ids.append(voyage_id)
                    a.sex_age_id = sas[r['Sexage']]
                    a.embarkation_port_id = get_place_id(r['Embarkation'])
                    a.disembarkation_port_id = get_place_id(
                        r['Disembarkation'])
                except Exception as e:
                    errors.setdefault(str(e), []).append((count, r))

        if errors:
            # Display a summary of errors.
            for e, l in list(errors.items()):
                failed = str([x[0] for x in l[0:3]])
                if len(l) > 3:
                    failed += ' plus ' + str(len(l) - 3) + ' other rows'
                print(e + ": " + failed)
        else:
            # At this point any remaining elements in names is no longer
            # present in the CSV so we might delete them.
            delete = len(names) > 0 and input(
                'Delete pre-existing records '
                '(' + str(len(names)) + ')'
                ' without a match in the CSV? (y/N) ').lower() == 'y'

            if len(insert) > 0:
                ans = input(
                    'There are ' + str(len(insert)) + ' country names '
                    'to insert. Continue? (y/N/q) ').lower()
                if ans == 'q':
                    print(sorted([c.name for c in insert]))
                    ans = input('Continue with insert? (y/N) ').lower()
                if ans != 'y':
                    return

            if len(missing_voyage_ids) > 0:
                ans = input(
                    'There are ' + str(len(missing_voyage_ids)) + ' voyage '
                    'IDs not found. Continue? (y/N/q) ').lower()
                if ans == 'q':
                    print(sorted(missing_voyage_ids))
                    ans = input('Continue with db transaction? (y/N) ').lower()
                if ans != 'y':
                    return

            # Run all DB changes in a single transaction.
            with transaction.atomic():
                if delete:
                    for item in list(names.values()):
                        item.delete()
                for c in insert:
                    c.save()
                for a in updated:
                    a.save()
            print(
                "Changes saved to the database, don't forget to run "
                "'manage.py update_index resources.AfricanNames --remove' "
                "to update Solr"
            )
