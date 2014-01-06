# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
import voyages
#from voyages.apps.voyage import legacy_models


# Keep
class Areas(voyages.apps.voyage.models.LegacyModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    order_num = models.IntegerField(null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    show_at_zoom = models.IntegerField()
    show_on_map = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'areas'

# Keep
class Estimates(voyages.apps.voyage.models.LegacyModel):
    nation = models.ForeignKey('EstimatesNations', db_column='nation')
    yeardep = models.IntegerField()
    majbuyrg = models.ForeignKey('EstimatesExportRegions', null=True, db_column='majbuyrg', blank=True)
    mjselimp = models.ForeignKey('EstimatesImportRegions', null=True, db_column='mjselimp', blank=True)
    slaximp = models.FloatField(null=True, blank=True)
    slamimp = models.FloatField(null=True, blank=True)
    id = models.BigIntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'estimates'

# Keep
class EstimatesExportAreas(voyages.apps.voyage.models.LegacyModel):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    order_num = models.IntegerField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    show_at_zoom = models.IntegerField()
    show_on_map = models.BooleanField()
    class Meta:
        db_table = 'estimates_export_areas'

# Keep
class EstimatesExportRegions(voyages.apps.voyage.models.LegacyModel):
#    id = models.BigIntegerField()
    name = models.CharField(max_length=200)
    order_num = models.IntegerField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    show_at_zoom = models.IntegerField()
    area = models.ForeignKey(EstimatesExportAreas)
    show_on_map = models.BooleanField()
    class Meta:
        db_table = 'estimates_export_regions'

# Keep
class EstimatesImportAreas(voyages.apps.voyage.models.LegacyModel):
#    id = models.BigIntegerField()
    name = models.CharField(max_length=200)
    order_num = models.IntegerField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    show_at_zoom = models.IntegerField()
    show_on_map = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'estimates_import_areas'

# Keep
class EstimatesImportRegions(voyages.apps.voyage.models.LegacyModel):
#    id = models.BigIntegerField()
    name = models.CharField(max_length=200)
    order_num = models.IntegerField()
    area = models.ForeignKey(EstimatesImportAreas)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    show_at_zoom = models.IntegerField()
    show_on_map = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'estimates_import_regions'

# Keep xmimpflag
class EstimatesNations(voyages.apps.voyage.models.LegacyModel):
#    id = models.BigIntegerField()
    name = models.CharField(max_length=200, blank=True)
    order_num = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'estimates_nations'

# Keep
class Fates(voyages.apps.voyage.models.LegacyModel):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    class Meta:
        managed = False
        db_table = 'fates'

# Keep
class FatesOwner(voyages.apps.voyage.models.LegacyModel):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    class Meta:
        managed = False
        db_table = 'fates_owner'

# Keep
class FatesSlaves(voyages.apps.voyage.models.LegacyModel):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    class Meta:
        managed = False
        db_table = 'fates_slaves'

# Keep
class FatesVessel(voyages.apps.voyage.models.LegacyModel):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    class Meta:
        managed = False
        db_table = 'fates_vessel'

# Keep
class Nations(voyages.apps.voyage.models.LegacyModel):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    order_num = models.IntegerField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'nations'

# Keep
class Ports(voyages.apps.voyage.models.LegacyModel):
#    id = models.BigIntegerField()
    region = models.ForeignKey('Regions')
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    order_num = models.IntegerField()
    show_at_zoom = models.IntegerField()
    show_on_main_map = models.BooleanField()
    show_on_voyage_map = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'ports'

# Keep
class Regions(voyages.apps.voyage.models.LegacyModel):
#    id = models.BigIntegerField()
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    area_id = models.IntegerField(null=True, blank=True)
    order_num = models.IntegerField()
    show_at_zoom = models.IntegerField()
    show_on_main_map = models.BooleanField()
    show_on_map = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'regions'

# Keep
class LegacyResistance(voyages.apps.voyage.models.LegacyModel):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    class Meta:
        managed = False
        db_table = 'resistance'

# Keep
class Sources(voyages.apps.voyage.models.LegacyModel):
    iid = models.BigIntegerField(primary_key=True)
    type = models.SmallIntegerField(null=True, blank=True)
    id = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=1000)
    class Meta:
        managed = False
        db_table = 'sources'

# Keep
class TonType(voyages.apps.voyage.models.LegacyModel):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    class Meta:
        managed = False
        db_table = 'ton_type'

# Keep
class VesselRigs(voyages.apps.voyage.models.LegacyModel):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    class Meta:
        managed = False
        db_table = 'vessel_rigs'

# Keep
class Voyages(voyages.apps.voyage.models.LegacyModel):
    voyageid = models.IntegerField(blank=True, primary_key=True)
    shipname = models.CharField(max_length=300, blank=True)
    captaina = models.CharField(max_length=60, blank=True)
    captainb = models.CharField(max_length=40, blank=True)
    captainc = models.CharField(max_length=40, blank=True)
    datedep = models.DateField(null=True, blank=True)
    plac1tra = models.ForeignKey(Ports, null=True, db_column='plac1tra', related_name='voyages_plac1tra', blank=True)
    plac2tra = models.ForeignKey(Ports, null=True, db_column='plac2tra', related_name='voyages_plac2tra', blank=True)
    plac3tra = models.ForeignKey(Ports, null=True, db_column='plac3tra', related_name='voyages_plac3tra', blank=True)
    npafttra = models.BigIntegerField(null=True, blank=True)
    sla1port = models.ForeignKey(Ports, null=True, db_column='sla1port', related_name='voyages_sla1port', blank=True)
    tslavesd = models.IntegerField(null=True, blank=True)
    slaarriv = models.IntegerField(null=True, blank=True)
    slas32 = models.IntegerField(null=True, blank=True)
    adpsale1 = models.ForeignKey(Ports, null=True, db_column='adpsale1', related_name='voyages_adpsale1', blank=True)
    slas36 = models.IntegerField(null=True, blank=True)
    adpsale2 = models.ForeignKey(Ports, null=True, db_column='adpsale2', related_name='voyages_adpsale2', blank=True)
    slas39 = models.IntegerField(null=True, blank=True)
    portret = models.ForeignKey(Ports, null=True, db_column='portret', related_name='voyages_portret', blank=True)
    fate = models.ForeignKey(Fates, null=True, db_column='fate', blank=True)
    sourcea = models.CharField(max_length=60, blank=True)
    sourceb = models.CharField(max_length=60, blank=True)
    sourcec = models.CharField(max_length=60, blank=True)
    sourced = models.CharField(max_length=60, blank=True)
    sourcee = models.CharField(max_length=60, blank=True)
    sourcef = models.CharField(max_length=60, blank=True)
    sourceg = models.CharField(max_length=60, blank=True)
    sourceh = models.CharField(max_length=60, blank=True)
    sourcei = models.CharField(max_length=60, blank=True)
    sourcej = models.CharField(max_length=60, blank=True)
    sourcek = models.CharField(max_length=60, blank=True)
    sourcel = models.CharField(max_length=60, blank=True)
    sourcem = models.CharField(max_length=60, blank=True)
    sourcen = models.CharField(max_length=60, blank=True)
    sourceo = models.CharField(max_length=60, blank=True)
    sourcep = models.CharField(max_length=60, blank=True)
    sourceq = models.CharField(max_length=60, blank=True)
    sourcer = models.CharField(max_length=60, blank=True)
    slintend = models.IntegerField(null=True, blank=True)
    tonnage = models.IntegerField(null=True, blank=True)
    crewdied = models.IntegerField(null=True, blank=True)
    ncar13 = models.IntegerField(null=True, blank=True)
    ncar15 = models.IntegerField(null=True, blank=True)
    ncar17 = models.IntegerField(null=True, blank=True)
    guns = models.IntegerField(null=True, blank=True)
    crew1 = models.IntegerField(null=True, blank=True)
    rig = models.ForeignKey(VesselRigs, null=True, db_column='rig', blank=True)
    placcons = models.ForeignKey(Ports, null=True, db_column='placcons', related_name='voyages_placcons', blank=True)
    yrreg = models.IntegerField(null=True, blank=True)
    crew3 = models.IntegerField(null=True, blank=True)
    resistance = models.ForeignKey(LegacyResistance, null=True, db_column='resistance', blank=True)
    ownera = models.CharField(max_length=60, blank=True)
    ownerb = models.CharField(max_length=60, blank=True)
    ownerc = models.CharField(max_length=60, blank=True)
    ownerd = models.CharField(max_length=60, blank=True)
    ownere = models.CharField(max_length=60, blank=True)
    ownerf = models.CharField(max_length=60, blank=True)
    ownerg = models.CharField(max_length=60, blank=True)
    ownerh = models.CharField(max_length=60, blank=True)
    owneri = models.CharField(max_length=60, blank=True)
    ownerj = models.CharField(max_length=60, blank=True)
    ownerk = models.CharField(max_length=60, blank=True)
    ownerl = models.CharField(max_length=60, blank=True)
    ownerm = models.CharField(max_length=60, blank=True)
    ownern = models.CharField(max_length=60, blank=True)
    ownero = models.CharField(max_length=60, blank=True)
    ownerp = models.CharField(max_length=60, blank=True)
    natinimp = models.IntegerField(null=True, blank=True)
    retrnreg = models.ForeignKey(Regions, null=True, db_column='retrnreg', related_name='voyages_retrnreg', blank=True)
    yearam = models.IntegerField(null=True, blank=True)
    tonmod = models.FloatField(null=True, blank=True)
    vymrtimp = models.IntegerField(null=True, blank=True)
    regem1 = models.ForeignKey(Regions, null=True, db_column='regem1', related_name='voyages_regem1', blank=True)
    regem2 = models.ForeignKey(Regions, null=True, db_column='regem2', related_name='voyages_regem2', blank=True)
    regem3 = models.ForeignKey(Regions, null=True, db_column='regem3', related_name='voyages_regem3', blank=True)
    majbyimp = models.ForeignKey(Regions, null=True, db_column='majbyimp', related_name='voyages_majbyimp', blank=True)
    regdis1 = models.ForeignKey(Regions, null=True, db_column='regdis1', related_name='voyages_regdis1', blank=True)
    regdis2 = models.ForeignKey(Regions, null=True, db_column='regdis2', related_name='voyages_regdis2', blank=True)
    regdis3 = models.ForeignKey(Regions, null=True, db_column='regdis3', related_name='voyages_regdis3', blank=True)
    fate2 = models.ForeignKey(FatesSlaves, null=True, db_column='fate2', blank=True)
    fate3 = models.ForeignKey(FatesVessel, null=True, db_column='fate3', blank=True)
    fate4 = models.ForeignKey(FatesOwner, null=True, db_column='fate4', blank=True)
    mjselimp = models.ForeignKey(Regions, null=True, db_column='mjselimp', related_name='voyages_mjselimp', blank=True)
    vymrtrat = models.FloatField(null=True, blank=True)
    slaximp = models.IntegerField(null=True, blank=True)
    slamimp = models.IntegerField(null=True, blank=True)
    voy2imp = models.IntegerField(null=True, blank=True)
    voy1imp = models.IntegerField(null=True, blank=True)
    malrat7 = models.FloatField(null=True, blank=True)
    chilrat7 = models.FloatField(null=True, blank=True)
    womrat7 = models.FloatField(null=True, blank=True)
    menrat7 = models.FloatField(null=True, blank=True)
    girlrat7 = models.FloatField(null=True, blank=True)
    boyrat7 = models.FloatField(null=True, blank=True)
    jamcaspr = models.FloatField(null=True, blank=True)
    mjbyptimp = models.ForeignKey(Ports, null=True, db_column='mjbyptimp', related_name='voyages_mjbyptimp', blank=True)
    yrcons = models.IntegerField(null=True, blank=True)
    placreg = models.BigIntegerField(null=True, blank=True)
    ptdepimp = models.BigIntegerField(null=True, blank=True)
    mjslptimp = models.BigIntegerField(null=True, blank=True)
    deptregimp = models.BigIntegerField(null=True, blank=True)
    datebuy = models.DateField(null=True, blank=True)
    datedepam = models.DateField(null=True, blank=True)
    dateend = models.DateField(null=True, blank=True)
    dateland1 = models.DateField(null=True, blank=True)
    dateland2 = models.DateField(null=True, blank=True)
    dateland3 = models.DateField(null=True, blank=True)
    dateleftafr = models.DateField(null=True, blank=True)
    e_majbyimp = models.ForeignKey(EstimatesExportRegions, null=True, db_column='e_majbyimp', blank=True)
    e_mjselimp = models.BigIntegerField(null=True, blank=True)
    e_natinimp = models.ForeignKey(EstimatesNations, null=True, db_column='e_natinimp', blank=True)
    portdep = models.ForeignKey(Ports, null=True, db_column='portdep', related_name='voyages_portdep', blank=True)
    embport = models.ForeignKey(Ports, null=True, db_column='embport', related_name='voyages_embport', blank=True)
    arrport = models.ForeignKey(Ports, null=True, db_column='arrport', related_name='voyages_arrport', blank=True)
    tontype = models.IntegerField(null=True, blank=True)
    sladamer = models.IntegerField(null=True, blank=True)
    saild1 = models.IntegerField(null=True, blank=True)
    saild2 = models.IntegerField(null=True, blank=True)
    saild3 = models.IntegerField(null=True, blank=True)
    saild4 = models.IntegerField(null=True, blank=True)
    saild5 = models.IntegerField(null=True, blank=True)
    embport2 = models.ForeignKey(Ports, null=True, db_column='embport2', related_name='voyages_embport2', blank=True)
    voyage = models.IntegerField(null=True, blank=True)
    child2 = models.IntegerField(null=True, blank=True)
    child3 = models.IntegerField(null=True, blank=True)
    crew4 = models.IntegerField(null=True, blank=True)
    crew5 = models.IntegerField(null=True, blank=True)
    adult1 = models.IntegerField(null=True, blank=True)
    child1 = models.IntegerField(null=True, blank=True)
    female1 = models.IntegerField(null=True, blank=True)
    male1 = models.IntegerField(null=True, blank=True)
    men1 = models.IntegerField(null=True, blank=True)
    women1 = models.IntegerField(null=True, blank=True)
    boy1 = models.IntegerField(null=True, blank=True)
    girl1 = models.IntegerField(null=True, blank=True)
    female2 = models.IntegerField(null=True, blank=True)
    male2 = models.IntegerField(null=True, blank=True)
    men2 = models.IntegerField(null=True, blank=True)
    women2 = models.IntegerField(null=True, blank=True)
    boy2 = models.IntegerField(null=True, blank=True)
    girl2 = models.IntegerField(null=True, blank=True)
    female3 = models.IntegerField(null=True, blank=True)
    male3 = models.IntegerField(null=True, blank=True)
    men3 = models.IntegerField(null=True, blank=True)
    women3 = models.IntegerField(null=True, blank=True)
    boy3 = models.IntegerField(null=True, blank=True)
    girl3 = models.IntegerField(null=True, blank=True)
    child4 = models.IntegerField(null=True, blank=True)
    female4 = models.IntegerField(null=True, blank=True)
    male4 = models.IntegerField(null=True, blank=True)
    men4 = models.IntegerField(null=True, blank=True)
    women4 = models.IntegerField(null=True, blank=True)
    boy4 = models.IntegerField(null=True, blank=True)
    girl4 = models.IntegerField(null=True, blank=True)
    child6 = models.IntegerField(null=True, blank=True)
    female6 = models.IntegerField(null=True, blank=True)
    male6 = models.IntegerField(null=True, blank=True)
    men6 = models.IntegerField(null=True, blank=True)
    women6 = models.IntegerField(null=True, blank=True)
    boy6 = models.IntegerField(null=True, blank=True)
    girl6 = models.IntegerField(null=True, blank=True)
    crew2 = models.IntegerField(null=True, blank=True)
    infantm3 = models.IntegerField(null=True, blank=True)
    infantf3 = models.IntegerField(null=True, blank=True)
    sladied1 = models.IntegerField(null=True, blank=True)
    sladied2 = models.IntegerField(null=True, blank=True)
    sladied3 = models.IntegerField(null=True, blank=True)
    sladied4 = models.IntegerField(null=True, blank=True)
    sladied5 = models.IntegerField(null=True, blank=True)
    sladied6 = models.IntegerField(null=True, blank=True)
    adult3 = models.IntegerField(null=True, blank=True)
    insurrec = models.IntegerField(null=True, blank=True)
    child5 = models.IntegerField(null=True, blank=True)
    female5 = models.IntegerField(null=True, blank=True)
    male5 = models.IntegerField(null=True, blank=True)
    men5 = models.IntegerField(null=True, blank=True)
    women5 = models.IntegerField(null=True, blank=True)
    boy5 = models.IntegerField(null=True, blank=True)
    girl5 = models.IntegerField(null=True, blank=True)
    arrport2 = models.ForeignKey(Ports, null=True, db_column='arrport2', related_name='voyages_arrport2', blank=True)
    infant3 = models.IntegerField(null=True, blank=True)
    infant1 = models.IntegerField(null=True, blank=True)
    adult5 = models.IntegerField(null=True, blank=True)
    adult2 = models.IntegerField(null=True, blank=True)
    adult4 = models.IntegerField(null=True, blank=True)
    infant4 = models.IntegerField(null=True, blank=True)
    crew = models.IntegerField(null=True, blank=True)
    suggestion = models.NullBooleanField(null=True, blank=True)
    revision = models.IntegerField(null=True, blank=True)
    nppretra = models.IntegerField(null=True, blank=True)
    tslavesp = models.IntegerField(null=True, blank=True)
    sladvoy = models.IntegerField(null=True, blank=True)
    npprior = models.IntegerField(null=True, blank=True)
    national = models.IntegerField(null=True, blank=True)
    slinten2 = models.IntegerField(null=True, blank=True)
    ndesert = models.IntegerField(null=True, blank=True)
    sladafri = models.IntegerField(null=True, blank=True)
    adult6 = models.IntegerField(null=True, blank=True)
    yeardep = models.IntegerField(null=True, blank=True)
    datepl = models.IntegerField(null=True, blank=True)
    datepc = models.IntegerField(null=True, blank=True)
    datedepc = models.IntegerField(null=True, blank=True)
    datedepa = models.IntegerField(null=True, blank=True)
    datedepb = models.IntegerField(null=True, blank=True)
    d1slatrc = models.IntegerField(null=True, blank=True)
    d1slatrb = models.IntegerField(null=True, blank=True)
    d1slatra = models.IntegerField(null=True, blank=True)
    dlslatrc = models.IntegerField(null=True, blank=True)
    dlslatrb = models.IntegerField(null=True, blank=True)
    dlslatra = models.IntegerField(null=True, blank=True)
    datarr = models.IntegerField(null=True, blank=True)
    datarr33 = models.IntegerField(null=True, blank=True)
    datarr32 = models.IntegerField(null=True, blank=True)
    datarr31 = models.IntegerField(null=True, blank=True)
    datarr34 = models.IntegerField(null=True, blank=True)
    datarr40 = models.IntegerField(null=True, blank=True)
    datarr39 = models.IntegerField(null=True, blank=True)
    ddepamb = models.IntegerField(null=True, blank=True)
    ddepam = models.IntegerField(null=True, blank=True)
    ddepamc = models.IntegerField(null=True, blank=True)
    datarr44 = models.IntegerField(null=True, blank=True)
    datarr43 = models.IntegerField(null=True, blank=True)
    datarr45 = models.IntegerField(null=True, blank=True)
    datarr36 = models.IntegerField(null=True, blank=True)
    datarr37 = models.IntegerField(null=True, blank=True)
    yearaf = models.IntegerField(null=True, blank=True)
    year100 = models.IntegerField(null=True, blank=True)
    year25 = models.IntegerField(null=True, blank=True)
    year5 = models.IntegerField(null=True, blank=True)
    tslmtimp = models.IntegerField(null=True, blank=True)
    sla32imp = models.FloatField(null=True, blank=True)
    sla36imp = models.FloatField(null=True, blank=True)
    imprat = models.FloatField(null=True, blank=True)
    sla39imp = models.FloatField(null=True, blank=True)
    ncr13imp = models.FloatField(null=True, blank=True)
    ncr15imp = models.FloatField(null=True, blank=True)
    ncr17imp = models.FloatField(null=True, blank=True)
    exprat = models.FloatField(null=True, blank=True)
    male1imp = models.FloatField(null=True, blank=True)
    feml1imp = models.FloatField(null=True, blank=True)
    chil1imp = models.FloatField(null=True, blank=True)
    malrat1 = models.FloatField(null=True, blank=True)
    chilrat1 = models.FloatField(null=True, blank=True)
    slavemx1 = models.FloatField(null=True, blank=True)
    slavema1 = models.FloatField(null=True, blank=True)
    male3imp = models.FloatField(null=True, blank=True)
    feml3imp = models.FloatField(null=True, blank=True)
    chil3imp = models.FloatField(null=True, blank=True)
    malrat3 = models.FloatField(null=True, blank=True)
    chilrat3 = models.FloatField(null=True, blank=True)
    slavemx3 = models.FloatField(null=True, blank=True)
    slavema3 = models.FloatField(null=True, blank=True)
    adlt3imp = models.FloatField(null=True, blank=True)
    #filter_$ = models.FloatField(null=True, blank=True)
    womrat1 = models.FloatField(null=True, blank=True)
    womrat3 = models.FloatField(null=True, blank=True)
    menrat1 = models.FloatField(null=True, blank=True)
    menrat3 = models.FloatField(null=True, blank=True)
    girlrat1 = models.FloatField(null=True, blank=True)
    girlrat3 = models.FloatField(null=True, blank=True)
    boyrat3 = models.FloatField(null=True, blank=True)
    boyrat1 = models.FloatField(null=True, blank=True)
    #pound_price = models.FloatField(null=True, blank=True)
    female7 = models.FloatField(null=True, blank=True)
    male7 = models.FloatField(null=True, blank=True)
    men7 = models.FloatField(null=True, blank=True)
    women7 = models.FloatField(null=True, blank=True)
    boy7 = models.FloatField(null=True, blank=True)
    girl7 = models.FloatField(null=True, blank=True)
    child7 = models.FloatField(null=True, blank=True)
    adult7 = models.FloatField(null=True, blank=True)
    xmimpflag = models.FloatField(null=True, blank=True)
    slavemx7 = models.FloatField(null=True, blank=True)
    slavema7 = models.FloatField(null=True, blank=True)
    year10 = models.IntegerField(null=True, blank=True)
    captcat = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)
    datarr38 = models.IntegerField(null=True, blank=True)
    datarr41 = models.IntegerField(null=True, blank=True)
    spanpre1640 = models.IntegerField(null=True, blank=True)
    spanpre1595 = models.IntegerField(null=True, blank=True)
    rice = models.FloatField(null=True, blank=True)
    yearrice = models.IntegerField(null=True, blank=True)
    riceafrica = models.FloatField(null=True, blank=True)
    majbuypt = models.IntegerField(null=True, blank=True)
    majselpt = models.IntegerField(null=True, blank=True)
    destin = models.IntegerField(null=True, blank=True)
    constreg = models.IntegerField(null=True, blank=True)
    regisreg = models.IntegerField(null=True, blank=True)
    deptreg = models.IntegerField(null=True, blank=True)
    embreg = models.IntegerField(null=True, blank=True)
    embreg2 = models.IntegerField(null=True, blank=True)
    majbuyreg = models.IntegerField(null=True, blank=True)
    regarr = models.IntegerField(null=True, blank=True)
    regarr2 = models.IntegerField(null=True, blank=True)
    majselrg = models.IntegerField(null=True, blank=True)
    deptreg1 = models.IntegerField(null=True, blank=True)
    deptregimp1 = models.IntegerField(null=True, blank=True)
    majbyimp1 = models.IntegerField(null=True, blank=True)
    regdis11 = models.IntegerField(null=True, blank=True)
    regdis22 = models.IntegerField(null=True, blank=True)
    mjselimp1 = models.IntegerField(null=True, blank=True)
    retrnreg1 = models.IntegerField(null=True, blank=True)
    iid = models.IntegerField(unique=True)
    evgreen = models.NullBooleanField(null=True, blank=True)
    adlt1imp = models.IntegerField(null=True, blank=True)
    slavmax1 = models.IntegerField(null=True, blank=True)
    slavmax3 = models.IntegerField(null=True, blank=True)
    slavmax7 = models.IntegerField(null=True, blank=True)
    adlt2imp = models.IntegerField(null=True, blank=True)
    chil2imp = models.IntegerField(null=True, blank=True)
    male2imp = models.IntegerField(null=True, blank=True)
    feml2imp = models.IntegerField(null=True, blank=True)
    infant2 = models.IntegerField(null=True, blank=True)
    infant5 = models.IntegerField(null=True, blank=True)
    infant6 = models.IntegerField(null=True, blank=True)
    placcons_port = models.BigIntegerField(null=True, blank=True)
    placcons_region = models.BigIntegerField(null=True, blank=True)
    placcons_area = models.BigIntegerField(null=True, blank=True)
    placreg_port = models.BigIntegerField(null=True, blank=True)
    placreg_region = models.BigIntegerField(null=True, blank=True)
    placreg_area = models.BigIntegerField(null=True, blank=True)
    ptdepimp_port = models.BigIntegerField(null=True, blank=True)
    ptdepimp_region = models.BigIntegerField(null=True, blank=True)
    ptdepimp_area = models.BigIntegerField(null=True, blank=True)
    plac1tra_port = models.BigIntegerField(null=True, blank=True)
    plac1tra_region = models.BigIntegerField(null=True, blank=True)
    plac1tra_area = models.BigIntegerField(null=True, blank=True)
    plac2tra_port = models.BigIntegerField(null=True, blank=True)
    plac2tra_region = models.BigIntegerField(null=True, blank=True)
    plac2tra_area = models.BigIntegerField(null=True, blank=True)
    plac3tra_port = models.BigIntegerField(null=True, blank=True)
    plac3tra_region = models.BigIntegerField(null=True, blank=True)
    plac3tra_area = models.BigIntegerField(null=True, blank=True)
    mjbyptimp_port = models.BigIntegerField(null=True, blank=True)
    mjbyptimp_region = models.BigIntegerField(null=True, blank=True)
    mjbyptimp_area = models.BigIntegerField(null=True, blank=True)
    npafttra_port = models.BigIntegerField(null=True, blank=True)
    npafttra_region = models.BigIntegerField(null=True, blank=True)
    npafttra_area = models.BigIntegerField(null=True, blank=True)
    sla1port_port = models.BigIntegerField(null=True, blank=True)
    sla1port_region = models.BigIntegerField(null=True, blank=True)
    sla1port_area = models.BigIntegerField(null=True, blank=True)
    adpsale1_port = models.BigIntegerField(null=True, blank=True)
    adpsale1_region = models.BigIntegerField(null=True, blank=True)
    adpsale1_area = models.BigIntegerField(null=True, blank=True)
    adpsale2_port = models.BigIntegerField(null=True, blank=True)
    adpsale2_region = models.BigIntegerField(null=True, blank=True)
    adpsale2_area = models.BigIntegerField(null=True, blank=True)
    mjslptimp_port = models.BigIntegerField(null=True, blank=True)
    mjslptimp_region = models.BigIntegerField(null=True, blank=True)
    mjslptimp_area = models.BigIntegerField(null=True, blank=True)
    portret_port = models.BigIntegerField(null=True, blank=True)
    portret_region = models.BigIntegerField(null=True, blank=True)
    portret_area = models.BigIntegerField(null=True, blank=True)
    portdep_port = models.BigIntegerField(null=True, blank=True)
    portdep_region = models.BigIntegerField(null=True, blank=True)
    portdep_area = models.BigIntegerField(null=True, blank=True)
    embport_port = models.BigIntegerField(null=True, blank=True)
    embport_region = models.BigIntegerField(null=True, blank=True)
    embport_area = models.BigIntegerField(null=True, blank=True)
    arrport_port = models.BigIntegerField(null=True, blank=True)
    arrport_region = models.BigIntegerField(null=True, blank=True)
    arrport_area = models.BigIntegerField(null=True, blank=True)
    embport2_port = models.BigIntegerField(null=True, blank=True)
    embport2_region = models.BigIntegerField(null=True, blank=True)
    embport2_area = models.BigIntegerField(null=True, blank=True)
    arrport2_port = models.BigIntegerField(null=True, blank=True)
    arrport2_region = models.BigIntegerField(null=True, blank=True)
    arrport2_area = models.BigIntegerField(null=True, blank=True)
    shipname_index = models.TextField(blank=True) # This field type is a guess.
    captains_index = models.TextField(blank=True) # This field type is a guess.
    owners_index = models.TextField(blank=True) # This field type is a guess.
    sources_index = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        managed = False
        db_table = 'voyages'

# Keep
class Xmimpflag(voyages.apps.voyage.models.LegacyModel):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    class Meta:
        managed = False
        db_table = 'xmimpflag'
