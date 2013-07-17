# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LessonPlanFile'
        db.create_table(u'education_lessonplanfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('filetitle', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['education.LessonPlan'])),
        ))
        db.send_create_signal(u'education', ['LessonPlanFile'])

        # Adding model 'LessonPlan'
        db.create_table(u'education_lessonplan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('grade_level', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('course', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('key_words', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('abstract', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'education', ['LessonPlan'])

        # Adding model 'LessonStandard'
        db.create_table(u'education_lessonstandard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['education.LessonStandardType'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['education.LessonPlan'])),
        ))
        db.send_create_signal(u'education', ['LessonStandard'])

        # Adding model 'LessonStandardType'
        db.create_table(u'education_lessonstandardtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'education', ['LessonStandardType'])


    def backwards(self, orm):
        # Deleting model 'LessonPlanFile'
        db.delete_table(u'education_lessonplanfile')

        # Deleting model 'LessonPlan'
        db.delete_table(u'education_lessonplan')

        # Deleting model 'LessonStandard'
        db.delete_table(u'education_lessonstandard')

        # Deleting model 'LessonStandardType'
        db.delete_table(u'education_lessonstandardtype')


    models = {
        u'education.lessonplan': {
            'Meta': {'ordering': "['order']", 'object_name': 'LessonPlan'},
            'abstract': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'course': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'grade_level': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_words': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'education.lessonplanfile': {
            'Meta': {'object_name': 'LessonPlanFile'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filetitle': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['education.LessonPlan']"})
        },
        u'education.lessonstandard': {
            'Meta': {'object_name': 'LessonStandard'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['education.LessonPlan']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['education.LessonStandardType']"})
        },
        u'education.lessonstandardtype': {
            'Meta': {'object_name': 'LessonStandardType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['education']