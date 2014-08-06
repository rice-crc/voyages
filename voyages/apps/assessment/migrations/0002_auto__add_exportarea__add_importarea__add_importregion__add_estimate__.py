# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExportArea'
        db.create_table(u'assessment_exportarea', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('area_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('order_num', self.gf('django.db.models.fields.IntegerField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('show_at_zoom', self.gf('django.db.models.fields.IntegerField')()),
            ('show_on_map', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'assessment', ['ExportArea'])

        # Adding model 'ImportArea'
        db.create_table(u'assessment_importarea', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('area_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('order_num', self.gf('django.db.models.fields.IntegerField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('show_at_zoom', self.gf('django.db.models.fields.IntegerField')()),
            ('show_on_map', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'assessment', ['ImportArea'])

        # Adding model 'ImportRegion'
        db.create_table(u'assessment_importregion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('order_num', self.gf('django.db.models.fields.IntegerField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('show_at_zoom', self.gf('django.db.models.fields.IntegerField')()),
            ('show_on_map', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'assessment', ['ImportRegion'])

        # Adding model 'Estimate'
        db.create_table(u'assessment_estimate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('estimate_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('embarkation_region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assessment.ExportRegion'], null=True, blank=True)),
            ('disembarkation_region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assessment.ImportRegion'], null=True, blank=True)),
            ('embarked_slaves', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('disembarked_slaves', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'assessment', ['Estimate'])

        # Adding model 'ExportRegion'
        db.create_table(u'assessment_exportregion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('order_num', self.gf('django.db.models.fields.IntegerField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('show_at_zoom', self.gf('django.db.models.fields.IntegerField')()),
            ('show_on_map', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'assessment', ['ExportRegion'])


    def backwards(self, orm):
        # Deleting model 'ExportArea'
        db.delete_table(u'assessment_exportarea')

        # Deleting model 'ImportArea'
        db.delete_table(u'assessment_importarea')

        # Deleting model 'ImportRegion'
        db.delete_table(u'assessment_importregion')

        # Deleting model 'Estimate'
        db.delete_table(u'assessment_estimate')

        # Deleting model 'ExportRegion'
        db.delete_table(u'assessment_exportregion')


    models = {
        u'assessment.estimate': {
            'Meta': {'object_name': 'Estimate'},
            'disembarkation_region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['assessment.ImportRegion']", 'null': 'True', 'blank': 'True'}),
            'disembarked_slaves': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'embarkation_region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['assessment.ExportRegion']", 'null': 'True', 'blank': 'True'}),
            'embarked_slaves': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'estimate_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4'})
        },
        u'assessment.exportarea': {
            'Meta': {'object_name': 'ExportArea'},
            'area_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order_num': ('django.db.models.fields.IntegerField', [], {}),
            'show_at_zoom': ('django.db.models.fields.IntegerField', [], {}),
            'show_on_map': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'assessment.exportregion': {
            'Meta': {'object_name': 'ExportRegion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order_num': ('django.db.models.fields.IntegerField', [], {}),
            'region_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'show_at_zoom': ('django.db.models.fields.IntegerField', [], {}),
            'show_on_map': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'assessment.importarea': {
            'Meta': {'object_name': 'ImportArea'},
            'area_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order_num': ('django.db.models.fields.IntegerField', [], {}),
            'show_at_zoom': ('django.db.models.fields.IntegerField', [], {}),
            'show_on_map': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'assessment.importregion': {
            'Meta': {'object_name': 'ImportRegion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order_num': ('django.db.models.fields.IntegerField', [], {}),
            'region_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'show_at_zoom': ('django.db.models.fields.IntegerField', [], {}),
            'show_on_map': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['assessment']