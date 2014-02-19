import traceback
from django.core.paginator import Paginator
from django.core.management.base import BaseCommand, CommandError
from voyages.apps.voyage import models, legacy_models
from decimal import *

class Command(BaseCommand):
    args = '<>'
    help = 'Syncs the data from the legacy wilson database to the database configured in this project.'
    def handle(self, *args, **options):
        unknown_port_value = 99801
        pag = Paginator(legacy_models.Voyages.objects.filter(suggestion=False, revision=1).order_by('voyageid'), 100)
        print "Paginator count %s" % pag.count
        print "Paginator page range count %s" % len(pag.page_range)
        print "Paginator last page number %s" % pag.page_range[-1]
        models.Voyage.objects.all().delete()
        models.VoyageShip.objects.all().delete()
        models.VoyageShipOwnerConnection.objects.all().delete()
        models.VoyageShipOwner.objects.all().delete()
        models.VoyageOutcome.objects.all().delete()
        models.VoyageDates.objects.all().delete()
        models.VoyageCaptain.objects.all().delete()
        models.VoyageCaptainConnection.objects.all().delete()
        models.VoyageSourcesConnection.objects.all().delete()
        models.VoyageItinerary.objects.all().delete()
        models.VoyageSlavesNumbers.objects.all().delete()
        listSources = models.VoyageSources.objects.all()
        count = 0
        try:
            for x in pag.page_range:
                for i in pag.page(x).object_list:
                    voyageObj = models.Voyage()
                    count += 1
                    print count
                    if i.voyageid is not None:
                        voyageObj.voyage_id = i.voyageid
                        voyageObj.save()
                    ship = models.VoyageShip()
                    #ship.voyage = voyageObj
                    # There are some null values in wilson that should be false instead
                    voyageObj.voyage_in_cd_rom = not not i.evgreen
                    if i.xmimpflag:
                        xmimpflag = int(i.xmimpflag)
                        xmimpflags = models.VoyageGroupings.objects.filter(value=xmimpflag)
                        if i.xmimpflag and len(xmimpflags) >= 1:
                            voyageObj.voyage_groupings = xmimpflags[0]
                        if i.xmimpflag and len(xmimpflags) < 1:
                            print "ERROR: xmimpflag has invalid VoyageGroupings value: %s" % xmimpflag
                    if i.shipname:
                        ship.ship_name = i.shipname
                    if i.national:
                        ship.nationality_ship = models.Nationality.objects.get(value=i.national)
                    ship.tonnage = i.tonnage
                    if i.tontype:
                        ship.ton_type = models.TonType.objects.get(value=i.tontype)
                    if i.rig:
                        ship.rig_of_vessel = models.RigOfVessel.objects.get(value=i.rig.id)
                    ship.guns_mounted = i.guns
                    ship.year_of_construction = i.yrcons
                    if i.placcons:
                        ship.vessel_construction_place = models.Place.objects.get(value=i.placcons.id)
                    if i.constreg:
                        ship.vessel_constructoin_region = models.Region.objects.get(value=i.constreg)
                    ship.year_of_construction = i.yrcons
                    ship.registered_year = i.yrreg
                    if i.placreg:
                        ship.registered_place = models.Place.objects.get(value=i.placreg)
                    if i.regisreg:
                        ship.registered_region = models.Region.objects.get(value=i.regisreg)
                    if i.natinimp:
                        ship.imputed_nationality = models.Nationality.objects.get(value=i.natinimp)
                    if i.tonmod:
                        ship.tonnage_mod = str(round(i.tonmod, 1))
                    #ship.save()
                    #voyageObj.voyage_ship = ship
                    #voyageObj.save()

                    # Owners section
                    letters = map(chr, range(97, 97 + 16)) # from a to p
                    for idx, letter in enumerate(letters):
                        # Inserting ownera, ownerb, ..., ownerp
                        attr = getattr(i, 'owner' + letter)
                        if attr:
                            # TODO: see if this should just be a create instead
                            tmpOwner = models.VoyageShipOwner.objects.create(name=attr)
                            # Create voyage-owner connection
                            models.VoyageShipOwnerConnection.objects.create(owner=tmpOwner, voyage=voyageObj, owner_order=(idx+1))
                    outcome = models.VoyageOutcome()
                    #outcome.voyage = voyageObj
                    if i.fate:
                        outcome.particular_outcome = models.ParticularOutcome.objects.get(value=i.fate.id)
                    if i.resistance:
                        outcome.resistance = models.Resistance.objects.get(value=i.resistance.id)
                    if i.fate2:
                        outcome.outcome_slaves = models.SlavesOutcome.objects.get(value=i.fate2.id)
                    if i.fate3:
                        outcome.vessel_captured_outcome = models.VesselCapturedOutcome.objects.get(value=i.fate3.id)
                    if i.fate4:
                        outcome.outcome_owner = models.OwnerOutcome.objects.get(value=i.fate4.id)
                    #outcome.save()

                    itinerary = models.VoyageItinerary()
                    #itinerary.voyage = voyageObj
                    if i.portdep:
                        itinerary.port_of_departure = models.Place.objects.get(value=i.portdep.id)
                    if i.embport:
                        itinerary.int_first_port_emb = models.Place.objects.get(value=i.embport.id)
                    if i.embport2:
                        itinerary.int_second_port_emb = models.Place.objects.get(value=i.embport2.id)
                    if i.embreg:
                        itinerary.int_first_region_purchase_slaves = models.Region.objects.get(value=i.embreg)
                    if i.embreg2:
                        itinerary.int_second_region_purchase_slaves = models.Region.objects.get(value=i.embreg2)
                    if i.arrport:
                        itinerary.int_first_port_dis = models.Place.objects.get(value=i.arrport.id)
                    if i.arrport2:
                        itinerary.int_second_port_dis = models.Place.objects.get(value=i.arrport2.id)
                    if i.regarr:
                        itinerary.int_first_region_slave_landing = models.Region.objects.get(value=i.regarr)
                    if i.regarr2:
                        itinerary.int_second_region_slave_landing = models.Region.objects.get(value=i.regarr2)
                    itinerary.ports_called_buying_slaves = i.nppretra
                    if i.plac1tra:
                        itinerary.first_place_slave_purchase = models.Place.objects.get(value=i.plac1tra.id)
                    if i.plac2tra:
                        itinerary.second_place_slave_purchase = models.Place.objects.get(value=i.plac2tra.id)
                    if i.plac3tra:
                        itinerary.third_place_slave_purchase = models.Place.objects.get(value=i.plac3tra.id)
                    if i.regem1:
                        itinerary.first_region_slave_emb = models.Region.objects.get(value=i.regem1.id)
                    if i.regem2:
                        itinerary.second_region_slave_emb = models.Region.objects.get(value=i.regem2.id)
                    if i.regem3:
                        itinerary.third_region_slave_emb = models.Region.objects.get(value=i.regem3.id)
                    npafttras = models.Place.objects.filter(value=i.npafttra)
                    if i.npafttra and len(npafttras) >= 1:
                        itinerary.port_of_call_before_atl_crossing = npafttras[0]
                    if i.npafttra and len(npafttras) < 1:
                        print "WARNING: npafttra is invalid port value of %s, replacing value with '???' 99801" % i.npafttra
                        itinerary.port_of_call_before_atl_crossing = models.Place.objects.get(value=unknown_port_value)
                    itinerary.number_of_ports_of_call = i.npprior
                    if i.sla1port:
                        itinerary.first_landing_place = models.Place.objects.get(value=i.sla1port.id)
                    if i.adpsale1:
                        itinerary.second_landing_place = models.Place.objects.get(value=i.adpsale1.id)
                    if i.adpsale2:
                        itinerary.third_landing_place = models.Place.objects.get(value=i.adpsale2.id)
                    if i.regdis1:
                        itinerary.first_landing_region = models.Region.objects.get(value=i.regdis1.id)
                    if i.regdis2:
                        itinerary.second_landing_region = models.Region.objects.get(value=i.regdis2.id)
                    if i.regdis3:
                        itinerary.third_landing_region = models.Region.objects.get(value=i.regdis3.id)
                    if i.portret:
                        itinerary.place_voyage_ended = models.Place.objects.get(value=i.portret.id)
                    if i.retrnreg:
                        itinerary.region_of_return = models.Region.objects.get(value=i.retrnreg.id)
                    if i.retrnreg1:
                        itinerary.broad_region_of_return = models.BroadRegion.objects.get(value=i.retrnreg1)
                    # Imputed itinerary variables
                    if i.ptdepimp:
                        itinerary.imp_port_voyage_begin = models.Place.objects.get(value=i.ptdepimp)
                    if i.deptregimp:
                        itinerary.imp_region_voyage_begin = models.Region.objects.get(value=i.deptregimp)
                    if i.deptregimp1:
                        itinerary.imp_broad_region_voyage_begin = models.BroadRegion.objects.get(value=i.deptregimp1)
                    if i.majbuypt:
                        itinerary.principal_place_of_slave_purchase = models.Place.objects.get(value=i.majbuypt)
                    if i.mjbyptimp:
                        itinerary.imp_principal_place_of_slave_purchase = models.Place.objects.get(value=i.mjbyptimp.id)
                    if i.majbyimp:
                        itinerary.imp_principal_region_of_slave_purchase = models.Region.objects.get(value=i.majbyimp.id)
                    if i.majbyimp1:
                        itinerary.imp_broad_region_of_slave_purchase = models.BroadRegion.objects.get(value=i.majbyimp1)
                    if i.majselpt:
                        itinerary.principal_port_of_slave_dis = models.Place.objects.get(value=i.majselpt)
                    if i.mjslptimp:
                        itinerary.imp_principal_port_slave_dis = models.Place.objects.get(value=i.mjslptimp)
                    if i.mjselimp:
                        itinerary.imp_principal_region_slave_dis = models.Region.objects.get(value=i.mjselimp.id)
                    if i.mjselimp1:
                        itinerary.imp_broad_region_slave_dis = models.BroadRegion.objects.get(value=i.mjselimp1)
                    #itinerary.save()
                    #voyageObj.voyage_itinerary = itinerary
                    #voyageObj.save()

                    def mk_date(day_value, month_value, year_value):
                        """
                        :param day_value:
                        :param month_value:
                        :param year_value:
                        :return "mm,dd, yyyy":
                        """
                        tmpStr = ""
                        if month_value:
                            tmpStr += str(month_value)
                        tmpStr += ","
                        if day_value:
                            tmpStr += str(day_value)
                        tmpStr += ","
                        if year_value:
                            tmpStr += str(year_value)
                        if tmpStr == ',,':
                            return None
                        return tmpStr
                    # Voyage dates
                    date_info = models.VoyageDates()
                    #date_info.voyage = voyageObj
                    date_info.voyage_began = mk_date(i.datedepa, i.datedepb, i.datedepc)
                    date_info.slave_purchase_began = mk_date(i.d1slatra, i.d1slatrb, i.d1slatrc)
                    date_info.vessel_left_port = mk_date(i.dlslatra, i.dlslatrb, i.dlslatrc)
                    date_info.first_dis_of_slaves = mk_date(i.datarr32, i.datarr33, i.datarr34)
                    date_info.arrival_at_second_place_landing = mk_date(i.datarr36, i.datarr37, i.datarr38)
                    date_info.departure_last_place_of_landing = mk_date(i.ddepam, i.ddepamb, i.ddepamc)
                    date_info.voyage_completed = mk_date(i.datarr43, i.datarr44, i.datarr45)
                    if i.yeardep:
                        date_info.imp_voyage_began = ",," + str(i.yeardep)
                    if i.yearaf:
                        date_info.imp_departed_africa = ",," + str(i.yearaf)
                    if i.yearam:
                        date_info.imp_arrival_at_port_of_dis = ",," + str(i.yearam)
                    date_info.imp_length_home_to_disembark = i.voy1imp
                    date_info.imp_length_leaving_africa_to_disembark = i.voy2imp
                    # dateleftafr is made of:
                    # day: dlslatra
                    # month: dlslatrb
                    # year: dlslatrc
                    # Maybe the dlslatr. variables should be used always instead of the dateleftafr
                    if i.dateleftafr:
                        tmp = i.dateleftafr
                        # MM,DD,YYYY
                        date_info.date_departed_africa = mk_date(tmp.day, tmp.month, tmp.year)
                    elif i.dlslatrc:
                        date_info.date_departed_africa = mk_date(i.dlslatra, i.dlslatrb, i.dlslatrc)
                    #date_info.save()
                    #voyageObj.voyage_dates = date_info
                    #voyageObj.save()

                    # Captain and Crew section
                    crew = models.VoyageCrew()
                    #crew.voyage = voyageObj
                    crew.crew_voyage_outset = i.crew1
                    crew.crew_departure_last_port = i.crew2
                    crew.crew_first_landing = i.crew3
                    crew.crew_return_begin = i.crew4
                    crew.crew_end_voyage = i.crew5
                    crew.unspecified_crew = i.crew
                    crew.crew_died_before_first_trade = i.saild1
                    crew.crew_died_while_ship_african = i.saild2
                    crew.crew_died_middle_passage = i.saild3
                    crew.crew_died_in_americas = i.saild4
                    crew.crew_died_on_return_voyage = i.saild5
                    crew.crew_died_complete_voyage = i.crewdied
                    crew.crew_deserted = i.ndesert
                    if i.captaina:
                        #TODO change to get_or_create
                        first_captain = models.VoyageCaptain.objects.create(name=i.captaina)
                        models.VoyageCaptainConnection.objects.create(captain_order=1, captain=first_captain, voyage=voyageObj)
                    if i.captainb:
                        #TODO change to get_or_create
                        second_captain  = models.VoyageCaptain.objects.create(name=i.captainb)
                        models.VoyageCaptainConnection.objects.create(captain_order=2, captain=second_captain, voyage=voyageObj)
                    if i.captainc:
                        #TODO change to get_or_create
                        third_captain = models.VoyageCaptain.objects.create(name=i.captainc)
                        models.VoyageCaptainConnection.objects.create(captain_order=3, captain=third_captain, voyage=voyageObj)
                    #crew.save()
                    #voyageObj.voyage_crew = crew
                    #voyageObj.save()

                    # Voyage numbers and characteristics
                    characteristics = models.VoyageSlavesNumbers()
                    #characteristics.voyage = voyageObj
                    characteristics.num_slaves_intended_first_port = i.slintend
                    characteristics.num_slaves_intended_second_port = i.slinten2
                    characteristics.num_slaves_carried_first_port = i.ncar13
                    characteristics.num_slaves_carried_second_port = i.ncar15
                    characteristics.num_slaves_carried_third_port = i.ncar17
                    characteristics.total_num_slaves_purchased = i.tslavesp
                    characteristics.total_num_slaves_dep_last_slaving_port = i.tslavesd
                    characteristics.total_num_slaves_arr_first_port_embark = i.slaarriv
                    characteristics.num_slaves_disembark_first_place = i.slas32
                    characteristics.num_slaves_disembark_second_place = i.slas36
                    characteristics.num_slaves_disembark_third_place = i.slas39
                    #Imputed variables
                    characteristics.imp_total_num_slaves_embarked = i.slaximp
                    characteristics.imp_total_num_slaves_disembarked = i.slamimp
                    if i.jamcaspr:
                        characteristics.imp_jamaican_cash_price = str(i.jamcaspr)
                    characteristics.imp_mortality_during_voyage = i.vymrtimp

                    characteristics.num_men_embark_first_port_purchase = i.men1
                    characteristics.num_women_embark_first_port_purchase = i.women1
                    characteristics.num_boy_embark_first_port_purchase = i.boy1
                    characteristics.num_girl_embark_first_port_purchase = i.girl1
                    characteristics.num_adult_embark_first_port_purchase = i.adult1
                    characteristics.num_child_embark_first_port_purchase = i.child1
                    characteristics.num_infant_embark_first_port_purchase = i.infant1
                    characteristics.num_males_embark_first_port_purchase = i.male1
                    characteristics.num_females_embark_first_port_purchase = i.female1

                    characteristics.num_men_died_middle_passage = i.men2
                    characteristics.num_women_died_middle_passage = i.women2
                    characteristics.num_boy_died_middle_passage = i.boy2
                    characteristics.num_girl_died_middle_passage = i.girl2
                    characteristics.num_adult_died_middle_passage = i.adult2
                    characteristics.num_child_died_middle_passage = i.child2
                    characteristics.num_infant_died_middle_passage = i.infant2
                    characteristics.num_males_died_middle_passage = i.male2
                    characteristics.num_females_died_middle_passage = i.female2

                    characteristics.num_men_disembark_first_landing = i.men3
                    characteristics.num_women_disembark_first_landing = i.women3
                    characteristics.num_boy_disembark_first_landing = i.boy3
                    characteristics.num_girl_disembark_first_landing = i.girl3
                    characteristics.num_adult_disembark_first_landing = i.adult3
                    characteristics.num_child_disembark_first_landing = i.child3
                    characteristics.num_infant_disembark_first_landing = i.infant3
                    characteristics.num_males_disembark_first_landing = i.male3
                    characteristics.num_females_disembark_first_landing = i.female3

                    characteristics.num_men_embark_second_port_purchase = i.men4
                    characteristics.num_women_embark_second_port_purchase = i.women4
                    characteristics.num_boy_embark_second_port_purchase = i.boy4
                    characteristics.num_girl_embark_second_port_purchase = i.girl4
                    characteristics.num_adult_embark_second_port_purchase = i.adult4
                    characteristics.num_child_embark_second_port_purchase = i.child4
                    characteristics.num_infant_embark_second_port_purchase = i.infant4
                    characteristics.num_males_embark_second_port_purchase = i.male4
                    characteristics.num_females_embark_second_port_purchase = i.female4

                    characteristics.num_men_embark_third_port_purchase = i.men5
                    characteristics.num_women_embark_third_port_purchase = i.women5
                    characteristics.num_boy_embark_third_port_purchase = i.boy5
                    characteristics.num_girl_embark_third_port_purchase = i.girl5
                    characteristics.num_adult_embark_third_port_purchase = i.adult5
                    characteristics.num_child_embark_third_port_purchase = i.child5
                    characteristics.num_infant_embark_third_port_purchase = i.infant5
                    characteristics.num_males_embark_third_port_purchase = i.male5
                    characteristics.num_females_embark_third_port_purchase = i.female5

                    characteristics.num_men_disembark_second_landing = i.men6
                    characteristics.num_women_embark_first_port_purchase = i.women6
                    characteristics.num_boy_embark_first_port_purchase = i.boy6
                    characteristics.num_girl_embark_first_port_purchase = i.girl6
                    characteristics.num_adult_embark_first_port_purchase = i.adult6
                    characteristics.num_child_embark_first_port_purchase = i.child6
                    characteristics.num_infant_embark_first_port_purchase = i.infant6
                    characteristics.num_males_embark_first_port_purchase = i.male6
                    characteristics.num_females_embark_first_port_purchase = i.female6

                    # imputed variables 7
                    characteristics.imp_num_men_total = i.men7
                    characteristics.imp_num_women_total = i.women7
                    characteristics.imp_num_boy_total = i.boy7
                    characteristics.imp_num_girl_total = i.girl7
                    characteristics.imp_num_adult_total = i.adult7
                    characteristics.imp_num_child_total = i.child7
                    characteristics.imp_num_males_total = i.male7
                    characteristics.imp_num_females_total = i.female7

                    characteristics.imp_total_num_slaves_embarked = i.slaximp
                    characteristics.imp_num_adult_embarked = i.adlt1imp
                    characteristics.imp_num_children_embarked = i.chil1imp
                    characteristics.imp_num_male_embarked = i.male1imp
                    characteristics.imp_num_female_embarked = i.feml1imp
                    characteristics.total_slaves_embarked_age_identified = i.slavema1
                    characteristics.total_slaves_embarked_gender_identified = i.slavemx1

                    characteristics.imp_adult_death_middle_passage = i.adlt2imp
                    characteristics.imp_child_death_middle_passage = i.chil2imp
                    characteristics.imp_male_death_middle_passage = i.male2imp
                    characteristics.imp_female_death_middle_passage = i.feml2imp
                    characteristics.imp_num_adult_landed = i.adlt3imp
                    characteristics.imp_num_child_landed = i.chil3imp
                    characteristics.imp_num_male_landed = i.male3imp
                    characteristics.imp_num_female_landed = i.feml3imp
                    characteristics.total_slaves_landed_age_identified = i.slavema3
                    characteristics.total_slaves_landed_gender_identified = i.slavemx3
                    characteristics.total_slaves_dept_or_arr_age_identified = i.slavema7
                    characteristics.total_slaves_dept_or_arr_gender_identified = i.slavemx7
                    characteristics.imp_slaves_embarked_for_mortality = i.tslmtimp

                    characteristics.imp_mortality_ratio = i.vymrtrat

                    characteristics.percentage_men = i.menrat7
                    characteristics.percentage_women = i.womrat7
                    characteristics.percentage_boy = i.boyrat7
                    characteristics.percentage_girl = i.girlrat7
                    characteristics.percentage_male = i.malrat7
                    characteristics.percentage_child = i.chilrat7
                    if i.chilrat7:
                        characteristics.percentage_adult = 1 - i.chilrat7
                    if i.malrat7:
                        characteristics.percentage_female = 1 - i.malrat7

                    #characteristics.save()
                    #voyageObj.voyage_slaves_numbers = characteristics
                    #voyageObj.save()

                    voyageObj.save()
                    
                    ship.voyage = voyageObj
                    outcome.voyage = voyageObj
                    itinerary.voyage = voyageObj
                    date_info.voyage = voyageObj
                    crew.voyage = voyageObj
                    characteristics.voyage = voyageObj
                    
                    ship.save()
                    outcome.save()
                    itinerary.save()
                    date_info.save()
                    crew.save()
                    characteristics.save()

                    voyageObj.voyage_ship = ship
                    #voyageObj.voyage_outcome = outcome
                    voyageObj.voyage_itinerary = itinerary
                    voyageObj.voyage_dates = date_info
                    voyageObj.voyage_crew = crew
                    voyageObj.voyage_slaves_numbers = characteristics
                    
                    voyageObj.save()

                    def findBestMatchingSource(matchstring):
                        #Base case
                        if len(matchstring) <= 1:
                            return None
                        for source in listSources:
                            if not source.short_ref:
                                continue
                            if len(source.short_ref) < len(matchstring):
                                continue
                            sourcestr = source.short_ref
                            if sourcestr.find(matchstring) > -1:
                                return source
                        # Find the best matching/contains the substring
                        # : should be the last delimiter, then (except : is not always the last delimiter
                        posList = [ matchstring.rfind(':'), matchstring.rfind(","), matchstring.rfind("-") ]
                        posList.sort()
                        posList.reverse()
                        if posList[0] > -1:
                            if posList[0] < len(matchstring):
                                return findBestMatchingSource(matchstring[: posList[0]])
                            elif posList[1] > -1:
                                return findBestMatchingSource(matchstring[: posList[1]])
                        return None

                    def insertSource(fieldvalue, order):
                        if fieldvalue:
                            to_be_matched = fieldvalue
                            src = findBestMatchingSource(to_be_matched)
                            if src:
                                models.VoyageSourcesConnection.objects.create(source=src, source_order = order, text_ref=fieldvalue, group=voyageObj)
                            else:
                                models.VoyageSourcesConnection.objects.create(source_order=order, text_ref=fieldvalue, group=voyageObj)
                                pass
                    # Alphabetical letters between a and r
                    letters = map(chr, range(97, 97+18))
                    for idx, letter in enumerate(letters):
                        # Inserting sourcea, sourceb, ..., sourcer
                        insertSource(getattr(i, 'source' + letter), (idx + 1))
                    voyageObj.save()
        except Exception as ex:
            traceback.print_exc()
