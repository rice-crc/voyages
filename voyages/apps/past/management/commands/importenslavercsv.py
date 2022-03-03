from django.core.management.base import BaseCommand
from django.db import connection
from django.db import transaction
from django.utils.encoding import smart_str
from voyages.apps.common.models import year_mod

from voyages.apps.common.utils import *
from voyages.apps.past.models import EnslavedInRelation, EnslavementRelation, EnslavementRelationType, EnslaverAlias, EnslaverIdentity, EnslaverIdentitySourceConnection, EnslaverInRelation, EnslaverRole, EnslaverVoyageConnection
from voyages.apps.voyage.models import Place, Voyage
import re

class Command(BaseCommand):
    help = ('Imports CSV files with the full Enslaver data-set and converts the data '
            'to the Django models.')

    def add_arguments(self, parser):
        parser.add_argument('enslaver_csv_files', nargs='+')
        parser.add_argument('--skip_invalid', dest='skip_invalid', default=False)
        parser.add_argument('--start_pk', dest='start_pk', default=None)
        parser.add_argument(
            '--db',
            dest='db',
            default='mysql',
            help=('Specifies the DB backend so that the appropriate raw sql '
                  'is generated. Supported values: "mysql" and "pgsql"'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = 0

    def handle(self, enslaver_csv_files, *args, **options):
        # List the smallest unambiguous prefix of months in English so that we can parse
        MONTHS = ["JA", "F", "MAR", "AP", "MAY", "JUN", "JUL", "AUG", "S", "O", "N", "D"]
        MAX_NAME_CHARS = 255
        MAX_WILL_FIELDS_CHARS = 100
        self.errors = 0
        target_db = options.get('db')
        skip_invalid = options.get('skip_invalid', False)
        start_pk = options.get('start_pk')

        error_reporting = ErrorReporting()
        if target_db not in ('mysql', 'pgsql'):
            error_reporting.report(
                'Supported dbs are "mysql" and "pgsql". Aborting...')
            return
        print('Targetting db: ' + target_db)
        helper = BulkImportationHelper(target_db)
        source_finder = SourceReferenceFinder()
        print("Please ensure that all csv files are UTF8-BOM encoded")
        all_enslavers = {} # principal name : string => (enslaver: EnslaverIdentity, principal_alias: EnslaverAlias)
        all_aliases = []
        enslaver_voyage_conn = []
        source_connections = []
        enslavement_relations = [] # (rel: EnslavementRelation, enslaved: EnslavedInRelation[], enslavers: EnslaverInRelation[])
        marriage_relation_type = EnslavementRelationType.objects.get(name='Marriage')
        spouse_role = EnslaverRole.objects.get(name='Spouse')

        primary_keys = {}
        
        def create(model):
            key = primary_keys.get(model, start_pk)
            key = 1 if key is None else int(key)
            item = model()
            item.pk = key
            primary_keys[model] = key + 1
            return item

        def fatal_error(msg):
            error_reporting.report(msg)
            if not skip_invalid:
                raise Exception(msg)

        def clean_name(name):
            if name is None or name == '':
                return None
            # Remove any annotations (between parenthesis).
            name = re.sub("\(.*\)", "", name)
            # Remove trailing characters.
            name = re.sub("[,.\s]+$", "", name)
            return name if name != '' else None

        def parse_year(val):
            if val is not None and val != "":
                match = re.match(".*(\d{4}).*", val)
                if match:
                    return int(match[1])
                error_reporting.report("Could not parse year: " + val)
            return None
        
        def match_month(val):
            month = None
            for i in range(0, 12):
                if val.startswith(MONTHS[i]):
                    month = i + 1
                    break
            return month

        def parse_day_and_month(val):
            month = None
            day = None
            if val is not None and val != "":
                match = re.match("^(\d+)[-/]([\w]+)", val)
                if match:
                    day = int(match[1])
                    month = match_month(match[2].upper())
                    if month is None:
                        # If there is a day, then the month should be valid.
                        error_reporting.report("Could not parse month: " + val)
                else:
                    # Maybe we can match just the month.
                    match = re.match("^([\w]{3,})", val)
                    if match:
                        month = match_month(match[1].upper())
                    if month is None:
                        error_reporting.report("Could not parse date: " + val)
            return (day, month)

        def get_voyage_ids(val):
            if val is None or val == '':
                return []
            res = []
            for x in val.replace('V_', '').split(':'):
                try:
                    res.append(int(x))
                except:
                    fatal_error("Bad voyage id in: " + val)
            return res

        # Iterate through csv files and import them.
        for file in enslaver_csv_files:
            with open(file, 'rb') as f:
                reader = helper.read_to_dict(f)
                print("Importing " + file)
                error_reporting.reset_row()
                for r in reader:
                    rh = RowHelper(r, error_reporting)
                    # Start with the list of voyages associated with the enslaver.
                    voyage_list = []
                    for voyage_id in get_voyage_ids(rh.get('voyage list')):
                        try:
                            voyage = Voyage.all_dataset_objects.get(pk=int(voyage_id))
                        except:
                            voyage = None
                        if voyage is None:
                            fatal_error("Voyage id not found: " + str(voyage_id))
                        else:
                            voyage_list.append(voyage)
                    if len(voyage_list) == 0:
                        fatal_error("No voyages associated with enslaver")
                    # TODO Q: how should we represent composite roles?
                    # Our initial approach of using flags might make more sense.
                    role = rh.get_by_value(EnslaverRole, "role", "name", allow_null=False)
                    principal_alias = clean_name(rh.get('fullname', max_chars=MAX_NAME_CHARS))
                    if principal_alias in all_enslavers:
                        fatal_error("Duplicate principal alias: " + principal_alias)
                    enslaver = create(EnslaverIdentity)
                    aliases = {principal_alias}
                    for i in range(1, 9):
                        alias_value = clean_name(rh.get("alias" + "{:02d}".format(i), max_chars=MAX_NAME_CHARS))
                        if alias_value is not None and alias_value != "":
                            aliases.add(alias_value)
                    e_principal = None
                    for alias in aliases:
                        e_alias = create(EnslaverAlias)
                        e_alias.alias = alias
                        e_alias.identity = enslaver
                        all_aliases.append(e_alias)
                        if alias == principal_alias:
                            e_principal = e_alias
                    all_enslavers[principal_alias] = (enslaver, e_principal)
                    # Link voyages to the principal alias.
                    for voyage in voyage_list:
                        conn = create(EnslaverVoyageConnection)
                        conn.voyage = voyage
                        conn.role = role
                        conn.enslaver_alias = e_principal
                        # TODO Q: will order be used in this connection?
                        enslaver_voyage_conn.append(conn)
                    # Set enslaver personal info.
                    enslaver.principal_alias = principal_alias
                    enslaver.birth_year = parse_year(rh.get("birth year"))
                    (birth_day, birth_month) = parse_day_and_month(rh.get('birth date'))
                    enslaver.birth_day = birth_day
                    enslaver.birth_month = birth_month
                    enslaver.death_year = parse_year(rh.get("death year"))
                    (death_day, death_month) = parse_day_and_month(rh.get('death date'))
                    enslaver.death_day = death_day
                    enslaver.death_month = death_month
                    enslaver.father_name = clean_name(rh.get("father's name"))
                    enslaver.father_occupation = clean_name(rh.get("father's occupation"))
                    enslaver.mother_name = clean_name(rh.get("mother's name"))
                    enslaver.probate_date = rh.get("probate date", max_chars=MAX_WILL_FIELDS_CHARS)
                    enslaver.will_value_pounds = rh.get("will value lbs", max_chars=MAX_WILL_FIELDS_CHARS)
                    enslaver.will_value_dollars = rh.get("will value dollars", max_chars=MAX_WILL_FIELDS_CHARS)
                    enslaver.will_court = rh.get("will court/s", max_chars=MAX_WILL_FIELDS_CHARS)
                    enslaver.text_id = rh.get("## person id")
                    enslaver.birth_place = rh.get_by_value(Place, "birth place", "place")
                    enslaver.death_place = rh.get_by_value(Place, "death place", "place")
                    # TODO Q: sheet's NOTE field goes where??
                    # Parse sources associated with this enslaver.
                    order = 1
                    for key in get_multi_valued_column_suffix(6):
                        source_ref = rh.get('source ' + key, max_chars=MAX_NAME_CHARS)
                        if len(source_ref) > 200:
                            print('source [' + str(len(source_ref)) + ']: ')
                        if source_ref is None or empty.match(source_ref):
                            break
                        (source, match) = source_finder.get(source_ref)
                        if source is None:
                            self.errors += 1
                            error_reporting.report(
                                'Source not found for '
                                'ensaver: "' + principal_alias + '" '
                                'source_ref: '
                                '"' + smart_str(source_ref) + '"'
                                ', longest partial '
                                'match: ' + smart_str(match),
                                source_ref)
                            continue
                        source_connection = create(EnslaverIdentitySourceConnection)
                        source_connection.identity = enslaver
                        source_connection.source = source
                        source_connection.source_order = order
                        source_connection.text_ref = source_ref
                        source_connections.append(source_connection)
                        order += 1
                    # Include spouses in the enslaver table.               
                    def add_spouse(spouse, date):
                        if spouse:
                            # Check if there is already that person in the enslavers record.
                            existing = all_enslavers.get(spouse)
                            if existing is None:
                                spouse_ens = create(EnslaverIdentity)
                                spouse_ens_alias = create(EnslaverAlias)
                                spouse_ens_alias.identity = spouse_ens
                                spouse_ens_alias.alias = spouse
                                spouse_ens.principal_alias = spouse
                                all_aliases.append(spouse_ens_alias)
                                all_enslavers[spouse] = (spouse_ens, spouse_ens_alias)
                            else:
                                (spouse_ens, spouse_ens_alias) = existing
                            marriage = create(EnslavementRelation)
                            marriage.relation_type = marriage_relation_type
                            try:
                                year_match = re.match("[0-9]{4}", date)
                                marriage.date = ',,' + year_match[0]
                            except:
                                pass
                            in_relation_a = create(EnslaverInRelation)
                            in_relation_a.relation = marriage
                            in_relation_a.enslaver_alias = e_principal
                            in_relation_a.role = spouse_role
                            in_relation_b = create(EnslaverInRelation)
                            in_relation_b.relation = marriage
                            in_relation_b.enslaver_alias = spouse_ens_alias
                            in_relation_b.role = spouse_role
                            enslavement_relations.append((marriage, [], [in_relation_a, in_relation_b]))

                    add_spouse(clean_name(rh.get('s1 name')), rh.get('s1 marriage date'))
                    add_spouse(clean_name(rh.get('s2 name')), rh.get('s2 marriage date'))

        print('Constructed ' + str(len(all_enslavers)) + ' Enslavers from CSV.')

        if error_reporting.errors > 0:
            print(str(error_reporting.errors) + ' total errors reported!')

        confirm = input(
            "Are you sure you want to continue? "
            "The existing data will be deleted! (yes/[no]): "
        ).strip()
        print('"' + confirm + '"')
        if confirm != 'yes':
            for model_name, missing_keys in error_reporting.missing.items():
                print("Missing entries for " + str(model_name) + ":")
                for key in missing_keys:
                    print(key)
            return

        with transaction.atomic():
            with connection.cursor() as cursor:
                print('Deleting old data...')
                helper.disable_fks(cursor)
                helper.delete_all(cursor, EnslaverInRelation)
                helper.delete_all(cursor, EnslavedInRelation)
                helper.delete_all(cursor, EnslavementRelation)
                helper.delete_all(cursor, EnslaverVoyageConnection)
                helper.delete_all(cursor, EnslaverAlias)
                helper.delete_all(cursor, EnslaverIdentitySourceConnection)
                helper.delete_all(cursor, EnslaverIdentity)
                print('Inserting new enslaver records...')
                helper.bulk_insert(EnslaverIdentity, [eid for (eid, _) in all_enslavers.values()])
                helper.bulk_insert(EnslaverIdentitySourceConnection, source_connections)
                helper.bulk_insert(EnslaverAlias, all_aliases)
                helper.bulk_insert(EnslaverVoyageConnection, enslaver_voyage_conn)
                helper.bulk_insert(EnslavementRelation, [rel for (rel, _, _) in enslavement_relations])
                helper.bulk_insert(EnslavedInRelation, [enslaved_in_rel for (_, enslaved, _) in enslavement_relations for enslaved_in_rel in enslaved])
                helper.bulk_insert(EnslaverInRelation, [enslaver_in_rel for (_, _, enslaver) in enslavement_relations for enslaver_in_rel in enslaver])
                helper.re_enable_fks(cursor)

        print("Completed!")