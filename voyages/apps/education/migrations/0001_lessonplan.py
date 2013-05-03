# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LessonPlan'
        db.create_table('education_lessonplan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('grade_level', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('course', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('key_words', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('abstract', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('education', ['LessonPlan'])

        # Adding model 'LessonStandard'
        db.create_table('education_lessonstandard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['education.LessonPlan'])),
        ))
        db.send_create_signal('education', ['LessonStandard'])


    def backwards(self, orm):
        # Deleting model 'LessonPlan'
        db.delete_table('education_lessonplan')

        # Deleting model 'LessonStandard'
        db.delete_table('education_lessonstandard')


    models = {
        'education.lessonplan': {
            'Meta': {'object_name': 'LessonPlan'},
            'abstract': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'course': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'grade_level': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_words': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'education.lessonstandard': {
            'Meta': {'object_name': 'LessonStandard'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['education.LessonPlan']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['education']