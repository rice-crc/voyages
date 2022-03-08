## importing new voyages

Adding this on Jan 11, 2021 as I don't think it's been properly documented before.

To bulk import new voyages, do the following:

1. Ensure you have your csv-formatted SPSS export ready
1. Secure a fresh database dump from production
1. Load that db into your test server
	1. can be local
	1. does not need to be reindexed
1. Export a csv of all the voyages from this test server
	1. Log into your test server's editorial platform 
	1. Navigate to 'contribute': https://www.slavevoyages.org/contribute/editor_main
	1. Click the "Download Voyages" menu option
	1. Download, with the following options checked:
		1. Only select "published"
		1. Choose "both" voyage datsets
		1. Don't check the "remove line breaks" option
1. Once you have this csv, create a temp folder in your test server: voyage/apps/voyage/tmp
	1. Place your new csv dump file and your spss export csv file in here
1. Log into your django app container like ```docker exec -it voyages-django /bin/bash```
1. In your django app container, kick off the export with ```python3 manage.py importcsv tmp/SITE_DUMP_FILENAME.csv tmp/SPSS_EXPORT_FILENAME.csv```
1. Now run your reindex and see how it looks!