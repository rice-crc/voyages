import os
import re
import sys

#get a quick csv of the image files formats and sizes.
###if the filenames are in the format INSTITUTION_NAME_COLORORWHITE_WIDTH_HEIGHT.FILTEYTPE
#### e.g. nmaahc_white_7510_3126.png

##it also adds an extra two columns: integer width/height according to dimensions of image.
##set the active variable below to an integer
##set the inactive to "None"
heightconstraint=100
widthconstraint=None

filetypes=['svg','png','gif','jpeg','jpg']
logo_fnames=[f for f in os.listdir('.') if re.search('(?<=\.)[^.]+$',f).group(0) in filetypes]

try:
	os.remove('idx.csv')
except:
	pass
d=open('idx.csv','a')

headers=['filename','filetype','reduced','color','organization','width','height','recommendedwidth','recommendedheight']
d.write(','.join(headers))
d.write('\n')

for fname in logo_fnames:
	print(fname)
	filetype=re.search('(?<=\.)[^.]+$',fname).group(0)
	reduced=fname[:len(fname)-len(filetype)-1]
	width_height=re.search('[0-9]+_[0-9]+',reduced).group(0)
	width,height=[int(i) for i in width_height.split('_')]
	reduced=reduced[:len(reduced)-len(width_height)-1]
	color=re.search('(?<=_).+?$',reduced).group(0)
	organization=reduced[:len(reduced)-len(color)-1]
	if heightconstraint==None and type(widthconstraint)==int:

		recommendedheight=int(widthconstraint*height/width)
		recommendedwidth=widthconstraint

	elif widthconstraint==None and type(heightconstraint)==int:
		recommendedwidth=int(heightconstraint*width/height)
		recommendedheight=heightconstraint
	else:
		recommendedheight=0
		recommendedwidth=0
	
	d.write(','.join([fname,filetype,reduced,color,organization,str(width),str(height),str(recommendedwidth),str(recommendedheight)]))
	d.write('\n')
d.close