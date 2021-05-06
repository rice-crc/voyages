# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voyage', '0002_auto_20151210_0937'),
        ('contribute', '0011_auto_20160906_1232'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterimPrivateNoteOrCollectionSource',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('information',
                 models.TextField(max_length=1000, null=True, blank=True)),
                ('url', models.TextField(max_length=400, null=True,
                                         blank=True)),
                ('source_ref_text',
                 models.CharField(max_length=255, null=True, blank=True)),
                ('authors',
                 models.TextField(max_length=1000, null=True, blank=True)),
                ('title', models.CharField(max_length=255,
                                           null=True,
                                           blank=True)),
                ('location',
                 models.CharField(max_length=255, null=True, blank=True)),
                ('year', models.IntegerField(null=True)),
                ('page', models.CharField(max_length=20, null=True,
                                          blank=True)),
                ('created_voyage_sources',
                 models.ForeignKey(related_name='+',
                                   to='voyage.VoyageSources',
                                   null=True,
                                   on_delete=models.CASCADE)),
                ('interim_voyage',
                 models.ForeignKey(
                     related_name='private_note_or_collection_sources',
                     to='contribute.InterimVoyage',
                     on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InterimUnpublishedSecondarySource',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('information',
                 models.TextField(max_length=1000, null=True, blank=True)),
                ('url', models.TextField(max_length=400, null=True,
                                         blank=True)),
                ('source_ref_text',
                 models.CharField(max_length=255, null=True, blank=True)),
                ('authors',
                 models.TextField(max_length=1000, null=True, blank=True)),
                ('title', models.CharField(max_length=255,
                                           null=True,
                                           blank=True)),
                ('location',
                 models.CharField(max_length=255, null=True, blank=True)),
                ('year', models.IntegerField(null=True)),
                ('page', models.CharField(max_length=20, null=True,
                                          blank=True)),
                ('created_voyage_sources',
                 models.ForeignKey(related_name='+',
                                   to='voyage.VoyageSources',
                                   null=True,
                                   on_delete=models.CASCADE)),
                ('interim_voyage',
                 models.ForeignKey(
                     related_name='unpublished_secondary_sources',
                     to='contribute.InterimVoyage',
                     on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='interimothersource',
            name='created_voyage_sources',
        ),
        migrations.RemoveField(
            model_name='interimothersource',
            name='interim_voyage',
        ),
        migrations.DeleteModel(name='InterimOtherSource',),
    ]
