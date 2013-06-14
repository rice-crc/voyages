#!/usr/bin/env python

import os
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # load test settings when running tests
        import voyages.testsettings as settings
        from django.core.management import execute_manager
        execute_manager(settings)
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voyages.settings")
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    
