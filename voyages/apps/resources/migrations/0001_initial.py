# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Image'
        db.create_table(u'resources_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True)),
            ('width', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('size', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True)),
            ('other_references', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('emory', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('emory_location', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('authorization_status', self.gf('django.db.models.fields.IntegerField')()),
            ('image_status', self.gf('django.db.models.fields.IntegerField')()),
            ('ready_to_go', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order_num', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resources.ImageCategory'])),
            ('voyage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voyage.Voyage'])),
        ))
        db.send_create_signal(u'resources', ['Image'])

        # Adding model 'ImageCategory'
        db.create_table(u'resources_imagecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'resources', ['ImageCategory'])


    def backwards(self, orm):
        # Deleting model 'Image'
        db.delete_table(u'resources_image')

        # Deleting model 'ImageCategory'
        db.delete_table(u'resources_imagecategory')


    models = {
        u'resources.image': {
            'Meta': {'object_name': 'Image'},
            'authorization_status': ('django.db.models.fields.IntegerField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resources.ImageCategory']"}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'date': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'emory': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'emory_location': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_status': ('django.db.models.fields.IntegerField', [], {}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'order_num': ('django.db.models.fields.IntegerField', [], {}),
            'other_references': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'ready_to_go': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'voyage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.Voyage']"}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'resources.imagecategory': {
            'Meta': {'object_name': 'ImageCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'voyage.voyage': {
            'Meta': {'ordering': "['voyage_id']", 'object_name': 'Voyage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'voyage_captain': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['voyage.VoyageCaptain']", 'null': 'True', 'through': u"orm['voyage.VoyageCaptainConnection']", 'blank': 'True'}),
            'voyage_groupings': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voyage.VoyageGroupings']", 'null': 'True', 'blank': 'True'}),
            'voyage_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'voyage_in_cd_rom': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'max_length': '1'}),
            'voyage_ship_owner': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['voyage.VoyageShipOwner']", 'null': 'True', 'through': u"orm['voyage.VoyageShipOwnerConnection']", 'blank': 'True'}),
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
        u'voyage.voyagegroupings': {
            'Meta': {'object_name': 'VoyageGroupings'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '30'})
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
        u'voyage.voyagesources': {
            'Meta': {'ordering': "['short_ref', 'full_ref']", 'object_name': 'VoyageSources'},
            'full_ref': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_ref': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'voyage.voyagesourcesconnection': {
            'Meta': {'object_name': 'VoyageSourcesConnection'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'group'", 'to': u"orm['voyage.Voyage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'source'", 'null': 'True', 'to': u"orm['voyage.VoyageSources']"}),
            'source_order': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'text_ref': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['resources']