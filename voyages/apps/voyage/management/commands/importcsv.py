from django.core.management.base import BaseCommand
from django.utils.encoding import smart_str
from voyages.apps.voyage.models import *
from voyages.apps.resources.models import Image, AfricanName
from unidecode import unidecode
import re
import sys
import unicodecsv

empty = re.compile(r"^\s*$")

class Command(BaseCommand):
    help = 'Imports a CSV file with the full data-set and converts the data to the Django models.'

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
            sys.stderr.write('Supported dbs are "mysql" and "pgsql". Aborting...\n')
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
        africans = list(AfricanName.objects.all())
        images = list(Image.objects.all())

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
            If the row.get(field_name) is None, no errors will be logged.
            :param allowNull: whether the field value is allowed to be None
            :return: The corresponding model, or None if not found.
            """
            val = cint(row.get(field_name), allow_null)
            if val is None:
                return None
            model = prefetch[model_name].get(val)
            if model is None:
                sys.stderr.write('Failed to locate "' + model_name + '" with value: ' + str(val) + \
                      ' for field "' + field_name + '"\n')
                self.errors += 1
            return model

        def filter_out_source_letter(letter):
            return letter == ' ' or letter == ','

        # Prefetch data: Sources
        all_sources = VoyageSources.objects.all()
        trie = {}
        _end = '_end'
        
        def add_to_trie(key, value):
            dict = trie
            for letter in plain:
                if filter_out_source_letter(letter):
                    continue
                dict = dict.setdefault(letter, {})
            dict[_end] = value
            
        for source in all_sources:
            plain = unidecode(source.short_ref).lower()
            add_to_trie(plain, source)

        # This method searches the Sources trie and obtain the
        # Source whose short reference matches the longest
        # prefix of the given reference.
        def get_source(ref):
            best = None
            match = ''
            dict = trie
            plain = unidecode(ref).lower()
            for letter in plain:
                if filter_out_source_letter(letter):
                    continue
                dict = dict.get(letter)
                if dict is None:
                    break
                match += letter
                best = dict.get(_end, best)
            return best, match

        def cint(val, allow_null=True):
            if (val is None or empty.match(val)) and not allow_null:
                self.errors += 1
                return None
            if val is None: return None
            try:
                return int(val)
            except:
                if allow_null: return None
                raise Exception("Invalid value for int: " + str(val))

        def cfloat(val, allow_null=True):
            if (val is None or empty.match(val)) and not allow_null:
                self.errors += 1
                return None
            if val is None: return None
            try:
                return float(val)
            except:
                if allow_null: return None
                raise Exception("Invalid value for float: " + str(val))

        def date_csv(var_name_prefix, suffixes=[u'a', u'b', u'c']):
            """
            Fetches date fields (day, month, year) and produce a CSV
            string in the format MM,DD,YYYY
            :param var_name_prefix: the variable name prefix
            :param suffixes: the day, month, and year suffixes, use None
            to specify that there is no variable corresponding to the
            date component.
            :return: the CSV date.
            """
            return (row.get(var_name_prefix + suffixes[1], '') if suffixes[1] is not None else '').strip() + ',' + \
                   (row.get(var_name_prefix + suffixes[0], '') if suffixes[0] is not None else '').strip() + ',' + \
                   (row.get(var_name_prefix + suffixes[2], '') if suffixes[2] is not None else '').strip()

        def date_iso_csv(iso_value):
            """
            Converts a date in the ISO format YYYY-MM-DD to the
            CSV format MM,DD,YYYY
            :param iso_value: the iso formatted date
            :return: the CSV date
            """
            if iso_value is None or empty.match(iso_value):
                return ''
            components = iso_value.split('-')
            if len(components) != 3:
                components = iso_value.split(',')
            if len(components) != 3:
                self.errors += 1
                sys.stderr.write('Error with date ' + iso_value + '\n')
                return ''
            return components[1].strip() + ',' + components[2].strip() + ',' + components[0].strip()

        import itertools
        def lower_headers(iterator):
            return itertools.chain([next(iterator).lower()], iterator)

        for file in csv_file:
            with open(file, 'rU') as f:
                reader = unicodecsv.DictReader(lower_headers(f), delimiter=',')
                # Ensure lower case is used.
                for row in reader:
                    # Create a voyage corresponding to this row
                    voyage = Voyage()
                    id = cint(row.get(u'voyageid'), False)
                    if id in voyages:
                        sys.stderr.write('Duplicate voyage found: ' + str(id) + '\n')
                        return
                    voyage.voyage_id = id
                    voyages[id] = voyage
                    # Next we set up voyage direct and nested members
                    in_cd_room = row.get(u'evgreen', '0')
                    voyage.voyage_in_cd_rom = in_cd_room == '1' or in_cd_room.lower() == 'true'
                    voyage.voyage_groupings = get_by_value('groupings', 'xmimpflag')
                    voyage.is_intra_american = cint(row.get(u'IntraAmer')) == 1
                    # Ship
                    ship_model = VoyageShip()
                    ship_model.ship_name = row.get(u'shipname')
                    ship_model.nationality_ship = get_by_value('nationalities', 'national')
                    ship_model.tonnage = cint(row.get(u'tonnage'))
                    ship_model.ton_type = get_by_value('ton_types', 'tontype')
                    ship_model.rig_of_vessel = get_by_value('rigs', 'rig')
                    ship_model.guns_mounted = cint(row.get(u'guns'))
                    ship_model.year_of_construction = cint(row.get(u'yrcons'))
                    ship_model.vessel_construction_place = get_by_value('places', 'placcons')
                    ship_model.vessel_construction_region = get_by_value('regions', 'constreg')
                    ship_model.registered_year = cint(row.get(u'yrreg'))
                    ship_model.registered_place = get_by_value('places', 'placreg')
                    ship_model.registered_region = get_by_value('regions', 'regisreg')
                    ship_model.imputed_nationality = get_by_value('nationalities', 'natinimp')
                    ship_model.tonnage_mod = cfloat(row.get(u'tonmod'))
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
                    itinerary.ports_called_buying_slaves = cint(row.get(u'nppretra'))
                    itinerary.first_place_slave_purchase = get_by_value('places', 'plac1tra')
                    itinerary.second_place_slave_purchase = get_by_value('places', 'plac2tra')
                    itinerary.third_place_slave_purchase = get_by_value('places', 'plac3tra')
                    itinerary.first_region_slave_emb = get_by_value('regions', 'regem1')
                    itinerary.second_region_slave_emb = get_by_value('regions', 'regem2')
                    itinerary.third_region_slave_emb = get_by_value('regions', 'regem3')
                    itinerary.port_of_call_before_atl_crossing = get_by_value('places', 'npafttra')
                    itinerary.number_of_ports_of_call = cint(row.get(u'npprior'))
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
                    dates.date_departed_africa = date_iso_csv(row.get(u'dateleftafr'))
                    dates.arrival_at_second_place_landing = date_csv('datarr', ['36', '37', '38'])
                    dates.third_dis_of_slaves = date_csv('datarr', ['39', '40', '41'])
                    dates.departure_last_place_of_landing = date_csv('ddepam', ['', 'b', 'c'])
                    dates.voyage_completed = date_csv('datarr', ['43', '44', '45'])
                    dates.length_middle_passage_days = cint(row.get(u'voyage'))
                    dates.imp_voyage_began = date_csv('yeardep', [None, None, ''])
                    dates.imp_departed_africa = date_csv('yearaf', [None, None, ''])
                    dates.imp_arrival_at_port_of_dis = date_csv('yearam', [None, None, ''])
                    dates.imp_length_home_to_disembark = cint(row.get(u'voy1imp'))
                    dates.imp_length_leaving_africa_to_disembark = cint(row.get(u'voy2imp'))
                    dates.voyage = voyage
                    voyage_dates.append(dates)
                    # voyage.voyage_dates = dates
                    # Crew
                    crew = VoyageCrew()
                    crew.crew_voyage_outset = cint(row.get(u'crew1'))
                    crew.crew_departure_last_port = cint(row.get(u'crew2'))
                    crew.crew_first_landing = cint(row.get(u'crew3'))
                    crew.crew_return_begin = cint(row.get(u'crew4'))
                    crew.crew_end_voyage = cint(row.get(u'crew5'))
                    crew.unspecified_crew = cint(row.get(u'crew'))
                    crew.crew_died_before_first_trade = cint(row.get(u'saild1'))
                    crew.crew_died_while_ship_african = cint(row.get(u'saild2'))
                    crew.crew_died_middle_passage = cint(row.get(u'saild3'))
                    crew.crew_died_in_americas = cint(row.get(u'saild4'))
                    crew.crew_died_on_return_voyage = cint(row.get(u'saild5'))
                    crew.crew_died_complete_voyage = cint(row.get(u'crewdied'))
                    crew.crew_deserted = cint(row.get(u'ndesert'))
                    crew.voyage = voyage
                    crews.append(crew)
                    # voyage.voyage_crew = crew
                    # Slave numbers
                    numbers = VoyageSlavesNumbers()
                    numbers.slave_deaths_before_africa = cint(row.get(u'sladafri'))
                    numbers.slave_deaths_between_africa_america = cint(row.get(u'sladvoy'))
                    numbers.slave_deaths_between_arrival_and_sale = cint(row.get(u'sladamer'))
                    numbers.num_slaves_intended_first_port = cint(row.get(u'slintend'))
                    numbers.num_slaves_intended_second_port = cint(row.get(u'slinten2'))
                    numbers.num_slaves_carried_first_port = cint(row.get(u'ncar13'))
                    numbers.num_slaves_carried_second_port = cint(row.get(u'ncar15'))
                    numbers.num_slaves_carried_third_port = cint(row.get(u'ncar17'))
                    numbers.total_num_slaves_purchased = cint(row.get(u'tslavesp'))
                    numbers.total_num_slaves_dep_last_slaving_port = cint(row.get(u'tslavesd'))
                    numbers.total_num_slaves_arr_first_port_embark = cint(row.get(u'slaarriv'))
                    numbers.num_slaves_disembark_first_place = cint(row.get(u'slas32'))
                    numbers.num_slaves_disembark_second_place = cint(row.get(u'slas36'))
                    numbers.num_slaves_disembark_third_place = cint(row.get(u'slas39'))
                    numbers.imp_total_num_slaves_embarked = cint(row.get(u'slaximp'))
                    numbers.imp_total_num_slaves_disembarked = cint(row.get(u'slamimp'))
                    numbers.imp_jamaican_cash_price = cfloat(row.get(u'jamcaspr'))
                    numbers.imp_mortality_during_voyage = cint(row.get(u'vymrtimp'))
                    numbers.num_men_embark_first_port_purchase = cint(row.get(u'men1'))
                    numbers.num_women_embark_first_port_purchase = cint(row.get(u'women1'))
                    numbers.num_boy_embark_first_port_purchase = cint(row.get(u'boy1'))
                    numbers.num_girl_embark_first_port_purchase = cint(row.get(u'girl1'))
                    numbers.num_adult_embark_first_port_purchase = cint(row.get(u'adult1'))
                    numbers.num_child_embark_first_port_purchase = cint(row.get(u'child1'))
                    numbers.num_infant_embark_first_port_purchase = cint(row.get(u'infant1'))
                    numbers.num_males_embark_first_port_purchase = cint(row.get(u'male1'))
                    numbers.num_females_embark_first_port_purchase = cint(row.get(u'female1'))
                    numbers.num_men_died_middle_passage = cint(row.get(u'men2'))
                    numbers.num_women_died_middle_passage = cint(row.get(u'women2'))
                    numbers.num_boy_died_middle_passage = cint(row.get(u'boy2'))
                    numbers.num_girl_died_middle_passage = cint(row.get(u'girl2'))
                    numbers.num_adult_died_middle_passage = cint(row.get(u'adult2'))
                    numbers.num_child_died_middle_passage = cint(row.get(u'child2'))
                    numbers.num_infant_died_middle_passage = cint(row.get(u'infant2'))
                    numbers.num_males_died_middle_passage = cint(row.get(u'male2'))
                    numbers.num_females_died_middle_passage = cint(row.get(u'female2'))
                    numbers.num_men_disembark_first_landing = cint(row.get(u'men3'))
                    numbers.num_women_disembark_first_landing = cint(row.get(u'women3'))
                    numbers.num_boy_disembark_first_landing = cint(row.get(u'boy3'))
                    numbers.num_girl_disembark_first_landing = cint(row.get(u'girl3'))
                    numbers.num_adult_disembark_first_landing = cint(row.get(u'adult3'))
                    numbers.num_child_disembark_first_landing = cint(row.get(u'child3'))
                    numbers.num_infant_disembark_first_landing = cint(row.get(u'infant3'))
                    numbers.num_males_disembark_first_landing = cint(row.get(u'male3'))
                    numbers.num_females_disembark_first_landing = cint(row.get(u'female3'))
                    numbers.num_men_embark_second_port_purchase = cint(row.get(u'men4'))
                    numbers.num_women_embark_second_port_purchase = cint(row.get(u'women4'))
                    numbers.num_boy_embark_second_port_purchase = cint(row.get(u'boy4'))
                    numbers.num_girl_embark_second_port_purchase = cint(row.get(u'girl4'))
                    numbers.num_adult_embark_second_port_purchase = cint(row.get(u'adult4'))
                    numbers.num_child_embark_second_port_purchase = cint(row.get(u'child4'))
                    numbers.num_infant_embark_second_port_purchase = cint(row.get(u'infant4'))
                    numbers.num_males_embark_second_port_purchase = cint(row.get(u'male4'))
                    numbers.num_females_embark_second_port_purchase = cint(row.get(u'female4'))
                    numbers.num_men_embark_third_port_purchase = cint(row.get(u'men5'))
                    numbers.num_women_embark_third_port_purchase = cint(row.get(u'women5'))
                    numbers.num_boy_embark_third_port_purchase = cint(row.get(u'boy5'))
                    numbers.num_girl_embark_third_port_purchase = cint(row.get(u'girl5'))
                    numbers.num_adult_embark_third_port_purchase = cint(row.get(u'adult5'))
                    numbers.num_child_embark_third_port_purchase = cint(row.get(u'child5'))
                    numbers.num_infant_embark_third_port_purchase = cint(row.get(u'infant5'))
                    numbers.num_males_embark_third_port_purchase = cint(row.get(u'male5'))
                    numbers.num_females_embark_third_port_purchase = cint(row.get(u'female5'))
                    numbers.num_men_disembark_second_landing = cint(row.get(u'men6'))
                    numbers.num_women_disembark_second_landing = cint(row.get(u'women6'))
                    numbers.num_boy_disembark_second_landing = cint(row.get(u'boy6'))
                    numbers.num_girl_disembark_second_landing = cint(row.get(u'girl6'))
                    numbers.num_adult_disembark_second_landing = cint(row.get(u'adult6'))
                    numbers.num_child_disembark_second_landing = cint(row.get(u'child6'))
                    numbers.num_infant_disembark_second_landing = cint(row.get(u'infant6'))
                    numbers.num_males_disembark_second_landing = cint(row.get(u'male6'))
                    numbers.num_females_disembark_second_landing = cint(row.get(u'female6'))
                    numbers.imp_num_adult_embarked = cint(row.get(u'adlt1imp'))
                    numbers.imp_num_children_embarked = cint(row.get(u'chil1imp'))
                    numbers.imp_num_male_embarked = cint(row.get(u'male1imp'))
                    numbers.imp_num_female_embarked = cint(row.get(u'feml1imp'))
                    numbers.total_slaves_embarked_age_identified = cint(row.get(u'slavema1'))
                    numbers.total_slaves_embarked_gender_identified = cint(row.get(u'slavemx1'))
                    numbers.imp_adult_death_middle_passage = cint(row.get(u'adlt2imp'))
                    numbers.imp_child_death_middle_passage = cint(row.get(u'chil2imp'))
                    numbers.imp_male_death_middle_passage = cint(row.get(u'male2imp'))
                    numbers.imp_female_death_middle_passage = cint(row.get(u'feml2imp'))
                    numbers.imp_num_adult_landed = cint(row.get(u'adlt3imp'))
                    numbers.imp_num_child_landed = cint(row.get(u'chil3imp'))
                    numbers.imp_num_male_landed = cint(row.get(u'male3imp'))
                    numbers.imp_num_female_landed = cint(row.get(u'feml3imp'))
                    numbers.total_slaves_landed_age_identified = cint(row.get(u'slavema3'))
                    numbers.total_slaves_landed_gender_identified = cint(row.get(u'slavemx3'))
                    numbers.total_slaves_dept_or_arr_age_identified = cint(row.get(u'slavema7'))
                    numbers.total_slaves_dept_or_arr_gender_identified = cint(row.get(u'slavemx7'))
                    numbers.imp_slaves_embarked_for_mortality = cint(row.get(u'tslmtimp'))
                    numbers.imp_num_men_total = cint(row.get(u'men7'))
                    numbers.imp_num_women_total = cint(row.get(u'women7'))
                    numbers.imp_num_boy_total = cint(row.get(u'boy7'))
                    numbers.imp_num_girl_total = cint(row.get(u'girl7'))
                    numbers.imp_num_adult_total = cint(row.get(u'adult7'))
                    numbers.imp_num_child_total = cint(row.get(u'child7'))
                    numbers.imp_num_males_total = cint(row.get(u'male7'))
                    numbers.imp_num_females_total = cint(row.get(u'female7'))
                    numbers.percentage_men = cfloat(row.get(u'menrat7'))
                    numbers.percentage_women = cfloat(row.get(u'womrat7'))
                    numbers.percentage_boy = cfloat(row.get(u'boyrat7'))
                    numbers.percentage_girl = cfloat(row.get(u'girlrat7'))
                    numbers.percentage_male = cfloat(row.get(u'malrat7'))
                    numbers.percentage_child = cfloat(row.get(u'chilrat7'))
                    numbers.percentage_adult = 1 - numbers.percentage_child \
                        if numbers.percentage_child is not None else None
                    numbers.percentage_female = 1 - numbers.percentage_male \
                        if numbers.percentage_male is not None else None
                    numbers.imp_mortality_ratio = cfloat(row.get(u'vymrtrat'))
                    numbers.voyage = voyage
                    voyage_numbers.append(numbers)
                    # voyage.voyage_slaves_numbers = numbers
                    # Captains
                    order = 1
                    for key in 'abc':
                        captain_name = row.get(u'captain' + key)
                        if captain_name is None or empty.match(captain_name):
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
                        owner_name = row.get(u'owner' + key)
                        if owner_name is None or empty.match(owner_name):
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
                        source_ref = row.get(u'source' + key)
                        if source_ref is None or empty.match(source_ref):
                            break
                        (source, match) = get_source(source_ref)
                        if source is None:
                            self.errors += 1
                            sys.stderr.write('Source not found for "' + smart_str(source_ref) +
                                            '", longest partial match: ' + smart_str(match) + '\n')
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

        quote_char = '`' if target_db == 'mysql' else '"'
        
        from django.db import connection 
        cursor = connection.cursor()

        def clear_fk(fk_field):
            sql = 'UPDATE {0}{1}{0} SET {0}{2}{0}=NULL'
            sql = sql.format(quote_char, Voyage._meta.db_table, fk_field)
            print sql
            cursor.execute(sql)

        def delete_all(model):
            sql = 'DELETE FROM {0}' + model._meta.db_table + '{0}'
            sql = sql.format(quote_char)
            print sql
            cursor.execute(sql)

        clear_fk('voyage_ship_id')
        clear_fk('voyage_itinerary_id')
        clear_fk('voyage_dates_id')
        clear_fk('voyage_crew_id')
        clear_fk('voyage_slaves_numbers_id')
        delete_all(VoyageCaptainConnection)
        delete_all(VoyageShipOwnerConnection)
        delete_all(VoyageSourcesConnection)
        delete_all(VoyageCaptain)
        delete_all(VoyageCrew)
        delete_all(VoyageDates)
        delete_all(VoyageItinerary)
        delete_all(VoyageOutcome)
        delete_all(VoyageShip)
        delete_all(VoyageShipOwner)
        delete_all(VoyageSlavesNumbers)
        delete_all(AfricanName)
        delete_all(Image)
        delete_all(Voyage)

        print 'Inserting new records...'

        def bulk_insert(model, lst, attr_key=None, manager=None):
            print 'Bulk inserting ' + str(model)
            if manager is None:
                manager = model.objects
            manager.bulk_create(lst, batch_size=100)
            return None if attr_key is None else \
                {getattr(x, attr_key): x for x in manager.all()}

        voyages = bulk_insert(Voyage, voyages.values(), 'voyage_id', Voyage.both_objects)
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
        bulk_insert(AfricanName, africans)
        bulk_insert(Image, images)

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
                quote_char,
                Voyage._meta.db_table,
                related_model._meta.db_table,
                fk_on_related,
                fk_on_voyages
            )
            print 'Executing query...'
            print sql
            return sql

        cursor.execute(get_raw_sql(VoyageShip, 'voyage_ship_id'))
        cursor.execute(get_raw_sql(VoyageItinerary, 'voyage_itinerary_id'))
        cursor.execute(get_raw_sql(VoyageDates, 'voyage_dates_id'))
        cursor.execute(get_raw_sql(VoyageCrew, 'voyage_crew_id'))
        cursor.execute(get_raw_sql(VoyageSlavesNumbers, 'voyage_slaves_numbers_id'))

        print "Completed! Don't forget to rebuild_index on Solr."
