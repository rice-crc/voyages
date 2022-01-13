from tkinter import Spinbox
from django.core.management.base import BaseCommand
from django.db import connection
from django.db import transaction
from django.utils.encoding import smart_str
from voyages.apps.common.models import year_mod

from voyages.apps.common.utils import *
from voyages.apps.past.models import EnslavementRelation, EnslavementRelationType, EnslaverAlias, EnslaverIdentity, EnslaverIdentitySourceConnection, EnslaverInRelation, EnslaverRole, EnslaverVoyageConnection
from voyages.apps.voyage.models import Place, Voyage
import re

class Command(BaseCommand):
    help = ('Imports CSV files with the full Enslaver data-set and converts the data '
            'to the Django models.')

    def add_arguments(self, parser):
        parser.add_argument('enslaver_csv_files', nargs='+')
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
        MONTHS = ["Ja", "F", "Mar", "Ap", "May", "Jun", "Jul", "Au", "S", "O", "N", "D"]
        MAX_NAME_CHARS = 255
        MAX_WILL_FIELDS_CHARS = 100
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
        all_enslavers = {} # principal name : string => (enslaver: EnslaverIdentity, principal_alias: EnslaverAlias)
        aliases = []
        enslaver_voyage_conn = []
        source_connections = []
        enslavement_relations = [] # (rel: EnslavementRelation, enslaved: EnslavedInRelation[], enslavers: EnslaverInRelation[])
        marriage_relation_type = EnslavementRelationType.objects.get(name='Marriage')

        def fatal_error(msg):
            error_reporting.report(msg)
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
                re.sub("^c?\.?\s*", "", val)
                try:
                    return int(val)
                except:
                    error_reporting.report("Could not parse year: " + val)
            return None

        def parse_day_and_month(val):
            month = None
            day = None
            if val is not None and val != "":
                match = re.match("^(\d+)[-/]([\w]+)", val)
                if match:
                    day = int(match[1])
                    for i in range(0, 12):
                        if match[2].upper().startswith(MONTHS[i]):
                            month = i + 1
                            break
                    if month is None:
                        error_reporting.report("Could not parse month: " + val)
                else:
                    error_reporting.report("Could not parse date: " + val)
            return (day, month)

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
                    for voyage_id in [int(x) for x in rh.get('voyage list').replace('V_').split(':')]:
                        voyage = Voyage.all_dataset_objects.get(pk=int(voyage_id))
                        if voyage is None:
                            fatal_error("Voyage id not found: " + str(voyage_id))
                        voyage_list.append(voyage)
                    if len(voyage_list) == 0:
                        fatal_error("No voyages associated with enslaver")
                    # TODO Q: how should we represent composite roles?
                    # Our initial approach of using flags might make more sense.
                    role = rh.get_by_value(EnslaverRole, "role", "name", allow_null=False)
                    principal_alias = clean_name(rh.get('fullname', max_chars=MAX_NAME_CHARS))
                    if principal_alias in all_enslavers:
                        fatal_error("Duplicate principal alias: " + principal_alias)
                    enslaver = EnslaverIdentity()
                    aliases = {principal_alias}
                    for i in range(1, 9):
                        alias_value = rh.get("alias" + "{:02d}".format(i), max_chars=MAX_NAME_CHARS)
                        if alias_value is not None and alias_value != "":
                            aliases.add(alias_value)
                    e_principal = None
                    for alias in aliases:
                        e_alias = EnslaverAlias()
                        e_alias.alias = alias
                        e_alias.identity = enslaver
                        aliases.append(e_alias)
                        if alias == principal_alias:
                            e_principal = e_alias
                    all_enslavers[principal_alias] = (enslaver, e_principal)
                    # Link voyages to the principal alias.
                    for voyage in voyage_list:
                        conn = EnslaverVoyageConnection()
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
                    # TODO Q: should we make birth place a FK?
                    # enslaver.birth_place = rh.get_by_value(Place, "birth place", "place")
                    # TODO Q: sheet's NOTE field goes where??
                    # Parse sources associated with this enslaver.
                    order = 1
                    for key in get_multi_valued_column_suffix(6):
                        source_ref = rh.get('source' + key)
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
                        source_connection = EnslaverIdentitySourceConnection()
                        source_connection.identity = enslaver
                        source_connection.source = source
                        source_connection.source_order = order
                        source_connection.text_ref = source_ref
                        source_connections.append(source_connection)
                        order += 1
                    # Include spouses in the enslaver table.
                    # TODO Q: should we have separate EnslavementRelationType(s) for
                    # first and second marrriages or just a single "Marriage" type?                    
                    def add_spouse(spouse, date):
                        if spouse:
                            # Check if there is already that person in the enslavers record.
                            existing = all_enslavers.get(spouse)
                            if existing is None:
                                spouse_ens = EnslaverIdentity()
                                spouse_ens_alias = EnslaverAlias()
                                spouse_ens_alias.identity = spouse_ens
                                spouse_ens_alias.alias = spouse
                                spouse_ens.principal_alias = spouse
                            else:
                                (spouse_ens, spouse_ens_alias) = existing
                            marriage = EnslavementRelation()
                            marriage.relation_type = marriage_relation_type
                            try:
                                year_match = re.match("[0-9]{4}", date)
                                marriage.date = ',,' + year_match[0]
                            except:
                                pass
                            in_relation_a = EnslaverInRelation()
                            in_relation_a.relation = marriage
                            in_relation_a.enslaver_alias = e_principal
                            in_relation_a.role = spouse_role
                            in_relation_b = EnslaverInRelation()
                            in_relation_b.relation = marriage
                            in_relation_b.enslaver_alias = spouse_ens_alias
                            in_relation_b.role = spouse_role
                            enslavement_relations.append((marriage, [], []))

                    add_spouse(clean_name(rh.get('s1 name')), rh.get('s1 marriage date'))
                    add_spouse(clean_name(rh.get('s2 name')), rh.get('s2 marriage date'))
