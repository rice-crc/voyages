from bs4 import BeautifulSoup

import csv

#this one creates the footer block from idx.csv
#it depends on the row & column fields being filled in (as integers)
###but only for those logos that the user wants to have appear in the footer
#and the other hard-coded variables taken from logo_idx.py having values:
### url, orgname, width, height

csvfile = csv.DictReader(open("idx.csv"))

grid={}

for entry in csvfile:
	if 'row' in entry:
		gridrow=entry['row']
		gridcol=int(entry['col'])
	
		if row not in grid:
			grid[gridrow]={col:entry}
		else:
			#just in case the user gives the same column idx to two items in the same row,
			#dodge that entry
			if col in grid[gridrow]:
				col +=1
			grid[gridrow][col]=entry

soup = BeautifulSoup("<div class=\"logo-grid-container\" id=\"LGC\"> <\div>")

for row in grid:
	soup.append("<div class=\"logo-grid\" id=\"%s\"> </div>" %str(row) )
	for entry in row:
		url=entry['url']
		organization=entry['organization']
		width=entry['recommendedwidth']
		height=entry['recommendedheight']
		entrysoup=BeautifulSoup("<a href=\"%s\" target=\"_blank\" rel=\"noopener\" alt=\"Omohundro Institute\"> <div class=\"logo-grid-item fade-in\" style=\"width: %s;height:%s\"> <img class=\"card-img sponsor-card-img block lazy\" data-src=\"{{ STATIC_URL }}images/site/logos/%\" alt=\"%s\" > </div> </a>" %(url,organization,width,height))
		soup['div'][str(row)].append(entrysoup)

print(soup.prettify())

#then write it to an html file once the above output is looking good.