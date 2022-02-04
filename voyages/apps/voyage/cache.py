from __future__ import absolute_import, unicode_literals

import threading

from .models import (BroadRegion, Nationality, OwnerOutcome, ParticularOutcome,
                     Place, Region, Resistance, RigOfVessel, SlavesOutcome,
                     TonType, VesselCapturedOutcome, Voyage, VoyageDates)


class CachedGeo:
    """
    Caches a geographical place (could be a port, region, or broad region)
    """

    def __init__(self, pk, value, name, lat, lng, _, parent):
        self.pk = pk
        self.value = value
        self.name = name
        self.lat = lat
        self.lng = lng
        # Ignore show in favor of having proper coordinates.
        self.show = lat is not None and lng is not None and \
            (abs(lat) + abs(lng) > 0.1)
        self.parent = parent

    @classmethod
    def get_hierarchy(cls, pk):
        """
        Fetches a tuple (port, region, broad_region) given the primary key of a
        port.
        """
        port = VoyageCache.ports.get(pk)
        if port is None:
            return None
        region = VoyageCache.regions.get(port.parent)
        if region is None:
            return None
        broad_region = VoyageCache.broad_regions.get(region.parent)
        return port, region, broad_region


class CachedVoyage:
    """
    Cache the most basic information of a voyage for map generation and
    aggregation
    """

    def __init__(self, pk, voyage_id, emb_pk, dis_pk, ship_nat_pk, ship_name,
                 ship_ton, date_voyage_began, embarked, disembarked):
        self.pk = pk
        self.voyage_id = voyage_id
        self.emb_pk = emb_pk
        self.dis_pk = dis_pk
        self.ship_nat_pk = ship_nat_pk
        self.ship_name = ship_name
        self.ship_ton = ship_ton
        self.year = VoyageDates.get_date_year(date_voyage_began)
        self.month = VoyageDates.get_date_month(date_voyage_began)
        self.embarked = embarked
        self.disembarked = disembarked


class VoyageCache:
    """
    Caches all geo locations and all voyages in the db loading only the minimum
    amount of fields required.
    """
    voyages = {}
    ports = {}
    ports_by_value = {}
    regions = {}
    regions_by_value = {}
    broad_regions = {}
    broad_regions_by_value = {}
    nations = {}
    nations_by_value = {}
    particular_outcomes = {}
    slave_outcomes = {}
    owner_outcomes = {}
    captured_outcomes = {}
    resistances = {}
    rigs = {}
    ton_types = {}

    _loaded = False
    _lock = threading.Lock()

    @classmethod
    def load(cls, force_reload=False):
        with cls._lock:
            if not force_reload and cls._loaded:
                return
            cls._loaded = False
            cls.ports = {
                x[0]: CachedGeo(x[0], x[1], x[2], x[3], x[4], x[5], x[6])
                for x in Place.objects.values_list(
                    'pk', 'value', 'place', 'latitude', 'longitude',
                    'show_on_main_map', 'region_id').iterator()
            }
            cls.ports_by_value = {x.value: x for x in list(cls.ports.values())}
            cls.regions = {
                x[0]: CachedGeo(x[0], x[1], x[2], x[3], x[4], x[5], x[6])
                for x in Region.objects.values_list(
                    'pk', 'value', 'region', 'latitude', 'longitude',
                    'show_on_main_map', 'broad_region_id').iterator()
            }
            cls.regions_by_value = {
                x.value: x for x in list(cls.regions.values())
            }
            cls.broad_regions = {
                x[0]: CachedGeo(x[0], x[1], x[2], x[3], x[4], x[5], None)
                for x in BroadRegion.objects.values_list(
                    'pk', 'value', 'broad_region', 'latitude', 'longitude',
                    'show_on_map').iterator()
            }
            cls.broad_regions_by_value = {
                x.value: x for x in list(cls.broad_regions.values())
            }
            nations = list(
                Nationality.objects.values_list('pk', 'label', 'value'))
            cls.nations = {x[0]: x[1] for x in nations}
            cls.nations_by_value = {x[2]: x[1] for x in nations}
            cls.particular_outcomes = {
                o.pk: o for o in ParticularOutcome.objects.all()
            }
            cls.slave_outcomes = {o.pk: o for o in SlavesOutcome.objects.all()}
            cls.owner_outcomes = {o.pk: o for o in OwnerOutcome.objects.all()}
            cls.captured_outcomes = {
                o.pk: o for o in VesselCapturedOutcome.objects.all()
            }
            cls.resistances = {r.pk: r for r in Resistance.objects.all()}
            cls.rigs = {r.pk: r for r in RigOfVessel.objects.all()}
            cls.ton_types = {tt.pk: tt for tt in TonType.objects.all()}
            cls.voyages = {
                x[0]: CachedVoyage(x[0], x[1], x[2], x[3], x[4], x[5], x[6],
                                   x[7], x[8], x[9])
                for x in Voyage.all_dataset_objects.values_list(
                    'pk', 'voyage_id',
                    'voyage_itinerary_'
                    '_imp_principal_place_of_slave_purchase_id',
                    'voyage_itinerary__imp_principal_port_slave_dis_id',
                    'voyage_ship__imputed_nationality_id',
                    'voyage_ship__ship_name', 'voyage_ship__tonnage',
                    'voyage_dates__imp_arrival_at_port_of_dis',
                    'voyage_slaves_numbers__imp_total_num_slaves_embarked',
                    'voyage_slaves_numbers__imp_total_num_slaves_disembarked').
                iterator()
            }
            cls._loaded = True
