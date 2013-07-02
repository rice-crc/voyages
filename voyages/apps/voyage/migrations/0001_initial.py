# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BroadRegion'
        db.create_table(u'voyage_broadregion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('show_on_map', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'voyage', ['BroadRegion'])

        # Adding model 'Region'
        db.create_table(u'voyage_region', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('broad_region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.BroadRegion'])),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('how_on_map', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_on_main_map', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'voyage', ['Region'])

        # Adding model 'Place'
        db.create_table(u'voyage_place', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.Region'])),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=7, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=7, blank=True)),
            ('show_on_main_map', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_on_voyage_map', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'voyage', ['Place'])

        # Adding model 'VoyageGroupings'
        db.create_table(u'voyage_voyagegroupings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('grouping_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'voyage', ['VoyageGroupings'])

        # Adding model 'Nationality'
        db.create_table(u'voyage_nationality', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nationality', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
        ))
        db.send_create_signal(u'voyage', ['Nationality'])

        # Adding model 'TonType'
        db.create_table(u'voyage_tontype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ton_type', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
        ))
        db.send_create_signal(u'voyage', ['TonType'])

        # Adding model 'RigOfVessel'
        db.create_table(u'voyage_rigofvessel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rig_of_vessel', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
        ))
        db.send_create_signal(u'voyage', ['RigOfVessel'])

        # Adding model 'VoyageShip'
        db.create_table(u'voyage_voyageship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ship_name', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('nationality_ship', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='nationality_ship', null=True, to=orm['voyage.Nationality'])),
            ('tonnage', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('ton_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.TonType'], null=True, blank=True)),
            ('rig_of_vessel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.RigOfVessel'], null=True, blank=True)),
            ('guns_mounted', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('year_of_construction', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('vessel_construction_place', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='vessel_construction_place', null=True, to=orm['voyage.Place'])),
            ('vessel_construction_region', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='vessel_construction_region', null=True, to=orm['voyage.Region'])),
            ('registered_year', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('registered_place', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='registered_place', null=True, to=orm['voyage.Place'])),
            ('registered_region', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='registered_region', null=True, to=orm['voyage.Region'])),
            ('imputed_nationality', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='imputed_nationality', null=True, to=orm['voyage.Nationality'])),
            ('tonnage_mod', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('voyage', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='voyage_name_ship', null=True, to=orm['voyage.Voyage'])),
        ))
        db.send_create_signal(u'voyage', ['VoyageShip'])

        # Adding model 'VoyageShipOwner'
        db.create_table(u'voyage_voyageshipowner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal(u'voyage', ['VoyageShipOwner'])

        # Adding model 'VoyageShipOwnerConnection'
        db.create_table(u'voyage_voyageshipownerconnection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owner_name', to=orm['voyage.VoyageShipOwner'])),
            ('voyage', self.gf('django.db.models.fields.related.ForeignKey')(related_name='voyage_related', to=orm['voyage.Voyage'])),
            ('owner_order', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
        ))
        db.send_create_signal(u'voyage', ['VoyageShipOwnerConnection'])

        # Adding model 'ParticularOutcome'
        db.create_table(u'voyage_particularoutcome', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
        ))
        db.send_create_signal(u'voyage', ['ParticularOutcome'])

        # Adding model 'SlavesOutcome'
        db.create_table(u'voyage_slavesoutcome', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
        ))
        db.send_create_signal(u'voyage', ['SlavesOutcome'])

        # Adding model 'VesselCapturedOutcome'
        db.create_table(u'voyage_vesselcapturedoutcome', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
        ))
        db.send_create_signal(u'voyage', ['VesselCapturedOutcome'])

        # Adding model 'OwnerOutcome'
        db.create_table(u'voyage_owneroutcome', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
        ))
        db.send_create_signal(u'voyage', ['OwnerOutcome'])

        # Adding model 'Resistance'
        db.create_table(u'voyage_resistance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
        ))
        db.send_create_signal(u'voyage', ['Resistance'])

        # Adding model 'VoyageOutcome'
        db.create_table(u'voyage_voyageoutcome', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('particular_outcome', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.ParticularOutcome'], null=True, blank=True)),
            ('resistance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.Resistance'], null=True, blank=True)),
            ('outcome_slaves', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.SlavesOutcome'], null=True, blank=True)),
            ('vessel_captured_outcome', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.VesselCapturedOutcome'], null=True, blank=True)),
            ('outcome_owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.OwnerOutcome'], null=True, blank=True)),
            ('voyage', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='voyage_name_outcome', null=True, to=orm['voyage.Voyage'])),
        ))
        db.send_create_signal(u'voyage', ['VoyageOutcome'])

        # Adding model 'VoyageItinerary'
        db.create_table(u'voyage_voyageitinerary', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('port_of_departure', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='port_of_departure', null=True, to=orm['voyage.Place'])),
            ('int_first_port_emb', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='int_first_port_emb', null=True, to=orm['voyage.Place'])),
            ('int_second_port_emb', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='int_second_port_emb', null=True, to=orm['voyage.Place'])),
            ('int_first_region_purchase_slaves', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='int_first_region_purchase_slaves', null=True, to=orm['voyage.Region'])),
            ('int_second_region_purchase_slaves', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='int_second_region_purchase_slaves', null=True, to=orm['voyage.Region'])),
            ('int_first_port_dis', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='int_first_port_dis', null=True, to=orm['voyage.Place'])),
            ('int_second_port_dis', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='int_second_port_dis', null=True, to=orm['voyage.Place'])),
            ('int_first_region_slave_landing', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='int_first_region_slave_landing', null=True, to=orm['voyage.Region'])),
            ('int_second_region_slave_landing', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='int_second_region_slave_landing', null=True, to=orm['voyage.Region'])),
            ('ports_called_buying_slaves', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('first_place_slave_purchase', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='first_place_slave_purchase', null=True, to=orm['voyage.Place'])),
            ('second_place_slave_purchase', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='second_place_slave_purchase', null=True, to=orm['voyage.Place'])),
            ('third_place_slave_purchase', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='third_place_slave_purchase', null=True, to=orm['voyage.Place'])),
            ('first_region_slave_emb', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='first_region_slave_emb', null=True, to=orm['voyage.Region'])),
            ('second_region_slave_emb', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='second_region_slave_emb', null=True, to=orm['voyage.Region'])),
            ('third_region_slave_emb', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='third_region_slave_emb', null=True, to=orm['voyage.Region'])),
            ('port_of_call_before_atl_crossing', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='port_of_call_before_atl_crossing', null=True, to=orm['voyage.Place'])),
            ('number_of_ports_of_call', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='number_of_ports_of_call', null=True, to=orm['voyage.Place'])),
            ('first_landing_place', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='first_landing_place', null=True, to=orm['voyage.Place'])),
            ('second_landing_place', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='second_landing_place', null=True, to=orm['voyage.Place'])),
            ('third_landing_place', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='third_landing_place', null=True, to=orm['voyage.Place'])),
            ('first_landing_region', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='first_landing_region', null=True, to=orm['voyage.Region'])),
            ('second_landing_region', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='second_landing_region', null=True, to=orm['voyage.Region'])),
            ('third_landing_region', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='third_landing_region', null=True, to=orm['voyage.Region'])),
            ('place_voyage_ended', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='place_voyage_ended', null=True, to=orm['voyage.Place'])),
            ('region_of_return', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='region_of_return', null=True, to=orm['voyage.Region'])),
            ('broad_region_of_return', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='broad_region_of_return', null=True, to=orm['voyage.Region'])),
            ('imp_port_voyage_begin', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='imp_port_voyage_begin', null=True, to=orm['voyage.Place'])),
            ('imp_region_voyage_begin', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='imp_region_voyage_begin', null=True, to=orm['voyage.Region'])),
            ('imp_broad_region_voyage_begin', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='imp_broad_region_voyage_begin', null=True, to=orm['voyage.BroadRegion'])),
            ('principal_place_of_slave_purchase', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='principal_place_of_slave_purchase', null=True, to=orm['voyage.Place'])),
            ('imp_principal_place_of_slave_purchase', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='imp_principal_place_of_slave_purchase', null=True, to=orm['voyage.Place'])),
            ('imp_principal_region_of_slave_purchase', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='imp_principal_region_of_slave_purchase', null=True, to=orm['voyage.Region'])),
            ('imp_broad_region_of_slave_purchase', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='imp_broad_region_of_slave_purchase', null=True, to=orm['voyage.BroadRegion'])),
            ('principal_port_of_slave_dis', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='principal_port_of_slave_dis', null=True, to=orm['voyage.Place'])),
            ('imp_principal_port_slave_dis', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='imp_principal_port_slave_dis', null=True, to=orm['voyage.Place'])),
            ('imp_principal_region_slave_dis', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='imp_principal_region_slave_dis', null=True, to=orm['voyage.Region'])),
            ('imp_broad_region_slave_dis', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='imp_broad_region_slave_dis', null=True, to=orm['voyage.BroadRegion'])),
            ('voyage', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='voyage_name_itinerary', null=True, to=orm['voyage.Voyage'])),
        ))
        db.send_create_signal(u'voyage', ['VoyageItinerary'])

        # Adding model 'IntegerDate'
        db.create_table(u'voyage_integerdate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'voyage', ['IntegerDate'])

        # Adding model 'VoyageDates'
        db.create_table(u'voyage_voyagedates', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voyage_began', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10, null=True, blank=True)),
            ('slave_purchase_began', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10, null=True, blank=True)),
            ('vessel_left_port', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10, null=True, blank=True)),
            ('first_dis_of_slaves', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10, null=True, blank=True)),
            ('arrival_at_second_place_landing', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10, null=True, blank=True)),
            ('third_dis_of_slaves', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10, null=True, blank=True)),
            ('departure_last_place_of_landing', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10, null=True, blank=True)),
            ('voyage_completed', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10, null=True, blank=True)),
            ('imp_voyage_began', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10, null=True, blank=True)),
            ('imp_departed_africa', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=4, null=True, blank=True)),
            ('imp_arrival_at_port_of_dis', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=4, null=True, blank=True)),
            ('voyage', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='voyage_name_dates', null=True, to=orm['voyage.Voyage'])),
        ))
        db.send_create_signal(u'voyage', ['VoyageDates'])

        # Adding model 'VoyageCaptain'
        db.create_table(u'voyage_voyagecaptain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal(u'voyage', ['VoyageCaptain'])

        # Adding model 'VoyageCaptainConnection'
        db.create_table(u'voyage_voyagecaptainconnection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('captain', self.gf('django.db.models.fields.related.ForeignKey')(related_name='captain_name', to=orm['voyage.VoyageCaptain'])),
            ('voyage', self.gf('django.db.models.fields.related.ForeignKey')(related_name='voyage', to=orm['voyage.Voyage'])),
            ('captain_order', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
        ))
        db.send_create_signal(u'voyage', ['VoyageCaptainConnection'])

        # Adding model 'VoyageCrew'
        db.create_table(u'voyage_voyagecrew', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('crew_voyage_outset', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('crew_departure_last_port', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('crew_first_landing', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('crew_return_begin', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('crew_end_voyage', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('unspecified_crew', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('crew_died_before_first_trade', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('crew_died_while_ship_african', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('crew_died_middle_passge', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('crew_died_in_americas', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('crew_died_on_return_voyage', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('crew_died_complete_voyage', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('crew_deserted', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('voyage', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='voyage_name_crew', null=True, to=orm['voyage.Voyage'])),
        ))
        db.send_create_signal(u'voyage', ['VoyageCrew'])

        # Adding model 'VoyageSlavesNumbers'
        db.create_table(u'voyage_voyageslavesnumbers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slave_deaths_before_africa', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('slave_deaths_between_africa_america', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_slaves_intended_first_port', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('num_slaves_intended_second_port', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('num_slaves_carried_first_port', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('num_slaves_carried_second_port', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('num_slaves_carried_third_port', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('total_num_slaves_purchased', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('total_num_slaves_dep_last_slaving_port', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('total_num_slaves_arr_first_port_embark', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('num_slaves_disembark_first_place', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_slaves_disembark_second_place', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_slaves_disembark_third_place', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_men_embark_first_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_women_embark_first_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_boy_embark_first_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_girl_embark_first_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_adult_embark_first_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_child_embark_first_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_infant_embark_first_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_males_embark_first_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_females_embark_first_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_men_died_middle_passage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_women_died_middle_passage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_boy_died_middle_passage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_girl_died_middle_passage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_adult_died_middle_passage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_child_died_middle_passage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_infant_died_middle_passage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_males_died_middle_passage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_females_died_middle_passage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_men_disembark_first_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_women_disembark_first_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_boy_disembark_first_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_girl_disembark_first_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_adult_disembark_first_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_child_disembark_first_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_infant_disembark_first_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_males_disembark_first_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_females_disembark_first_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_men_embark_second_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_women_embark_second_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_boy_embark_second_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_girl_embark_second_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_adult_embark_second_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_child_embark_second_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_infant_embark_second_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_males_embark_second_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_females_embark_second_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_men_embark_third_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_women_embark_third_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_boy_embark_third_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_girl_embark_third_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_adult_embark_third_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_child_embark_third_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_infant_embark_third_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_males_embark_third_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_females_embark_third_port_purchase', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_men_disembark_second_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_women_disembark_second_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_boy_disembark_second_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_girl_disembark_second_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_adult_disembark_second_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_child_disembark_second_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_infant_disembark_second_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_males_disembark_second_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_females_disembark_second_landing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('voyage', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='voyage_name_slave_characteristics', null=True, to=orm['voyage.Voyage'])),
        ))
        db.send_create_signal(u'voyage', ['VoyageSlavesNumbers'])

        # Adding model 'VoyageSources'
        db.create_table(u'voyage_voyagesources', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_ref', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('full_ref', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
        ))
        db.send_create_signal(u'voyage', ['VoyageSources'])

        # Adding model 'VoyageSourcesConnection'
        db.create_table(u'voyage_voyagesourcesconnection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='source', to=orm['voyage.VoyageSources'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='group', to=orm['voyage.Voyage'])),
            ('source_order', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('text_ref', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'voyage', ['VoyageSourcesConnection'])

        # Adding model 'Voyage'
        db.create_table(u'voyage_voyage', (
            ('voyage_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voyage_in_cd_rom', self.gf('django.db.models.fields.BooleanField')(default=False, max_length=1)),
            ('voyage_groupings', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.VoyageGroupings'])),
        ))
        db.send_create_signal(u'voyage', ['Voyage'])


    def backwards(self, orm):
        # Deleting model 'BroadRegion'
        db.delete_table(u'voyage_broadregion')

        # Deleting model 'Region'
        db.delete_table(u'voyage_region')

        # Deleting model 'Place'
        db.delete_table(u'voyage_place')

        # Deleting model 'VoyageGroupings'
        db.delete_table(u'voyage_voyagegroupings')

        # Deleting model 'Nationality'
        db.delete_table(u'voyage_nationality')

        # Deleting model 'TonType'
        db.delete_table(u'voyage_tontype')

        # Deleting model 'RigOfVessel'
        db.delete_table(u'voyage_rigofvessel')

        # Deleting model 'VoyageShip'
        db.delete_table(u'voyage_voyageship')

        # Deleting model 'VoyageShipOwner'
        db.delete_table(u'voyage_voyageshipowner')

        # Deleting model 'VoyageShipOwnerConnection'
        db.delete_table(u'voyage_voyageshipownerconnection')

        # Deleting model 'ParticularOutcome'
        db.delete_table(u'voyage_particularoutcome')

        # Deleting model 'SlavesOutcome'
        db.delete_table(u'voyage_slavesoutcome')

        # Deleting model 'VesselCapturedOutcome'
        db.delete_table(u'voyage_vesselcapturedoutcome')

        # Deleting model 'OwnerOutcome'
        db.delete_table(u'voyage_owneroutcome')

        # Deleting model 'Resistance'
        db.delete_table(u'voyage_resistance')

        # Deleting model 'VoyageOutcome'
        db.delete_table(u'voyage_voyageoutcome')

        # Deleting model 'VoyageItinerary'
        db.delete_table(u'voyage_voyageitinerary')

        # Deleting model 'IntegerDate'
        db.delete_table(u'voyage_integerdate')

        # Deleting model 'VoyageDates'
        db.delete_table(u'voyage_voyagedates')

        # Deleting model 'VoyageCaptain'
        db.delete_table(u'voyage_voyagecaptain')

        # Deleting model 'VoyageCaptainConnection'
        db.delete_table(u'voyage_voyagecaptainconnection')

        # Deleting model 'VoyageCrew'
        db.delete_table(u'voyage_voyagecrew')

        # Deleting model 'VoyageSlavesNumbers'
        db.delete_table(u'voyage_voyageslavesnumbers')

        # Deleting model 'VoyageSources'
        db.delete_table(u'voyage_voyagesources')

        # Deleting model 'VoyageSourcesConnection'
        db.delete_table(u'voyage_voyagesourcesconnection')

        # Deleting model 'Voyage'
        db.delete_table(u'voyage_voyage')


    models = {
        u'voyage.broadregion': {
            'Meta': {'object_name': 'BroadRegion'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'show_on_map': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'voyage.integerdate': {
            'Meta': {'object_name': 'IntegerDate'},
            'day': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'voyage.nationality': {
            'Meta': {'object_name': 'Nationality'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        u'voyage.owneroutcome': {
            'Meta': {'object_name': 'OwnerOutcome'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        u'voyage.particularoutcome': {
            'Meta': {'object_name': 'ParticularOutcome'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        u'voyage.place': {
            'Meta': {'object_name': 'Place'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '7', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '7', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.Region']"}),
            'show_on_main_map': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_on_voyage_map': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'voyage.region': {
            'Meta': {'object_name': 'Region'},
            'broad_region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.BroadRegion']"}),
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'how_on_map': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'show_on_main_map': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'voyage.resistance': {
            'Meta': {'object_name': 'Resistance'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '35'})
        },
        u'voyage.rigofvessel': {
            'Meta': {'object_name': 'RigOfVessel'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rig_of_vessel': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'voyage.slavesoutcome': {
            'Meta': {'object_name': 'SlavesOutcome'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        u'voyage.tontype': {
            'Meta': {'object_name': 'TonType'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ton_type': ('django.db.models.fields.CharField', [], {'max_length': '35'})
        },
        u'voyage.vesselcapturedoutcome': {
            'Meta': {'object_name': 'VesselCapturedOutcome'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        u'voyage.voyage': {
            'Meta': {'object_name': 'Voyage'},
            'voyage_captain': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['voyage.VoyageCaptain']", 'null': 'True', 'through': u"orm['voyage.VoyageCaptainConnection']", 'blank': 'True'}),
            'voyage_groupings': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.VoyageGroupings']"}),
            'voyage_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'voyage_in_cd_rom': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'max_length': '1'}),
            'voyage_ship_owner': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['voyage.VoyageShipOwner']", 'null': 'True', 'through': u"orm['voyage.VoyageShipOwnerConnection']", 'blank': 'True'}),
            'voyage_sources': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'voyage_sources'", 'to': u"orm['voyage.VoyageSources']", 'through': u"orm['voyage.VoyageSourcesConnection']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'})
        },
        u'voyage.voyagecaptain': {
            'Meta': {'object_name': 'VoyageCaptain'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'voyage.voyagecaptainconnection': {
            'Meta': {'object_name': 'VoyageCaptainConnection'},
            'captain': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'captain_name'", 'to': u"orm['voyage.VoyageCaptain']"}),
            'captain_order': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'voyage': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'voyage'", 'to': u"orm['voyage.Voyage']"})
        },
        u'voyage.voyagecrew': {
            'Meta': {'object_name': 'VoyageCrew'},
            'crew_departure_last_port': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'crew_deserted': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'crew_died_before_first_trade': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'crew_died_complete_voyage': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'crew_died_in_americas': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'crew_died_middle_passge': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'crew_died_on_return_voyage': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'crew_died_while_ship_african': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'crew_end_voyage': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'crew_first_landing': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'crew_return_begin': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'crew_voyage_outset': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unspecified_crew': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'voyage': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'voyage_name_crew'", 'null': 'True', 'to': u"orm['voyage.Voyage']"})
        },
        u'voyage.voyagedates': {
            'Meta': {'object_name': 'VoyageDates'},
            'arrival_at_second_place_landing': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'departure_last_place_of_landing': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'first_dis_of_slaves': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imp_arrival_at_port_of_dis': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'imp_departed_africa': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'imp_voyage_began': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'slave_purchase_began': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'third_dis_of_slaves': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'vessel_left_port': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'voyage': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'voyage_name_dates'", 'null': 'True', 'to': u"orm['voyage.Voyage']"}),
            'voyage_began': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'voyage_completed': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'voyage.voyagegroupings': {
            'Meta': {'object_name': 'VoyageGroupings'},
            'grouping_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'voyage.voyageitinerary': {
            'Meta': {'object_name': 'VoyageItinerary'},
            'broad_region_of_return': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'broad_region_of_return'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'first_landing_place': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'first_landing_place'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'first_landing_region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'first_landing_region'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'first_place_slave_purchase': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'first_place_slave_purchase'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'first_region_slave_emb': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'first_region_slave_emb'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imp_broad_region_of_slave_purchase': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imp_broad_region_of_slave_purchase'", 'null': 'True', 'to': u"orm['voyage.BroadRegion']"}),
            'imp_broad_region_slave_dis': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imp_broad_region_slave_dis'", 'null': 'True', 'to': u"orm['voyage.BroadRegion']"}),
            'imp_broad_region_voyage_begin': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imp_broad_region_voyage_begin'", 'null': 'True', 'to': u"orm['voyage.BroadRegion']"}),
            'imp_port_voyage_begin': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imp_port_voyage_begin'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'imp_principal_place_of_slave_purchase': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imp_principal_place_of_slave_purchase'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'imp_principal_port_slave_dis': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imp_principal_port_slave_dis'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'imp_principal_region_of_slave_purchase': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imp_principal_region_of_slave_purchase'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'imp_principal_region_slave_dis': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imp_principal_region_slave_dis'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'imp_region_voyage_begin': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imp_region_voyage_begin'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'int_first_port_dis': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'int_first_port_dis'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'int_first_port_emb': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'int_first_port_emb'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'int_first_region_purchase_slaves': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'int_first_region_purchase_slaves'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'int_first_region_slave_landing': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'int_first_region_slave_landing'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'int_second_port_dis': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'int_second_port_dis'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'int_second_port_emb': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'int_second_port_emb'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'int_second_region_purchase_slaves': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'int_second_region_purchase_slaves'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'int_second_region_slave_landing': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'int_second_region_slave_landing'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'number_of_ports_of_call': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'number_of_ports_of_call'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'place_voyage_ended': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'place_voyage_ended'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'port_of_call_before_atl_crossing': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'port_of_call_before_atl_crossing'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'port_of_departure': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'port_of_departure'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'ports_called_buying_slaves': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'principal_place_of_slave_purchase': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'principal_place_of_slave_purchase'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'principal_port_of_slave_dis': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'principal_port_of_slave_dis'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'region_of_return': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'region_of_return'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'second_landing_place': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_landing_place'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'second_landing_region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_landing_region'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'second_place_slave_purchase': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_place_slave_purchase'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'second_region_slave_emb': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_region_slave_emb'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'third_landing_place': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'third_landing_place'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'third_landing_region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'third_landing_region'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'third_place_slave_purchase': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'third_place_slave_purchase'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'third_region_slave_emb': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'third_region_slave_emb'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'voyage': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'voyage_name_itinerary'", 'null': 'True', 'to': u"orm['voyage.Voyage']"})
        },
        u'voyage.voyageoutcome': {
            'Meta': {'object_name': 'VoyageOutcome'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outcome_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.OwnerOutcome']", 'null': 'True', 'blank': 'True'}),
            'outcome_slaves': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.SlavesOutcome']", 'null': 'True', 'blank': 'True'}),
            'particular_outcome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.ParticularOutcome']", 'null': 'True', 'blank': 'True'}),
            'resistance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.Resistance']", 'null': 'True', 'blank': 'True'}),
            'vessel_captured_outcome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.VesselCapturedOutcome']", 'null': 'True', 'blank': 'True'}),
            'voyage': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'voyage_name_outcome'", 'null': 'True', 'to': u"orm['voyage.Voyage']"})
        },
        u'voyage.voyageship': {
            'Meta': {'object_name': 'VoyageShip'},
            'guns_mounted': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imputed_nationality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imputed_nationality'", 'null': 'True', 'to': u"orm['voyage.Nationality']"}),
            'nationality_ship': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'nationality_ship'", 'null': 'True', 'to': u"orm['voyage.Nationality']"}),
            'registered_place': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'registered_place'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'registered_region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'registered_region'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'registered_year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'rig_of_vessel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.RigOfVessel']", 'null': 'True', 'blank': 'True'}),
            'ship_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'ton_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.TonType']", 'null': 'True', 'blank': 'True'}),
            'tonnage': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'tonnage_mod': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'vessel_construction_place': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vessel_construction_place'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'vessel_construction_region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vessel_construction_region'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'voyage': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'voyage_name_ship'", 'null': 'True', 'to': u"orm['voyage.Voyage']"}),
            'year_of_construction': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        u'voyage.voyageshipowner': {
            'Meta': {'object_name': 'VoyageShipOwner'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'voyage.voyageshipownerconnection': {
            'Meta': {'object_name': 'VoyageShipOwnerConnection'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner_name'", 'to': u"orm['voyage.VoyageShipOwner']"}),
            'owner_order': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'voyage': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'voyage_related'", 'to': u"orm['voyage.Voyage']"})
        },
        u'voyage.voyageslavesnumbers': {
            'Meta': {'object_name': 'VoyageSlavesNumbers'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_adult_died_middle_passage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_adult_disembark_first_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_adult_disembark_second_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_adult_embark_first_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_adult_embark_second_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_adult_embark_third_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_boy_died_middle_passage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_boy_disembark_first_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_boy_disembark_second_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_boy_embark_first_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_boy_embark_second_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_boy_embark_third_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_child_died_middle_passage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_child_disembark_first_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_child_disembark_second_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_child_embark_first_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_child_embark_second_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_child_embark_third_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_females_died_middle_passage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_females_disembark_first_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_females_disembark_second_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_females_embark_first_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_females_embark_second_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_females_embark_third_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_girl_died_middle_passage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_girl_disembark_first_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_girl_disembark_second_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_girl_embark_first_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_girl_embark_second_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_girl_embark_third_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_infant_died_middle_passage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_infant_disembark_first_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_infant_disembark_second_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_infant_embark_first_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_infant_embark_second_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_infant_embark_third_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_males_died_middle_passage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_males_disembark_first_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_males_disembark_second_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_males_embark_first_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_males_embark_second_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_males_embark_third_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_men_died_middle_passage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_men_disembark_first_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_men_disembark_second_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_men_embark_first_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_men_embark_second_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_men_embark_third_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_slaves_carried_first_port': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'num_slaves_carried_second_port': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'num_slaves_carried_third_port': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'num_slaves_disembark_first_place': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_slaves_disembark_second_place': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_slaves_disembark_third_place': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_slaves_intended_first_port': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'num_slaves_intended_second_port': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'num_women_died_middle_passage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_women_disembark_first_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_women_disembark_second_landing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_women_embark_first_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_women_embark_second_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_women_embark_third_port_purchase': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slave_deaths_before_africa': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slave_deaths_between_africa_america': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_num_slaves_arr_first_port_embark': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'total_num_slaves_dep_last_slaving_port': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'total_num_slaves_purchased': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'voyage': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'voyage_name_slave_characteristics'", 'null': 'True', 'to': u"orm['voyage.Voyage']"})
        },
        u'voyage.voyagesources': {
            'Meta': {'object_name': 'VoyageSources'},
            'full_ref': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_ref': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'voyage.voyagesourcesconnection': {
            'Meta': {'object_name': 'VoyageSourcesConnection'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'group'", 'to': u"orm['voyage.Voyage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source'", 'to': u"orm['voyage.VoyageSources']"}),
            'source_order': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'text_ref': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['voyage']