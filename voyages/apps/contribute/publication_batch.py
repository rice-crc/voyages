from __future__ import print_function, unicode_literals

# This is a script file to run a full db backup and publication script.
import os
import sys

import django

from voyages.apps.contribute.publication import publish_accepted_contributions

sys.path.append('/home/domingos/Documents/projects/voyages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'voyages.settings'
django.setup()

if len(sys.argv) <= 1:
    print("Pass the filename of output log as argument")
    sys.exit()

f = open(sys.argv[1], 'w')
f.write('Starting publication script.\n')
publish_accepted_contributions(f)

f.close()
