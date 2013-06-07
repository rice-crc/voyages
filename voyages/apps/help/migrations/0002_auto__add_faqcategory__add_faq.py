# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FaqCategory'
        db.create_table('help_faqcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('type_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('help', ['FaqCategory'])

        # Adding model 'Faq'
        db.create_table('help_faq', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.TextField')(max_length=300)),
            ('answer', self.gf('django.db.models.fields.TextField')(max_length=2000)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['help.FaqCategory'])),
            ('question_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('help', ['Faq'])


    def backwards(self, orm):
        # Deleting model 'FaqCategory'
        db.delete_table('help_faqcategory')

        # Deleting model 'Faq'
        db.delete_table('help_faq')


    models = {
        'help.faq': {
            'Meta': {'ordering': "['question_order']", 'object_name': 'Faq'},
            'answer': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['help.FaqCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'question_order': ('django.db.models.fields.IntegerField', [], {})
        },
        'help.faqcategory': {
            'Meta': {'ordering': "['type_order']", 'object_name': 'FaqCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type_order': ('django.db.models.fields.IntegerField', [], {})
        },
        'help.glossary': {
            'Meta': {'ordering': "['term']", 'object_name': 'Glossary'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['help']