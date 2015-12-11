from django.core.management.base import BaseCommand, CommandError
from voyages.apps.voyage.models import *
import unicodecsv

class Command(BaseCommand):
    args = '<csv_file>'
    help = 'Imports a CSV file with the full data-set and converts the data to the Django models. The user can ' \
           'decide to apply the results to the DB or generate .json files that can be imported into DBs with ' \
           'the loaddata command.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='+')
        parser.add_argument('--db',
            dest='db',
            default='mysql',
            help='Specifies the DB backend so that the appropriate raw sql is generated. '
                 'Supported values: "mysql" and "pgsql"')

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.errors = 0

    def handle(self, csv_file, *args, **options):
        self.errors = 0
        target_db = options.get('db')
        if target_db != 'mysql' and target_db != 'pgsql':
            print 'Supported dbs are "mysql" and "pgsql". Aborting...'
            return
        print 'Targetting db: ' + target_db

        # Store related models that need to be persisted in the following lists/dicts
        voyages = {}
        captains = {}
        ship_owners = {}
        captain_connections = []
        ship_owner_connections = []
        source_connections = []
        crews = []
        itineraries = []
        outcomes = []
        ships = []
        voyage_dates = []
        voyage_numbers = []

        # Prefetch data: Geography
        broad_regions = {b.value: b for b in BroadRegion.objects.all()}
        regions = {r.value: r for r in Region.objects.all()}
        places = {p.value: p for p in Place.objects.all()}

        # Prefetch data: Outcomes
        owner_outcomes = {o.value: o for o in OwnerOutcome.objects.all()}
        particular_outcomes = {o.value: o for o in ParticularOutcome.objects.all()}
        slaves_outcomes = {o.value: o for o in SlavesOutcome.objects.all()}
        vessel_captured_outcomes = {o.value: o for o in VesselCapturedOutcome.objects.all()}

        # Prefetch data: Miscellaneous
        groupings = {x.value: x for x in VoyageGroupings.objects.all()}
        nationalities = {x.value: x for x in Nationality.objects.all()}
        resistances = {o.value: o for o in Resistance.objects.all()}
        rigs = {x.value: x for x in RigOfVessel.objects.all()}
        ton_types = {x.value: x for x in TonType.objects.all()}

        # Declare a dict containing all pre-fetch dicts so that we can
        # easily log any errors when looking for pre-fetched data.
        prefetch = {'broad_regions': broad_regions,
                    'regions': regions,
                    'places': places,
                    'owner_outcomes': owner_outcomes,
                    'particular_outcomes': particular_outcomes,
                    'slaves_outcomes': slaves_outcomes,
                    'vessel_captured_outcomes': vessel_captured_outcomes,
                    'groupings': groupings,
                    'nationalities': nationalities,
                    'resistances': resistances,
                    'rigs': rigs,
                    'ton_types': ton_types}

        def get_by_value(model_name, field_name, allow_null=True):
            """
            Gets the pre-fetched model corresponding to the given
            value and logs an error if the model is not found.
            :param model_name: the pre-fetched model type
            :param field_name: the field containing the numerical
            value of the model.
            If the row[field_name] is None, no errors will be logged.
            :param allowNull: whether the field value is allowed to be None
            :return: The corresponding model, or None if not found.
            """
            val = cint(row[field_name], allow_null)
            if val is None:
                return None
            model = prefetch[model_name].get(val)
            if model is None:
                print 'Failed to locate "' + model_name + '" with value: ' + str(val) + \
                      ' for field "' + field_name + '"'
                self.errors += 1
            return model

        # Prefetch data: Sources
        all_sources = VoyageSources.objects.all()
        trie = {}
        _end = '_end'
        for source in all_sources:
            dict = trie
            for letter in source.short_ref:
                dict = dict.setdefault(letter, {})
            dict[_end] = source

        # This method searches the Sources trie and obtain the
        # Source whose short reference matches the longest
        # prefix of the given reference.
        def get_source(ref):
            best = None
            dict = trie
            for letter in ref:
                dict = dict.get(letter)
                if dict is None:
                    break
                best = dict.get(_end, best)
            return best

        def cint(val, allow_null=True):
            if (val is None or val == '') and not allow_null:
                self.errors += 1
                return None
            return int(val) if val != '' else None

        def cfloat(val, allow_null=True):
            if (val is None or val == '') and not allow_null:
                self.errors += 1
                return None
            return float(val) if val != '' else None

        def date_csv(var_name_prefix, suffixes=['a', 'b', 'c']):
            """
            Fetches date fields (day, month, year) and produce a CSV
            string in the format MM,DD,YYYY
            :param var_name_prefix: the variable name prefix
            :param suffixes: the day, month, and year suffixes, use None
            to specify that there is no variable corresponding to the
            date component.
            :return: the CSV date.
            """
            return (row[var_name_prefix + suffixes[1]] if suffixes[1] is not None else '') + ',' + \
                   (row[var_name_prefix + suffixes[0]] if suffixes[0] is not None else '') + ',' + \
                   (row[var_name_prefix + suffixes[2]] if suffixes[2] is not None else '')

        def date_iso_csv(iso_value):
            """
            Converts a date in the ISO format YYYY-MM-DD to the
            CSV format MM,DD,YYYY
            :param iso_value: the iso formatted date
            :return: the CSV date
            """
            if iso_value == '':
                return ''
            components = iso_value.split('-')
            if len(components) != 3:
                self.errors += 1
                print 'Error with date ' + iso_value
                return ''
            return components[1] + ',' + components[2] + ',' + components[0]

        with open(csv_file[0], 'rU') as f:
            reader = unicodecsv.DictReader(f, delimiter=',')
            for row in reader:
                # Create a voyage corresponding to this row
                voyage = Voyage()
                id = cint(row['voyageid'], False)
                if id in voyages:
                    print 'Duplicate voyage found: ' + str(id)
                    return
                voyage.voyage_id = id
                voyages[id] = voyage
                # Next we set up voyage direct and nested members
                voyage.voyage_in_cd_rom = row['evgreen']
                voyage.voyage_groupings = get_by_value('groupings', 'xmimpflag')
                # Ship
                ship_model = VoyageShip()
                ship_model.ship_name = row['shipname']
                ship_model.nationality_ship = get_by_value('nationalities', 'national')
                ship_model.tonnage = cint(row['tonnage'])
                ship_model.ton_type = get_by_value('ton_types', 'tontype')
                ship_model.rig_of_vessel = get_by_value('rigs', 'rig')
                ship_model.guns_mounted = cint(row['guns'])
                ship_model.year_of_construction = cint(row['yrcons'])
                ship_model.vessel_construction_place = get_by_value('places', 'placcons')
                ship_model.vessel_construction_region = get_by_value('regions', 'constreg')
                ship_model.registered_year = cint(row['yrreg'])
                ship_model.registered_place = get_by_value('places', 'placreg')
                ship_model.registered_region = get_by_value('regions', 'regisreg')
                ship_model.imputed_nationality = get_by_value('nationalities', 'natinimp')
                ship_model.tonnage_mod = cfloat(row['tonmod'])
                ship_model.voyage = voyage
                ships.append(ship_model)
                # voyage.voyage_ship = ship_model
                # Itinerary
                itinerary = VoyageItinerary()
                itinerary.port_of_departure = get_by_value('places', 'portdep')
                itinerary.int_first_port_emb = get_by_value('places', 'embport')
                itinerary.int_second_port_emb = get_by_value('places', 'embport2')
                itinerary.int_first_region_purchase_slaves = get_by_value('regions', 'embreg')
                itinerary.int_second_region_purchase_slaves = get_by_value('regions', 'embreg2')
                itinerary.int_first_port_dis = get_by_value('places', 'arrport')
                itinerary.int_second_port_dis = get_by_value('places', 'arrport2')
                itinerary.int_first_region_slave_landing = get_by_value('regions', 'regarr')
                itinerary.int_second_place_region_slave_landing = get_by_value('regions', 'regarr2')
                itinerary.ports_called_buying_slaves = cint(row['nppretra'])
                itinerary.first_place_slave_purchase = get_by_value('places', 'plac1tra')
                itinerary.second_place_slave_purchase = get_by_value('places', 'plac2tra')
                itinerary.third_place_slave_purchase = get_by_value('places', 'plac3tra')
                itinerary.first_region_slave_emb = get_by_value('regions', 'regem1')
                itinerary.second_region_slave_emb = get_by_value('regions', 'regem2')
                itinerary.third_region_slave_emb = get_by_value('regions', 'regem3')
                itinerary.port_of_call_before_atl_crossing = get_by_value('places', 'npafttra')
                itinerary.number_of_ports_of_call = cint(row['npprior'])
                itinerary.first_landing_place = get_by_value('places', 'sla1port')
                itinerary.second_landing_place = get_by_value('places', 'adpsale1')
                itinerary.third_landing_place = get_by_value('places', 'adpsale2')
                itinerary.first_landing_region = get_by_value('regions', 'regdis1')
                itinerary.second_landing_region = get_by_value('regions', 'regdis2')
                itinerary.third_landing_region = get_by_value('regions', 'regdis3')
                itinerary.place_voyage_ended = get_by_value('places', 'portret')
                itinerary.region_of_return = get_by_value('regions', 'retrnreg')
                itinerary.broad_region_of_return = get_by_value('broad_regions', 'retrnreg1')
                itinerary.imp_port_voyage_begin = get_by_value('places', 'ptdepimp')
                itinerary.imp_region_voyage_begin = get_by_value('regions', 'deptregimp')
                itinerary.imp_broad_region_voyage_begin = get_by_value('broad_regions', 'deptregimp1')
                itinerary.principal_place_of_slave_purchase = get_by_value('places', 'majbuypt')
                itinerary.imp_principal_place_of_slave_purchase = get_by_value('places', 'mjbyptimp')
                itinerary.imp_principal_region_of_slave_purchase = get_by_value('regions', 'majbyimp')
                itinerary.imp_broad_region_of_slave_purchase = get_by_value('broad_regions', 'majbyimp1')
                itinerary.principal_port_of_slave_dis = get_by_value('places', 'majselpt')
                itinerary.imp_principal_port_slave_dis = get_by_value('places', 'mjslptimp')
                itinerary.imp_principal_region_slave_dis = get_by_value('regions', 'mjselimp')
                itinerary.imp_broad_region_slave_dis = get_by_value('broad_regions', 'mjselimp1')
                itinerary.voyage = voyage
                itineraries.append(itinerary)
                # voyage.voyage_itinerary = itinerary
                # Dates
                dates = VoyageDates()
                dates.voyage_began = date_csv('datedep')
                dates.slave_purchase_began = date_csv('d1slatr')
                dates.vessel_left_port = date_csv('dlslatr')
                dates.first_dis_of_slaves = date_csv('datarr', ['32', '33', '34'])
                dates.date_departed_africa = date_iso_csv(row['datedep'])
                dates.arrival_at_second_place_landing = date_csv('datarr', ['36', '37', '38'])
                dates.third_dis_of_slaves = date_csv('datarr', ['39', '40', '41'])
                dates.departure_last_place_of_landing = date_csv('ddepam', ['', 'b', 'c'])
                dates.voyage_completed = date_csv('datarr', ['43', '44', '45'])
                dates.length_middle_passage_days = cint(row['voyage'])
                dates.imp_voyage_began = date_csv('yeardep', [None, None, ''])
                dates.imp_departed_africa = date_csv('yearaf', [None, None, ''])
                dates.imp_arrival_at_port_of_dis = date_csv('yearam', [None, None, ''])
                dates.imp_length_home_to_disembark = cint(row['voy1imp'])
                dates.imp_length_leaving_africa_to_disembark = cint(row['voy2imp'])
                dates.voyage = voyage
                voyage_dates.append(dates)
                # voyage.voyage_dates = dates
                # Crew
                crew = VoyageCrew()
                crew.crew_voyage_outset = cint(row['crew1'])
                crew.crew_departure_last_port = cint(row['crew2'])
                crew.crew_first_landing = cint(row['crew3'])
                crew.crew_return_begin = cint(row['crew4'])
                crew.crew_end_voyage = cint(row['crew5'])
                crew.unspecified_crew = cint(row['crew'])
                crew.crew_died_before_first_trade = cint(row['saild1'])
                crew.crew_died_while_ship_african = cint(row['saild2'])
                crew.crew_died_middle_passage = cint(row['saild3'])
                crew.crew_died_in_americas = cint(row['saild4'])
                crew.crew_died_on_return_voyage = cint(row['saild5'])
                crew.crew_died_complete_voyage = cint(row['crewdied'])
                crew.crew_deserted = cint(row['ndesert'])
                crew.voyage = voyage
                crews.append(crew)
                # voyage.voyage_crew = crew
                # Slave numbers
                numbers = VoyageSlavesNumbers()
                numbers.slave_deaths_before_africa = cint(row['sladafri'])
                numbers.slave_deaths_between_africa_america = cint(row['sladvoy'])
                numbers.slave_deaths_between_arrival_and_sale = cint(row['sladamer'])
                numbers.num_slaves_intended_first_port = cint(row['slintend'])
                numbers.num_slaves_intended_second_port = cint(row['slinten2'])
                numbers.num_slaves_carried_first_port = cint(row['ncar13'])
                numbers.num_slaves_carried_second_port = cint(row['ncar15'])
                numbers.num_slaves_carried_third_port = cint(row['ncar17'])
                numbers.total_num_slaves_purchased = cint(row['tslavesp'])
                numbers.total_num_slaves_dep_last_slaving_port = cint(row['tslavesd'])
                numbers.total_num_slaves_arr_first_port_embark = cint(row['slaarriv'])
                numbers.num_slaves_disembark_first_place = cint(row['slas32'])
                numbers.num_slaves_disembark_second_place = cint(row['slas36'])
                numbers.num_slaves_disembark_third_place = cint(row['slas39'])
                numbers.imp_total_num_slaves_embarked = cint(row['slaximp'])
                numbers.imp_total_num_slaves_disembarked = cint(row['slamimp'])
                numbers.imp_jamaican_cash_price = cfloat(row['jamcaspr'])
                numbers.imp_mortality_during_voyage = cint(row['vymrtimp'])
                numbers.num_men_embark_first_port_purchase = cint(row['men1'])
                numbers.num_women_embark_first_port_purchase = cint(row['women1'])
                numbers.num_boy_embark_first_port_purchase = cint(row['boy1'])
                numbers.num_girl_embark_first_port_purchase = cint(row['girl1'])
                numbers.num_adult_embark_first_port_purchase = cint(row['adult1'])
                numbers.num_child_embark_first_port_purchase = cint(row['child1'])
                numbers.num_infant_embark_first_port_purchase = cint(row['infant1'])
                numbers.num_males_embark_first_port_purchase = cint(row['male1'])
                numbers.num_females_embark_first_port_purchase = cint(row['female1'])
                numbers.num_men_died_middle_passage = cint(row['men2'])
                numbers.num_women_died_middle_passage = cint(row['women2'])
                numbers.num_boy_died_middle_passage = cint(row['boy2'])
                numbers.num_girl_died_middle_passage = cint(row['girl2'])
                numbers.num_adult_died_middle_passage = cint(row['adult2'])
                numbers.num_child_died_middle_passage = cint(row['child2'])
                # numbers.num_infant_died_middle_passage = cint(row['infant2'])
                numbers.num_males_died_middle_passage = cint(row['male2'])
                numbers.num_females_died_middle_passage = cint(row['female2'])
                numbers.num_men_disembark_first_landing = cint(row['men3'])
                numbers.num_women_disembark_first_landing = cint(row['women3'])
                numbers.num_boy_disembark_first_landing = cint(row['boy3'])
                numbers.num_girl_disembark_first_landing = cint(row['girl3'])
                numbers.num_adult_disembark_first_landing = cint(row['adult3'])
                numbers.num_child_disembark_first_landing = cint(row['child3'])
                numbers.num_infant_disembark_first_landing = cint(row['infant3'])
                numbers.num_males_disembark_first_landing = cint(row['male3'])
                numbers.num_females_disembark_first_landing = cint(row['female3'])
                numbers.num_men_embark_second_port_purchase = cint(row['men4'])
                numbers.num_women_embark_second_port_purchase = cint(row['women4'])
                numbers.num_boy_embark_second_port_purchase = cint(row['boy4'])
                numbers.num_girl_embark_second_port_purchase = cint(row['girl4'])
                numbers.num_adult_embark_second_port_purchase = cint(row['adult4'])
                numbers.num_child_embark_second_port_purchase = cint(row['child4'])
                numbers.num_infant_embark_second_port_purchase = cint(row['infant4'])
                numbers.num_males_embark_second_port_purchase = cint(row['male4'])
                numbers.num_females_embark_second_port_purchase = cint(row['female4'])
                numbers.num_men_embark_third_port_purchase = cint(row['men5'])
                numbers.num_women_embark_third_port_purchase = cint(row['women5'])
                numbers.num_boy_embark_third_port_purchase = cint(row['boy5'])
                numbers.num_girl_embark_third_port_purchase = cint(row['girl5'])
                numbers.num_adult_embark_third_port_purchase = cint(row['adult5'])
                numbers.num_child_embark_third_port_purchase = cint(row['child5'])
                # numbers.num_infant_embark_third_port_purchase = cint(row['infant5'])
                numbers.num_males_embark_third_port_purchase = cint(row['male5'])
                numbers.num_females_embark_third_port_purchase = cint(row['female5'])
                numbers.num_men_disembark_second_landing = cint(row['men6'])
                numbers.num_women_disembark_second_landing = cint(row['women6'])
                numbers.num_boy_disembark_second_landing = cint(row['boy6'])
                numbers.num_girl_disembark_second_landing = cint(row['girl6'])
                numbers.num_adult_disembark_second_landing = cint(row['adult6'])
                numbers.num_child_disembark_second_landing = cint(row['child6'])
                # numbers.num_infant_disembark_second_landing = cint(row['infant6'])
                numbers.num_males_disembark_second_landing = cint(row['male6'])
                numbers.num_females_disembark_second_landing = cint(row['female6'])
                numbers.imp_num_adult_embarked = cint(row['adlt1imp'])
                numbers.imp_num_children_embarked = cint(row['chil1imp'])
                numbers.imp_num_male_embarked = cint(row['male1imp'])
                numbers.imp_num_female_embarked = cint(row['feml1imp'])
                numbers.total_slaves_embarked_age_identified = cint(row['slavema1'])
                numbers.total_slaves_embarked_gender_identified = cint(row['slavemx1'])
                numbers.imp_adult_death_middle_passage = cint(row['adlt2imp'])
                numbers.imp_child_death_middle_passage = cint(row['chil2imp'])
                numbers.imp_male_death_middle_passage = cint(row['male2imp'])
                numbers.imp_female_death_middle_passage = cint(row['feml2imp'])
                numbers.imp_num_adult_landed = cint(row['adlt3imp'])
                numbers.imp_num_child_landed = cint(row['chil3imp'])
                numbers.imp_num_male_landed = cint(row['male2imp'])
                numbers.imp_num_female_landed = cint(row['feml3imp'])
                numbers.total_slaves_landed_age_identified = cint(row['slavema3'])
                numbers.total_slaves_landed_gender_identified = cint(row['slavemx3'])
                numbers.total_slaves_dept_or_arr_age_identified = cint(row['slavema7'])
                numbers.total_slaves_dept_or_arr_gender_identified = cint(row['slavemx7'])
                numbers.imp_slaves_embarked_for_mortality = cint(row['tslmtimp'])
                numbers.imp_num_men_total = cint(row['men7'])
                numbers.imp_num_women_total = cint(row['women7'])
                numbers.imp_num_boy_total = cint(row['boy7'])
                numbers.imp_num_girl_total = cint(row['girl7'])
                numbers.imp_num_adult_total = cint(row['adult7'])
                numbers.imp_num_child_total = cint(row['child7'])
                numbers.imp_num_males_total = cint(row['male7'])
                numbers.imp_num_females_total = cint(row['female7'])
                numbers.percentage_men = cfloat(row['menrat7'])
                numbers.percentage_women = cfloat(row['womrat7'])
                numbers.percentage_boy = cfloat(row['boyrat7'])
                numbers.percentage_girl = cfloat(row['girlrat7'])
                numbers.percentage_male = cfloat(row['malrat7'])
                numbers.percentage_child = cfloat(row['chilrat7'])
                numbers.percentage_adult = 1 - numbers.percentage_child \
                    if numbers.percentage_child is not None else None
                numbers.percentage_female = 1 - numbers.percentage_male \
                    if numbers.percentage_male is not None else None
                numbers.imp_mortality_ratio = cfloat(row['vymrtrat'])
                numbers.voyage = voyage
                voyage_numbers.append(numbers)
                # voyage.voyage_slaves_numbers = numbers
                # Captains
                order = 1
                for key in 'abc':
                    captain_name = row['captain' + key]
                    if captain_name == '':
                        break
                    captain_model = captains.get(captain_name)
                    if captain_model is None:
                        captain_model = VoyageCaptain()
                        captain_model.name = captain_name
                        captains[captain_name] = captain_model
                    captain_connection = VoyageCaptainConnection()
                    captain_connection.captain = captain_model
                    captain_connection.captain_order = order
                    captain_connection.voyage = voyage
                    captain_connections.append(captain_connection)
                    order += 1
                # Ship owners
                order = 1
                for key in 'abcdefghijklmnop':
                    owner_name = row['owner' + key]
                    if owner_name == '':
                        break
                    owner_model = ship_owners.get(owner_name)
                    if owner_model is None:
                        owner_model = VoyageShipOwner()
                        owner_model.name = owner_name
                        ship_owners[owner_name] = owner_model
                    owner_connection = VoyageShipOwnerConnection()
                    owner_connection.owner = owner_model
                    owner_connection.owner_order = order
                    owner_connection.voyage = voyage
                    ship_owner_connections.append(owner_connection)
                    order += 1
                # Sources
                order = 1
                for key in 'abcdefghijklmnopqr':
                    source_ref = row['source' + key]
                    if source_ref == '':
                        break
                    source = get_source(source_ref)
                    if source is None:
                        self.errors += 1
                        print 'Source not found for "' + source_ref + '"'
                        continue
                    source_connection = VoyageSourcesConnection()
                    source_connection.group = voyage
                    source_connection.source = source
                    source_connection.source_order = order
                    source_connection.text_ref = source_ref
                    source_connections.append(source_connection)
                    order += 1
                # Outcome
                outcome = VoyageOutcome()
                outcome.particular_outcome = get_by_value('particular_outcomes', 'fate')
                outcome.outcome_slaves = get_by_value('slaves_outcomes', 'fate2')
                outcome.vessel_captured_outcome = get_by_value('vessel_captured_outcomes', 'fate3')
                outcome.outcome_owner = get_by_value('owner_outcomes', 'fate4')
                outcome.resistance = get_by_value('resistances', 'resistance')
                outcome.voyage = voyage
                outcomes.append(outcome)
        print 'Constructed ' + str(len(voyages)) + ' voyages from CSV.'
        if self.errors > 0:
            print str(self.errors) + ' errors occurred, please check the messages above.'

        confirm = raw_input("Are you sure you want to continue? The existing data will be deleted! (yes/[no]): ")
        print '"' + confirm + '"'
        if confirm != 'yes':
            return

        print 'Deleting old data...'

        def delete_all(model):
            model.objects.all().delete()

        delete_all(Voyage)
        delete_all(VoyageCaptain)
        delete_all(VoyageCrew)
        delete_all(VoyageDates)
        delete_all(VoyageItinerary)
        delete_all(VoyageOutcome)
        delete_all(VoyageShip)
        delete_all(VoyageShipOwner)
        delete_all(VoyageSlavesNumbers)
        delete_all(VoyageCaptainConnection)
        delete_all(VoyageShipOwnerConnection)
        delete_all(VoyageSourcesConnection)

        print 'Inserting new records...'

        def bulk_insert(model, lst, attr_key=None):
            print 'Bulk inserting ' + str(model)
            model.objects.bulk_create(lst)
            return None if attr_key is None else \
                {getattr(x, attr_key): x for x in model.objects.all()}

        voyages = bulk_insert(Voyage, voyages.values(), 'voyage_id')
        captains = bulk_insert(VoyageCaptain, captains.values(), 'name')
        ship_owners = bulk_insert(VoyageShipOwner, ship_owners.values(), 'name')

        def set_foreign_keys(items, dict, key_func, fk_field):
            for item in items:
                x = dict[key_func(item)]
                setattr(item, fk_field + '_id', x.pk)

        def set_voyages_fk(items):
            set_foreign_keys(items, voyages, lambda x: x.voyage.voyage_id, 'voyage')

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
        set_foreign_keys(captain_connections, captains, lambda x: x.captain.name, 'captain')
        set_voyages_fk(ship_owner_connections)
        set_foreign_keys(ship_owner_connections, ship_owners, lambda x: x.owner.name, 'owner')
        set_foreign_keys(source_connections, voyages, lambda x: x.group.voyage_id, 'group')
        bulk_insert(VoyageCaptainConnection, captain_connections)
        bulk_insert(VoyageShipOwnerConnection, ship_owner_connections)
        bulk_insert(VoyageSourcesConnection, source_connections)

        # Update the one-to-one references for Voyages' models
        # This is a redundant foreign key, however, this design
        # choice precedes the development of this command.
        def get_raw_sql(related_model, fk_on_voyages, fk_on_related='voyage_id'):
            if target_db == 'mysql':
                update_query_template = 'UPDATE {0}{1}{0} a JOIN {0}{2}{0} b ON a.{0}id{0}=b.{0}{3}{0} ' \
                                        'SET a.{0}{4}{0}=b.{0}id{0}'
            elif target_db == 'pgsql':
                update_query_template = 'UPDATE {0}{1}{0} as a SET {0}{4}{0}=b.{0}id{0} ' \
                                        'FROM {0}{2}{0} as b WHERE a.{0}id{0}=b.{0}{3}{0}'
            sql = update_query_template.format(
                '`' if target_db == 'mysql' else '"',
                Voyage._mkilleta.db_table,
                related_model._meta.db_table,
                fk_on_related,
                fk_on_voyages
            )
            print 'Executing query...'
            print sql
            return sql

        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(get_raw_sql(VoyageShip, 'voyage_ship_id'))
        cursor.execute(get_raw_sql(VoyageItinerary, 'voyage_itinerary_id'))
        cursor.execute(get_raw_sql(VoyageDates, 'voyage_dates_id'))
        cursor.execute(get_raw_sql(VoyageCrew, 'voyage_crew_id'))
        cursor.execute(get_raw_sql(VoyageSlavesNumbers, 'voyage_slaves_numbers_id'))

        print 'Completed - go have fun!'
