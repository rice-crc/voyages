from django.db import models
from django.utils.translation import ugettext as _

# Voyage Regions and Places
class BroadRegion(models.Model):
    """
    Broad Regions (continents).
    """

    name = models.CharField("Broad region", max_length=35)
    code = models.IntegerField("Numeric code", max_length=5)

    class Meta:
        verbose_name = 'Broad Region'
        verbose_name_plural = "Broad Regions"

    def __unicode__(self):
        return self.name


class Region(models.Model):
    """
    Specific Regions (countries or colonies).
    related to: :model:
    `voyages.apps.voyages.Voyage.GeoLocation.BroadRegion`
    """

    name = models.CharField("Specific region (country or colony",
                                               max_length=35)
    broad_region = models.ForeignKey('BroadRegion')
    code = models.IntegerField("Numeric code", max_length=5)

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = "Regions"

    def __unicode__(self):
        return self.name


class Place(models.Model):
    """
    Place (port or location).
    related to: :model:
    `voyages.apps.voyages.Voyage.GeoLocation.Region`
    """

    name = models.CharField(max_length=35)
    region = models.ForeignKey('Region')
    code = models.IntegerField("Numeric code", max_length=5)
    longtitude = models.DecimalField("Longtitude of point",
                                     max_length=7, max_digits=3, decimal_places=3,
                                     blank=True)
    latitude = models.DecimalField("Latitude of point",
                                     max_length=7, max_digits=3, decimal_places=3,
                                     blank=True)

    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = "Places"

    def __unicode__(self):
        return self.name


# Voyage Groupings
class VoyageGroupings(models.Model):
    """
    Labels for groupings names.
    """
    grouping_name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Grouping for estimating imputed slaves"
        verbose_name_plural = "Groupings for estimating imputed slaves"

    def __unicode__(self):
        return self.grouping_name


# Voyage Ship, Nation, Owners
class VoyageShip(models.Model):
    """
    Information about voyage ship.
    related to: :model:`voyages.apps.voyages.Voyage.SpecificRegion`
    related to: :model:`voyages.apps.voyages.Voyage.Place`
    """

    class Nationality(models.Model):
        """
        Nationalities of ships.
        """
        nationality = models.CharField(max_length=70)
        code = models.IntegerField(max_length=2)

        def __unicode__(self):
            return self.nationality

    class TonType(models.Model):
        """
        Types of tonnage.
        """
        ton_type = models.CharField(max_length=35)
        code = models.IntegerField(max_length=2)

        def __unicode__(self):
            return self.ton_type

    class RigOfVessel(models.Model):
        """
        Rig of Vessel.
        """
        rig_of_vessel = models.CharField(max_length=25)
        code = models.IntegerField(max_length=2)

        def __unicode__(self):
            return self.rig_of_vessel

    # Data variables
    ship_name = models.CharField("Name of vessel", max_length=60,
                                 null=True, blank=True)
    nationality_ship = models.ForeignKey('Nationality',
                                         related_name="nationality_ship",
                                         null=True, blank=True)
    tonnage = models.IntegerField("Tonnage of vessel", max_length=4,
                                  null=True, blank=True)
    ton_type = models.ForeignKey('TonType', null=True, blank=True)
    rig_of_vessel = models.ForeignKey('RigOfVessel', null=True, blank=True)
    guns_mounted = models.IntegerField("Guns mounted", max_length=2,
                                       null=True, blank=True)
    year_of_construction = models.IntegerField\
            ("Year of vessel's construction", max_length=4,
             null=True, blank=True)
    vessel_construction_place = models.ForeignKey \
            ('Place', related_name="vessel_construction_place",
             null=True, blank=True)
    vessel_construction_region = models.ForeignKey \
            ('Region', related_name="vessel_construction_region",
             null=True, blank=True)
    registered_year = models.IntegerField\
            ("Year of vessel's registration", max_length=4,
             null=True, blank=True)
    registered_place = models.ForeignKey \
            ('Place', related_name="registered_place",
             null=True, blank=True)
    registered_region = models.ForeignKey \
            ('Region', related_name="registered_region",
             null=True, blank=True)

    # Imputed variables
    imputed_nationality = models.ForeignKey\
            ('Nationality', related_name="imputed_nationality",
             null=True, blank=True)
    tonnage_mod = models.DecimalField("Tonnage standardized on British"
                                      "measured tons, 1773-1835",
                                      max_digits=8,
                                      decimal_places=2,
                                      null=True, blank=True)

    voyage = models.ForeignKey('Voyage', null=True, blank=True, related_name="voyage_name_ship")

    def __unicode__(self):
        return self.ship_name

    class Meta:
        verbose_name = 'Ship'
        verbose_name_plural = "Ships"


class VoyageShipOwner(models.Model):
    """
    Owner name.
    Represents first_owner, second_owner, ...
    """
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return self.name


class VoyageShipOwnerConnection(models.Model):
    """
    Represents the relation between Voyage Ship owners and
    Owner.
    captain_order represents order of each captain (1st, 2nd, ...)
    """
    owner = models.ForeignKey('VoyageShipOwner', related_name="owner_name")
    voyage = models.ForeignKey('Voyage', related_name="voyage_related")
    captain_order = models.IntegerField(max_length=2)


# Voyage Outcome
class VoyageOutcome(models.Model):
    """
    Information about Outcomes
    """

    class ParticularOutcome(models.Model):
        """
        Particular outcome.
        """
        name = models.CharField("Outcome label", max_length=70)
        code = models.IntegerField("Code of outcome", max_length=3)

        def __unicode__(self):
            return self.name

    class SlavesOutcome(models.Model):
        """
        Outcome of voyage for slaves.
        """
        name = models.CharField("Outcome label", max_length=70)
        code = models.IntegerField("Code of outcome", max_length=1)

        def __unicode__(self):
            return self.name

    class VesselCapturedOutcome(models.Model):
        """
        Outcome of voyage if vessel captured.
        """
        name = models.CharField("Outcome label", max_length=70)
        code = models.IntegerField("Code of outcome", max_length=2)

        def __unicode__(self):
            return self.name

    class OwnerOutcome(models.Model):
        """
        Outcome of voyage for owner.
        """
        name = models.CharField("Outcome label", max_length=70)
        code = models.IntegerField("Code of outcome", max_length=1)

        def __unicode__(self):
            return self.name

    class Resistance(models.Model):
        """
        Resistance labels
        """
        name = models.CharField("Resistance label", max_length=35)
        code = models.IntegerField("Code of resistance", max_length=1)

        def __unicode__(self):
            return self.name

    # Data variables
    particular_outcome = models.ForeignKey('ParticularOutcome',
                                           null=True, blank=True)
    resistance = models.ForeignKey('Resistance',
                                   null=True, blank=True)

    # Imputed variables
    outcome_slaves = models.ForeignKey('SlavesOutcome',
                                       null=True, blank=True)
    vessel_captured_outcome = models.ForeignKey('VesselCapturedOutcome',
                                                null=True, blank=True)
    outcome_owner = models.ForeignKey('OwnerOutcome',
                                      null=True, blank=True)

    voyage = models.ForeignKey('Voyage', null=True, blank=True, related_name="voyage_name_outcome")

    def __unicode__(self):
        return self.particular_outcome

    class Meta:
        verbose_name = "Outcome"
        verbose_name_plural = "Outcomes"


# Voyage Itinerary
class VoyageItinerary(models.Model):
    """
    Voyage Itinerary data.
    related to: :model:`voyages.apps.voyages.Voyage.BroadRegion`
    related to: :model:`voyages.apps.voyages.Voyage.SpecificRegion`
    related to: :model:`voyages.apps.voyages.Voyage.Place`
    """

    # Data variables
    port_of_departure = models.ForeignKey \
            ('Place', related_name="port_of_departure", null=True, blank=True)
    # Intended variables
    int_first_port_emb = models.ForeignKey \
            ('Place', related_name="int_first_port_emb",
             null=True, blank=True)
    int_second_port_emb = models.ForeignKey \
            ('Place', related_name="int_second_port_emb",
             null=True, blank=True)
    int_first_region_purchase_slaves = models.ForeignKey \
            ('Region',
             related_name="int_first_region_purchase_slaves",
             null=True, blank=True)
    int_second_region_purchase_slaves = models.ForeignKey \
            ('Region',
             related_name="int_second_region_purchase_slaves",
             null=True, blank=True)
    int_first_port_dis = models.ForeignKey\
            ('Place', related_name="int_first_port_dis",
             null=True, blank=True)
    int_second_port_dis = models.ForeignKey\
            ('Place', related_name="int_second_port_dis",
             null=True, blank=True)
    int_first_region_slave_landing = models.ForeignKey \
            ('Region',
             related_name="int_first_region_slave_landing",
             null=True, blank=True)
    int_second_region_slave_landing = models.ForeignKey \
            ('Region',
             related_name="int_second_region_slave_landing",
             null=True, blank=True)

    # End of intended variables
    ports_called_buying_slaves = models.IntegerField\
            ("Number of ports of call prior to buying slaves",
             max_length=3, null=True, blank=True)
    first_place_slave_purchase = models.ForeignKey \
            ('Place', related_name="first_place_slave_purchase",
             null=True, blank=True)
    second_place_slave_purchase = models.ForeignKey \
            ('Place', related_name="second_place_slave_purchase",
             null=True, blank=True)
    third_place_slave_purchase = models.ForeignKey \
            ('Place', related_name="third_place_slave_purchase",
             null=True, blank=True)

    first_region_slave_emb = models.ForeignKey\
            ('Region', related_name="first_region_slave_emb",
             null=True, blank=True)
    second_region_slave_emb = models.ForeignKey\
            ('Region', related_name="second_region_slave_emb",
             null=True, blank=True)
    third_region_slave_emb = models.ForeignKey\
            ('Region', related_name="third_region_slave_emb",
             null=True, blank=True)

    port_of_call_before_atl_crossing = models.ForeignKey \
            ('Place', related_name="port_of_call_before_atl_crossing",
             null=True, blank=True)
    number_of_ports_of_call = models.ForeignKey \
            ('Place', related_name="number_of_ports_of_call",
             null=True, blank=True)

    first_landing_place = models.ForeignKey \
            ('Place', related_name="first_landing_place",
             null=True, blank=True)
    second_landing_place = models.ForeignKey \
            ('Place', related_name="second_landing_place",
             null=True, blank=True)
    third_landing_place = models.ForeignKey \
            ('Place', related_name="third_landing_place",
             null=True, blank=True)

    first_landing_region = models.ForeignKey \
            ('Region', related_name="first_landing_region",
             null=True, blank=True)
    second_landing_region = models.ForeignKey \
            ('Region', related_name="second_landing_region",
             null=True, blank=True)
    third_landing_region = models.ForeignKey \
            ('Region', related_name="third_landing_region",
             null=True, blank=True)

    place_voyage_ended = models.ForeignKey \
            ('Place', related_name="place_voyage_ended",
             null=True, blank=True)
    region_of_return = models.ForeignKey \
            ('Region', related_name="region_of_return",
             null=True, blank=True)
    broad_region_of_return = models.ForeignKey \
            ('Region', related_name="broad_region_of_return",
             null=True, blank=True)

    # Imputed variables
    imp_port_voyage_begin = models.ForeignKey \
            ('Place', related_name="imp_port_voyage_begin",
             null=True, blank=True)
    imp_region_voyage_begin = models.ForeignKey \
            ('Region', related_name="imp_region_voyage_begin",
             null=True, blank=True)
    imp_broad_region_voyage_begin = models.ForeignKey \
            ('BroadRegion', related_name="imp_broad_region_voyage_begin",
             null=True, blank=True)
    principal_place_of_slave_purchase = models.ForeignKey \
            ('Place', related_name="principal_place_of_slave_purchase",
             null=True, blank=True)
    imp_principal_place_of_slave_purchase = models.ForeignKey \
            ('Place',
             related_name="imp_principal_place_of_slave_purchase",
             null=True, blank=True)
    imp_principal_region_of_slave_purchase = models.ForeignKey \
            ('Region', related_name=
            "imp_principal_region_of_slave_purchase",
             null=True, blank=True)
    imp_broad_region_of_slave_purchase = models.ForeignKey\
            ('BroadRegion',
             related_name="imp_broad_region_of_slave_purchase",
             null=True, blank=True)
    principal_port_of_slave_dis = models.ForeignKey \
            ('Place', related_name="principal_port_of_slave_dis",
             null=True, blank=True)
    imp_principal_port_slave_dis = models.ForeignKey \
            ('Place', related_name="imp_principal_port_slave_dis",
             null=True, blank=True)
    imp_principal_region_slave_dis = models.ForeignKey \
            ('Region',
             related_name="imp_principal_region_slave_dis",
             null=True, blank=True)
    imp_broad_region_slave_dis = models.ForeignKey \
            ('BroadRegion', related_name="imp_broad_region_slave_dis",
             null=True, blank=True)

    voyage = models.ForeignKey('Voyage', null=True, blank=True, related_name="voyage_name_itinerary")

    class Meta:
        verbose_name = "Itinerary"
        verbose_name_plural = "Itineraries"


# Voyage Dates
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
    # Date variables
    voyage_began = models.CommaSeparatedIntegerField\
            ("Date that voyage began", max_length=10,
             blank=True, null=True)
    slave_purchase_began = models.CommaSeparatedIntegerField\
            ("Date that slave purchase began", max_length=10,
             blank=True, null=True)
    vessel_left_port = models.CommaSeparatedIntegerField\
            ("Date that vessel left last slaving port", max_length=10,
             blank=True, null=True)
    first_dis_of_slaves = models.CommaSeparatedIntegerField\
            ("Date of first disembarkation of slaves", max_length=10,
             blank=True, null=True)
    arrival_at_second_place_landing = models.CommaSeparatedIntegerField\
            ("Date of arrival at second place of landing", max_length=10,
             blank=True, null=True)
    third_dis_of_slaves = models.CommaSeparatedIntegerField\
            ("Date of third disembarkation of slaves", max_length=10,
             blank=True, null=True)
    departure_last_place_of_landing = models.CommaSeparatedIntegerField\
            ("Date of departure from last place of landing", max_length=10,
             blank=True, null=True)
    voyage_completed = models.CommaSeparatedIntegerField\
            ("Date on which slave voyage completed", max_length=10,
             blank=True, null=True)

    # Imputed variables
    imp_voyage_began = models.CommaSeparatedIntegerField\
            ("Year voyage began", max_length=10,
             blank=True, null=True)
    imp_departed_africa = models.IntegerField \
            ("Year departed Africa", max_length=4,
             blank=True, null=True)
    imp_arrival_at_port_of_dis = models.CommaSeparatedIntegerField\
            ("Year of arrival at port of disembarkation",
             max_length=4, blank=True, null=True)

    voyage = models.ForeignKey('Voyage', null=True, blank=True, related_name="voyage_name_dates")

    class Meta:
        verbose_name = 'Date'
        verbose_name_plural = "Dates"


# Voyage Captain and Crew
class VoyageCaptain(models.Model):
    """
    Voyage Captain and Crew.
    """
    name = models.CharField("Captain's name", max_length=60)

    def __unicode__(self):
        return self.name


class VoyageCaptainConnection(models.Model):
    CHOICES = ((1, "First"), (2, "Second"), (3, "Third"))
    captain = models.ForeignKey\
            ('VoyageCaptain', related_name='captain_name')
    voyage = models.ForeignKey\
            ('Voyage', related_name='voyage')
    captain_order = models.CharField(max_length=7,
                                     choices = CHOICES,
                                     default=1)


class VoyageCrew(models.Model):
    crew_voyage_outset = models.IntegerField\
            ("Crew at voyage outset",
             max_length=3, null=True, blank=True)
    crew_departure_last_port = models.IntegerField \
            ("Crew at departure from last port of slave purchase",
             max_length=3, null=True, blank=True)
    crew_first_landing = models.IntegerField \
            ("Crew at first landing of slaves", max_length=2,
             null=True, blank=True)
    crew_return_begin = models.IntegerField \
            ("Crew when return voyage begin", max_length=2,
             null=True, blank=True)
    crew_end_voyage = models.IntegerField \
            ("Crew at end of voyage", max_length=2,
             null=True, blank=True)
    unspecified_crew = models.IntegerField \
            ("Number of crew unspecified", max_length=3,
             null=True, blank=True)
    crew_died_before_first_trade = models.IntegerField \
            ("Crew died before first place of trade in Africa",
             max_length=2,
             null=True, blank=True)
    crew_died_while_ship_african = models.IntegerField \
            ("Crew died while ship was on African coast",
             max_length=2,
             null=True, blank=True)
    crew_died_middle_passge = models.IntegerField \
            ("Crew died during Middle Passage", max_length=2,
             null=True, blank=True)
    crew_died_in_americas = models.IntegerField \
            ("Crew died in the Americas", max_length=2,
             null=True, blank=True)
    crew_died_on_return_voyage = models.IntegerField \
            ("Crew died on return voyage", max_length=2,
             null=True, blank=True)
    crew_died_complete_voyage = models.IntegerField \
            ("Crew died during complete voyage", max_length=3,
             null=True, blank=True)
    crew_deserted = models.IntegerField \
            ("Total number of crew deserted", max_length=2,
             null=True, blank=True)

    voyage = models.ForeignKey('Voyage', null=True, blank=True, related_name="voyage_name_crew")

    class Meta:
        verbose_name = 'Crew'
        verbose_name_plural = "Crews"


# Voyage Slaves (numbers)
class VoyageSlavesNumbers(models.Model):
    """
    Voyage slaves (numbers).
    related to: :model:`voyages.apps.voyages.Voyage`
    """

    slave_deaths_before_africa = models.IntegerField \
            ("Slaves death before leaving Africa (SLADAFRI)")
    slave_deaths_between_africa_america = models.IntegerField \
            ("Slaves death between Africa and Americas (SLADVOY)",
             null=True, blank=True)
    slave_deaths_between_africa_america = models.IntegerField \
            ("Slaves death before arrival and sale (SLADAMER)",
             null=True, blank=True)
    num_slaves_intended_first_port = models.IntegerField \
            ("Number of slaves intended from first port of purchase "
             "(SLINTEND)", null=True, blank=True, max_length=4)
    num_slaves_intended_second_port = models.IntegerField \
            ("Number of slaves intended from second port of purchase "
             "(SLINTEND2)", null=True, blank=True, max_length=4)

    num_slaves_carried_first_port = models.IntegerField \
            ("Number of slaves carried from first port of purchase "
             "(NCAR13)", null=True, blank=True, max_length=4)
    num_slaves_carried_second_port = models.IntegerField \
            ("Number of slaves carried from second port of purchase "
             "(NCAR15)", null=True, blank=True, max_length=4)
    num_slaves_carried_third_port = models.IntegerField \
            ("Number of slaves carried from third port of purchase "
             "(NCAR17)", null=True, blank=True, max_length=4)

    total_num_slaves_purchased = models.IntegerField \
            ("Total slaves purchased (TSLAVESP)", null=True, blank=True, max_length=4)
    total_num_slaves_dep_last_slaving_port = models.IntegerField \
            ("Total slaves on board at departure from last slaving port "
             "(TSLAVESD)", null=True, blank=True, max_length=4)

    total_num_slaves_arr_first_port_embark = models.IntegerField \
            ("Total slaves arrived at first port of disembarkation "
             "(SLAARRIV)", null=True, blank=True, max_length=4)

    num_slaves_disembark_first_place = models.IntegerField \
            ("Number of slaves disembarked at first place "
             "(SLAS32)", null=True, blank=True)
    num_slaves_disembark_second_place = models.IntegerField \
            ("Number of slaves disembarked at second place "
             "(SLAS36)", null=True, blank=True)
    num_slaves_disembark_third_place = models.IntegerField \
            ("Number of slaves disembarked at third place "
             "(SLAS39)", null=True, blank=True)

    # Voyage characteristics

    # Representing MEN1 variables
    num_men_embark_first_port_purchase = models.IntegerField \
            ("Number of men (MEN1) embarked at first port of purchase", null=True, blank=True)
    # Representing WOMEN1 variables
    num_women_embark_first_port_purchase = models.IntegerField \
            ("Number of women (WOMEN1) embarked at first port of purchase", null=True, blank=True)
    # Representing BOY1 variables
    num_boy_embark_first_port_purchase = models.IntegerField \
            ("Number of boys (BOY1) embarked at first port of purchase", null=True, blank=True)
    # Representing GIRL1 variables
    num_girl_embark_first_port_purchase = models.IntegerField \
            ("Number of girls (GIRL1) embarked at first port of purchase", null=True, blank=True)
    # Representing ADULT1 variables
    num_adult_embark_first_port_purchase = models.IntegerField \
            ("Number of adults (gender unspecified) (ADULT1) embarked at first port of purchase",
             null=True, blank=True)
    # Representing CHILD1 variables
    num_child_embark_first_port_purchase = models.IntegerField \
            ("Number of children (gender unspecified) (CHILD1) embarked at first port of purchase",
             null=True, blank=True)
    # Representing INFANT1 variables
    num_infant_embark_first_port_purchase = models.IntegerField \
            ("Number of infants (INFANT1) embarked at first port of purchase", null=True, blank=True)
    # Representing MALE1 variables
    num_males_embark_first_port_purchase = models.IntegerField \
            ("Number of males (age unspecified) (MALE1) embarked at first port of purchase",
             null=True, blank=True)
    # Representing FEMALE1 variables
    num_females_embark_first_port_purchase = models.IntegerField \
            ("Number of females (age unspecified) (FEMALE1) embarked at first port of purchase",
             null=True, blank=True)


    # Representing MEN2 variables
    num_men_died_middle_passage = models.IntegerField \
            ("Number of men (MEN2) died on Middle Passage", null=True, blank=True)
    # Representing WOMEN2 variables
    num_women_died_middle_passage = models.IntegerField \
            ("Number of women (WOMEN2) died on Middle Passage", null=True, blank=True)
    # Representing BOY2 variables
    num_boy_died_middle_passage = models.IntegerField \
            ("Number of boys (BOY2) died on Middle Passage", null=True, blank=True)
    # Representing GIRL2 variables
    num_girl_died_middle_passage = models.IntegerField \
            ("Number of girls (GIRL2) died on Middle Passage", null=True, blank=True)
    # Representing ADULT2 variables
    num_adult_died_middle_passage = models.IntegerField \
            ("Number of adults (gender unspecified) (ADULT2) died on Middle Passage",
             null=True, blank=True)
    # Representing CHILD2 variables
    num_child_died_middle_passage = models.IntegerField \
            ("Number of children (gender unspecified) (CHILD2) died on Middle Passage",
             null=True, blank=True)
    # Representing INFANT2 variables
    num_infant_died_middle_passage = models.IntegerField \
            ("Number of infants (INFANT2) died on Middle Passage", null=True, blank=True)
    # Representing MALE2 variables
    num_males_died_middle_passage = models.IntegerField \
            ("Number of males (age unspecified) (MALE2) died on Middle Passage",
             null=True, blank=True)
    # Representing FEMALE2 variables
    num_females_died_middle_passage = models.IntegerField \
            ("Number of females (age unspecified) (FEMALE2) died on Middle Passage",
             null=True, blank=True)


    # Representing MEN3 variables
    num_men_disembark_first_landing = models.IntegerField \
            ("Number of men (MEN3) disembarked at first place of landing", null=True, blank=True)
    # Representing WOMEN3 variables
    num_women_disembark_first_landing = models.IntegerField \
            ("Number of women (WOMEN3) disembarked at first place of landing", null=True, blank=True)
    # Representing BOY3 variables
    num_boy_disembark_first_landing = models.IntegerField \
            ("Number of boys (BOY3) disembarked at first place of landing", null=True, blank=True)
    # Representing GIRL3 variables
    num_girl_disembark_first_landing = models.IntegerField \
            ("Number of girls (GIRL3) disembarked at first place of landing", null=True, blank=True)
    # Representing ADULT3 variables
    num_adult_disembark_first_landing = models.IntegerField \
            ("Number of adults (gender unspecified) (ADULT3) disembarked at first place of landing",
             null=True, blank=True)
    # Representing CHILD3 variables
    num_child_disembark_first_landing = models.IntegerField \
            ("Number of children (gender unspecified) (CHILD3) disembarked at first place of landing",
             null=True, blank=True)
    # Representing INFANT3 variables
    num_infant_disembark_first_landing = models.IntegerField \
            ("Number of infants (INFANT3) disembarked at first place of landing", null=True, blank=True)
    # Representing MALE3 variables
    num_males_disembark_first_landing = models.IntegerField \
            ("Number of males (age unspecified) (MALE3) disembarked at first place of landing",
             null=True, blank=True)
    # Representing FEMALE3 variables
    num_females_disembark_first_landing = models.IntegerField \
            ("Number of females (age unspecified) (FEMALE3) disembarked at first place of landing",
             null=True, blank=True)


    # Representing MEN4 variables
    num_men_embark_second_port_purchase = models.IntegerField \
            ("Number of men (MEN4) embarked at second port of purchase", null=True, blank=True)
    # Representing WOMEN4 variables
    num_women_embark_second_port_purchase = models.IntegerField \
            ("Number of women (WOMEN4) embarked at second port of purchase", null=True, blank=True)
    # Representing BOY4 variables
    num_boy_embark_second_port_purchase = models.IntegerField \
            ("Number of boys (BOY4) embarked at second port of purchase", null=True, blank=True)
    # Representing GIRL4 variables
    num_girl_embark_second_port_purchase = models.IntegerField \
            ("Number of girls (GIRL4) embarked at second port of purchase", null=True, blank=True)
    # Representing ADULT4 variables
    num_adult_embark_second_port_purchase = models.IntegerField \
            ("Number of adults (gender unspecified) (ADULT4) embarked at second port of purchase",
             null=True, blank=True)
    # Representing CHILD4 variables
    num_child_embark_second_port_purchase = models.IntegerField \
            ("Number of children (gender unspecified) (CHILD4) embarked at second port of purchase",
             null=True, blank=True)
    # Representing INFANT4 variables
    num_infant_embark_second_port_purchase = models.IntegerField \
            ("Number of infants (INFANT4) embarked at second port of purchase", null=True, blank=True)
    # Representing MALE4 variables
    num_males_embark_second_port_purchase = models.IntegerField \
            ("Number of males (age unspecified) (MALE4) embarked at second port of purchase",
             null=True, blank=True)
    # Representing FEMALE4 variables
    num_females_embark_second_port_purchase = models.IntegerField \
            ("Number of females (age unspecified) (FEMALE4) embarked at second port of purchase",
             null=True, blank=True)


    # Representing MEN5 variables
    num_men_embark_third_port_purchase = models.IntegerField \
            ("Number of men (MEN5) embarked at third port of purchase", null=True, blank=True)
    # Representing WOMEN5 variables
    num_women_embark_third_port_purchase = models.IntegerField \
            ("Number of women (WOMEN5) embarked at third port of purchase", null=True, blank=True)
    # Representing BOY5 variables
    num_boy_embark_third_port_purchase = models.IntegerField \
            ("Number of boys (BOY5) embarked at third port of purchase", null=True, blank=True)
    # Representing GIRL5 variables
    num_girl_embark_third_port_purchase = models.IntegerField \
            ("Number of girls (GIRL5) embarked at third port of purchase", null=True, blank=True)
    # Representing ADULT5 variables
    num_adult_embark_third_port_purchase = models.IntegerField \
            ("Number of adults (gender unspecified) (ADULT5) embarked at third port of purchase",
             null=True, blank=True)
    # Representing CHILD5 variables
    num_child_embark_third_port_purchase = models.IntegerField \
            ("Number of children (gender unspecified) (CHILD5) embarked at third port of purchase",
             null=True, blank=True)
    # Representing INFANT5 variables
    num_infant_embark_third_port_purchase = models.IntegerField \
            ("Number of infants (INFANT5) embarked at third port of purchase", null=True, blank=True)
    # Representing MALE5 variables
    num_males_embark_third_port_purchase = models.IntegerField \
            ("Number of males (age unspecified) (MALE5) embarked at third port of purchase",
             null=True, blank=True)
    # Representing FEMALE5 variables
    num_females_embark_third_port_purchase = models.IntegerField \
            ("Number of females (age unspecified) (FEMALE5) embarked at third port of purchase",
             null=True, blank=True)


    # Representing MEN6 variables
    num_men_disembark_second_landing = models.IntegerField \
            ("Number of men (MEN6) disembarked at second place of landing", null=True, blank=True)
    # Representing WOMEN6 variables
    num_women_disembark_second_landing = models.IntegerField \
            ("Number of women (WOMEN6) disembarked at second place of landing", null=True, blank=True)
    # Representing BOY6 variables
    num_boy_disembark_second_landing = models.IntegerField \
            ("Number of boys (BOY6) disembarked at second place of landing", null=True, blank=True)
    # Representing GIRL6 variables
    num_girl_disembark_second_landing = models.IntegerField \
            ("Number of girls (GIRL6) disembarked at second place of landing", null=True, blank=True)
    # Representing ADULT6 variables
    num_adult_disembark_second_landing = models.IntegerField \
            ("Number of adults (gender unspecified) (ADULT6) disembarked at second place of landing",
             null=True, blank=True)
    # Representing CHILD6 variables
    num_child_disembark_second_landing = models.IntegerField \
            ("Number of children (gender unspecified) (CHILD6) disembarked at second place of landing",
             null=True, blank=True)
    # Representing INFANT6 variables
    num_infant_disembark_second_landing = models.IntegerField \
            ("Number of infants (INFANT6) disembarked at second place of landing", null=True, blank=True)
    # Representing MALE6 variables
    num_males_disembark_second_landing = models.IntegerField \
            ("Number of males (age unspecified) (MALE6) disembarked at second place of landing",
             null=True, blank=True)
    # Representing FEMALE6 variables
    num_females_disembark_second_landing = models.IntegerField \
            ("Number of females (age unspecified) (FEMALE6) disembarked at second place of landing",
             null=True, blank=True)

    voyage = models.ForeignKey('Voyage', null=True, blank=True,
                               related_name="voyage_name_slave_characteristics")

    class Meta:
        verbose_name = 'Slaves Characteristic'
        verbose_name_plural = "Slaves Characteristics"


class GroupComposition(models.Model):
        """
        Basic composition of a group of slaves
            used by 'VoyageSlavesCharacteristics'
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
                ("Number of adults (gender unspecified) (ADULT*)",
                 null=True, blank=True)
        # Representing CHILD* variables
        num_child = models.IntegerField \
                ("Number of children (gender unspecified) (CHILD*)",
                 null=True, blank=True)
        # Representing INFANT* variables
        num_infant = models.IntegerField \
                ("Number of infants (INFANT*)", null=True, blank=True)
        # Representing MALE* variables
        num_males = models.IntegerField \
                ("Number of males (age unspecified) (MALE*)",
                 null=True, blank=True)
        # Representing FEMALE* variables
        num_females = models.IntegerField \
                ("Number of females (age unspecified) (FEMALE*)",
                 null=True, blank=True)


# Voyage Sources
class VoyageSources(models.Model):
    """
    Voyage sources.
    Representing the original variables SOURCEA, SOURCEB, SOURCEC
    and etc to SOURCER
    """
    short_ref = models.CharField(_('Short reference'),
                                 max_length=100, null=True, blank=True)
    # Might contain HTML text formatting
    full_ref = models.CharField(_('Full reference'),
                                max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = 'Source'
        verbose_name_plural = "Sources"

class VoyageSourcesConnection(models.Model):
    """
    Represents the relationship between Voyage and VoyageSources
    source_order determines the order sources appear for each voyage
    """
    source = models.ForeignKey('VoyageSources', related_name="source")
    group = models.ForeignKey('Voyage', related_name="group")
    source_order = models.IntegerField(max_length=2)
    text_ref = models.CharField(_('Text reference(citation)'), max_length=100, null=True, blank=True)


# Voyage (main) model
class Voyage(models.Model):
    """
    Information about voyages.
    """

    voyage_id = models.AutoField(primary_key=True)

    voyage_in_cd_rom = models.BooleanField("Voyage in 1999 CD-ROM", max_length=1, blank=True)

    # Technical variables
    voyage_groupings = models.ForeignKey \
            ('VoyageGroupings',
             help_text="Voyage Groupings for estimating imputed slaves")

    # Data and imputed variables

    voyage_captain = models.ManyToManyField \
            ("VoyageCaptain", through=VoyageCaptainConnection,
             help_text="Voyage Captain",
             blank=True, null=True)
    voyage_ship_owner = models.ManyToManyField \
        ("VoyageShipOwner", through=VoyageShipOwnerConnection,
         help_text="Voyage Ship Owner",
         blank=True, null=True)

    # One Voyage can contain multiple sources and one source can refer
    # to multiple voyages
    voyage_sources = models.ManyToManyField \
            ('VoyageSources', through='VoyageSourcesConnection',
             related_name='voyage_sources', blank=True, null=True)

    class Meta:
        verbose_name = 'Voyage'
        verbose_name_plural = "Voyages"

    def __unicode__(self):
        return "Voyage " + str(self.voyage_id)