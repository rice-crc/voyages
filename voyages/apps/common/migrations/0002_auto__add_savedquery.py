# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SavedQuery'
        db.create_table(u'common_savedquery', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=8, primary_key=True)),
            ('query', self.gf('django.db.models.fields.TextField')(unique=True)),
        ))
        db.send_create_signal(u'common', ['SavedQuery'])


    def backwards(self, orm):
        # Deleting model 'SavedQuery'
        db.delete_table(u'common_savedquery')


    models = {
        u'common.savedquery': {
            'Meta': {'object_name': 'SavedQuery'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'primary_key': 'True'}),
            'query': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['common']