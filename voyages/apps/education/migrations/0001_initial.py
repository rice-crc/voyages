# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LessonPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=100, verbose_name='Title')),
                ('author', models.CharField(max_length=50, verbose_name='Author')),
                ('grade_level', models.CharField(max_length=50, verbose_name='Grade Level')),
                ('course', models.CharField(max_length=50, verbose_name='Course')),
                ('key_words', models.CharField(max_length=200, verbose_name='Key Words')),
                ('abstract', models.TextField(max_length=1000, verbose_name='Abstract')),
                ('order', models.IntegerField()),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='LessonPlanFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'lessonplan')),
                ('filetitle', models.CharField(max_length=50, verbose_name=b'File name')),
                ('lesson', models.ForeignKey(to='education.LessonPlan')),
            ],
        ),
        migrations.CreateModel(
            name='LessonStandard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=100, verbose_name='Text')),
                ('lesson', models.ForeignKey(to='education.LessonPlan')),
            ],
        ),
        migrations.CreateModel(
            name='LessonStandardType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, verbose_name='Standard Type')),
            ],
        ),
        migrations.AddField(
            model_name='lessonstandard',
            name='type',
            field=models.ForeignKey(to='education.LessonStandardType'),
        ),
    ]
