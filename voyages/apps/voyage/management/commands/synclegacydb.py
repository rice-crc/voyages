from django.core.management.base import BaseCommand, CommandError
from voyages.apps.voyage.legacy_models import *
from voyages.apps.voyage import models
from decimal import *


class Command(BaseCommand):
    args = '<>'
    help = 'Syncs the data from the legacy wilson database to the database configured in this project'
    def handle(self, *args, **options):
        # BroadRegion
        #models.BroadRegion.objects.all().delete()
        for i in Areas.objects.all():
            b_region = models.BroadRegion()
            b_region.value = i.id
            b_region.show_on_map = i.show_on_map
            #b_region.save()

        # Region
        #models.Region.objects.all().delete()
        for i in Regions.objects.all():
            region = models.Region()
            region.region = i.name
            region.value = i.order_num
            region.show_on_map = i.show_on_map
            region.show_on_main_map = i.show_on_main_map
            broad_region = models.BroadRegion.objects.get(value=i.area_id)
            if broad_region:
                region.broad_region = broad_region
            #region.save()

        # Places Ports
        #models.Place.objects.all().delete()
        for i in Ports.objects.all():
            location = models.Place()
            location.place = i.name
            location.value = i.id
            location.longitude = Decimal(str(round(i.longitude, 5)))
            location.latitude = Decimal(str(round(i.latitude, 5)))
            reg = models.Region.objects.get(value=i.region.id)
            if reg:
                location.region = reg
            location.show_on_main_map = i.show_on_main_map
            location.show_on_voyage_map = i.show_on_voyage_map
            #location.save()

        # Fate
        #models.ParticularOutcome.objects.all().delete()
        for i in Fates.objects.all():
            fate = models.ParticularOutcome()
            fate.label = i.name
            fate.value = i.id
            #fate.save()

        # Owner Outcome
        #models.OwnerOutcome.objects.all().delete()
        for i in FatesOwner.objects.all():
            tmpObj = models.OwnerOutcome()
            tmpObj.label = i.name
            tmpObj.value = i.id
            #tmpObj.save()

        # Slave Outcome
        #models.SlavesOutcome.objects.all().delete()
        for i in FatesSlaves.objects.all():
            tmpObj = models.SlavesOutcome()
            tmpObj.label = i.name
            tmpObj.value = i.id
            #tmpObj.save()

        # Vessel Outcome
        #models.VesselCapturedOutcome.objects.all().delete()
        for i in FatesVessel.objects.all():
            tmpObj = models.VesselCapturedOutcome()
            tmpObj.label = i.name
            tmpObj.value = i.id
            #tmpObj.save()

        # Resistance
        #models.Resistance.objects.all().delete()
        for i in Resistance.objects.all():
            tmpObj = models.Resistance()
            tmpObj.label = i.name
            tmpObj.value = i.id
            #tmpObj.save()

        # Nations
        #models.Nationality.objects.all().delete()
        for i in Nations.objects.all():
            nation = models.Nationality()
            nation.value = i.order_num
            nation.label = i.name
            #nation.save()

        # Rig of Vessel
        #models.RigOfVessel.objects.all().delete()
        for i in VesselRigs.objects.all():
            rov_obj = models.RigOfVessel()
            rov_obj.value = i.id
            rov_obj.label = i.name
            #rov_obj.save()

        # Sources
        #models.VoyageSources.objects.all().delete()
        #models.VoyageSourcesType.objects.all().delete()
        obj0 = models.VoyageSourcesType()
        obj0.group_id = 0
        obj0.group_name = 'Documentary source'
        #obj0.save()
        obj1 = models.VoyageSourcesType()
        obj1.group_id = 1
        obj1.group_name = 'Newspaper'
        #obj1.save()
        obj2 = models.VoyageSourcesType()
        obj2.group_id = 2
        obj2.group_name = 'Published source'
        #obj2.save()
        obj3 = models.VoyageSourcesType()
        obj3.group_id = 3
        obj3.group_name = 'Unpublished secondary source'
        #obj3.save()
        obj4 = models.VoyageSourcesType()
        obj4.group_id = 4
        obj4.group_name = 'Private note or collection'
        #obj4.save()
        for i in Sources.objects.all():
            source = models.VoyageSources()
            source.short_ref = i.id
            source.full_ref = i.name
            stype = models.VoyageSourcesType.objects.get(group_id=i.type)
            if stype:
                source.source_type = stype
            #source.save()

        # Ton Type
        #models.TonType.objects.all().delete()
        for i in TonType.objects.all():
            ton_type = models.TonType()
            ton_type.value = i.id
            ton_type.label = i.name
            #ton_type.save()

        # Groupings
        #models.VoyageGroupings.objects.all().delete()
        for i in Xmimpflag.objects.all():
            group = models.VoyageGroupings()
            group.value = i.id
            group.label = i.name
            #group.save()
        
        # Voyages
        #models.Voyage.objects.all().delete()
        count = 0
        for i in Voyages.objects.all():
            #TODO: This if statement looks suspicious
            if i.suggestion or (i.revision != 1):
                continue
            voyageObj = models.Voyage()
            count += 1
            print "Voyage Number: " + str(count)
            if i.voyageid is not None:
                voyageObj.voyage_id = i.voyageid
                #voyageObj.save()
            ship = models.VoyageShip()
            ship.voyage = voyageObj
            voyageObj.voyage_in_cd_rom = i.evgreen
            grps = models.VoyageGroupings.objects.filter(value=i.xmimpflag)
            print "one"
            if len(grps) >= 1 and i.xmimpflag:
                voyageObj.voyage_groupings = grps[0]
            if i.shipname:
                ship.ship_name = i.shipname
            print "1.2"
            ntls = models.Nationality.objects.filter(value=i.national)
            print "1.5"
            if i.national and len(ntls) >= 1:
                ship.nationality_ship = ntls[0]
            print "1.7"
            ship.tonnage = i.tonnage
            tntps = models.TonType.objects.filter(value=i.tontype)
            print "two"
            if i.tontype and len(tntps) >= 1:
                ship.ton_type = tntps[0]
            rigs = models.RigOfVessel.objects.filter(value=i.rig)
            if i.rig and len(rigs) >= 1:
                ship.rig_of_vessel = rigs[0]
            ship.guns_mounted = i.guns
            ship.year_of_construction = i.yrcons
            print "three"
            plccns = models.Place.objects.filter(value=i.placcons)
            if i.placcons and len(plccns) >= 1:
                ship.vessel_construction_place = plccns[0]
            cnstrgs = models.Region.objects.filter(i.constreg)
            if i.constreg and len(cnstrgs) >= 1:
                ship.vessel_constructoin_region = cnstrgs[0]
            
