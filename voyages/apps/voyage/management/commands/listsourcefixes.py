from django.core.management.base import BaseCommand, CommandError
import re
import openpyxl
class Command(BaseCommand):
    args = '<xlsx_file>'
    help = 'Takes data from a xlsx file about the problem sources and converts it to json'
    def handle(self, xlsx_file, *args, **options):
        wb = openpyxl.load_workbook(xlsx_file)
        ws = wb.active
        rows = ws.rows
        beginre = r'^[^"]*"'
        endre = r'"[^"]*$'
        res = {} # Result that maps from the incorrect text_ref to the correct text_ref
        for row in rows[2:]:
            orig = row[0].value
            repla = row[5].value
            corre = row[7].value
            if orig == None:
                break
            new = None
            rep = None
            reorig = re.sub(endre, '', re.sub(beginre, '', orig))
            if repla != '' and repla != None:
                new = repla
            else:
                new = corre

            if new == 'DELETE':
#                print("Deleting for " + repla + " and " + corre)
                rep = None
            elif new == '' or new == None:
                print("WARNING: No replacement for text_ref: " + reorig)
                continue
            else:
                rep = new
            res[reorig] = rep
#        print("hello")
        print(res)
                    

