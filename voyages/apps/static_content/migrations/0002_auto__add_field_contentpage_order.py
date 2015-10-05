# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ContentPage.order'
        db.add_column(u'static_content_contentpage', 'order',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ContentPage.order'
        db.delete_column(u'static_content_contentpage', 'order')


    models = {
        u'static_content.contentgroup': {
            'Meta': {'object_name': 'ContentGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'static_content.contentpage': {
            'Meta': {'object_name': 'ContentPage'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['static_content.ContentGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['static_content']