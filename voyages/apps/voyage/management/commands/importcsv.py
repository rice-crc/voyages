from __future__ import print_function, unicode_literals

from builtins import input, next, str

from django.core.management.base import BaseCommand
from django.db import connection
from django.db import transaction
from django.db.models import F
from django.utils.encoding import smart_str
from voyages.apps.contribute.publication import CARGO_COLUMN_COUNT

from voyages.apps.voyage.models import (AfricanInfo, BroadRegion, CargoType, CargoUnit, LinkedVoyages,
                                        Nationality, OwnerOutcome,
                                        ParticularOutcome, Place, Region,
                                        Resistance, RigOfVessel, SlavesOutcome,
                                        TonType, VesselCapturedOutcome, Voyage,
                                        VoyageCaptain, VoyageCaptainConnection, VoyageCargoConnection,
                                        VoyageCrew, VoyageDates,
                                        VoyageGroupings, VoyageItinerary,
                                        VoyageOutcome, VoyageShip,
                                        VoyageShipOwner,
                                        VoyageShipOwnerConnection,
                                        VoyageSlavesNumbers, VoyageSources,
                                        VoyageSourcesConnection)
from voyages.apps.common.utils import *

import re

def _migrate_enslavers_from_legacy():
    from django.conf import settings
    if settings.VOYAGE_ENSLAVERS_MIGRATION_STAGE <= 1:
        # Not really necessary but it is convenient to reference the stage
        # settings variable so that we can later remove dead code paths once the
        # migration is finalized.
        return []
    # Try to match each Captain/Owner with an existing EnslaverAlias. If none
    # are found, we create the alias and the identity for it. In case of
    # duplicate identities with same alias already exist, check if one of them
    # is already associated with the existing voyage.
    from voyages.apps.past.models import EnslaverAlias, EnslaverIdentity, EnslaverVoyageConnection, VoyageCaptainOwnerHelper
    from unidecode import unidecode

    def clean_name(name):
        # Remove diacritics to increase the number of positive matches and put
        # everything in lower case.
        name = unidecode(name).lower()
        # Remove anything that is not a letter or space
        return re.sub(r'[^\w]', '', name)

    alias_to_identities = {} # Maps an alias (name) to the set of all identity ids
    identities_to_aliases = {} # Maps an identity id to all its aliases.
    connections = {} # Map an identity with all the voyages connected to one of its aliases.
    conn_fake_pk = 0
    voyage_data = {v['pk']: v for v in Voyage.all_dataset_objects \
                   .values('pk',
                           year=F('voyage_dates__imp_arrival_at_port_of_dis'),
                           ship_name=F('voyage_ship__ship_name'),
                           disembark=F('voyage_itinerary__imp_principal_port_slave_dis__region_id'))}
    for alias in EnslaverAlias.objects.all():
        name = clean_name(alias.alias)
        alias_to_identities.setdefault(name, set()).add(alias.identity_id)
        identities_to_aliases.setdefault(alias.identity_id, []).append((name, alias.pk))
        connections.setdefault(alias.identity_id, set())
    for conn in EnslaverVoyageConnection.objects.select_related().all():
        connections.setdefault(conn.enslaver_alias.identity_id, set()).add((conn.voyage_id, conn.role_id, conn.pk))

    non_natural_person_name_inc = ['company', 'compania', 'companhia', 'compagnie']
    def is_natural_person(name):
        for co_name in non_natural_person_name_inc:
            if co_name in name:
                return False
        return True

    def get_actions(name_and_voyages, role_ids):
        nonlocal conn_fake_pk
        migration_actions = []
        for name, voyage_id in name_and_voyages:
            decodedname = clean_name(name)
            natural_person = is_natural_person(decodedname)
            matches = alias_to_identities.get(decodedname)
            item = {
                'voyage_id': voyage_id,
                'name': name,
                'decodedname': decodedname,
                'reason': '',
                'steps': []
            }
            found = False
            if matches:
                good_match = None
                for identity_id in matches:
                    matching_with_voyage = [x for x in connections.get(identity_id, set()) if x[0] == voyage_id]
                    exact_role = any(x[1] in role_ids for x in matching_with_voyage)
                    if exact_role:
                        # Happy path! The appropriate voyage connection already
                        # exists for one of the identities with the given alias.
                        found = True
                        item['category'] = 1
                        item['reason'] = 'Exact match for voyage, enslaver alias, and role in ' + EnslaverVoyageConnection.__name__
                        break
                    if matching_with_voyage:
                        # A connection to the voyage already exists for this
                        # identity, but not with the same role, if we cannot
                        # find any better match (in another identity), then this
                        # is assumed to be the proper identity for the
                        # connection.
                        good_match = identity_id
                def get_voyage_year(v):
                    try:
                        return int(v['year'].replace(',', ''))
                    except:
                        return None
                if not found and len(matches) > 1 and not good_match:
                    # Our last chance to figure out a good match. We will use
                    # voyage associated to a candidate identity to match a year
                    # range and either ship name or disembarkation region.
                    current_voyage_data = voyage_data[voyage_id]
                    current_voyage_year = get_voyage_year(current_voyage_data)
                    if current_voyage_year:
                        MAX_YEAR_DIFF = 20
                        for iid in matches:
                            cluster = [voyage_data[vid] for (vid, _, _) in connections[iid]]
                            if natural_person:
                                # Only apply year heuristic if this is a natural
                                # person.
                                years = [y for y in [get_voyage_year(v) for v in cluster] if y]
                                if len(years) == 0:
                                    continue
                                max_year = max(years)
                                min_year = min(years)
                                if current_voyage_year < min(min_year, max_year - MAX_YEAR_DIFF) or \
                                        current_voyage_year > max(max_year, min(years) + MAX_YEAR_DIFF):
                                    continue
                            for field in ['ship_name', 'disembark']:
                                if current_voyage_data[field] in [v[field] for v in cluster]:
                                    good_match = iid
                                    break
                            if good_match:
                                break
                if not found:
                    if len(matches) == 1 or good_match:
                        # OK path
                        # We only need to create the connection for an existing alias.
                        match_alias_id = None
                        match_enslaver_id = good_match or next(matches.__iter__())
                        for alias_name, alias_id in identities_to_aliases[match_enslaver_id]:
                            if alias_name == decodedname:
                                match_alias_id = alias_id
                                break
                        if not match_alias_id:
                            raise Exception(f"Expected to find matching alias id: {identities_to_aliases[match_enslaver_id]} for '{decodedname}'")
                        item['reason'] = 'Found a single or "good" matching identity with the alias'
                        conn_fake_pk -= 1
                        item['steps'].append({
                            'type': EnslaverVoyageConnection.__name__,
                            'pk_ref': conn_fake_pk,
                            'values': {
                                'enslaver_alias_id': match_alias_id,
                                'voyage_id': voyage_id,
                                'role_id': role_ids[0]
                            }
                        })
                        # Store this in connections for future matches.
                        connections[match_enslaver_id].add((voyage_id, role_ids[0], conn_fake_pk))
                        # Treat this as a found alias.
                        found = True
                        item['category'] = 2
                    else:
                        # Not so good path. There are multiple identities
                        # maching this name and we could not determine for sure
                        # which is the right one.
                        item['category'] = 3
                        item['reason'] = 'Multiple identities containing the same alias'
            else:
                item['reason'] = 'No match found for enslaver alias'
                item['category'] = 4
            if not found:
                item['steps'].append({
                    'type': EnslaverIdentity.__name__,
                    'values': {
                        'principal_alias': name
                    }
                })
                next_id = -len(identities_to_aliases)
                item['steps'].append({
                    'type': EnslaverAlias.__name__,
                    'pk_ref': next_id,
                    'values': {
                        'alias': name
                    }
                })
                alias_to_identities.setdefault(decodedname, set()).add(next_id)
                identities_to_aliases[next_id] = [(decodedname, next_id)]
                conn_fake_pk -= 1
                connections[next_id] = {(voyage_id, role_ids[0], conn_fake_pk)}
                item['steps'].append({
                    'type': EnslaverVoyageConnection.__name__,
                    'pk_ref': conn_fake_pk,
                    'values': {
                        'enslaver_alias_id': next_id,
                        'voyage_id': voyage_id,
                        'role_id': role_ids[0]
                    }
                })
            migration_actions.append(item)
        return migration_actions

    helper = VoyageCaptainOwnerHelper()
    actions = get_actions(
        [[cc.captain.name, cc.voyage_id] for cc in \
            VoyageCaptainConnection.objects.select_related('captain').all()],
        helper.captain_role_ids
    )
    actions += get_actions(
        [[oc.owner.name, oc.voyage_id] for oc in \
            VoyageShipOwnerConnection.objects.select_related('owner').all()],
        helper.owner_role_ids
    )
    # Usage in django shell
    # from voyages.apps.voyage.management.commands import importcsv
    # actions = importcsv._migrate_enslavers_from_legacy()
    # by_reason = {}
    # for a in actions:
    #     by_reason.setdefault(a['reason'], []).append(a)
    # [(k, len(v)) for k, v in by_reason.items()]
    return actions


def _execute_migration_actions(actions, start_pk=None):
    from django.conf import settings
    if settings.VOYAGE_ENSLAVERS_MIGRATION_STAGE <= 1:
        # Not really necessary but it is convenient to reference the stage
        # settings variable so that we can later remove dead code paths once the
        # migration is finalized.
        return []    
    from voyages.apps.past.models import EnslaverAlias, EnslaverIdentity, EnslaverVoyageConnection
    
    def copy_values(source, target):
        for k, v in source.items():
            setattr(target, k, v)

    next_enslaver_identity_pk = start_pk
    next_enslaver_alias_pk = start_pk
    alias_pk_ref = {}
    with transaction.atomic():
        for item in actions:
            enslaver_identity_inserted_id = None
            enslaver_alias_inserted_id = None
            for step in item['steps']:
                if step['type'] == EnslaverIdentity.__name__:
                    eid = EnslaverIdentity()
                    copy_values(step['values'], eid)
                    if next_enslaver_identity_pk:
                        eid.pk = next_enslaver_identity_pk
                        next_enslaver_identity_pk += 1
                    eid.save()
                    enslaver_identity_inserted_id = eid.pk
                elif step['type'] == EnslaverAlias.__name__:
                    # We need the identity inserted first.
                    if enslaver_identity_inserted_id is None:
                        raise Exception("Unexpected step mode")
                    ealias = EnslaverAlias()
                    copy_values(step['values'], ealias)
                    ealias.identity_id = enslaver_identity_inserted_id
                    if next_enslaver_alias_pk:
                        ealias.pk = next_enslaver_alias_pk
                        next_enslaver_alias_pk += 1
                    ealias.save()
                    enslaver_alias_inserted_id = ealias.pk
                    alias_pk_ref[step['pk_ref']] = ealias.pk
                elif step['type'] == EnslaverVoyageConnection.__name__:
                    conn = EnslaverVoyageConnection()
                    copy_values(step['values'], conn)
                    if enslaver_alias_inserted_id:
                        conn.enslaver_alias_id = enslaver_alias_inserted_id
                    elif conn.enslaver_alias_id < 0:
                        conn.enslaver_alias_id = alias_pk_ref[conn.enslaver_alias_id]
                    conn.save()
                else:
                    raise Exception('Unexpected model type')

class Command(BaseCommand):
    help = ('Imports a CSV file with the full Voyages dataset and converts the data '
            'to the Django models.')

    def add_arguments(self, parser):
        parser.add_argument('csv_files', nargs='+')
        parser.add_argument(
            '--db',
            dest='db',
            default='mysql',
            help=('Specifies the DB backend so that the appropriate raw sql '
                  'is generated. Supported values: "mysql" and "pgsql"'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = 0

    def handle(self, csv_files, *args, **options):
        self.errors = 0
        target_db = options.get('db')
        error_reporting = ErrorReporting()
        if target_db not in ('mysql', 'pgsql'):
            error_reporting.report(
                'Supported dbs are "mysql" and "pgsql". Aborting...')
            return
        print('Targetting db: ' + target_db)

        # Store related models that need to be persisted in the following
        # lists/dicts
        voyages = {}
        captains = {}
        ship_owners = {}
        captain_connections = []
        ship_owner_connections = []
        source_connections = []
        afrinfo_conn = []
        cargo_conn = []
        crews = []
        itineraries = []
        outcomes = []
        ships = []
        voyage_dates = []
        voyage_numbers = []

        def check_hierarchy(voyage_id, field, place, region, broad_region):
            """
            Checks that the imported values match the geo database.
            """
            if place is not None:
                reg_pk = region.pk if region else None
                if place.region.pk != reg_pk:
                    error_reporting.report("Region mismatch for "
                                     "voyage_id " + str(voyage_id) + " on "
                                     "field '" + str(field) + "'")
                    self.errors += 1
                if reg_pk:
                    breg_pk = broad_region.pk if broad_region else None
                    if breg_pk != region.broad_region.pk:
                        error_reporting.report(
                            "Broad region mismatch for "
                            "voyage_id " + str(voyage_id) + " on "
                            "field '" + str(field) + "'")
                        self.errors += 1

        # Prefetch data: Sources
        source_finder = SourceReferenceFinder()

        def date_csv(var_name_prefix, suffixes=None):
            """
            Fetches date fields (day, month, year) and produce a CSV
            string in the format MM,DD,YYYY
            :param var_name_prefix: the variable name prefix
            :param suffixes: the day, month, and year suffixes, use None
            to specify that there is no variable corresponding to the
            date component.
            :return: the CSV date.
            """

            def get_component(suffix, expected_len):
                component = (rh.get(var_name_prefix + suffix, '')
                             if suffix is not None else '').strip()
                if expected_len == 2 and len(component) == 1:
                    component = '0' + component
                if len(component) != 0 and len(component) != expected_len:
                    self.errors += 1
                    error_reporting.report('Invalid date component length in: ' + component)
                    return ''
                return component
            if suffixes is None:
                suffixes = ['a', 'b', 'c']
            month = get_component(suffixes[1], 2)
            day = get_component(suffixes[0], 2) 
            year = get_component(suffixes[2], 4)
            return f"{month},{day},{year}" if month or day or year else ''

        def date_from_sep_values(value):
            """
            Converts a date with the format MM[sep]DD[sep]YYYY or
            YYYY[sep]MM[sep]DD--- where sep can be '-' or '/' or ','---into CSV
            format MM,DD,YYYY
            :param value: the formatted date
            :return: the CSV date
            """
            if value is None or empty.match(value):
                return ''
            components = value.split(',')
            if len(components) != 3:
                components = value.split('-')
            if len(components) != 3:
                components = value.split('/')
            if len(components) != 3:
                self.errors += 1
                error_reporting.report('Error with date ' + value)
                return ''
            
            def get_component_val(cval, min_value, max_value, mandatory):
                cval = cval.strip()
                if len(cval) > 0:
                    ival = int(cval)
                    if ival < min_value or ival > max_value:
                        raise Exception('Value outside range [' + str(min_value) + ', ' + str(max_value) + ']')
                    return ival
                if mandatory:
                    raise Exception('Missing mandatory date component')
                return ''

            try:
                coords = [2, 0, 1]
                if len(components[0].strip()) == 4:
                    # This date format starts with year, so we assume
                    # YYYY[sep]MM[sep]DD
                    coords = [0, 1, 2]
                day = get_component_val(components[coords[2]], 1, 31, False)
                month = get_component_val(components[coords[1]], 1, 12, bool(day))
                year = get_component_val(components[coords[0]], 999, 1900, bool(month))
                return f'{month},{day},{year}' if month or day or year else ''
            except Exception as e:
                self.errors += 1
                error_reporting.report('Invalid date "' + value + '" ' + str(e))
            return ''

        def row_to_ship(row, voyage):
            # Ship
            ship_model = VoyageShip()
            ship_model.ship_name = row.get('shipname')
            ship_model.nationality_ship = row.get_by_value(Nationality, 'national')
            ship_model.tonnage = row.cint('tonnage')
            ship_model.ton_type = row.get_by_value(TonType, 'tontype')
            ship_model.rig_of_vessel = row.get_by_value(RigOfVessel, 'rig')
            ship_model.guns_mounted = row.cint('guns')
            ship_model.year_of_construction = row.cint('yrcons')
            ship_model.vessel_construction_place = row.get_by_value(
                Place, 'placcons')
            ship_model.vessel_construction_region = row.get_by_value(
                Region, 'constreg')
            ship_model.registered_year = row.cint('yrreg')
            ship_model.registered_place = row.get_by_value(
                Place, 'placreg')
            ship_model.registered_region = row.get_by_value(
                Region, 'regisreg')
            ship_model.imputed_nationality = row.get_by_value(
                Nationality, 'natinimp')
            ship_model.tonnage_mod = row.cfloat('tonmod')
            ship_model.voyage = voyage
            # voyage.voyage_ship = ship_model
            return ship_model

        def row_to_itinerary(row, voyage):
            itinerary = VoyageItinerary()
            itinerary.port_of_departure = row.get_by_value(
                Place, 'portdep')
            itinerary.int_first_port_emb = row.get_by_value(
                Place, 'embport')
            itinerary.int_second_port_emb = row.get_by_value(
                Place, 'embport2')
            itinerary.int_first_region_purchase_slaves = row.get_by_value(
                Region, 'embreg')
            itinerary.int_second_region_purchase_slaves = row.get_by_value(
                Region, 'embreg2')
            itinerary.int_first_port_dis = row.get_by_value(
                Place, 'arrport')
            itinerary.int_second_port_dis = row.get_by_value(
                Place, 'arrport2')
            itinerary.int_third_port_dis = row.get_by_value(
                Place, 'arrport3')
            itinerary.int_fourth_port_dis = row.get_by_value(
                Place, 'arrport4')
            itinerary.int_first_region_slave_landing = row.get_by_value(
                Region, 'regarr')
            itinerary.int_second_place_region_slave_landing = (
                row.get_by_value(Region, 'regarr2'))
            itinerary.ports_called_buying_slaves = row.cint('nppretra')
            itinerary.first_place_slave_purchase = row.get_by_value(
                Place, 'plac1tra')
            itinerary.second_place_slave_purchase = row.get_by_value(
                Place, 'plac2tra')
            itinerary.third_place_slave_purchase = row.get_by_value(
                Place, 'plac3tra')
            itinerary.first_region_slave_emb = row.get_by_value(
                Region, 'regem1')
            itinerary.second_region_slave_emb = row.get_by_value(
                Region, 'regem2')
            itinerary.third_region_slave_emb = row.get_by_value(
                Region, 'regem3')
            itinerary.port_of_call_before_atl_crossing = row.get_by_value(
                Place, 'npafttra')
            itinerary.number_of_ports_of_call = row.cint('npprior')
            itinerary.first_landing_place = row.get_by_value(
                Place, 'sla1port')
            itinerary.second_landing_place = row.get_by_value(
                Place, 'adpsale1')
            itinerary.third_landing_place = row.get_by_value(
                Place, 'adpsale2')
            itinerary.first_landing_region = row.get_by_value(
                Region, 'regdis1')
            itinerary.second_landing_region = row.get_by_value(
                Region, 'regdis2')
            itinerary.third_landing_region = row.get_by_value(
                Region, 'regdis3')
            itinerary.place_voyage_ended = row.get_by_value(
                Place, 'portret')
            itinerary.region_of_return = row.get_by_value(
                Region, 'retrnreg')
            itinerary.broad_region_of_return = row.get_by_value(
                BroadRegion, 'retrnreg1')
            itinerary.imp_port_voyage_begin = row.get_by_value(
                Place, 'ptdepimp')
            itinerary.imp_region_voyage_begin = row.get_by_value(
                Region, 'deptregimp')
            itinerary.imp_broad_region_voyage_begin = row.get_by_value(
                BroadRegion, 'deptregimp1')
            itinerary.principal_place_of_slave_purchase = row.get_by_value(
                Place, 'majbuypt')
            itinerary.imp_principal_place_of_slave_purchase = (
                row.get_by_value(Place, 'mjbyptimp'))
            itinerary.imp_principal_region_of_slave_purchase = (
                row.get_by_value(Region, 'majbyimp'))
            itinerary.imp_broad_region_of_slave_purchase = (
                row.get_by_value(BroadRegion, 'majbyimp1'))
            itinerary.principal_port_of_slave_dis = row.get_by_value(
                Place, 'majselpt')
            itinerary.imp_principal_port_slave_dis = row.get_by_value(
                Place, 'mjslptimp')
            itinerary.imp_principal_region_slave_dis = row.get_by_value(
                Region, 'mjselimp')
            itinerary.imp_broad_region_slave_dis = row.get_by_value(
                BroadRegion, 'mjselimp1')
            itinerary.voyage = voyage
            check_hierarchy(voyage.voyage_id, 'ptdepimp',
                            itinerary.imp_port_voyage_begin,
                            itinerary.imp_region_voyage_begin,
                            itinerary.imp_broad_region_voyage_begin)
            check_hierarchy(voyage.voyage_id, 'mjbyptimp',
                            itinerary.imp_principal_place_of_slave_purchase,
                            itinerary.imp_principal_region_of_slave_purchase,
                            itinerary.imp_broad_region_of_slave_purchase)
            check_hierarchy(voyage.voyage_id, 'mjslptimp',
                            itinerary.imp_principal_port_slave_dis,
                            itinerary.imp_principal_region_slave_dis,
                            itinerary.imp_broad_region_slave_dis)
            # voyage.voyage_itinerary = itinerary
            return itinerary

        def row_to_dates(row, voyage):
            dates = VoyageDates()
            dates.voyage_began = date_csv('datedep')
            dates.slave_purchase_began = date_csv('d1slatr')
            dates.vessel_left_port = date_csv('dlslatr')
            dates.first_dis_of_slaves = date_csv(
                'datarr', ['32', '33', '34'])
            dates.date_departed_africa = date_from_sep_values(
                row.get('dateleftafr'))
            dates.arrival_at_second_place_landing = date_csv(
                'datarr', ['36', '37', '38'])
            dates.third_dis_of_slaves = date_csv(
                'datarr', ['39', '40', '41'])
            dates.departure_last_place_of_landing = date_csv(
                'ddepam', ['', 'b', 'c'])
            dates.voyage_completed = date_csv('datarr',
                                              ['43', '44', '45'])
            dates.length_middle_passage_days = row.cint('voyage')
            dates.imp_voyage_began = date_csv('yeardep',
                                              [None, None, ''])
            dates.imp_departed_africa = date_csv(
                'yearaf', [None, None, ''])
            dates.imp_arrival_at_port_of_dis = date_csv(
                'yearam', [None, None, ''])
            dates.imp_length_home_to_disembark = row.cint('voy1imp')
            dates.imp_length_leaving_africa_to_disembark = row.cint('voy2imp')
            dates.voyage = voyage
            # voyage.voyage_dates = dates
            return dates

        def row_to_crew(row, voyage):
            crew = VoyageCrew()
            crew.crew_voyage_outset = row.cint('crew1')
            crew.crew_departure_last_port = row.cint('crew2')
            crew.crew_first_landing = row.cint('crew3')
            crew.crew_return_begin = row.cint('crew4')
            crew.crew_end_voyage = row.cint('crew5')
            crew.unspecified_crew = row.cint('crew')
            crew.crew_died_before_first_trade = row.cint('saild1')
            crew.crew_died_while_ship_african = row.cint('saild2')
            crew.crew_died_middle_passage = row.cint('saild3')
            crew.crew_died_in_americas = row.cint('saild4')
            crew.crew_died_on_return_voyage = row.cint('saild5')
            crew.crew_died_complete_voyage = row.cint('crewdied')
            crew.crew_deserted = row.cint('ndesert')
            crew.voyage = voyage
            # voyage.voyage_crew = crew
            return crew

        def row_to_numbers(row, voyage):
            nums = VoyageSlavesNumbers()
            nums.slave_deaths_before_africa = row.cint('sladafri')
            nums.slave_deaths_between_africa_america = row.cint('sladvoy')
            nums.slave_deaths_between_arrival_and_sale = row.cint('sladamer')
            nums.num_slaves_intended_first_port = row.cint('slintend')
            nums.num_slaves_intended_second_port = row.cint('slinten2')
            nums.num_slaves_carried_first_port = row.cint('ncar13')
            nums.num_slaves_carried_second_port = row.cint('ncar15')
            nums.num_slaves_carried_third_port = row.cint('ncar17')
            nums.total_num_slaves_purchased = row.cint('tslavesp')
            nums.total_num_slaves_dep_last_slaving_port = row.cint('tslavesd')
            nums.total_num_slaves_arr_first_port_embark = row.cint('slaarriv')
            nums.num_slaves_disembark_first_place = row.cint('slas32')
            nums.num_slaves_disembark_second_place = row.cint('slas36')
            nums.num_slaves_disembark_third_place = row.cint('slas39')
            nums.imp_total_num_slaves_embarked = row.cint('slaximp')
            nums.imp_total_num_slaves_disembarked = row.cint('slamimp')
            nums.imp_jamaican_cash_price = row.cfloat('jamcaspr')
            nums.imp_mortality_during_voyage = row.cint('vymrtimp')
            nums.num_men_embark_first_port_purchase = row.cint('men1')
            nums.num_women_embark_first_port_purchase = row.cint('women1')
            nums.num_boy_embark_first_port_purchase = row.cint('boy1')
            nums.num_girl_embark_first_port_purchase = row.cint('girl1')
            nums.num_adult_embark_first_port_purchase = row.cint('adult1')
            nums.num_child_embark_first_port_purchase = row.cint('child1')
            nums.num_infant_embark_first_port_purchase = row.cint('infant1')
            nums.num_males_embark_first_port_purchase = row.cint('male1')
            nums.num_females_embark_first_port_purchase = row.cint('female1')
            nums.num_men_died_middle_passage = row.cint('men2')
            nums.num_women_died_middle_passage = row.cint('women2')
            nums.num_boy_died_middle_passage = row.cint('boy2')
            nums.num_girl_died_middle_passage = row.cint('girl2')
            nums.num_adult_died_middle_passage = row.cint('adult2')
            nums.num_child_died_middle_passage = row.cint('child2')
            nums.num_infant_died_middle_passage = row.cint('infant2')
            nums.num_males_died_middle_passage = row.cint('male2')
            nums.num_females_died_middle_passage = row.cint('female2')
            nums.num_men_disembark_first_landing = row.cint('men3')
            nums.num_women_disembark_first_landing = row.cint('women3')
            nums.num_boy_disembark_first_landing = row.cint('boy3')
            nums.num_girl_disembark_first_landing = row.cint('girl3')
            nums.num_adult_disembark_first_landing = row.cint('adult3')
            nums.num_child_disembark_first_landing = row.cint('child3')
            nums.num_infant_disembark_first_landing = row.cint('infant3')
            nums.num_males_disembark_first_landing = row.cint('male3')
            nums.num_females_disembark_first_landing = row.cint('female3')
            nums.num_men_embark_second_port_purchase = row.cint('men4')
            nums.num_women_embark_second_port_purchase = row.cint('women4')
            nums.num_boy_embark_second_port_purchase = row.cint('boy4')
            nums.num_girl_embark_second_port_purchase = row.cint('girl4')
            nums.num_adult_embark_second_port_purchase = row.cint('adult4')
            nums.num_child_embark_second_port_purchase = row.cint('child4')
            nums.num_infant_embark_second_port_purchase = row.cint('infant4')
            nums.num_males_embark_second_port_purchase = row.cint('male4')
            nums.num_females_embark_second_port_purchase = row.cint('female4')
            nums.num_men_embark_third_port_purchase = row.cint('men5')
            nums.num_women_embark_third_port_purchase = row.cint('women5')
            nums.num_boy_embark_third_port_purchase = row.cint('boy5')
            nums.num_girl_embark_third_port_purchase = row.cint('girl5')
            nums.num_adult_embark_third_port_purchase = row.cint('adult5')
            nums.num_child_embark_third_port_purchase = row.cint('child5')
            nums.num_infant_embark_third_port_purchase = row.cint('infant5')
            nums.num_males_embark_third_port_purchase = row.cint('male5')
            nums.num_females_embark_third_port_purchase = row.cint('female5')
            nums.num_men_disembark_second_landing = row.cint('men6')
            nums.num_women_disembark_second_landing = row.cint('women6')
            nums.num_boy_disembark_second_landing = row.cint('boy6')
            nums.num_girl_disembark_second_landing = row.cint('girl6')
            nums.num_adult_disembark_second_landing = row.cint('adult6')
            nums.num_child_disembark_second_landing = row.cint('child6')
            nums.num_infant_disembark_second_landing = row.cint('infant6')
            nums.num_males_disembark_second_landing = row.cint('male6')
            nums.num_females_disembark_second_landing = row.cint('female6')
            nums.imp_num_adult_embarked = row.cint('adlt1imp')
            nums.imp_num_children_embarked = row.cint('chil1imp')
            nums.imp_num_male_embarked = row.cint('male1imp')
            nums.imp_num_female_embarked = row.cint('feml1imp')
            nums.total_slaves_embarked_age_identified = row.cint('slavema1')
            nums.total_slaves_embarked_gender_identified = row.cint('slavemx1')
            nums.imp_adult_death_middle_passage = row.cint('adlt2imp')
            nums.imp_child_death_middle_passage = row.cint('chil2imp')
            nums.imp_male_death_middle_passage = row.cint('male2imp')
            nums.imp_female_death_middle_passage = row.cint('feml2imp')
            nums.imp_num_adult_landed = row.cint('adlt3imp')
            nums.imp_num_child_landed = row.cint('chil3imp')
            nums.imp_num_male_landed = row.cint('male3imp')
            nums.imp_num_female_landed = row.cint('feml3imp')
            nums.total_slaves_landed_age_identified = row.cint('slavema3')
            nums.total_slaves_landed_gender_identified = row.cint('slavemx3')
            nums.total_slaves_dept_or_arr_age_identified = row.cint('slavema7')
            nums.total_slaves_dept_or_arr_gender_identified = row.cint('slavemx7')
            nums.total_slaves_embarked_age_gender_identified = row.cint('slavmax1')
            nums.total_slaves_by_age_gender_identified_among_landed = row.cint('slavmax3')
            nums.total_slaves_by_age_gender_identified_departure_or_arrival = row.cint('slavmax7')
            nums.imp_slaves_embarked_for_mortality = row.cint('tslmtimp')
            nums.imp_num_men_total = row.cint('men7')
            nums.imp_num_women_total = row.cint('women7')
            nums.imp_num_boy_total = row.cint('boy7')
            nums.imp_num_girl_total = row.cint('girl7')
            nums.imp_num_adult_total = row.cint('adult7')
            nums.imp_num_child_total = row.cint('child7')
            nums.imp_num_males_total = row.cint('male7')
            nums.imp_num_females_total = row.cint('female7')
            nums.percentage_men = row.cfloat('menrat7')
            nums.percentage_women = row.cfloat('womrat7')
            nums.percentage_boy = row.cfloat('boyrat7')
            nums.percentage_girl = row.cfloat('girlrat7')
            nums.percentage_male = row.cfloat('malrat7')
            nums.percentage_child = row.cfloat('chilrat7')
            nums.percentage_adult = 1 - nums.percentage_child \
                if nums.percentage_child is not None else None
            nums.percentage_female = 1 - nums.percentage_male \
                if nums.percentage_male is not None else None
            nums.imp_mortality_ratio = row.cfloat('vymrtrat')
            nums.percentage_boys_among_embarked_slaves = row.cfloat('boyrat1')
            nums.child_ratio_among_embarked_slaves = row.cfloat('chilrat1')
            nums.percentage_girls_among_embarked_slaves = row.cfloat('girlrat1')
            nums.male_ratio_among_embarked_slaves = row.cfloat('malrat1')
            nums.percentage_men_among_embarked_slaves = row.cfloat('menrat1')
            nums.percentage_women_among_embarked_slaves = row.cfloat('womrat1')
            nums.percentage_boys_among_landed_slaves = row.cfloat('boyrat3')
            nums.child_ratio_among_landed_slaves = row.cfloat('chilrat3')
            nums.percentage_girls_among_landed_slaves = row.cfloat('girlrat3')
            nums.male_ratio_among_landed_slaves = row.cfloat('malrat3')
            nums.percentage_men_among_landed_slaves = row.cfloat('menrat3')
            nums.percentage_women_among_landed_slaves = row.cfloat('womrat3')
            # INSERT HERE any new number variables [import CSV]
            nums.voyage = voyage
            # voyage.voyage_slaves_numbers = numbers
            return nums

        counts = {}
        voyage_links = []
        helper = BulkImportationHelper(target_db)
        print("Please ensure that all csv files are UTF8-BOM encoded")
        for file in csv_files:
            with open(file, 'rb') as f:
                reader = helper.read_to_dict(f)
                print("Importing " + file)
                error_reporting.reset_row()
                for r in reader:
                    rh = RowHelper(r, error_reporting)
                    voyage_id = rh.cint('voyageid', False)
                    if voyage_id in voyages:
                        error_reporting.report('Fatal error: duplicate voyage found'
                                         ': ' + str(voyage_id))
                        return
                    # Create a voyage corresponding to this row
                    voyage = Voyage()
                    voyage.pk = voyage_id
                    voyage.voyage_id = voyage_id
                    voyages[voyage_id] = voyage
                    # Next we set up voyage direct and nested members
                    in_cd_room = rh.get('evgreen', '0')
                    if in_cd_room.lower() == 'true':
                        in_cd_room = '1'
                    voyage.voyage_in_cd_rom = in_cd_room == '1'
                    voyage.voyage_groupings = rh.get_by_value(VoyageGroupings, 'xmimpflag')
                    voyage.dataset = rh.cint('dataset', allow_null=False)
                    voyage.comments = rh.get('comments')
                    intra_american = voyage.dataset == 1
                    counts[voyage.dataset] = counts.get(voyage.dataset, 0) + 1
                    ships.append(row_to_ship(rh, voyage))
                    itineraries.append(row_to_itinerary(rh, voyage))
                    voyage_dates.append(row_to_dates(rh, voyage))
                    crews.append(row_to_crew(rh, voyage))
                    voyage_numbers.append(row_to_numbers(rh, voyage))
                    # Captains
                    for order, key in enumerate(get_multi_valued_column_suffix(3)):
                        captain_name = rh.get('captain' + key)
                        if captain_name is None or empty.match(captain_name):
                            continue
                        captain_model = captains.get(captain_name)
                        if captain_model is None:
                            captain_model = VoyageCaptain()
                            captain_model.name = captain_name
                            captains[captain_name] = captain_model
                        captain_connection = VoyageCaptainConnection()
                        captain_connection.captain = captain_model
                        captain_connection.captain_order = order + 1
                        captain_connection.voyage = voyage
                        captain_connections.append(captain_connection)
                    # Ship owners
                    for order, key in enumerate(get_multi_valued_column_suffix(45)):
                        owner_name = rh.get('owner' + key)
                        if owner_name is None or empty.match(owner_name):
                            continue
                        owner_model = ship_owners.get(owner_name)
                        if owner_model is None:
                            owner_model = VoyageShipOwner()
                            owner_model.name = owner_name
                            ship_owners[owner_name] = owner_model
                        owner_connection = VoyageShipOwnerConnection()
                        owner_connection.owner = owner_model
                        owner_connection.owner_order = order + 1
                        owner_connection.voyage = voyage
                        ship_owner_connections.append(owner_connection)
                    # Sources
                    for order, key in enumerate(get_multi_valued_column_suffix(18)):
                        source_ref = rh.get('source' + key)
                        if source_ref is None or empty.match(source_ref):
                            break
                        (source, match) = source_finder.get(source_ref)
                        if source is None:
                            self.errors += 1
                            error_reporting.report(
                                'Source not found for '
                                'voyage id: ' + str(voyage_id) + ' '
                                'source_ref: '
                                '"' + smart_str(source_ref) + '"'
                                ', longest partial '
                                'match: ' + smart_str(match))
                            continue
                        source_connection = VoyageSourcesConnection()
                        source_connection.group = voyage
                        source_connection.source = source
                        source_connection.source_order = order + 1
                        source_connection.text_ref = source_ref
                        source_connections.append(source_connection)
                    # African info
                    for key in get_multi_valued_column_suffix(3):
                        afrinfoval = rh.get_by_value(AfricanInfo, 'afrinfo' + key, key_name='id')
                        if afrinfoval is None:
                            continue
                        afrinfo_conn.append(Voyage.african_info.through(voyage_id=voyage_id, africaninfo_id=afrinfoval.id))
                    # Cargo
                    for key in get_multi_valued_column_suffix(CARGO_COLUMN_COUNT):
                        cargo_type = rh.get_by_value(CargoType, 'cargotype' + key, key_name='id')
                        if cargo_type is None:
                            continue
                        vcc = VoyageCargoConnection()
                        vcc.voyage = voyage
                        vcc.cargo = cargo_type
                        vcc.unit = rh.get_by_value(CargoUnit, 'cargounit' + key, key_name='id')
                        vcc.amount = rh.cfloat('cargoamount' + key)
                        cargo_conn.append(vcc)
                    # Outcome
                    outcome = VoyageOutcome()
                    outcome.particular_outcome = rh.get_by_value(
                        ParticularOutcome, 'fate')
                    outcome.outcome_slaves = rh.get_by_value(
                        SlavesOutcome, 'fate2')
                    outcome.vessel_captured_outcome = rh.get_by_value(
                        VesselCapturedOutcome, 'fate3')
                    outcome.outcome_owner = rh.get_by_value(
                        OwnerOutcome, 'fate4')
                    outcome.resistance = rh.get_by_value(Resistance,
                                                      'resistance')
                    outcome.voyage = voyage
                    outcomes.append(outcome)
                    # Links
                    if 'voyageid2' in rh.row:
                        link_mode = LinkedVoyages.INTRA_AMERICAN_LINK_MODE if intra_american else LinkedVoyages.UNSPECIFIED
                        for entry in re.split(',|;|/', rh.get('voyageid2')):
                            if not entry:
                                continue
                            try:
                                voyage_links.append(
                                    (voyage_id, int(entry), link_mode))
                            except:
                                print(f"Bad link value {entry}")

        print('Constructed ' + str(len(voyages)) + ' voyages from CSV')
        for k, v in counts.items():
            print('Dataset ' + str(k) + ': ' + str(v))

        previous_ids = set(Voyage.all_dataset_objects.values_list('voyage_id', flat=True))
        next_ids = set(voyages.keys())
        missing = previous_ids - next_ids
        if len(missing) > 0:
            self.errors += 1
            error_reporting.report(f"There are {len(missing)} existing voyages without replacement!!")
            print("Missing voyage ids:")
            print(missing)
        if self.errors > 0:
            print(
                str(self.errors) + ' errors occurred, '
                'please check the messages above.')

        confirm = input(
            "Are you sure you want to continue? "
            "The existing data will be deleted! (yes/[no]): "
        ).strip()
        print('"' + confirm + '"')
        if confirm != 'yes':
            return

        print('Deleting old data...')

        quote_char = helper.get_quote_char()
        with transaction.atomic():
            with connection.cursor() as cursor:

                def clear_fk(fk_field):
                    sql = 'UPDATE {0}{1}{0} SET {0}{2}{0}=NULL'
                    sql = sql.format(quote_char, Voyage._meta.db_table, fk_field)
                    print(sql)
                    cursor.execute(sql)

                # Disable foreign keys so that we are free to delete the
                # current voyages even if related tables reference them.
                helper.disable_fks(cursor)
                clear_fk('voyage_ship_id')
                clear_fk('voyage_itinerary_id')
                clear_fk('voyage_dates_id')
                clear_fk('voyage_crew_id')
                clear_fk('voyage_slaves_numbers_id')
                helper.delete_all(cursor, LinkedVoyages)
                helper.delete_all(cursor, VoyageCaptainConnection)
                helper.delete_all(cursor, VoyageShipOwnerConnection)
                helper.delete_all(cursor, VoyageSourcesConnection)
                helper.delete_all(cursor, VoyageCaptain)
                helper.delete_all(cursor, VoyageCrew)
                helper.delete_all(cursor, VoyageDates)
                helper.delete_all(cursor, VoyageItinerary)
                helper.delete_all(cursor, VoyageOutcome)
                helper.delete_all(cursor, VoyageShip)
                helper.delete_all(cursor, VoyageShipOwner)
                helper.delete_all(cursor, VoyageSlavesNumbers)
                helper.delete_all(cursor, Voyage.african_info.through)
                helper.delete_all(cursor, VoyageCargoConnection)
                helper.delete_all(cursor, Voyage)

                print('Inserting new records...')

                def bulk_insert(model, lst, attr_key=None, manager=None):
                    print('Bulk inserting ' + str(model))
                    if manager is None:
                        manager = model.objects
                    manager.bulk_create(lst, batch_size=100)
                    return None if attr_key is None else \
                        {getattr(x, attr_key): x for x in manager.all()}

                voyages = helper.bulk_insert(Voyage, list(voyages.values()), 'voyage_id',
                                    Voyage.all_dataset_objects)
                captains = helper.bulk_insert(VoyageCaptain, list(captains.values()), 'name')
                ship_owners = helper.bulk_insert(VoyageShipOwner, list(ship_owners.values()),
                                        'name')
                # At this point we have primary keys for voyages.

                # Create voyage links.
                for i, triple in enumerate(voyage_links):
                    if triple[0] in voyages and triple[1] in voyages:
                        link = LinkedVoyages()
                        link.first = voyages.get(triple[0])
                        link.second = voyages.get(triple[1])
                        link.mode = triple[2]
                        voyage_links[i] = link
                    else:
                        voyage_links[i] = None
                voyage_links = [link for link in voyage_links if link]

                def set_foreign_keys(items, dictionary, key_func, fk_field):
                    for item in items:
                        x = dictionary[key_func(item)]
                        setattr(item, fk_field + '_id', x.pk)

                def set_voyages_fk(items):
                    set_foreign_keys(items, voyages, lambda x: x.voyage.voyage_id,
                                    'voyage')

                # Insert dependent models in bulk
                set_voyages_fk(ships)
                set_voyages_fk(itineraries)
                set_voyages_fk(voyage_dates)
                set_voyages_fk(crews)
                set_voyages_fk(voyage_numbers)
                set_voyages_fk(outcomes)
                bulk_insert(VoyageShip, ships)
                bulk_insert(VoyageItinerary, itineraries)
                bulk_insert(VoyageDates, voyage_dates)
                bulk_insert(VoyageCrew, crews)
                bulk_insert(VoyageSlavesNumbers, voyage_numbers)
                bulk_insert(VoyageOutcome, outcomes)

                # Now insert the many-to-many connections
                set_voyages_fk(captain_connections)
                set_foreign_keys(captain_connections, captains,
                                lambda x: x.captain.name, 'captain')
                set_voyages_fk(ship_owner_connections)
                set_foreign_keys(ship_owner_connections, ship_owners,
                                lambda x: x.owner.name, 'owner')
                set_foreign_keys(source_connections, voyages,
                                lambda x: x.group.voyage_id, 'group')
                bulk_insert(LinkedVoyages, voyage_links)
                bulk_insert(VoyageCaptainConnection, captain_connections)
                bulk_insert(VoyageShipOwnerConnection, ship_owner_connections)
                bulk_insert(VoyageSourcesConnection, source_connections)
                bulk_insert(Voyage.african_info.through, afrinfo_conn)
                bulk_insert(VoyageCargoConnection, cargo_conn)

                # Update the one-to-one references for Voyages' models
                # This is a redundant foreign key, however, this design
                # choice precedes the development of this command.
                def get_raw_sql(related_model,
                                fk_on_voyages,
                                fk_on_related='voyage_id'):
                    if target_db == 'mysql':
                        update_query_template = (
                            'UPDATE {0}{1}{0} a JOIN {0}{2}{0} b '
                            'ON a.{0}id{0}=b.{0}{3}{0} '
                            'SET a.{0}{4}{0}=b.{0}id{0}')
                    elif target_db == 'pgsql':
                        update_query_template = (
                            'UPDATE {0}{1}{0} as a SET {0}{4}{0}=b.{0}id{0} '
                            'FROM {0}{2}{0} as b WHERE a.{0}id{0}=b.{0}{3}{0}')
                    sql = update_query_template.format(quote_char,
                                                    Voyage._meta.db_table,
                                                    related_model._meta.db_table,
                                                    fk_on_related, fk_on_voyages)
                    print('Executing query...')
                    print(sql)
                    return sql

                cursor.execute(get_raw_sql(VoyageShip, 'voyage_ship_id'))
                cursor.execute(get_raw_sql(VoyageItinerary, 'voyage_itinerary_id'))
                cursor.execute(get_raw_sql(VoyageDates, 'voyage_dates_id'))
                cursor.execute(get_raw_sql(VoyageCrew, 'voyage_crew_id'))
                cursor.execute(
                    get_raw_sql(VoyageSlavesNumbers, 'voyage_slaves_numbers_id'))

                helper.re_enable_fks(cursor)

        print("Completed! Don't forget to rebuild_index on Solr.")
