from __future__ import print_function, unicode_literals

from builtins import input, next, str

from django.core.management.base import BaseCommand
from django.db import connection
from django.db import transaction
from django.utils.encoding import smart_str
import csv
import os
import time
from voyages.apps.voyage.models import (AfricanInfo, BroadRegion, CargoType, CargoUnit, LinkedVoyages,
										Nationality, OwnerOutcome,
										ParticularOutcome, Place, Region,
										Resistance, RigOfVessel, SlavesOutcome,
										TonType, VesselCapturedOutcome, Voyage,
										VoyageCaptain, VoyageCaptainConnection, VoyageCargoConnection,
										VoyageCrew, VoyageDates,
										VoyageGroupings, VoyageItinerary,
										VoyageOutcome, VoyageShip,
										VoyageShipOwner,
										VoyageShipOwnerConnection,
										VoyageSlavesNumbers, VoyageSources,
										VoyageSourcesConnection)

class Command(BaseCommand):

	def handle(self, *args, **options):
		
		basedir='voyages/apps/voyage/management/commands/oct_2023_georecode'
		
		fname='1_update_broad_regions.tsv'
		print("--->",fname)
		with open(os.path.join(basedir,fname),encoding='utf-8') as csvfile:
			reader=csv.DictReader(csvfile,delimiter='\t')
			for row in reader:
				print(row)
				br=BroadRegion.objects.get(value=row['Old Code'])
				br.value=int(row['New Code'])
				br.save()
				print(br)
		
		fname='2_create_broad_regions.tsv'
		print("--->",fname)
		with open(os.path.join(basedir,fname),encoding='utf-8') as csvfile:
			reader=csv.DictReader(csvfile,delimiter='\t')
			for row in reader:
				print(row)
				br=BroadRegion.objects.create(
					value=int(row['New Code']),
					broad_region=row['Name']
				)
				br.save()
				print(br)

		fname='3_recode_other_regions.tsv'
		print("--->",fname)
		with open(os.path.join(basedir,fname),encoding='utf-8') as csvfile:
			reader=csv.DictReader(csvfile,delimiter='\t')
			for row in reader:
				print(row)
				reg=Region.objects.get(value=row['Old Code'])
				reg.value=int(row['New Code'])
				reg.region=row['Name']
				reg.save()
				print(reg)
		
		fname='4_delete_region_philippenes.tsv'
		print("--->",fname)
		with open(os.path.join(basedir,fname),encoding='utf-8') as csvfile:
			reader=csv.DictReader(csvfile,delimiter='\t')
			for row in reader:
				print(row)
				reg=Region.objects.get(value=row['Old Code'])
				reg.delete()

		fname='5_create_regions.tsv'
		print("--->",fname)
		with open(os.path.join(basedir,fname),encoding='utf-8') as csvfile:
			reader=csv.DictReader(csvfile,delimiter='\t')
			for row in reader:
				print(row)
				broad_region=BroadRegion.objects.get(broad_region=row['Parent Name'])
				reg=Region.objects.create(
					region=row['Name'],
					value=int(row['New Code']),
					broad_region=broad_region
				)
				reg.save()
				print(reg)

		fname='6_temp_place_recode.tsv'
		print("--->",fname)
		with open(os.path.join(basedir,fname),encoding='utf-8') as csvfile:
			reader=csv.DictReader(csvfile,delimiter='\t')
			for row in reader:
				print(row)
				place=Place.objects.get(value=row['Old Code'])
				place.value=int(row['New Code'])
				place.save()
				print(place)

		fname='7_rename_and_recode_regions.tsv'
		print("--->",fname)
		with open(os.path.join(basedir,fname),encoding='utf-8') as csvfile:
			reader=csv.DictReader(csvfile,delimiter='\t')
			for row in reader:
				print(row)
				reg=Region.objects.get(value=row['Old Code'])
				parent=BroadRegion.objects.get(broad_region=row['Parent Name'])
				reg.value=int(row['New Code'])
				reg.region=row['Name']
				reg.broad_region=parent
				reg.save()
				print(reg)

		fname='8_change_place_name_code_parent.tsv'
		print("--->",fname)
		with open(os.path.join(basedir,fname),encoding='utf-8') as csvfile:
			reader=csv.DictReader(csvfile,delimiter='\t')
			for row in reader:
				print(row)
				place=Place.objects.get(value=row['Old Code'])
				parent_region=Region.objects.get(region=row['Parent Name'])
				place.value=int(row['New Code'])
				place.place=row['Name']
				place.region=parent_region
				place.save()
				print(place,parent_region)

# 		fname='9_PLACE_MERGES.tsv'
# 		print("--->",fname)
# 		with open(os.path.join(basedir,fname),encoding='utf-8') as csvfile:
# 			reader=csv.DictReader(csvfile,delimiter='\t')
# 			for row in reader:
# 				print(row)

		time.sleep(5)
		fname='10_UNUSED_PLACE_DELETION.tsv'
		print("--->",fname)
		with open(os.path.join(basedir,fname),encoding='utf-8') as csvfile:
			reader=csv.DictReader(csvfile,delimiter='\t')
			for row in reader:
				print(row)
				place=Place.objects.get(value=row['Old Code'])
				place.delete()
		
		
		fname='11_create_places.tsv'
		print("--->",fname)
		with open(os.path.join(basedir,fname),encoding='utf-8') as csvfile:
			reader=csv.DictReader(csvfile,delimiter='\t')
			for row in reader:
				print(row)
				parent_region=Region.objects.get(region=row['Parent Name'])
				place,place_isnew=Place.objects.get_or_create(
					place=row['Name'],
					value=row['New Code'],
					region=parent_region
				)
				place.save()
				print(place,parent_region)

