# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ContentPage.title'
        db.alter_column(u'static_content_contentpage', 'title', self.gf('django.db.models.fields.TextField')(max_length=50))

        # Changing field 'ContentPage.description'
        db.alter_column(u'static_content_contentpage', 'description', self.gf('django.db.models.fields.TextField')(max_length=2000))

    def backwards(self, orm):

        # Changing field 'ContentPage.title'
        db.alter_column(u'static_content_contentpage', 'title', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'ContentPage.description'
        db.alter_column(u'static_content_contentpage', 'description', self.gf('django.db.models.fields.CharField')(max_length=2000))

    models = {
        u'static_content.contentgroup': {
            'Meta': {'object_name': 'ContentGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'static_content.contentpage': {
            'Meta': {'object_name': 'ContentPage'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['static_content.ContentGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'title': ('django.db.models.fields.TextField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['static_content']