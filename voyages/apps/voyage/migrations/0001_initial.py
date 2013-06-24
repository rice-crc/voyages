# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GroupComposition'
        db.create_table(u'voyage_groupcomposition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num_men', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_women', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_boy', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_girl', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_adult', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_child', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_infant', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_males', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_females', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'voyage', ['GroupComposition'])

        # Adding model 'VoyageSlavesCharacteristics'
        db.create_table(u'voyage_voyageslavescharacteristics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('embarked_first_port_purchase', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='embarked_first_port_purchase', unique=True, null=True, to=orm['voyage.GroupComposition'])),
            ('died_on_middle_passage', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='died_on_middle_passage', unique=True, null=True, to=orm['voyage.GroupComposition'])),
            ('disembarked_first_place', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='disembarked_first_place', unique=True, null=True, to=orm['voyage.GroupComposition'])),
            ('embarked_second_port_purchase', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='embarked_second_port_purchase', unique=True, null=True, to=orm['voyage.GroupComposition'])),
            ('embarked_third_port_purchase', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='embarked_third_port_purchase', unique=True, null=True, to=orm['voyage.GroupComposition'])),
            ('disembarked_second_place', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='disembarked_second_place', unique=True, null=True, to=orm['voyage.GroupComposition'])),
            ('slave_deaths_before_africa', self.gf('django.db.models.fields.IntegerField')()),
            ('slave_deaths_between_africa_america', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_slaves_intended_first_port', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_slaves_intended_second_port', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_slaves_carried_first_port', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_slaves_carried_second_port', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_slaves_carried_third_port', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('total_num_slaves_purchased', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('total_num_slaves_dep_last_slaving_port', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('total_num_slaves_arr_first_port_embark', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_slaves_disembark_first_place', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_slaves_disembark_second_place', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_slaves_disembark_third_place', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'voyage', ['VoyageSlavesCharacteristics'])

        # Adding model 'VoyageSources'
        db.create_table(u'voyage_voyagesources', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_ref', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('full_ref', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'voyage', ['VoyageSources'])

        # Adding model 'SourceVoyageConnection'
        db.create_table(u'voyage_sourcevoyageconnection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='source', to=orm['voyage.VoyageSources'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='group', to=orm['voyage.Voyage'])),
            ('source_order', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
        ))
        db.send_create_signal(u'voyage', ['SourceVoyageConnection'])

        # Adding model 'BroadRegion'
        db.create_table(u'voyage_broadregion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
        ))
        db.send_create_signal(u'voyage', ['BroadRegion'])

        # Adding model 'Region'
        db.create_table(u'voyage_region', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('broad_region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.BroadRegion'])),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
        ))
        db.send_create_signal(u'voyage', ['Region'])

        # Adding model 'Place'
        db.create_table(u'voyage_place', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.Region'])),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('longtitude', self.gf('django.db.models.fields.DecimalField')(max_length=7, max_digits=3, decimal_places=3, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_length=7, max_digits=3, decimal_places=3, blank=True)),
        ))
        db.send_create_signal(u'voyage', ['Place'])

        # Adding model 'VoyageGroupings'
        db.create_table(u'voyage_voyagegroupings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('grouping_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'voyage', ['VoyageGroupings'])

        # Adding model 'Owner'
        db.create_table(u'voyage_owner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_of_owner', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'voyage', ['Owner'])

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
            ('ship_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('nationality_ship', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nationality_ship', to=orm['voyage.Nationality'])),
            ('tonnage', self.gf('django.db.models.fields.IntegerField')(max_length=4, blank=True)),
            ('ton_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.TonType'])),
            ('rig_of_vessel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.RigOfVessel'])),
            ('guns_mounted', self.gf('django.db.models.fields.IntegerField')(max_length=2, blank=True)),
            ('year_of_construction', self.gf('django.db.models.fields.IntegerField')(max_length=4, blank=True)),
            ('vessel_construction_place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='vessel_construction_place', to=orm['voyage.Place'])),
            ('vessel_construction_region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='vessel_construction_region', to=orm['voyage.Region'])),
            ('registered_year', self.gf('django.db.models.fields.IntegerField')(max_length=4, blank=True)),
            ('registered_place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='registered_place', to=orm['voyage.Place'])),
            ('registered_region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='registered_region', to=orm['voyage.Region'])),
            ('owner_of_venture', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owner_of_venture', to=orm['voyage.Owner'])),
            ('imputed_nationality', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imputed_nationality', to=orm['voyage.Nationality'])),
            ('tonnage_mod', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2, blank=True)),
        ))
        db.send_create_signal(u'voyage', ['VoyageShip'])

        # Adding M2M table for field owners on 'VoyageShip'
        db.create_table(u'voyage_voyageship_owners', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('voyageship', models.ForeignKey(orm[u'voyage.voyageship'], null=False)),
            ('owner', models.ForeignKey(orm[u'voyage.owner'], null=False))
        ))
        db.create_unique(u'voyage_voyageship_owners', ['voyageship_id', 'owner_id'])

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
            ('particular_outcome', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.ParticularOutcome'])),
            ('resistance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.Resistance'])),
            ('outcome_slaves', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.SlavesOutcome'])),
            ('vessel_captured_outcome', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.VesselCapturedOutcome'])),
            ('outcome_owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.OwnerOutcome'])),
        ))
        db.send_create_signal(u'voyage', ['VoyageOutcome'])

        # Adding model 'VoyageItinerary'
        db.create_table(u'voyage_voyageitinerary', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('port_of_departure', self.gf('django.db.models.fields.related.ForeignKey')(related_name='port_of_departure', to=orm['voyage.Place'])),
            ('int_first_port_emb', self.gf('django.db.models.fields.related.ForeignKey')(related_name='int_first_port_emb', to=orm['voyage.Place'])),
            ('int_second_port_emb', self.gf('django.db.models.fields.related.ForeignKey')(related_name='int_second_port_emb', to=orm['voyage.Place'])),
            ('int_first_region_purchase_slaves', self.gf('django.db.models.fields.related.ForeignKey')(related_name='int_first_region_purchase_slaves', to=orm['voyage.Region'])),
            ('int_second_region_purchase_slaves', self.gf('django.db.models.fields.related.ForeignKey')(related_name='int_second_region_purchase_slaves', to=orm['voyage.Region'])),
            ('int_first_port_dis', self.gf('django.db.models.fields.related.ForeignKey')(related_name='int_first_port_dis', to=orm['voyage.Place'])),
            ('int_second_port_dis', self.gf('django.db.models.fields.related.ForeignKey')(related_name='int_second_port_dis', to=orm['voyage.Place'])),
            ('int_first_region_slave_landing', self.gf('django.db.models.fields.related.ForeignKey')(related_name='int_first_region_slave_landing', to=orm['voyage.Region'])),
            ('int_second_region_slave_landing', self.gf('django.db.models.fields.related.ForeignKey')(related_name='int_second_region_slave_landing', to=orm['voyage.Region'])),
            ('ports_called_buying_slaves', self.gf('django.db.models.fields.IntegerField')(max_length=3, blank=True)),
            ('first_place_slave_purchase', self.gf('django.db.models.fields.related.ForeignKey')(related_name='first_place_slave_purchase', to=orm['voyage.Place'])),
            ('second_place_slave_purchase', self.gf('django.db.models.fields.related.ForeignKey')(related_name='second_place_slave_purchase', to=orm['voyage.Place'])),
            ('third_place_slave_purchase', self.gf('django.db.models.fields.related.ForeignKey')(related_name='third_place_slave_purchase', to=orm['voyage.Place'])),
            ('first_region_slave_emb', self.gf('django.db.models.fields.related.ForeignKey')(related_name='first_region_slave_emb', to=orm['voyage.Region'])),
            ('second_region_slave_emb', self.gf('django.db.models.fields.related.ForeignKey')(related_name='second_region_slave_emb', to=orm['voyage.Region'])),
            ('third_region_slave_emb', self.gf('django.db.models.fields.related.ForeignKey')(related_name='third_region_slave_emb', to=orm['voyage.Region'])),
            ('port_of_call_before_atl_crossing', self.gf('django.db.models.fields.related.ForeignKey')(related_name='port_of_call_before_atl_crossing', to=orm['voyage.Place'])),
            ('number_of_ports_of_call', self.gf('django.db.models.fields.related.ForeignKey')(related_name='number_of_ports_of_call', to=orm['voyage.Place'])),
            ('first_landing_place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='first_landing_place', to=orm['voyage.Place'])),
            ('second_landing_place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='second_landing_place', to=orm['voyage.Place'])),
            ('third_landing_place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='third_landing_place', to=orm['voyage.Place'])),
            ('first_landing_region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='first_landing_region', to=orm['voyage.Region'])),
            ('second_landing_region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='second_landing_region', to=orm['voyage.Region'])),
            ('third_landing_region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='third_landing_region', to=orm['voyage.Region'])),
            ('place_voyage_ended', self.gf('django.db.models.fields.related.ForeignKey')(related_name='place_voyage_ended', to=orm['voyage.Place'])),
            ('region_of_return', self.gf('django.db.models.fields.related.ForeignKey')(related_name='region_of_return', to=orm['voyage.Region'])),
            ('broad_region_of_return', self.gf('django.db.models.fields.related.ForeignKey')(related_name='broad_region_of_return', to=orm['voyage.Region'])),
            ('imp_port_voyage_begin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imp_port_voyage_begin', to=orm['voyage.Place'])),
            ('imp_region_voyage_begin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imp_region_voyage_begin', to=orm['voyage.Region'])),
            ('imp_broad_region_voyage_begin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imp_broad_region_voyage_begin', to=orm['voyage.BroadRegion'])),
            ('principal_place_of_slave_purchase', self.gf('django.db.models.fields.related.ForeignKey')(related_name='principal_place_of_slave_purchase', to=orm['voyage.Place'])),
            ('imp_principal_place_of_slave_purchase', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imp_principal_place_of_slave_purchase', to=orm['voyage.Place'])),
            ('imp_principal_region_of_slave_purchase', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imp_principal_region_of_slave_purchase', to=orm['voyage.Region'])),
            ('imp_broad_region_of_slave_purchase', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imp_broad_region_of_slave_purchase', to=orm['voyage.BroadRegion'])),
            ('principal_port_of_slave_dis', self.gf('django.db.models.fields.related.ForeignKey')(related_name='principal_port_of_slave_dis', to=orm['voyage.Place'])),
            ('imp_principal_port_slave_dis', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imp_principal_port_slave_dis', to=orm['voyage.Place'])),
            ('imp_principal_region_slave_dis', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imp_principal_region_slave_dis', to=orm['voyage.Region'])),
            ('imp_broad_region_slave_dis', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imp_broad_region_slave_dis', to=orm['voyage.BroadRegion'])),
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
            ('voyage_began', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10)),
            ('slave_purchase_began', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10)),
            ('vessel_left_port', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10)),
            ('first_dis_of_slaves', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10)),
            ('arrival_at_second_place_landing', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10)),
            ('third_dis_of_slaves', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10)),
            ('departure_last_place_of_landing', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10)),
            ('voyage_completed', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10)),
            ('imp_voyage_began', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=4, null=True, blank=True)),
            ('imp_departed_africa', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=4, null=True, blank=True)),
            ('imp_arrival_at_port_of_dis', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=4, null=True, blank=True)),
            ('five_year_period', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=3, null=True, blank=True)),
            ('decade_of_voyage', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=3, null=True, blank=True)),
            ('quarter_century_of_voyage', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=3, null=True, blank=True)),
            ('century_of_voyage', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=4, null=True, blank=True)),
            ('voyage_length_home_to_dis', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=5, null=True, blank=True)),
            ('voyage_length_africa_to_dis', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=5, null=True, blank=True)),
        ))
        db.send_create_signal(u'voyage', ['VoyageDates'])

        # Adding model 'Captain'
        db.create_table(u'voyage_captain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal(u'voyage', ['Captain'])

        # Adding model 'VoyageCaptainCrew'
        db.create_table(u'voyage_voyagecaptaincrew', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('crew_voyage_outset', self.gf('django.db.models.fields.IntegerField')(max_length=3, blank=True)),
            ('crew_departure_last_port', self.gf('django.db.models.fields.IntegerField')(max_length=3, blank=True)),
            ('crew_first_landing', self.gf('django.db.models.fields.IntegerField')(max_length=2, blank=True)),
            ('crew_return_begin', self.gf('django.db.models.fields.IntegerField')(max_length=2, blank=True)),
            ('crew_end_voyage', self.gf('django.db.models.fields.IntegerField')(max_length=2, blank=True)),
            ('unspecified_crew', self.gf('django.db.models.fields.IntegerField')(max_length=3, blank=True)),
            ('crew_died_before_first_trade', self.gf('django.db.models.fields.IntegerField')(max_length=2, blank=True)),
            ('crew_died_while_ship_african', self.gf('django.db.models.fields.IntegerField')(max_length=2, blank=True)),
            ('crew_died_middle_passge', self.gf('django.db.models.fields.IntegerField')(max_length=2, blank=True)),
            ('crew_died_in_americas', self.gf('django.db.models.fields.IntegerField')(max_length=2, blank=True)),
            ('crew_died_on_return_voyage', self.gf('django.db.models.fields.IntegerField')(max_length=2, blank=True)),
            ('crew_died_complete_voyage', self.gf('django.db.models.fields.IntegerField')(max_length=3, blank=True)),
            ('crew_deserted', self.gf('django.db.models.fields.IntegerField')(max_length=2, blank=True)),
        ))
        db.send_create_signal(u'voyage', ['VoyageCaptainCrew'])

        # Adding M2M table for field first_captain on 'VoyageCaptainCrew'
        db.create_table(u'voyage_voyagecaptaincrew_first_captain', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('voyagecaptaincrew', models.ForeignKey(orm[u'voyage.voyagecaptaincrew'], null=False)),
            ('captain', models.ForeignKey(orm[u'voyage.captain'], null=False))
        ))
        db.create_unique(u'voyage_voyagecaptaincrew_first_captain', ['voyagecaptaincrew_id', 'captain_id'])

        # Adding M2M table for field second_captain on 'VoyageCaptainCrew'
        db.create_table(u'voyage_voyagecaptaincrew_second_captain', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('voyagecaptaincrew', models.ForeignKey(orm[u'voyage.voyagecaptaincrew'], null=False)),
            ('captain', models.ForeignKey(orm[u'voyage.captain'], null=False))
        ))
        db.create_unique(u'voyage_voyagecaptaincrew_second_captain', ['voyagecaptaincrew_id', 'captain_id'])

        # Adding M2M table for field third_captain on 'VoyageCaptainCrew'
        db.create_table(u'voyage_voyagecaptaincrew_third_captain', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('voyagecaptaincrew', models.ForeignKey(orm[u'voyage.voyagecaptaincrew'], null=False)),
            ('captain', models.ForeignKey(orm[u'voyage.captain'], null=False))
        ))
        db.create_unique(u'voyage_voyagecaptaincrew_third_captain', ['voyagecaptaincrew_id', 'captain_id'])

        # Adding model 'Voyage'
        db.create_table(u'voyage_voyage', (
            ('voyage_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voyage_in_cd_rom', self.gf('django.db.models.fields.IntegerField')(max_length=1, blank=True)),
            ('voyage_groupings', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['voyage.VoyageGroupings'], unique=True)),
            ('voyage_ship', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['voyage.VoyageShip'], unique=True)),
            ('voyage_outcome', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['voyage.VoyageOutcome'], unique=True)),
            ('voyage_itinerary', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['voyage.VoyageItinerary'], unique=True)),
            ('voyage_dates', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['voyage.VoyageDates'], unique=True)),
            ('voyage_captain_crew', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['voyage.VoyageCaptainCrew'], unique=True, null=True, blank=True)),
            ('voyage_slave_characteristics', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['voyage.VoyageSlavesCharacteristics'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'voyage', ['Voyage'])


    def backwards(self, orm):
        # Deleting model 'GroupComposition'
        db.delete_table(u'voyage_groupcomposition')

        # Deleting model 'VoyageSlavesCharacteristics'
        db.delete_table(u'voyage_voyageslavescharacteristics')

        # Deleting model 'VoyageSources'
        db.delete_table(u'voyage_voyagesources')

        # Deleting model 'SourceVoyageConnection'
        db.delete_table(u'voyage_sourcevoyageconnection')

        # Deleting model 'BroadRegion'
        db.delete_table(u'voyage_broadregion')

        # Deleting model 'Region'
        db.delete_table(u'voyage_region')

        # Deleting model 'Place'
        db.delete_table(u'voyage_place')

        # Deleting model 'VoyageGroupings'
        db.delete_table(u'voyage_voyagegroupings')

        # Deleting model 'Owner'
        db.delete_table(u'voyage_owner')

        # Deleting model 'Nationality'
        db.delete_table(u'voyage_nationality')

        # Deleting model 'TonType'
        db.delete_table(u'voyage_tontype')

        # Deleting model 'RigOfVessel'
        db.delete_table(u'voyage_rigofvessel')

        # Deleting model 'VoyageShip'
        db.delete_table(u'voyage_voyageship')

        # Removing M2M table for field owners on 'VoyageShip'
        db.delete_table('voyage_voyageship_owners')

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

        # Deleting model 'Captain'
        db.delete_table(u'voyage_captain')

        # Deleting model 'VoyageCaptainCrew'
        db.delete_table(u'voyage_voyagecaptaincrew')

        # Removing M2M table for field first_captain on 'VoyageCaptainCrew'
        db.delete_table('voyage_voyagecaptaincrew_first_captain')

        # Removing M2M table for field second_captain on 'VoyageCaptainCrew'
        db.delete_table('voyage_voyagecaptaincrew_second_captain')

        # Removing M2M table for field third_captain on 'VoyageCaptainCrew'
        db.delete_table('voyage_voyagecaptaincrew_third_captain')

        # Deleting model 'Voyage'
        db.delete_table(u'voyage_voyage')


    models = {
        u'voyage.broadregion': {
            'Meta': {'object_name': 'BroadRegion'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '35'})
        },
        u'voyage.captain': {
            'Meta': {'object_name': 'Captain'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'voyage.groupcomposition': {
            'Meta': {'object_name': 'GroupComposition'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_adult': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_boy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_child': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_females': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_girl': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_infant': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_males': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_men': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_women': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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
        u'voyage.owner': {
            'Meta': {'object_name': 'Owner'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_of_owner': ('django.db.models.fields.CharField', [], {'max_length': '40'})
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
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_length': '7', 'max_digits': '3', 'decimal_places': '3', 'blank': 'True'}),
            'longtitude': ('django.db.models.fields.DecimalField', [], {'max_length': '7', 'max_digits': '3', 'decimal_places': '3', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.Region']"})
        },
        u'voyage.region': {
            'Meta': {'object_name': 'Region'},
            'broad_region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.BroadRegion']"}),
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '35'})
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
        u'voyage.sourcevoyageconnection': {
            'Meta': {'object_name': 'SourceVoyageConnection'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'group'", 'to': u"orm['voyage.Voyage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source'", 'to': u"orm['voyage.VoyageSources']"}),
            'source_order': ('django.db.models.fields.IntegerField', [], {'max_length': '2'})
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
            'voyage_captain_crew': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['voyage.VoyageCaptainCrew']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'voyage_dates': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['voyage.VoyageDates']", 'unique': 'True'}),
            'voyage_groupings': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['voyage.VoyageGroupings']", 'unique': 'True'}),
            'voyage_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'voyage_in_cd_rom': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'blank': 'True'}),
            'voyage_itinerary': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['voyage.VoyageItinerary']", 'unique': 'True'}),
            'voyage_outcome': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['voyage.VoyageOutcome']", 'unique': 'True'}),
            'voyage_ship': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['voyage.VoyageShip']", 'unique': 'True'}),
            'voyage_slave_characteristics': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['voyage.VoyageSlavesCharacteristics']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'voyage_sources': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'voyage_sources'", 'to': u"orm['voyage.VoyageSources']", 'through': u"orm['voyage.SourceVoyageConnection']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'})
        },
        u'voyage.voyagecaptaincrew': {
            'Meta': {'object_name': 'VoyageCaptainCrew'},
            'crew_departure_last_port': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'blank': 'True'}),
            'crew_deserted': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'blank': 'True'}),
            'crew_died_before_first_trade': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'blank': 'True'}),
            'crew_died_complete_voyage': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'blank': 'True'}),
            'crew_died_in_americas': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'blank': 'True'}),
            'crew_died_middle_passge': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'blank': 'True'}),
            'crew_died_on_return_voyage': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'blank': 'True'}),
            'crew_died_while_ship_african': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'blank': 'True'}),
            'crew_end_voyage': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'blank': 'True'}),
            'crew_first_landing': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'blank': 'True'}),
            'crew_return_begin': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'blank': 'True'}),
            'crew_voyage_outset': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'blank': 'True'}),
            'first_captain': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'first_captain'", 'symmetrical': 'False', 'to': u"orm['voyage.Captain']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'second_captain': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'second captain'", 'symmetrical': 'False', 'to': u"orm['voyage.Captain']"}),
            'third_captain': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'third_captain'", 'symmetrical': 'False', 'to': u"orm['voyage.Captain']"}),
            'unspecified_crew': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'blank': 'True'})
        },
        u'voyage.voyagedates': {
            'Meta': {'object_name': 'VoyageDates'},
            'arrival_at_second_place_landing': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10'}),
            'century_of_voyage': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'decade_of_voyage': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'departure_last_place_of_landing': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10'}),
            'first_dis_of_slaves': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10'}),
            'five_year_period': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imp_arrival_at_port_of_dis': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'imp_departed_africa': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'imp_voyage_began': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'quarter_century_of_voyage': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'slave_purchase_began': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10'}),
            'third_dis_of_slaves': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10'}),
            'vessel_left_port': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10'}),
            'voyage_began': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10'}),
            'voyage_completed': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10'}),
            'voyage_length_africa_to_dis': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'voyage_length_home_to_dis': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '5', 'null': 'True', 'blank': 'True'})
        },
        u'voyage.voyagegroupings': {
            'Meta': {'object_name': 'VoyageGroupings'},
            'grouping_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'voyage.voyageitinerary': {
            'Meta': {'object_name': 'VoyageItinerary'},
            'broad_region_of_return': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'broad_region_of_return'", 'to': u"orm['voyage.Region']"}),
            'first_landing_place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_landing_place'", 'to': u"orm['voyage.Place']"}),
            'first_landing_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_landing_region'", 'to': u"orm['voyage.Region']"}),
            'first_place_slave_purchase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_place_slave_purchase'", 'to': u"orm['voyage.Place']"}),
            'first_region_slave_emb': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_region_slave_emb'", 'to': u"orm['voyage.Region']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imp_broad_region_of_slave_purchase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imp_broad_region_of_slave_purchase'", 'to': u"orm['voyage.BroadRegion']"}),
            'imp_broad_region_slave_dis': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imp_broad_region_slave_dis'", 'to': u"orm['voyage.BroadRegion']"}),
            'imp_broad_region_voyage_begin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imp_broad_region_voyage_begin'", 'to': u"orm['voyage.BroadRegion']"}),
            'imp_port_voyage_begin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imp_port_voyage_begin'", 'to': u"orm['voyage.Place']"}),
            'imp_principal_place_of_slave_purchase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imp_principal_place_of_slave_purchase'", 'to': u"orm['voyage.Place']"}),
            'imp_principal_port_slave_dis': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imp_principal_port_slave_dis'", 'to': u"orm['voyage.Place']"}),
            'imp_principal_region_of_slave_purchase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imp_principal_region_of_slave_purchase'", 'to': u"orm['voyage.Region']"}),
            'imp_principal_region_slave_dis': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imp_principal_region_slave_dis'", 'to': u"orm['voyage.Region']"}),
            'imp_region_voyage_begin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imp_region_voyage_begin'", 'to': u"orm['voyage.Region']"}),
            'int_first_port_dis': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'int_first_port_dis'", 'to': u"orm['voyage.Place']"}),
            'int_first_port_emb': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'int_first_port_emb'", 'to': u"orm['voyage.Place']"}),
            'int_first_region_purchase_slaves': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'int_first_region_purchase_slaves'", 'to': u"orm['voyage.Region']"}),
            'int_first_region_slave_landing': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'int_first_region_slave_landing'", 'to': u"orm['voyage.Region']"}),
            'int_second_port_dis': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'int_second_port_dis'", 'to': u"orm['voyage.Place']"}),
            'int_second_port_emb': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'int_second_port_emb'", 'to': u"orm['voyage.Place']"}),
            'int_second_region_purchase_slaves': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'int_second_region_purchase_slaves'", 'to': u"orm['voyage.Region']"}),
            'int_second_region_slave_landing': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'int_second_region_slave_landing'", 'to': u"orm['voyage.Region']"}),
            'number_of_ports_of_call': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'number_of_ports_of_call'", 'to': u"orm['voyage.Place']"}),
            'place_voyage_ended': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'place_voyage_ended'", 'to': u"orm['voyage.Place']"}),
            'port_of_call_before_atl_crossing': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'port_of_call_before_atl_crossing'", 'to': u"orm['voyage.Place']"}),
            'port_of_departure': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'port_of_departure'", 'to': u"orm['voyage.Place']"}),
            'ports_called_buying_slaves': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'blank': 'True'}),
            'principal_place_of_slave_purchase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'principal_place_of_slave_purchase'", 'to': u"orm['voyage.Place']"}),
            'principal_port_of_slave_dis': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'principal_port_of_slave_dis'", 'to': u"orm['voyage.Place']"}),
            'region_of_return': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'region_of_return'", 'to': u"orm['voyage.Region']"}),
            'second_landing_place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'second_landing_place'", 'to': u"orm['voyage.Place']"}),
            'second_landing_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'second_landing_region'", 'to': u"orm['voyage.Region']"}),
            'second_place_slave_purchase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'second_place_slave_purchase'", 'to': u"orm['voyage.Place']"}),
            'second_region_slave_emb': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'second_region_slave_emb'", 'to': u"orm['voyage.Region']"}),
            'third_landing_place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'third_landing_place'", 'to': u"orm['voyage.Place']"}),
            'third_landing_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'third_landing_region'", 'to': u"orm['voyage.Region']"}),
            'third_place_slave_purchase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'third_place_slave_purchase'", 'to': u"orm['voyage.Place']"}),
            'third_region_slave_emb': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'third_region_slave_emb'", 'to': u"orm['voyage.Region']"})
        },
        u'voyage.voyageoutcome': {
            'Meta': {'object_name': 'VoyageOutcome'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outcome_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.OwnerOutcome']"}),
            'outcome_slaves': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.SlavesOutcome']"}),
            'particular_outcome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.ParticularOutcome']"}),
            'resistance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.Resistance']"}),
            'vessel_captured_outcome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.VesselCapturedOutcome']"})
        },
        u'voyage.voyageship': {
            'Meta': {'object_name': 'VoyageShip'},
            'guns_mounted': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imputed_nationality': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imputed_nationality'", 'to': u"orm['voyage.Nationality']"}),
            'nationality_ship': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nationality_ship'", 'to': u"orm['voyage.Nationality']"}),
            'owner_of_venture': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner_of_venture'", 'to': u"orm['voyage.Owner']"}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'owners'", 'symmetrical': 'False', 'to': u"orm['voyage.Owner']"}),
            'registered_place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'registered_place'", 'to': u"orm['voyage.Place']"}),
            'registered_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'registered_region'", 'to': u"orm['voyage.Region']"}),
            'registered_year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'blank': 'True'}),
            'rig_of_vessel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.RigOfVessel']"}),
            'ship_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'ton_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.TonType']"}),
            'tonnage': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'blank': 'True'}),
            'tonnage_mod': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'vessel_construction_place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vessel_construction_place'", 'to': u"orm['voyage.Place']"}),
            'vessel_construction_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vessel_construction_region'", 'to': u"orm['voyage.Region']"}),
            'year_of_construction': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'blank': 'True'})
        },
        u'voyage.voyageslavescharacteristics': {
            'Meta': {'object_name': 'VoyageSlavesCharacteristics'},
            'died_on_middle_passage': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'died_on_middle_passage'", 'unique': 'True', 'null': 'True', 'to': u"orm['voyage.GroupComposition']"}),
            'disembarked_first_place': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'disembarked_first_place'", 'unique': 'True', 'null': 'True', 'to': u"orm['voyage.GroupComposition']"}),
            'disembarked_second_place': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'disembarked_second_place'", 'unique': 'True', 'null': 'True', 'to': u"orm['voyage.GroupComposition']"}),
            'embarked_first_port_purchase': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'embarked_first_port_purchase'", 'unique': 'True', 'null': 'True', 'to': u"orm['voyage.GroupComposition']"}),
            'embarked_second_port_purchase': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'embarked_second_port_purchase'", 'unique': 'True', 'null': 'True', 'to': u"orm['voyage.GroupComposition']"}),
            'embarked_third_port_purchase': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'embarked_third_port_purchase'", 'unique': 'True', 'null': 'True', 'to': u"orm['voyage.GroupComposition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_slaves_carried_first_port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_slaves_carried_second_port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_slaves_carried_third_port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_slaves_disembark_first_place': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_slaves_disembark_second_place': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_slaves_disembark_third_place': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_slaves_intended_first_port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_slaves_intended_second_port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slave_deaths_before_africa': ('django.db.models.fields.IntegerField', [], {}),
            'slave_deaths_between_africa_america': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_num_slaves_arr_first_port_embark': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_num_slaves_dep_last_slaving_port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_num_slaves_purchased': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'voyage.voyagesources': {
            'Meta': {'object_name': 'VoyageSources'},
            'full_ref': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_ref': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
        }
    }

    complete_apps = ['voyage']