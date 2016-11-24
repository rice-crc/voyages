# This is a script file to run a full db backup and publication script.
import os, sys
import django
from django.conf import settings

sys.path.append('/home/domingos/Documents/projects/voyages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'voyages.settings'
django.setup()

from voyages.apps.contribute.publication import publish_accepted_contributions

if len(sys.argv) <= 1:
    print "Pass the filename of output log as argument"
    exit()

f = open(sys.argv[1], 'w')
f.write('Starting publication script.\n')
f.write('Backing up all data.\n')

# Step 1 - Backup database
#os.system('python manage.py dumpdata > /var/tmp/db.json')

f.write('Finished backup.\n')
f.write('Publishing accepted contributions...\n')
publish_accepted_contributions(f)

f.close()