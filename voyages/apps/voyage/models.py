from django.db import models
from django.utils.translation import ugettext as _


class Voyage(models.Model):
    """
    Information about voyages.
    """

    class BroadRegion(models.Model):
        """
        Broad Regions (continents).
        """

        broad_region = models.CharField("Broad region", max_length=35)

    class SpecificRegion(models.Model):
        """
        Specific Regions (countries or colonies).
        related to: :model:`voyages.apps.voyages.Voyage.BroadRegion`
        """

        specific_region = models.CharField("Specific region (country or colony",
                                           max_length=35)
        broad = models.ForeignKey('BroadRegion')

    class Place(models.Model):
        """
        Place (port or location).
        related to: :model:`voyages.apps.voyages.Voyage.BroadRegion`
        related to: :model:`voyages.apps.voyages.Voyage.SpecificRegion`
        """
        place_name = models.CharField(max_length=35)
        broad_region = models.ForeignKey('BroadRegion')
        specific_region = models.ForeignKey('SpecificRegion')

    class VoyageGroupings(models.Model):
        """
        Labels for groupings names.
        """
        grouping_name = models.CharField(max_length=30)

    class VoyageShip(models.Model):
        """
        Information about voyage ship.
        related to: :model:`voyages.apps.voyages.Voyage.SpecificRegion`
        related to: :model:`voyages.apps.voyages.Voyage.Place`

        """

        class VoyageVentureOwner(models.Model):
            """
            Information about other owners.
            """
            number_of_owner = models.IntegerField(max_length=2, blank=True)
            name_of_owner = models.CharField(max_length=40)

        class NationalityOfShip(models.Model):
            """
            Nationalities of ships.
            """
            nationality_of_ship = models.CharField(max_length=35)

        class ImputedCountryShip(models.Model):
            """
            Imputed country in which ship registered.
            """
            imputed_country = models.CharField("Imputed country "
                                               "in which ship registered.",
                                               max_length=35)

        class TonType(models.Model):
            """
            Types of tonnage.
            """
            ton_type = models.CharField(max_length=35)

        class RigOfVessel(models.Model):
            """
            Rig of Vessel.
            """
            rig_of_vessel = models.CharField(max_length=25)

        # Data variables
        ship_name = models.CharField("Name of vessel", max_length=60)
        nationality = models.ForeignKey('NationalityOfShip')
        tonnage = models.IntegerField("Tonnage of vessel", max_length=4,
                                      blank=True)
        ton_type = models.ForeignKey('TonType')
        rig_of_vessel = models.ForeignKey('RigOfVessel')
        guns_mounted = models.IntegerField("Guns mounted", max_length=2,
                                           blank=True)
        year_of_construction = models.DateField \
                ("Year of vessel's construction")
        vessel_construction_place = models.ForeignKey \
                ('Place', related_name="vessel_construction_place")
        vessel_construction_region = models.ForeignKey \
                ('SpecificRegion', related_name="vessel_construction_region")
        registered_year = models.DateField("Year of vessel's registration")
        registered_place = models.ForeignKey \
                ('Place', related_name="registered_place")
        registered_region = models.ForeignKey \
                ('SpecificRegion', related_name="registered_region")
        owner_of_venture = models.CharField("First owner of venture", max_length=60)
        owners = models.ForeignKey('VoyageVentureOwner')

        # Imputed variables
        imputed_nationality = models.ForeignKey('ImputedCountryShip')
        tonnage_mod = models.DecimalField("Tonnage standardized on British"
                                          "measured tons, 1773-1835",
                                          max_digits=8,
                                          decimal_places=2,
                                          blank=True)


    class VoyageOutcome(models.Model):
        """
        Information about Outcomes
        """

        class ParticularOutcome(models.Model):
            """
            Particular outcome.
            """
            particular_outcome = models.CharField("Outcome label", max_length=70)

        class SlavesOutcome(models.Model):
            """
            Outcome of voyage for slaves.
            """
            slaves_outcome = models.CharField("Outcome label", max_length=70)

        class VesselCapturedOutcome(models.Model):
            """
            Outcome of voyage if vessel captured.
            """
            vessel_captured_outcome = models.CharField("Outcome label",
                                                       max_length=35)

        class OwnerOutcome(models.Model):
            """
            Outcome of voyage for owner.
            """
            owner_outcome = models.CharField("Outcome label", max_length=35)

        class Resistance(models.Model):
            """
            Resistance labels
            """
            resistance_name = models.CharField("Resistance label", max_length=35)

        # Data variables
        particular_outcome = models.ForeignKey('ParticularOutcome')
        resistance = models.ForeignKey('Resistance')

        # Imputed variables
        outcome_slaves = models.ForeignKey('SlavesOutcome')
        vessel_captured_outcome = models.ForeignKey('VesselCapturedOutcome')
        outcome_owner = models.ForeignKey('OwnerOutcome')


    class VoyageItinerary(models.Model):
        """
        Voyage Itinerary data.
        related to: :model:`voyages.apps.voyages.Voyage.BroadRegion`
        related to: :model:`voyages.apps.voyages.Voyage.SpecificRegion`
        related to: :model:`voyages.apps.voyages.Voyage.Place`
        """

        # Data variables
        port_of_departure = models.ForeignKey \
                ('Place', related_name="port_of_departure")
        # Intended variables
        int_first_port_emb = models.ForeignKey \
                ('Place', related_name="int_first_port_emb")
        int_second_port_emb = models.ForeignKey \
                ('Place', related_name="int_second_port_emb")
        int_first_region_purchase_slaves = models.ForeignKey \
                ('SpecificRegion',
                 related_name="int_first_region_purchase_slaves")
        int_second_region_purchase_slaves = models.ForeignKey \
                ('SpecificRegion',
                 related_name="int_second_region_purchase_slaves")
        int_first_port_dis = models.ForeignKey('Place',
                                               related_name=
                                               "int_first_port_dis")
        int_second_port_dis = models.ForeignKey('Place',
                                                related_name=
                                                "int_second_port_dis")
        int_first_region_slave_landing = models.ForeignKey \
                ('SpecificRegion', related_name="int_first_region_slave_landing")
        int_second_region_slave_landing = models.ForeignKey \
                ('SpecificRegion', related_name="int_second_region_slave_landing")

        # End of intended variables
        ports_called_buying_slaves = models.IntegerField("Number of ports "
                                                         "of call prior "
                                                         "to buying slaves",
                                                         max_length=3,
                                                         blank=True)
        first_place_slave_purchase = models.ForeignKey \
                ('Place', related_name="first_place_slave_purchase")
        second_place_slave_purchase = models.ForeignKey \
                ('Place', related_name="second_place_slave_purchase")
        third_place_slave_purchase = models.ForeignKey \
                ('Place', related_name="third_place_slave_purchase")

        first_region_slave_emb = models.ForeignKey('SpecificRegion',
                                                   related_name=
                                                   "first_region_slave_emb")
        second_region_slave_emb = models.ForeignKey('SpecificRegion',
                                                    related_name=
                                                    "second_region_slave_emb")
        third_region_slave_emb = models.ForeignKey('SpecificRegion',
                                                   related_name=
                                                   "third_region_slave_emb")

        port_of_call_before_atl_crossing = models.ForeignKey \
                ('Place', related_name="port_of_call_before_atl_crossing")
        number_of_ports_of_call = models.ForeignKey \
                ('Place', related_name="number_of_ports_of_call")

        first_landing_place = models.ForeignKey \
                ('Place', related_name="first_landing_place")
        second_landing_place = models.ForeignKey \
                ('Place', related_name="second_landing_place")
        third_landing_place = models.ForeignKey \
                ('Place', related_name="third_landing_place")

        first_landing_region = models.ForeignKey \
                ('SpecificRegion', related_name="first_landing_region")
        second_landing_region = models.ForeignKey \
                ('SpecificRegion', related_name="second_landing_region")
        third_landing_region = models.ForeignKey \
                ('SpecificRegion', related_name="third_landing_region")

        place_voyage_ended = models.ForeignKey \
                ('Place', related_name="place_voyage_ended")
        region_of_return = models.ForeignKey \
                ('SpecificRegion', related_name="region_of_return")
        broad_region_of_return = models.ForeignKey \
                ('BroadRegion', related_name="broad_region_of_return")

        # Imputed variables
        imp_port_voyage_begin = models.ForeignKey \
                ('Place', related_name="imp_port_voyage_begin")
        imp_region_voyage_begin = models.ForeignKey \
                ('SpecificRegion', related_name="imp_region_voyage_begin")
        imp_broad_region_voyage_begin = models.ForeignKey \
                ('BroadRegion', related_name="imp_broad_region_voyage_begin")
        principal_place_of_slave_purchase = models.ForeignKey \
                ('Place', related_name="principal_place_of_slave_purchase")
        imp_principal_place_of_slave_purchase = models.ForeignKey \
                ('Place', related_name="imp_principal_place_of_slave_purchase")
        imp_principal_region_of_slave_purchase = models.ForeignKey \
                ('SpecificRegion', related_name=
            "imp_principal_region_of_slave_purchase")
        imp_broad_region_of_slave_purchase = models. \
            ForeignKey('BroadRegion', related_name=
        "imp_broad_region_of_slave_purchase")
        principal_port_of_slave_dis = models.ForeignKey \
                ('Place', related_name="principal_port_of_slave_dis")
        imp_principal_port_slave_dis = models.ForeignKey \
                ('Place', related_name="imp_principal_port_slave_dis")
        imp_principal_region_slave_dis = models.ForeignKey \
                ('SpecificRegion', related_name=""
                                                "imp_principal_region_slave_dis")
        imp_broad_region_slave_dis = models.ForeignKey \
                ('BroadRegion', related_name="imp_broad_region_slave_dis")


    class VoyageDates(models.Model):
        """
        Voyage dates.
        """

        class IntegerDate(models.Model):
            """
            Date in integer numbers
            """
            day = models.IntegerField()

        # Data variables
        # Integer variables
        day_voyage_began = models.IntegerField \
                ("Day that voyage began", max_length=2, blank=True)
        month_voyage_began = models.IntegerField \
                ("Month that voyage began", max_length=2, blank=True)
        year_voyage_began = models.IntegerField \
                ("Year that voyage began", max_length=4, blank=True)
        day_slave_purchase_began = models.IntegerField \
                ("Day that slave purchase began", max_length=2, blank=True)
        month_slave_purchase_began = models.IntegerField \
                ("Month that slave purchase began", max_length=2, blank=True)
        year_slave_purchase_began = models.IntegerField \
                ("Year that slave purchase began", max_length=4, blank=True)
        day_vessel_left_port = models.IntegerField \
                ("Day that vessel left last slaving port", max_length=2,
                 blank=True)
        month_vessel_left_port = models.IntegerField \
                ("Month that vessel left last slaving port", max_length=2,
                 blank=True)
        year_vessel_left_port = models.IntegerField \
                ("Year that vessel left last slaving port", max_length=4,
                 blank=True)
        day_first_dis_of_slaves = models.IntegerField \
                ("Day of first disembarkation of slaves", max_length=2,
                 blank=True)
        month_first_dis_of_slaves = models.IntegerField \
                ("Month of first disembarkation of slaves", max_length=2,
                 blank=True)
        year_first_dis_of_slaves = models.IntegerField \
                ("Year of first disembarkation of slaves", max_length=4,
                 blank=True)
        day_arrival_at_second_place_landing = models.IntegerField \
                ("Day of arrival at second place of landing", max_length=2,
                 blank=True)
        month_arrival_at_second_place_landing = models.IntegerField \
                ("Month of arrival at second place of landing", max_length=2,
                 blank=True)
        year_arrival_at_second_place_landing = models.IntegerField \
                ("Year of arrival at second place of landing", max_length=4,
                 blank=True)
        day_third_dis_of_slaves = models.IntegerField \
                ("Day of third disembarkation of slaves", max_length=2,
                 blank=True)
        month_third_dis_of_slaves = models.IntegerField \
                ("Month of third disembarkation of slaves", max_length=2,
                 blank=True)
        year_third_dis_of_slaves = models.IntegerField \
                ("Year of third disembarkation of slaves", max_length=4,
                 blank=True)
        day_departure_last_place_of_landing = models.IntegerField \
                ("Day of departure from last place of landing", max_length=2,
                 blank=True)
        month_departure_last_place_of_landing = models.IntegerField \
                ("Month of departure from last place of landing", max_length=2,
                 blank=True)
        year_departure_last_place_of_landing = models.IntegerField \
                ("Year of departure from last place of landing", max_length=4,
                 blank=True)
        day_voyage_completed = models.IntegerField \
                ("Day on which slave voyage completed", max_length=2,
                 blank=True)
        month_voyage_completed = models.IntegerField \
                ("Month on which slave voyage completed", max_length=2,
                 blank=True)
        year_voyage_completed = models.IntegerField \
                ("Year on which slave voyage completed", max_length=4,
                 blank=True)

        # Date variables
        voyage_began = models.DateField("Date that voyage began")
        slave_purchase_began = models.DateField \
                ("Date that slave purchase began")
        vessel_left_port = models.DateField \
                ("Date that vessel left last slaving port")
        first_dis_of_slaves = models.DateField \
                ("Date of first disembarkation of slaves")
        arrival_at_second_place_landing = models.DateField \
                ("Date of arrival at second place of landing")
        third_dis_of_slaves = models.DateField \
                ("Date of third disembarkation of slaves")
        departure_last_place_of_landing = models.DateField \
                ("Date of departure from last place of landing")
        voyage_completed = models.DateField \
                ("Date on which slave voyage completed")

        # Imputed variables
        imp_voyage_began = models.IntegerField \
                ("Year voyage began", max_length=4, blank=True)
        imp_departed_africa = models.IntegerField \
                ("Year departed Africa", max_length=4, blank=True)
        imp_arrival_at_port_of_dis = models.IntegerField \
                ("Year of arrival at port of disembarkation",
                 max_length=4, blank=True)
        five_year_period = models.IntegerField \
                ("5-year period in which voyage occurred",
                 max_length=3, blank=True)
        decade_of_voyage = models.IntegerField \
                ("Decade in which voyage occurred",
                 max_length=3, blank=True)
        quarter_century_of_voyage = models.IntegerField \
                ("Quarter-century in which voyage occurred",
                 max_length=3, blank=True)
        century_of_voyage = models.IntegerField \
                ("Century in which voyage occurred",
                 max_length=4, blank=True)
        voyage_length_home_to_dis = models.IntegerField \
                ("Voyage length from home port to disembarkation (days)",
                 max_length=5, blank=True)
        voyage_length_africa_to_dis = models.IntegerField \
                ("Voyage length from leaving Africa to disembarkation (days)",
                 max_length=5, blank=True)

    class VoyageCaptainCrew(models.Model):
        """
        Voyage Captain and Crew.
        """

        class Captain(models.Model):
            """
            Captain information (name).
            """
            name = models.CharField("Captain's name", max_length=60)

        # Data variables
        first_captain = models.ManyToManyField \
                (Captain, related_name="first_captain")
        second_captain = models.ManyToManyField \
                (Captain, related_name="second captain")
        third_captain = models.ManyToManyField \
                (Captain, related_name="third_captain")

        crew_voyage_outset = models.IntegerField("Crew at voyage outset",
                                                 max_length=3, blank=True)
        crew_departure_last_port = models.IntegerField \
                ("Crew at departure from last port of slave purchase",
                 max_length=3, blank=True)
        crew_first_landing = models.IntegerField \
                ("Crew at first landing of slaves", max_length=2, blank=True)
        crew_return_begin = models.IntegerField \
                ("Crew when return voyage begin", max_length=2, blank=True)
        crew_end_voyage = models.IntegerField \
                ("Crew at end of voyage", max_length=2, blank=True)
        unspecified_crew = models.IntegerField \
                ("Number of crew unspecified", max_length=3, blank=True)
        crew_died_before_first_trade = models.IntegerField \
                ("Crew died before first place of trade in Africa",
                 max_length=2, blank=True)
        crew_died_while_ship_african = models.IntegerField \
                ("Crew died while ship was on African coast",
                 max_length=2, blank=True)

        crew_died_middle_passge = models.IntegerField \
                ("Crew died during Middle Passage", max_length=2, blank=True)
        crew_died_in_americas = models.IntegerField \
                ("Crew died in the Americas", max_length=2, blank=True)
        crew_died_on_return_voyage = models.IntegerField \
                ("Crew died on return voyage", max_length=2, blank=True)
        crew_died_complete_voyage = models.IntegerField \
                ("Crew died during complete voyage", max_length=3, blank=True)
        crew_deserted = models.IntegerField \
                ("Total number of crew deserted", max_length=2, blank=True)

    class VoyageSlaveNumber(models.Model):
        """
        Voyage slaves (numbers).
        """
        num_slaves_intended_first_port = models.IntegerField \
                ("Number of slaves intended from first port of purchase", null=True, blank=True)
        num_slaves_intended_second_port = models.IntegerField \
                ("Number of slaves intended from second port of purchase", null=True, blank=True)

        num_slaves_carried_first_port = models.IntegerField \
                ("Number of slaves carried from first port of purchase", null=True, blank=True)
        num_slaves_carried_second_port = models.IntegerField \
                ("Number of slaves carried from second port of purchase", null=True, blank=True)
        num_slaves_carried_third_port = models.IntegerField \
                ("Number of slaves carried from third port of purchase", null=True, blank=True)

        total_num_slaves_purchased = models.IntegerField \
                ("Total slaves purchased", null=True, blank=True)
        total_num_slaves_dep_last_slaving_port = models.IntegerField \
                ("Total slaves on board at departure from last slaving port", null=True, blank=True)

        total_num_slaves_arr_first_port_embark = models.IntegerField \
                ("Total slaves arrived at first port of disembarkation", null=True, blank=True)

        num_slaves_disembark_first_place = models.IntegerField \
                ("Number of slaves disembarked at first place", null=True, blank=True)
        num_slaves_disembark_second_place = models.IntegerField \
                ("Number of slaves disembarked at second place", null=True, blank=True)
        num_slaves_disembark_third_place = models.IntegerField \
                ("Number of slaves disembarked at third place", null=True, blank=True)


    class VoyageSlavesCharacteristics(models.Model):
        """
        Voyage slaves (characteristics).
        """

        class GroupComposition(models.Model):
            """
            Basic composition of a group of slaves
                used by 'Voyage.VoyageSlavesCharacteristics'
            """
            # Representing MEN* variables
            num_men = models.IntegerField \
                    ("Number of men (MEN*)", null=True, blank=True)
            # Representing WOMEN* variables
            num_women = models.IntegerField \
                    ("Number of women (WOMEN*)", null=True, blank=True)
            # Representing BOY* variables
            num_boy = models.IntegerField \
                    ("Number of boys (BOY*)", null=True, blank=True)
            # Representing GIRL* variables
            num_girl = models.IntegerField \
                    ("Number of girls (GIRL*)", null=True, blank=True)
            # Representing ADULT* variables
            num_adult = models.IntegerField \
                    ("Number of adults (gender unspecified) (ADULT*)", null=True, blank=True)
            # Representing CHILD* variables
            num_child = models.IntegerField \
                    ("Number of children (gender unspecified) (CHILD*)", null=True, blank=True)
            # Representing INFANT* variables
            num_infant = models.IntegerField \
                    ("Number of infants (INFANT*)", null=True, blank=True)
            # Representing MALE* variables
            num_males = models.IntegerField \
                    ("Number of males (age unspecified) (MALE*)", null=True, blank=True)
            # Representing FEMALE* variables
            num_females = models.IntegerField \
                    ("Number of females (age unspecified) (FEMALE*)", null=True, blank=True)

        # Group *1 (MEN1, WOMEN1, BOY1, ... FEMALE1)
        embarked_first_port_purchase = models.OneToOneField\
                ('GroupComposition',
                 help_text="Number embarked at first port of purchase (Group *1)",
                 related_name="embarked_first_port_purchase")

        # Group *4
        embarked_second_port_purchase = models.OneToOneField\
                ('GroupComposition',
                 help_text="Number embarked at second port of purchase (Group *4)",
                 related_name="embarked_second_port_purchase")

        # Group *5
        embarked_third_port_purchase = models.OneToOneField \
                ('GroupComposition',
                 help_text="Number embarked at third port of purchase (Group *5)",
                 related_name="embarked_third_port_purchase")

        # Group *2
        died_on_middle_passage = models.OneToOneField \
                ('GroupComposition',
                 help_text="Number died on Middle Passage (Group *2)", related_name="died_on_middle_passage")

        # Group *3
        disembarked_first_place = models.OneToOneField \
                ('GroupComposition',
                 help_text="Number disembarked at first place of landing (Group *3)",
                 related_name="disembarked_first_place")

        # Group *6
        disembarked_second_place = models.OneToOneField \
                ('GroupComposition',
                 help_text="Number disembarked at second place of landing", related_name="disembarked_second_place")
        slave_deaths_before_africa = models.IntegerField \
                ("Slaves death before leaving Africa")
        slave_deaths_between_africa_america = models.IntegerField \
                ("Slaves death between Africa and Americas")
        slave_deaths_between_africa_america = models.IntegerField \
                ("Slaves death before arrival and sale")

    class VoyageSources(models.Model):
        """
        Voyage sources.
        Representing the original variables SOURCEA, SOURCEB, SOURCEC and etc to SOURCER
        """
        source_unique_ref = models.CharField(_('Short reference'), max_length=40, unique=True)
        # Might contain HTML text formatting
        source_full_ref = models.CharField(_('Full reference'), max_length=500)

    class SourceVoyageConnection(models.Model):
        """
        Represents the relationship between Voyage and Voyage.VoyageSources
        source_order determines the order sources appear for each voyage
        """
        source = models.ForeignKey('VoyageSources', related_name="source")
        group = models.ForeignKey('Voyage', related_name="group")
        source_order = models.IntegerField(max_length=2)

    voyage_id = models.AutoField(primary_key=True)
    voyage_in_cdrom = models.IntegerField("Voyage in 1999 CD-ROM", max_length=1,
                                          blank=True)
    voyage_groupings = models.OneToOneField('VoyageGroupings')
    voyage_outcome = models.OneToOneField('VoyageShip')

    # One Voyage can contain multiple sources and 
    voyage_sources = models.ManyToManyField('VoyageSources', \
                                            through='SourceVoyageConnection', related_name='voyage_sources')

    voyage_slave_number = models.OneToOneField \
            ('VoyageSlaveNumber', help_text="Slaves (numbers) of the voyage", \
             related_name='voyage_slave_number')
    voyage_slave_characteristics = models.OneToOneField \
            ('VoyageSlavesCharacteristics', help_text="Slaves (Characteristics) of the voyage", \
             related_name='voyage_slave_characteristics')
