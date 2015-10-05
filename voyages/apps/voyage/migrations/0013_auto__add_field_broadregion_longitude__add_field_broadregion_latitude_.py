# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BroadRegion.longitude'
        db.add_column(u'voyage_broadregion', 'longitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=7, blank=True),
                      keep_default=False)

        # Adding field 'BroadRegion.latitude'
        db.add_column(u'voyage_broadregion', 'latitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=7, blank=True),
                      keep_default=False)

        # Adding field 'Region.longitude'
        db.add_column(u'voyage_region', 'longitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=7, blank=True),
                      keep_default=False)

        # Adding field 'Region.latitude'
        db.add_column(u'voyage_region', 'latitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=7, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'BroadRegion.longitude'
        db.delete_column(u'voyage_broadregion', 'longitude')

        # Deleting field 'BroadRegion.latitude'
        db.delete_column(u'voyage_broadregion', 'latitude')

        # Deleting field 'Region.longitude'
        db.delete_column(u'voyage_region', 'longitude')

        # Deleting field 'Region.latitude'
        db.delete_column(u'voyage_region', 'latitude')


    models = {
        u'voyage.broadregion': {
            'Meta': {'ordering': "['value']", 'object_name': 'BroadRegion'},
            'broad_region': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '7', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '7', 'blank': 'True'}),
            'show_on_map': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {'max_length': '5'})
        },
        u'voyage.nationality': {
            'Meta': {'ordering': "['value']", 'object_name': 'Nationality'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'value': ('django.db.models.fields.IntegerField', [], {'max_length': '2'})
        },
        u'voyage.owneroutcome': {
            'Meta': {'ordering': "['value']", 'object_name': 'OwnerOutcome'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.IntegerField', [], {'max_length': '1'})
        },
        u'voyage.particularoutcome': {
            'Meta': {'ordering': "['value']", 'object_name': 'ParticularOutcome'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.IntegerField', [], {'max_length': '3'})
        },
        u'voyage.place': {
            'Meta': {'ordering': "['value']", 'object_name': 'Place'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '7', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '7', 'blank': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.Region']"}),
            'show_on_main_map': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_on_voyage_map': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'max_length': '5'})
        },
        u'voyage.region': {
            'Meta': {'ordering': "['value']", 'object_name': 'Region'},
            'broad_region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.BroadRegion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '7', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '7', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'show_on_main_map': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_on_map': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {'max_length': '5'})
        },
        u'voyage.resistance': {
            'Meta': {'ordering': "['value']", 'object_name': 'Resistance'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'value': ('django.db.models.fields.IntegerField', [], {'max_length': '1'})
        },
        u'voyage.rigofvessel': {
            'Meta': {'ordering': "['value']", 'object_name': 'RigOfVessel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'value': ('django.db.models.fields.IntegerField', [], {'max_length': '2'})
        },
        u'voyage.slavesoutcome': {
            'Meta': {'ordering': "['value']", 'object_name': 'SlavesOutcome'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.IntegerField', [], {'max_length': '1'})
        },
        u'voyage.tontype': {
            'Meta': {'ordering': "['value']", 'object_name': 'TonType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'value': ('django.db.models.fields.IntegerField', [], {'max_length': '2'})
        },
        u'voyage.vesselcapturedoutcome': {
            'Meta': {'ordering': "['value']", 'object_name': 'VesselCapturedOutcome'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.IntegerField', [], {'max_length': '2'})
        },
        u'voyage.voyage': {
            'Meta': {'ordering': "['voyage_id']", 'object_name': 'Voyage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'voyage_captain': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['voyage.VoyageCaptain']", 'null': 'True', 'through': u"orm['voyage.VoyageCaptainConnection']", 'blank': 'True'}),
            'voyage_crew': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'voyage_crew'", 'null': 'True', 'to': u"orm['voyage.VoyageCrew']"}),
            'voyage_dates': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'voyage_dates'", 'null': 'True', 'to': u"orm['voyage.VoyageDates']"}),
            'voyage_groupings': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.VoyageGroupings']", 'null': 'True', 'blank': 'True'}),
            'voyage_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'voyage_in_cd_rom': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'max_length': '1'}),
            'voyage_itinerary': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'voyage_itinerary'", 'null': 'True', 'to': u"orm['voyage.VoyageItinerary']"}),
            'voyage_ship': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'voyage_ship'", 'null': 'True', 'to': u"orm['voyage.VoyageShip']"}),
            'voyage_ship_owner': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['voyage.VoyageShipOwner']", 'null': 'True', 'through': u"orm['voyage.VoyageShipOwnerConnection']", 'blank': 'True'}),
            'voyage_slaves_numbers': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'voyage_slaves_numbers'", 'null': 'True', 'to': u"orm['voyage.VoyageSlavesNumbers']"}),
            'voyage_sources': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'voyage_sources'", 'to': u"orm['voyage.VoyageSources']", 'through': u"orm['voyage.VoyageSourcesConnection']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'})
        },
        u'voyage.voyagecaptain': {
            'Meta': {'object_name': 'VoyageCaptain'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'})
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
            'crew_died_middle_passage': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
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
            'date_departed_africa': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'departure_last_place_of_landing': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'first_dis_of_slaves': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imp_arrival_at_port_of_dis': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'imp_departed_africa': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'imp_length_home_to_disembark': ('django.db.models.fields.IntegerField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'imp_length_leaving_africa_to_disembark': ('django.db.models.fields.IntegerField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'imp_voyage_began': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'length_middle_passage_days': ('django.db.models.fields.IntegerField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'slave_purchase_began': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'third_dis_of_slaves': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'vessel_left_port': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'voyage': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'voyage_name_dates'", 'null': 'True', 'to': u"orm['voyage.Voyage']"}),
            'voyage_began': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'voyage_completed': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'voyage.voyagegroupings': {
            'Meta': {'object_name': 'VoyageGroupings'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'value': ('django.db.models.fields.IntegerField', [], {'max_length': '3'})
        },
        u'voyage.voyageitinerary': {
            'Meta': {'object_name': 'VoyageItinerary'},
            'broad_region_of_return': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'broad_region_of_return'", 'null': 'True', 'to': u"orm['voyage.BroadRegion']"}),
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
            'int_second_place_region_slave_landing': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'int_second_region_slave_landing'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'int_second_port_dis': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'int_second_port_dis'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'int_second_port_emb': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'int_second_port_emb'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'int_second_region_purchase_slaves': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'int_second_region_purchase_slaves'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'number_of_ports_of_call': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'ship_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'ton_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.TonType']", 'null': 'True', 'blank': 'True'}),
            'tonnage': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'tonnage_mod': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '1', 'blank': 'True'}),
            'vessel_construction_place': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vessel_construction_place'", 'null': 'True', 'to': u"orm['voyage.Place']"}),
            'vessel_construction_region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vessel_construction_region'", 'null': 'True', 'to': u"orm['voyage.Region']"}),
            'voyage': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'voyage_name_ship'", 'null': 'True', 'to': u"orm['voyage.Voyage']"}),
            'year_of_construction': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        u'voyage.voyageshipowner': {
            'Meta': {'object_name': 'VoyageShipOwner'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'})
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
            'imp_adult_death_middle_passage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_child_death_middle_passage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_female_death_middle_passage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_jamaican_cash_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'imp_male_death_middle_passage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_mortality_during_voyage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_mortality_ratio': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'imp_num_adult_embarked': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_num_adult_landed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_num_adult_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_num_boy_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_num_child_landed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_num_child_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_num_children_embarked': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_num_female_embarked': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_num_female_landed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_num_females_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_num_girl_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_num_male_embarked': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_num_male_landed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_num_males_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_num_men_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_num_women_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_slaves_embarked_for_mortality': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_total_num_slaves_disembarked': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imp_total_num_slaves_embarked': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'percentage_adult': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'percentage_boy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'percentage_child': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'percentage_female': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'percentage_girl': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'percentage_male': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'percentage_men': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'percentage_women': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'slave_deaths_before_africa': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slave_deaths_between_africa_america': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_num_slaves_arr_first_port_embark': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'total_num_slaves_dep_last_slaving_port': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'total_num_slaves_purchased': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'total_slaves_dept_or_arr_age_identified': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_slaves_dept_or_arr_gender_identified': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_slaves_embarked_age_identified': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_slaves_embarked_gender_identified': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_slaves_landed_age_identified': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_slaves_landed_gender_identified': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'voyage': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'voyage_name_slave_characteristics'", 'to': u"orm['voyage.Voyage']"})
        },
        u'voyage.voyagesources': {
            'Meta': {'ordering': "['short_ref', 'full_ref']", 'object_name': 'VoyageSources'},
            'full_ref': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_ref': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'source_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.VoyageSourcesType']", 'null': 'True'})
        },
        u'voyage.voyagesourcesconnection': {
            'Meta': {'object_name': 'VoyageSourcesConnection'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'group'", 'to': u"orm['voyage.Voyage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'source'", 'null': 'True', 'to': u"orm['voyage.VoyageSources']"}),
            'source_order': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'text_ref': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'voyage.voyagesourcestype': {
            'Meta': {'ordering': "['group_id']", 'object_name': 'VoyageSourcesType'},
            'group_id': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['voyage']