from __future__ import print_function, unicode_literals

from builtins import range

import xlrd
from django.core.management.base import BaseCommand

from voyages.apps.voyage import models


class Command(BaseCommand):
    args = '<sources_xls>'
    help = 'Takes the sources from an xls file and puts it into the database'

    def handle(self, sources_xls, *args, **options):
        wb = xlrd.open_workbook(filename=sources_xls)
        sheet = wb.sheet_by_index(0)
        # iid => ignore
        # type => SourcesType group_id
        # id => short_ref
        # name => full_ref
        for i in range(4):
            if sheet.cell_value(0, i) == 'type':
                src_type_col = i
            elif sheet.cell_value(0, i) == 'id':
                short_ref_col = i
            elif sheet.cell_value(0, i) == 'name':
                full_ref_col = i
        idx = 1
        models.VoyageSources.objects.all().delete()
        while idx < sheet.nrows and sheet.cell_value(
                idx,
                full_ref_col) and sheet.cell_value(idx, full_ref_col) != '':
            short_ref = sheet.cell_value(idx, short_ref_col)
            full_ref = sheet.cell_value(idx, full_ref_col)
            src_type = models.VoyageSourcesType.objects.get(
                group_id=sheet.cell_value(idx, src_type_col))
            models.VoyageSources.objects.create(short_ref=short_ref,
                                                full_ref=full_ref,
                                                source_type=src_type)
            idx += 1
        print("Finished")
