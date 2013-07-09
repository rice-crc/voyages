from django.db import models
from django.utils.translation import ugettext as _

# Voyage Regions and Places
class BroadRegion(models.Model):
    """
    Broad Regions (continents).
    """

    name = models.CharField("Broad region (Area) name", max_length=70)
    code = models.IntegerField("Numeric code", max_length=5)
    show_on_map = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Broad Region'
        verbose_name_plural = "Broad Regions"

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Broad region (area)'
        verbose_name_plural = 'Broad regions (areas)'
        ordering = ['code']


class Region(models.Model):
    """
    Specific Regions (countries or colonies).
    related to: :model:`voyages.apps.voyages.BroadRegion`
    """

    name = models.CharField("Specific region (country or colony)",
                                               max_length=70)
    broad_region = models.ForeignKey('BroadRegion')
    code = models.IntegerField("Numeric code", max_length=5)
    show_on_map = models.BooleanField(default=True)
    show_on_main_map = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = "Regions"

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['code']


class Place(models.Model):
    """
    Place (port or location).
    related to: :model:`voyages.apps.voyages.Region`
    """

    name = models.CharField(max_length=70)
    region = models.ForeignKey('Region')
    code = models.IntegerField("Numeric code", max_length=5)
    longitude = models.DecimalField("Longitude of point",
                                     max_digits=10, decimal_places=7,
                                     null=True, blank=True)
    latitude = models.DecimalField("Latitude of point",
                                     max_digits=10, decimal_places=7,
                                     null=True, blank=True)
    show_on_main_map = models.BooleanField(default=True)
    show_on_voyage_map = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Place (Port or Location)'
        verbose_name_plural = "Places (Ports or Locations)"
        ordering = ['code']

    def __unicode__(self):
        return self.name


# Voyage Groupings
class VoyageGroupings(models.Model):
    """
    Labels for groupings names.
    """
    value = models.CharField(max_length=30)
    label = models.IntegerField(max_length=3)

    class Meta:
        verbose_name = "Grouping for estimating imputed slaves"
        verbose_name_plural = "Groupings for estimating imputed slaves"

    def __unicode__(self):
        return self.value


# Voyage Ship, Nation, Owners
class VoyageShip(models.Model):
    """
    Information about voyage ship.
    related to: :model:`voyages.apps.voyages.Region`
    related to: :model:`voyages.apps.voyages.Place`
    related to: :model:`voyages.apps.voyages.Voyage`
    """

    class Nationality(models.Model):
        """
        Nationality of ships.
        """
        nationality = models.CharField(max_length=70)
        code = models.IntegerField(max_length=2)

        class Meta:
            verbose_name = "Nationality"
            verbose_name_plural = "Nationalities"
            ordering = ['code']

        def __unicode__(self):
            return self.nationality

    class TonType(models.Model):
        """
        Types of tonnage.
        """
        ton_type = models.CharField(max_length=70)
        code = models.IntegerField(max_length=2)

        class Meta:
            verbose_name = "Type of tons"
            verbose_name_plural = "Types of tons"
            ordering = ['code']

        def __unicode__(self):
            return self.ton_type

    class RigOfVessel(models.Model):
        """
        Rig of Vessel.
        """
        rig_of_vessel = models.CharField(max_length=25)
        code = models.IntegerField(max_length=2)

        class Meta:
            verbose_name = "Rig of vessel"
            verbose_name_plural = "Rigs of vessel"
            ordering = ['code']

        def __unicode__(self):
            return self.rig_of_vessel

    # Data variables
    ship_name = models.CharField("Name of vessel", max_length=70,
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
             verbose_name="Place where vessel constructed",
             null=True, blank=True)
    vessel_construction_region = models.ForeignKey \
            ('Region', related_name="vessel_construction_region",
             verbose_name="Region where vessel constructed",
             null=True, blank=True)
    registered_year = models.IntegerField\
            ("Year of vessel's registration", max_length=4,
             null=True, blank=True)
    registered_place = models.ForeignKey \
            ('Place', related_name="registered_place",
             verbose_name="Place where vessel registered",
             null=True, blank=True)
    registered_region = models.ForeignKey \
            ('Region', related_name="registered_region",
             verbose_name="Region where vessel registered",
             null=True, blank=True)

    # Imputed variables
    imputed_nationality = models.ForeignKey\
            ('Nationality', related_name="imputed_nationality",
             null=True, blank=True)
    tonnage_mod = models.DecimalField("Tonnage standardized on British"
                                      "measured tons, 1773-1870",
                                      max_digits=8,
                                      decimal_places=1,
                                      null=True, blank=True)

    voyage = models.ForeignKey('Voyage', null=True, blank=True,
                               related_name="voyage_name_ship")

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
    name = models.CharField(max_length=70)

    def __unicode__(self):
        return self.name


class VoyageShipOwnerConnection(models.Model):
    """
    Represents the relation between Voyage Ship owners and
    Owner.
    owner_order represents order of each owner (1st, 2nd, ...)
    """
    owner = models.ForeignKey('VoyageShipOwner', related_name="owner_name")
    voyage = models.ForeignKey('Voyage', related_name="voyage_related")
    owner_order = models.IntegerField(max_length=2)

    def __unicode__(self):
        return "Ship owner:"


# Voyage Outcome
class VoyageOutcome(models.Model):
    """
    Information about Outcomes
    """

    class ParticularOutcome(models.Model):
        """
        Particular outcome.
        """
        name = models.CharField("Outcome label", max_length=200)
        code = models.IntegerField("Code of outcome", max_length=3)

        def __unicode__(self):
            return self.name

        class Meta:
            ordering = ['code']
            verbose_name = 'Fate (particular outcome of voyage)'
            verbose_name_plural = 'Fates (particular outcomes of voyages)'


    class SlavesOutcome(models.Model):
        """
        Outcome of voyage for slaves.
        """
        name = models.CharField("Outcome label", max_length=200)
        code = models.IntegerField("Code of outcome", max_length=1)

        def __unicode__(self):
            return self.name

        class Meta:
            ordering = ['code']

    class VesselCapturedOutcome(models.Model):
        """
        Outcome of voyage if vessel captured.
        """
        name = models.CharField("Outcome label", max_length=200)
        code = models.IntegerField("Code of outcome", max_length=2)

        def __unicode__(self):
            return self.name

        class Meta:
            ordering = ['code']

    class OwnerOutcome(models.Model):
        """
        Outcome of voyage for owner.
        """
        name = models.CharField("Outcome label", max_length=200)
        code = models.IntegerField("Code of outcome", max_length=1)

        def __unicode__(self):
            return self.name

        class Meta:
            ordering = ['code']

    class Resistance(models.Model):
        """
        Resistance labels
        """
        name = models.CharField("Resistance label", max_length=70)
        code = models.IntegerField("Code of resistance", max_length=1)

        def __unicode__(self):
            return self.name

        class Meta:
            ordering = ['code']

    # Data variables
    particular_outcome = models.ForeignKey('ParticularOutcome',
                                           verbose_name="Particular Outcome",
                                           null=True, blank=True)
    resistance = models.ForeignKey('Resistance',
                                   verbose_name="Resistance",
                                   null=True, blank=True)

    # Imputed variables
    outcome_slaves = models.ForeignKey('SlavesOutcome',
                                       verbose_name="Slaves Outcome",
                                       null=True, blank=True)
    vessel_captured_outcome = models.ForeignKey\
            ('VesselCapturedOutcome', verbose_name="Vessel Captured Outcome",
             null=True, blank=True)
    outcome_owner = models.ForeignKey('OwnerOutcome',
                                      verbose_name="Owner Outcome",
                                      null=True, blank=True)

    voyage = models.ForeignKey('Voyage', null=True, blank=True,
                               related_name="voyage_name_outcome")

    def __unicode__(self):
        #TODO: We may want to change this.
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
            ('Place', related_name="port_of_departure",
             verbose_name="Port of departure (PORTDEP)",
             null=True, blank=True)
    # Intended variables
    int_first_port_emb = models.ForeignKey \
            ('Place', related_name="int_first_port_emb",
             verbose_name="First intended port of embarkation (EMBPORT)",
             null=True, blank=True)
    int_second_port_emb = models.ForeignKey \
            ('Place', related_name="int_second_port_emb",
             verbose_name="Second intended port of embarkation (EMBPORT2)",
             null=True, blank=True)
    int_first_region_purchase_slaves = models.ForeignKey \
            ('Region',
             related_name="int_first_region_purchase_slaves",
             verbose_name="First intended region of purchase of slaves (EMBREG)",
             null=True, blank=True)
    int_second_region_purchase_slaves = models.ForeignKey \
            ('Region',
             related_name="int_second_region_purchase_slaves",
             verbose_name="Second intended region of purchase of slaves (EMBREG2)",
             null=True, blank=True)
    int_first_port_dis = models.ForeignKey\
            ('Place', related_name="int_first_port_dis",
             verbose_name="First intended port of disembarkation (ARRPORT)",
             null=True, blank=True)
    int_second_port_dis = models.ForeignKey\
            ('Place', related_name="int_second_port_dis",
             verbose_name="Second intended port of disembarkation (ARRPORT2)",
             null=True, blank=True)
    int_first_region_slave_landing = models.ForeignKey \
            ('Region',
             related_name="int_first_region_slave_landing",
             verbose_name="First intended region of slave landing (REGARR)",
             null=True, blank=True)
    int_second_place_region_slave_landing = models.ForeignKey \
            ('Region',
             related_name="int_second_region_slave_landing",
             verbose_name="Second intended region of slave landing (REGARR2)",
             null=True, blank=True)

    # End of intended variables
    ports_called_buying_slaves = models.IntegerField\
            ("Number of ports of call prior to buying slaves (NPPRETRA)",
             max_length=3, null=True, blank=True)

    first_place_slave_purchase = models.ForeignKey \
            ('Place', related_name="first_place_slave_purchase",
            verbose_name="First place of slave purchase (PLAC1TRA)",
             null=True, blank=True)
    second_place_slave_purchase = models.ForeignKey \
            ('Place', related_name="second_place_slave_purchase",
             verbose_name="Second place of slave purchase (PLAC2TRA)",
             null=True, blank=True)
    third_place_slave_purchase = models.ForeignKey \
            ('Place', related_name="third_place_slave_purchase",
             verbose_name="Third place of slave purchase (PLAC3TRA)",
             null=True, blank=True)

    first_region_slave_emb = models.ForeignKey\
            ('Region', related_name="first_region_slave_emb",
             verbose_name="First region of embarkation of slaves (REGEM1)",
             null=True, blank=True)
    second_region_slave_emb = models.ForeignKey\
            ('Region', related_name="second_region_slave_emb",
             verbose_name="Second region of embarkation of slaves (REGEM2)",
             null=True, blank=True)
    third_region_slave_emb = models.ForeignKey\
            ('Region', related_name="third_region_slave_emb",
             verbose_name="Third region of embarkation of slaves (REGEM3)",
             null=True, blank=True)

    port_of_call_before_atl_crossing = models.ForeignKey \
            ('Place', related_name="port_of_call_before_atl_crossing",
             verbose_name="Port of call before Atlantic crossing (NPAFTTRA)",
             null=True, blank=True)

    number_of_ports_of_call = models.IntegerField\
            ("Number of ports of call in Americas prior to sale of slaves (NPPRIOR)",
             null=True, blank=True)
    first_landing_place = models.ForeignKey \
            ('Place', related_name="first_landing_place",
             verbose_name="First place of slave landing (SLA1PORT)",
             null=True, blank=True)
    second_landing_place = models.ForeignKey \
            ('Place', related_name="second_landing_place",
             verbose_name="Second place of slave landing (ADPSALE1)",
             null=True, blank=True)
    third_landing_place = models.ForeignKey \
            ('Place', related_name="third_landing_place",
             verbose_name="Third place of slave landing (ADPSALE2)",
             null=True, blank=True)

    first_landing_region = models.ForeignKey \
            ('Region', related_name="first_landing_region",
             verbose_name="First region of slave landing (REGDIS1)",
             null=True, blank=True)
    second_landing_region = models.ForeignKey \
            ('Region', related_name="second_landing_region",
             verbose_name="Second region of slave landing (REGDIS2)",
             null=True, blank=True)
    third_landing_region = models.ForeignKey \
            ('Region', related_name="third_landing_region",
             verbose_name="Third region of slave landing (REGDIS3)",
             null=True, blank=True)

    place_voyage_ended = models.ForeignKey \
            ('Place', related_name="place_voyage_ended",
             verbose_name="Place at which voyage ended (PORTRET)",
             null=True, blank=True)
    region_of_return = models.ForeignKey \
            ('Region', related_name="region_of_return",
             verbose_name="Region of return (RETRNREG)",
             null=True, blank=True)
    broad_region_of_return = models.ForeignKey \
            ('BroadRegion', related_name="broad_region_of_return",
             verbose_name="Broad region of return (RETRNREG1)",
             null=True, blank=True)

    # Imputed variables
    imp_port_voyage_begin = models.ForeignKey \
            ('Place', related_name="imp_port_voyage_begin",
             verbose_name="Imputed port where voyage began (PTDEPIMP)",
             null=True, blank=True)
    imp_region_voyage_begin = models.ForeignKey \
            ('Region', related_name="imp_region_voyage_begin",
             verbose_name="Imputed region where voyage began (DEPTREGIMP)",
             null=True, blank=True)
    imp_broad_region_voyage_begin = models.ForeignKey \
            ('BroadRegion', related_name="imp_broad_region_voyage_begin",
             verbose_name="Imputed broad region where voyage began (DEPTREGIMP1)",
             null=True, blank=True)
    principal_place_of_slave_purchase = models.ForeignKey \
            ('Place', related_name="principal_place_of_slave_purchase",
             verbose_name="Principal place of slave purchase (MAJBUYPT)",
             null=True, blank=True)
    imp_principal_place_of_slave_purchase = models.ForeignKey \
            ('Place',
             related_name="imp_principal_place_of_slave_purchase",
             verbose_name="Imputed principal place of slave purchase (MJBYPTIMP)",
             null=True, blank=True)
    imp_principal_region_of_slave_purchase = models.ForeignKey \
            ('Region',
             related_name="imp_principal_region_of_slave_purchase",
             verbose_name="Imputed principal region of slave purchase (c)",
             null=True, blank=True)
    imp_broad_region_of_slave_purchase = models.ForeignKey\
            ('BroadRegion',
             related_name="imp_broad_region_of_slave_purchase",
             verbose_name="Imputed principal broad region of slave purchase (MAJBYIMP1)",
             null=True, blank=True)
    principal_port_of_slave_dis = models.ForeignKey \
            ('Place', related_name="principal_port_of_slave_dis",
             verbose_name="Principal port of slave disembarkation (MAJSELPT)",
             null=True, blank=True)
    imp_principal_port_slave_dis = models.ForeignKey \
            ('Place', related_name="imp_principal_port_slave_dis",
             verbose_name="Imputed principal port of slave disembarkation (MJSLPTIMP)",
             null=True, blank=True)
    imp_principal_region_slave_dis = models.ForeignKey \
            ('Region',
             related_name="imp_principal_region_slave_dis",
             verbose_name="Imputed principal region of slave disembarkation (MJSELIMP)",
             null=True, blank=True)
    imp_broad_region_slave_dis = models.ForeignKey \
            ('BroadRegion', related_name="imp_broad_region_slave_dis",
             verbose_name="Imputed broad region of slave disembarkation (MJSELIMP1)",
             null=True, blank=True)

    voyage = models.ForeignKey('Voyage', null=True, blank=True,
                               related_name="voyage_name_itinerary")

    class Meta:
        verbose_name = "Itinerary"
        verbose_name_plural = "Itineraries"


# Voyage Dates
class VoyageDates(models.Model):
    """
    Voyage dates.
    """

    # Constant variables
    # Dates start
    years_start = {'5': 1525, '10': 1500, '25': 1500, '100': 1500}

    # Data variables
    voyage_began = models.CommaSeparatedIntegerField\
            ("Date that voyage began (DATEDEPB,A,C)", max_length=10,
             blank=True, null=True,
             help_text="Date in format: MM,DD,YYYY")
    slave_purchase_began = models.CommaSeparatedIntegerField\
            ("Date that slave purchase began (D1SLATRB,A,C)", max_length=10,
             blank=True, null=True,
             help_text="Date in format: MM,DD,YYYY")
    vessel_left_port = models.CommaSeparatedIntegerField\
            ("Date that vessel left last slaving port (DLSLATRB,A,C)", max_length=10,
             blank=True, null=True,
             help_text="Date in format: MM,DD,YYYY")
    first_dis_of_slaves = models.CommaSeparatedIntegerField\
            ("Date of first disembarkation of slaves (DATARR33,32,34)", max_length=10,
             blank=True, null=True,
             help_text="Date in format: MM,DD,YYYY")
    arrival_at_second_place_landing = models.CommaSeparatedIntegerField\
            ("Date of arrival at second place of landing (DATARR37,36,38)", max_length=10,
             blank=True, null=True,
             help_text="Date in format: MM,DD,YYYY")
    third_dis_of_slaves = models.CommaSeparatedIntegerField\
            ("Date of third disembarkation of slaves (DATARR40,39,41)", max_length=10,
             blank=True, null=True,
             help_text="Date in format: MM,DD,YYYY")
    departure_last_place_of_landing = models.CommaSeparatedIntegerField\
            ("Date of departure from last place of landing (DDEPAMB,*,C)", max_length=10,
             blank=True, null=True,
             help_text="Date in format: MM,DD,YYYY")
    voyage_completed = models.CommaSeparatedIntegerField\
            ("Date on which slave voyage completed (DATARR44,43,45)", max_length=10,
             blank=True, null=True,
             help_text="Date in format: MM,DD,YYYY")

    # Later this can become just a property/ can be calculated
    length_middle_passage_days = models.IntegerField\
            ("Length of Middle Passage in (days) (VOYAGE)",
             max_length=6, null=True, blank=True)

    # Imputed variables
    imp_voyage_began = models.CommaSeparatedIntegerField \
            ("Year voyage began", max_length=10,
             blank=True, null=True,
             help_text="Date in format: MM,DD,YYYY")
    imp_departed_africa = models.CommaSeparatedIntegerField \
            ("Year departed Africa", max_length=10,
             blank=True, null=True,
             help_text="Date in format: MM,DD,YYYY")
    imp_arrival_at_port_of_dis = models.CommaSeparatedIntegerField\
            ("Year of arrival at port of disembarkation",
             max_length=10, blank=True, null=True,
             help_text="Date in format: MM,DD,YYYY")

    # Later this can become just a property/ can be calculated
    imp_length_home_to_disembark = models.IntegerField\
            ("Voyage length from home port to disembarkation (days) (VOY1IMP)",
             max_length=6, null=True, blank=True)
    imp_length_leaving_africa_to_disembark = models.IntegerField\
            ("Voyage length from leaving Africa to disembarkation (days) (VOY2IMP)",
             max_length=6, null=True, blank=True)

    voyage = models.ForeignKey('Voyage', null=True, blank=True,
                               related_name="voyage_name_dates")


    @property
    def _calculate_year_period(self, period):
        """
        Property to calculates proper period.

        Keyword arguments:
        period -- which period to calculate
        """
        if ((self.imp_arrival_at_port_of_dis[2]-self.years_start[period])
                % period != 0):
            return ((self.imp_arrival_at_port_of_dis[2]-self.years_start[period])
                    / period +1)
        else:
            return (self.imp_arrival_at_port_of_dis[2]-self.years_start[period]) \
                   / period

    # Calculated variables
    year_five = property(_calculate_year_period, 5)
    year_ten = property(_calculate_year_period, 10)
    year_twenty_five = property(_calculate_year_period, 25)
    year_hundred = property(_calculate_year_period, 100)


    class Meta:
        verbose_name = 'Date'
        verbose_name_plural = 'Dates'


# Voyage Captain and Crew
class VoyageCaptain(models.Model):
    """
    Voyage Captain and Crew.
    """
    name = models.CharField("Captain's name", max_length=70)

    def __unicode__(self):
        return self.name


class VoyageCaptainConnection(models.Model):
    """
    Represents the relation between Voyage Captain and
    Voyage.
    captain_order represents order of each captain (1st, 2nd, ...)
    related to: :model:`voyages.apps.voyages.VoyageCaptain`
    related to: :model:`voyages.apps.voyages.Voyage`
    """

    captain = models.ForeignKey\
            ('VoyageCaptain', related_name='captain_name')
    voyage = models.ForeignKey\
            ('Voyage', related_name='voyage')
    captain_order = models.IntegerField(max_length=1)

    class Meta:
        verbose_name = 'Voyage captain information'
        verbose_name_plural = 'Voyage captain information'

    def __unicode__(self):
        return "Captain: %d %s" % (self.captain_order, self.captain )


class VoyageCrew(models.Model):
    """
    Voyage Crew.
    related to: :model:`voyages.apps.voyages.Voyage`
    """

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
    crew_died_middle_passage = models.IntegerField \
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

    voyage = models.ForeignKey('Voyage', null=True, blank=True,
                               related_name="voyage_name_crew")

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
            ("Slaves death before leaving Africa (SLADAFRI)",
             null=True, blank=True)
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
             "(SLINTEN2)", null=True, blank=True, max_length=4)

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
            ("Total slaves purchased (TSLAVESP)",
             null=True, blank=True, max_length=4)
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
            ("Number of men (MEN1) embarked at first port of purchase",
             null=True, blank=True)
    # Representing WOMEN1 variables
    num_women_embark_first_port_purchase = models.IntegerField \
            ("Number of women (WOMEN1) embarked at first port of purchase",
             null=True, blank=True)
    # Representing BOY1 variables
    num_boy_embark_first_port_purchase = models.IntegerField \
            ("Number of boys (BOY1) embarked at first port of purchase",
             null=True, blank=True)
    # Representing GIRL1 variables
    num_girl_embark_first_port_purchase = models.IntegerField \
            ("Number of girls (GIRL1) embarked at first port of purchase",
             null=True, blank=True)
    # Representing ADULT1 variables
    num_adult_embark_first_port_purchase = models.IntegerField \
            ("Number of adults (gender unspecified) (ADULT1) "
             "embarked at first port of purchase",
             null=True, blank=True)
    # Representing CHILD1 variables
    num_child_embark_first_port_purchase = models.IntegerField \
            ("Number of children (gender unspecified) (CHILD1) "
             "embarked at first port of purchase",
             null=True, blank=True)
    # Representing INFANT1 variables
    num_infant_embark_first_port_purchase = models.IntegerField \
            ("Number of infants (INFANT1) embarked at first port of purchase",
             null=True, blank=True)
    # Representing MALE1 variables
    num_males_embark_first_port_purchase = models.IntegerField \
            ("Number of males (age unspecified) (MALE1)"
             " embarked at first port of purchase",
             null=True, blank=True)
    # Representing FEMALE1 variables
    num_females_embark_first_port_purchase = models.IntegerField \
            ("Number of females (age unspecified) (FEMALE1) "
             "embarked at first port of purchase",
             null=True, blank=True)

    # Representing MEN2 variables
    num_men_died_middle_passage = models.IntegerField \
            ("Number of men (MEN2) died on Middle Passage",
             null=True, blank=True)
    # Representing WOMEN2 variables
    num_women_died_middle_passage = models.IntegerField \
            ("Number of women (WOMEN2) died on Middle Passage",
             null=True, blank=True)
    # Representing BOY2 variables
    num_boy_died_middle_passage = models.IntegerField \
            ("Number of boys (BOY2) died on Middle Passage",
             null=True, blank=True)
    # Representing GIRL2 variables
    num_girl_died_middle_passage = models.IntegerField \
            ("Number of girls (GIRL2) died on Middle Passage",
             null=True, blank=True)
    # Representing ADULT2 variables
    num_adult_died_middle_passage = models.IntegerField \
            ("Number of adults (gender unspecified) (ADULT2) "
             "died on Middle Passage",
             null=True, blank=True)
    # Representing CHILD2 variables
    num_child_died_middle_passage = models.IntegerField \
            ("Number of children (gender unspecified) (CHILD2) "
             "died on Middle Passage",
             null=True, blank=True)
    # Representing INFANT2 variables
    num_infant_died_middle_passage = models.IntegerField \
            ("Number of infants (INFANT2) died on Middle Passage",
             null=True, blank=True)
    # Representing MALE2 variables
    num_males_died_middle_passage = models.IntegerField \
            ("Number of males (age unspecified) (MALE2) "
             "died on Middle Passage",
             null=True, blank=True)
    # Representing FEMALE2 variables
    num_females_died_middle_passage = models.IntegerField \
            ("Number of females (age unspecified) (FEMALE2) "
             "died on Middle Passage",
             null=True, blank=True)

    # Representing MEN3 variables
    num_men_disembark_first_landing = models.IntegerField \
            ("Number of men (MEN3) disembarked at first place of landing",
             null=True, blank=True)
    # Representing WOMEN3 variables
    num_women_disembark_first_landing = models.IntegerField \
            ("Number of women (WOMEN3) disembarked at first place of landing",
             null=True, blank=True)
    # Representing BOY3 variables
    num_boy_disembark_first_landing = models.IntegerField \
            ("Number of boys (BOY3) disembarked at first place of landing",
             null=True, blank=True)
    # Representing GIRL3 variables
    num_girl_disembark_first_landing = models.IntegerField \
            ("Number of girls (GIRL3) disembarked at first place of landing",
             null=True, blank=True)
    # Representing ADULT3 variables
    num_adult_disembark_first_landing = models.IntegerField \
            ("Number of adults (gender unspecified) (ADULT3) "
             "disembarked at first place of landing",
             null=True, blank=True)
    # Representing CHILD3 variables
    num_child_disembark_first_landing = models.IntegerField \
            ("Number of children (gender unspecified) (CHILD3) "
             "disembarked at first place of landing",
             null=True, blank=True)
    # Representing INFANT3 variables
    num_infant_disembark_first_landing = models.IntegerField \
            ("Number of infants (INFANT3) disembarked "
             "at first place of landing", null=True, blank=True)
    # Representing MALE3 variables
    num_males_disembark_first_landing = models.IntegerField \
            ("Number of males (age unspecified) (MALE3) "
             "disembarked at first place of landing",
             null=True, blank=True)
    # Representing FEMALE3 variables
    num_females_disembark_first_landing = models.IntegerField \
            ("Number of females (age unspecified) (FEMALE3) "
             "disembarked at first place of landing",
             null=True, blank=True)

    # Representing MEN4 variables
    num_men_embark_second_port_purchase = models.IntegerField \
            ("Number of men (MEN4) embarked at second port of purchase",
             null=True, blank=True)
    # Representing WOMEN4 variables
    num_women_embark_second_port_purchase = models.IntegerField \
            ("Number of women (WOMEN4) embarked at second port of purchase",
             null=True, blank=True)
    # Representing BOY4 variables
    num_boy_embark_second_port_purchase = models.IntegerField \
            ("Number of boys (BOY4) embarked at second port of purchase",
             null=True, blank=True)
    # Representing GIRL4 variables
    num_girl_embark_second_port_purchase = models.IntegerField \
            ("Number of girls (GIRL4) embarked at second port of purchase",
             null=True, blank=True)
    # Representing ADULT4 variables
    num_adult_embark_second_port_purchase = models.IntegerField \
            ("Number of adults (gender unspecified) (ADULT4) "
             "embarked at second port of purchase",
             null=True, blank=True)
    # Representing CHILD4 variables
    num_child_embark_second_port_purchase = models.IntegerField \
            ("Number of children (gender unspecified) (CHILD4) "
             "embarked at second port of purchase",
             null=True, blank=True)
    # Representing INFANT4 variables
    num_infant_embark_second_port_purchase = models.IntegerField \
            ("Number of infants (INFANT4) embarked "
             "at second port of purchase", null=True, blank=True)
    # Representing MALE4 variables
    num_males_embark_second_port_purchase = models.IntegerField \
            ("Number of males (age unspecified) (MALE4) "
             "embarked at second port of purchase",
             null=True, blank=True)
    # Representing FEMALE4 variables
    num_females_embark_second_port_purchase = models.IntegerField \
            ("Number of females (age unspecified) (FEMALE4) "
             "embarked at second port of purchase",
             null=True, blank=True)


    # Representing MEN5 variables
    num_men_embark_third_port_purchase = models.IntegerField \
            ("Number of men (MEN5) embarked at third port of purchase",
             null=True, blank=True)
    # Representing WOMEN5 variables
    num_women_embark_third_port_purchase = models.IntegerField \
            ("Number of women (WOMEN5) embarked at third port of purchase",
             null=True, blank=True)
    # Representing BOY5 variables
    num_boy_embark_third_port_purchase = models.IntegerField \
            ("Number of boys (BOY5) embarked at third port of purchase",
             null=True, blank=True)
    # Representing GIRL5 variables
    num_girl_embark_third_port_purchase = models.IntegerField \
            ("Number of girls (GIRL5) embarked at third port of purchase",
             null=True, blank=True)
    # Representing ADULT5 variables
    num_adult_embark_third_port_purchase = models.IntegerField \
            ("Number of adults (gender unspecified) (ADULT5) "
             "embarked at third port of purchase",
             null=True, blank=True)
    # Representing CHILD5 variables
    num_child_embark_third_port_purchase = models.IntegerField \
            ("Number of children (gender unspecified) (CHILD5) "
             "embarked at third port of purchase",
             null=True, blank=True)
    # Representing INFANT5 variables
    num_infant_embark_third_port_purchase = models.IntegerField \
            ("Number of infants (INFANT5) embarked at third port of purchase",
             null=True, blank=True)
    # Representing MALE5 variables
    num_males_embark_third_port_purchase = models.IntegerField \
            ("Number of males (age unspecified) (MALE5) embarked "
             "at third port of purchase",
             null=True, blank=True)
    # Representing FEMALE5 variables
    num_females_embark_third_port_purchase = models.IntegerField \
            ("Number of females (age unspecified) (FEMALE5) embarked "
             "at third port of purchase",
             null=True, blank=True)


    # Representing MEN6 variables
    num_men_disembark_second_landing = models.IntegerField \
            ("Number of men (MEN6) disembarked at second place of landing",
             null=True, blank=True)
    # Representing WOMEN6 variables
    num_women_disembark_second_landing = models.IntegerField \
            ("Number of women (WOMEN6) disembarked "
             "at second place of landing", null=True, blank=True)
    # Representing BOY6 variables
    num_boy_disembark_second_landing = models.IntegerField \
            ("Number of boys (BOY6) disembarked at second place of landing",
             null=True, blank=True)
    # Representing GIRL6 variables
    num_girl_disembark_second_landing = models.IntegerField \
            ("Number of girls (GIRL6) disembarked at second place of landing",
             null=True, blank=True)
    # Representing ADULT6 variables
    num_adult_disembark_second_landing = models.IntegerField \
            ("Number of adults (gender unspecified) (ADULT6) disembarked "
             "at second place of landing", null=True, blank=True)
    # Representing CHILD6 variables
    num_child_disembark_second_landing = models.IntegerField \
            ("Number of children (gender unspecified) (CHILD6) "
             "disembarked at second place of landing", null=True, blank=True)
    # Representing INFANT6 variables
    num_infant_disembark_second_landing = models.IntegerField \
            ("Number of infants (INFANT6) disembarked "
             "at second place of landing", null=True, blank=True)
    # Representing MALE6 variables
    num_males_disembark_second_landing = models.IntegerField \
            ("Number of males (age unspecified) (MALE6) "
             "disembarked at second place of landing", null=True, blank=True)
    # Representing FEMALE6 variables
    num_females_disembark_second_landing = models.IntegerField \
            ("Number of females (age unspecified) (FEMALE6) "
             "disembarked at second place of landing", null=True, blank=True)

    voyage = models.ForeignKey('Voyage',
                               related_name="voyage_name_slave_characteristics")

    class Meta:
        verbose_name = 'Slaves Characteristic'
        verbose_name_plural = "Slaves Characteristics"


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
        ordering = ['short_ref', 'full_ref']

    def __unicode__(self):
        return self.full_ref

class VoyageSourcesConnection(models.Model):
    """
    Represents the relationship between Voyage and VoyageSources
    source_order determines the order sources appear for each voyage
    related to: :model:`voyages.apps.voyages.VoyageSources`
    related to: :model:`voyages.apps.voyages.Voyage`
    """
    source = models.ForeignKey('VoyageSources', related_name="source",
                               null=True, blank=True)
    group = models.ForeignKey('Voyage', related_name="group")
    source_order = models.IntegerField(max_length=2)
    text_ref = models.CharField(_('Text reference(citation)'),
                                max_length=100, null=True, blank=True)


# Voyage (main) model
class Voyage(models.Model):
    """
    Information about voyages.
    related to: :model:`voyages.apps.voyages.VoyageGroupings`
    related to: :model:`voyages.apps.voyages.VoyageCaptain`
    related to: :model:`voyages.apps.voyages.VoyageShipOwner`
    related to: :model:`voyages.apps.voyages.VoyageSources`
    """
    #voyage_id = models.AutoField(primary_key=True)
    voyage_id = models.IntegerField("Voyage ID (can be empty)", null=True, blank=True)

    voyage_in_cd_rom = models.BooleanField("Voyage in 1999 CD-ROM?",
                                           max_length=1, blank=True)

    # Technical variables
    voyage_groupings = models.ForeignKey('VoyageGroupings', blank=True, null=True)

    # Data and imputed variables

    voyage_captain = models.ManyToManyField \
            ("VoyageCaptain", through='VoyageCaptainConnection',
             help_text="Voyage Captain",
             blank=True, null=True)
    voyage_ship_owner = models.ManyToManyField \
        ("VoyageShipOwner", through='VoyageShipOwnerConnection',
         help_text="Voyage Ship Owner",
         blank=True, null=True)

    # One Voyage can contain multiple sources and one source can refer
    # to multiple voyages
    voyage_sources = models.ManyToManyField \
            ('VoyageSources', through='VoyageSourcesConnection',
             related_name='voyage_sources', blank=True, null=True)

    class Meta:
        ordering = ['voyage_id',]
        verbose_name = 'Voyage'
        verbose_name_plural = "Voyages"

    def __unicode__(self):
        return "Voyage #%s" % str(self.voyage_id)