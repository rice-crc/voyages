from __future__ import print_function, unicode_literals

from builtins import input, next, str

from django.core.management.base import BaseCommand
from django.db import connection
from django.db import transaction
from django.utils.encoding import smart_str

from voyages.apps.resources.models import AfricanName, Image
from voyages.apps.voyage.models import (BroadRegion, LinkedVoyages,
                                        Nationality, OwnerOutcome,
                                        ParticularOutcome, Place, Region,
                                        Resistance, RigOfVessel, SlavesOutcome,
                                        TonType, VesselCapturedOutcome, Voyage,
                                        VoyageCaptain, VoyageCaptainConnection,
                                        VoyageCrew, VoyageDates,
                                        VoyageGroupings, VoyageItinerary,
                                        VoyageOutcome, VoyageShip,
                                        VoyageShipOwner,
                                        VoyageShipOwnerConnection,
                                        VoyageSlavesNumbers, VoyageSources,
                                        VoyageSourcesConnection)
from voyages.apps.common.utils import *

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
        crews = []
        itineraries = []
        outcomes = []
        ships = []
        voyage_dates = []
        voyage_numbers = []

        # Prefetch data: Miscellaneous
        africans = list(AfricanName.objects.all())
        images = list(Image.objects.all())

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
            return get_component(suffixes[1], 2) + ',' + \
                get_component(suffixes[0], 2) + ',' + \
                get_component(suffixes[2], 4)

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
                return f'{month},{day},{year}'
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
                    intra_american = voyage.dataset == 1
                    counts[voyage.dataset] = counts.get(voyage.dataset, 0) + 1
                    ships.append(row_to_ship(rh, voyage))
                    itineraries.append(row_to_itinerary(rh, voyage))
                    voyage_dates.append(row_to_dates(rh, voyage))
                    crews.append(row_to_crew(rh, voyage))
                    voyage_numbers.append(row_to_numbers(rh, voyage))
                    # Captains
                    order = 1
                    for key in get_multi_valued_column_suffix(3):
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
                        captain_connection.captain_order = order
                        captain_connection.voyage = voyage
                        captain_connections.append(captain_connection)
                        order += 1
                    # Ship owners
                    order = 1
                    for key in get_multi_valued_column_suffix(45):
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
                        owner_connection.owner_order = order
                        owner_connection.voyage = voyage
                        ship_owner_connections.append(owner_connection)
                        order += 1
                    # Sources
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
                                'voyage id: ' + str(voyage_id) + ' '
                                'source_ref: '
                                '"' + smart_str(source_ref) + '"'
                                ', longest partial '
                                'match: ' + smart_str(match))
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
                    if intra_american and 'voyageid2' in rh.row:
                        voyage_links.append(
                            (voyage_id, rh.cint('voyageid2'),
                             LinkedVoyages.INTRA_AMERICAN_LINK_MODE))

        print('Constructed ' + str(len(voyages)) + ' voyages from CSV')
        for k, v in counts.items():
            print('Dataset ' + str(k) + ': ' + str(v))
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
                helper.delete_all(cursor, AfricanName)
                helper.delete_all(cursor, Image)
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
                bulk_insert(AfricanName, africans)
                bulk_insert(Image, images)

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
