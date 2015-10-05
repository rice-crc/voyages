# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ContentGroup'
        db.create_table(u'static_content_contentgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'static_content', ['ContentGroup'])

        # Adding model 'ContentPage'
        db.create_table(u'static_content_contentpage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['static_content.ContentGroup'])),
        ))
        db.send_create_signal(u'static_content', ['ContentPage'])


    def backwards(self, orm):
        # Deleting model 'ContentGroup'
        db.delete_table(u'static_content_contentgroup')

        # Deleting model 'ContentPage'
        db.delete_table(u'static_content_contentpage')


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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['static_content']