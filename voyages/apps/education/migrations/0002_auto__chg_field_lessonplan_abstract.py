# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'LessonPlan.abstract'
        db.alter_column('education_lessonplan', 'abstract', self.gf('django.db.models.fields.TextField')(max_length=2000))

    def backwards(self, orm):

        # Changing field 'LessonPlan.abstract'
        db.alter_column('education_lessonplan', 'abstract', self.gf('django.db.models.fields.CharField')(max_length=500))

    models = {
        'education.lessonplan': {
            'Meta': {'object_name': 'LessonPlan'},
            'abstract': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
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