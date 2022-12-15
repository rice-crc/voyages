from voyages.apps.past.models import Enslaved,LanguageGroup,ModernCountry
from voyages.apps.common.utils import *
import csv
from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):


	def handle(self, *args, **options):

		# Before running this you should follow the instructions in ./languagegroups/importnotes.md
	
		#first we create the new language groups & tie them to their modern countries
		with open('voyages/apps/past/management/commands/languagegroups/final_languages.tsv', newline='\n', encoding='utf-8') as csvfile:
			reader = csv.DictReader(csvfile,delimiter='\t')
			for row in reader:
				colnames=['ID','AfricLangGroup','Lat','Long','ModernCountry']
				print(row)
			
				id=row['ID']
				name=row['NAME']
				longitude=row['LONG']
				latitude=row['LAT']			
			
				if longitude=='':
					longitude=None
				if latitude=='':
					latitude=None
			
				print(id,name,longitude,latitude)
			
				newlanguage=LanguageGroup.objects.create(
					id=id,
					name=name,
					longitude=longitude,
					latitude=latitude
				)
			
				newlanguage.save()
			
				countrycodes=row['COUNTRYCODE'].split(',')
				
				for countrycode in countrycodes:
					#if a modern country doesn't exist, create a blank entry and raise a warning
					try:
						country=ModernCountry.objects.get(pk=countrycode)
					except:
						country=ModernCountry.objects.create(id=countrycode,name='',latitude=0.0,longitude=0.0)
						print("--->created new blank modern country with id=",countrycode)
				
					country.languages.add(newlanguage)
			
					country.save()
	
		#then we attach the individuals who have languagegroup id's to those, as created above
	
		#substituting merged language groups
		languagegroupmap={160273:160272,160524:160523,160525:160523,560601:160499}
	
		with open('voyages/apps/past/management/commands/languagegroups/people_to_languagegroups.tsv', newline='\n', encoding='utf-8') as csvfile:
			reader = csv.DictReader(csvfile,delimiter='\t')
			for row in reader:
				colnames=['enslaved_id','language_group_id']
			
				enslaved_id=row['enslaved_id']
				language_group_id=row['language_group_id']
			
				if language_group_id != '':
				
					enslaved_id=int(enslaved_id)
					language_group_id=int(language_group_id)
				
					print(enslaved_id,language_group_id)
				
					if language_group_id in languagegroupmap:
						language_group_id=languagegroupmap[language_group_id]
						print("subbed-->",language_group_id)
				
					enslaved=Enslaved.objects.get(pk=enslaved_id)
					language_group=LanguageGroup.objects.get(pk=language_group_id)
				
					enslaved.language_group=language_group
					enslaved.save()