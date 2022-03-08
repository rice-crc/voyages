
from django.core.management.base import BaseCommand
from django.db import connection
from django.db import transaction
from django.utils.encoding import smart_str

from voyages.apps.common.utils import *
from voyages.apps.past.models import CaptiveFate, CaptiveStatus, Enslaved, EnslavedSourceConnection, EnslaverAlias, LanguageGroup, RegisterCountry
from voyages.apps.voyage.models import Place, Voyage

class Command(BaseCommand):    
    help = ('Imports CSV files with the full PAST data-set and converts the data '
            'to the Django models. TODO: implement enslavers import!')

    def add_arguments(self, parser):
        parser.add_argument('enslaved_csv_files', nargs='+')
        parser.add_argument('--skip_invalid', dest='skip_invalid', default=False)
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
        skip_invalid = options.get('skip_invalid', False)
        if skip_invalid:
            print('WARNING: skipping invalid may produce an inconsistent importation')
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
                    v = rh.get_by_value(Voyage, 'voyageid', 'voyage_id', True, manager=Voyage.all_dataset_objects)
                    if v is None:
                        if skip_invalid:
                            # We need to skip this entry.
                            continue
                        abort_msg = 'Voyage id not found, aborting!'
                        error_reporting.report(abort_msg)
                        raise Exception(abort_msg)
                    enslaved = Enslaved()
                    enslaved.voyage = v
                    enslaved.enslaved_id = rh.cint('uniqueid')
                    dataset = rh.cint('dataset', allow_null=False)
                    enslaved.dataset = dataset
                    # This importation script handles datasets
                    # slightly different since the columns have
                    # context-dependent meaning.
                    MAX_CHARS = 100
                    if dataset == 0:
                        enslaved.documented_name = rh.get('africanname', max_chars=MAX_CHARS)
                        enslaved.name_first = rh.get('africanname2', max_chars=MAX_CHARS)
                        enslaved.name_second = rh.get('africanname3', max_chars=MAX_CHARS)
                        enslaved.modern_name = rh.get('modernafricanname', max_chars=MAX_CHARS)
                        enslaved.editor_modern_names_certainty = rh.cint('certainty')
                        enslaved.language_group = rh.get_by_value(LanguageGroup, 'africlanggroup', 'id')
                        enslaved.register_country = rh.get_by_value(RegisterCountry, 'africancountry', 'id')
                    elif dataset == 1:
                        enslaved.documented_name = rh.get('westernname', max_chars=MAX_CHARS)
                    else:
                        raise Exception('Unknown dataset ' + str(dataset))
                    enslaved.captive_fate = rh.get_by_value(CaptiveFate, 'captivefate', 'id')
                    enslaved.captive_status = rh.get_by_value(CaptiveStatus, 'captivestatus', 'id')
                    enslaved.age = rh.cint('age')
                    # Note: the gender/sex code from the CSV files has 1 -
                    # Female, 2 - Male, which is the opposite of our internal
                    # representation.
                    gender_code  = rh.cint('gender')
                    enslaved.gender = 1 if gender_code == 2 else (2 if gender_code == 1 else gender_code)
                    enslaved.height = rh.cfloat('height')
                    enslaved.skin_color = rh.get('skincolor', max_chars=MAX_CHARS)
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
                helper.delete_all(cursor, EnslavedSourceConnection)
                helper.bulk_insert(Enslaved, all_enslaved.values())
                helper.bulk_insert(EnslavedSourceConnection, source_connections)
                helper.re_enable_fks(cursor)
