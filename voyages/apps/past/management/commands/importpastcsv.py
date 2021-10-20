
from django.core.management.base import BaseCommand
from django.db import connection
from django.db import transaction
from django.utils.encoding import smart_str

from voyages.apps.common.utils import *
from voyages.apps.past.models import Enslaved, EnslavedSourceConnection, EnslaverAlias, LanguageGroup, RegisterCountry
from voyages.apps.voyage.models import Place, Voyage

class Command(BaseCommand):    
    help = ('Imports CSV files with the full PAST data-set and converts the data '
            'to the Django models. TODO: implement enslavers import!')

    def add_arguments(self, parser):
        parser.add_argument('enslaved_csv_files', nargs='+')
        parser.add_argument(
            '--db',
            dest='db',
            default='mysql',
            help=('Specifies the DB backend so that the appropriate raw sql '
                  'is generated. Supported values: "mysql" and "pgsql"'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = 0

    def handle(self, enslaved_csv_files, *args, **options):
        self.errors = 0
        target_db = options.get('db')
        error_reporting = ErrorReporting()
        if target_db not in ('mysql', 'pgsql'):
            error_reporting.report(
                'Supported dbs are "mysql" and "pgsql". Aborting...')
            return
        print('Targetting db: ' + target_db)
        helper = BulkImportationHelper(target_db)
        source_finder = SourceReferenceFinder()
        print("Please ensure that all csv files are UTF8-BOM encoded")
        # Store models that will be persistent in the following variables.
        all_enslaved = {}
        source_connections = []
        # Iterate through csv files and import them.
        for file in enslaved_csv_files:
            with open(file, 'rb') as f:
                reader = helper.read_to_dict(f)
                print("Importing " + file)
                error_reporting.reset_row()
                for r in reader:
                    rh = RowHelper(r, error_reporting)
                    enslaved = Enslaved()
                    enslaved.enslaved_id = rh.cint('uniqueid')
                    dataset = rh.cint('dataset')
                    enslaved.dataset = dataset
                    enslaved.voyage = rh.get_by_value(Voyage, 'voyageid', 'voyage_id', False, manager=Voyage.all_dataset_objects)
                    # This importation script handles datasets
                    # slightly different since the columns have
                    # context-dependent meaning.
                    if dataset == 0:
                        enslaved.documented_name = rh.get('africanname')
                        enslaved.name_first = rh.get('africanname2')
                        enslaved.name_second = rh.get('africanname3')
                        enslaved.modern_name = rh.get('modernafricanname')
                        enslaved.editor_modern_names_certainty = rh.cint('certainty')
                        enslaved.language_group = rh.get_by_value(LanguageGroup, 'africanlanguagegroup', 'id')
                        enslaved.register_country = rh.get_by_value(RegisterCountry, 'africancountry', 'id')
                    elif dataset == 1:
                        enslaved.documented_name = rh.get('westernname')
                    else:
                        raise Exception('Unknown dataset ' + str(dataset))
                    enslaved.age = rh.cint('age')
                    enslaved.gender = rh.cint('gender')
                    enslaved.height = rh.cfloat('height')
                    enslaved.skin_color = rh.cint('skincolor')
                    enslaved.notes = rh.get('notes')
                    enslaved.post_disembark_location = rh.get_by_value(Place, 'lastknownlocation')
                    all_enslaved[enslaved.enslaved_id] = enslaved
                    order = 1
                    for key in get_multi_valued_column_suffix(18):
                        source_ref = rh.get('source' + key)
                        if source_ref is None or empty.match(source_ref):
                            break
                        (source, match) = source_finder.get(source_ref)
                        if source is None:
                            self.errors += 1
                            error_reporting.report(
                                'Source not found for '
                                'ensaved id: ' + str(enslaved.enslaved_id) + ' '
                                'source_ref: '
                                '"' + smart_str(source_ref) + '"'
                                ', longest partial '
                                'match: ' + smart_str(match),
                                source_ref)
                            continue
                        source_connection = EnslavedSourceConnection()
                        source_connection.enslaved = enslaved
                        source_connection.source = source
                        source_connection.source_order = order
                        source_connection.text_ref = source_ref
                        source_connections.append(source_connection)
                        order += 1

        print('Constructed ' + str(len(all_enslaved)) + ' Enslaved from CSV.')

        if error_reporting.errors > 0:
            print(str(error_reporting.errors) + ' total errors reported!')

        confirm = input(
            "Are you sure you want to continue? "
            "The existing data will be deleted! (yes/[no]): "
        ).strip()
        print('"' + confirm + '"')
        if confirm != 'yes':
            return

        print('Deleting old data...')

        with transaction.atomic():
            with connection.cursor() as cursor:
                helper.disable_fks(cursor)
                helper.delete_all(cursor, Enslaved)
                helper.bulk_insert(Enslaved, all_enslaved.values())
                helper.re_enable_fks(cursor)
