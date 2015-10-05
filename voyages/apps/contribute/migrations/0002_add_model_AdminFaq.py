# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AdminFaq'
        db.create_table(u'contribute_adminfaq', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('answer', self.gf('django.db.models.fields.TextField')(max_length=1000)),
        ))
        db.send_create_signal(u'contribute', ['AdminFaq'])


    def backwards(self, orm):
        # Deleting model 'AdminFaq'
        db.delete_table(u'contribute_adminfaq')


    models = {
        u'contribute.adminfaq': {
            'Meta': {'ordering': "['question']", 'object_name': 'AdminFaq'},
            'answer': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['contribute']