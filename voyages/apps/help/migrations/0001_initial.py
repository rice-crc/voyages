# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Glossary'
        db.create_table('help_glossary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=1000)),
        ))
        db.send_create_signal('help', ['Glossary'])


    def backwards(self, orm):
        # Deleting model 'Glossary'
        db.delete_table('help_glossary')


    models = {
        'help.glossary': {
            'Meta': {'object_name': 'Glossary'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['help']