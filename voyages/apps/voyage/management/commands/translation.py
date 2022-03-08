from __future__ import print_function, unicode_literals

from datetime import datetime

from django.core.management.base import BaseCommand

from voyages.apps.voyage.models import (OwnerOutcome, ParticularOutcome,
                                        Resistance, SlavesOutcome,
                                        VesselCapturedOutcome,
                                        VoyageSourcesType)


class Command(BaseCommand):
    help = 'Extract text from the database that needs to be translated.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fieldsets = {
            VoyageSourcesType: ['group_name'],
            ParticularOutcome: ['label'],
            SlavesOutcome: ['label'],
            VesselCapturedOutcome: ['label'],
            OwnerOutcome: ['label'],
            Resistance: ['label'],
        }

    def handle(self, *args, **options):
        data = []
        for k, fields in list(self.fieldsets.items()):
            for field in fields:
                data += k.objects.values_list(field, flat=True)
        data = sorted(set(data))
        # POT Header.
        print('# Auto-generated file based on entries in the voyage database')
        print('#')
        print('msgid ""')
        print('msgstr ""')
        print('"Project-Id-Version: slave-voyages.org\\n"')
        print('"POT-Creation-Date'
              ': ' + datetime.now().strftime("%Y-%m-%d %H:%M") + '\\n"')
        print('"PO-Revision-Date:'
              ' ' + datetime.now().strftime("%Y-%m-%d %H:%M") + '\\n"')
        print('"Last-Translator: ?\\n"')
        print('"Language-Team: Voyages\\n"')
        print('"MIME-Version: 1.0\\n"')
        print('"Content-Type: text/plain; charset=UTF-8\\n"')
        print('"Content-Transfer-Encoding: 8bit\\n"')
        for s in data:
            print('')
            print('msgid "' + s + '"')
            print('msgstr ""')
