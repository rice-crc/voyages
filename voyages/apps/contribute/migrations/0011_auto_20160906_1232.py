# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voyage', '0002_auto_20151210_0937'),
        ('contribute', '0010_auto_20160901_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterimNewspaperSource',
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
                ('name', models.CharField(max_length=255, null=True,
                                          blank=True)),
                ('alternative_name',
                 models.CharField(max_length=255, null=True, blank=True)),
                ('city', models.CharField(max_length=255, null=True,
                                          blank=True)),
                ('country',
                 models.CharField(max_length=60, null=True, blank=True)),
                ('created_voyage_sources',
                 models.ForeignKey(related_name='+',
                                   to='voyage.VoyageSources',
                                   null=True,
                                   on_delete=models.CASCADE)),
                ('interim_voyage',
                 models.ForeignKey(related_name='newspaper_sources',
                                   to='contribute.InterimVoyage',
                                   on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='interimarticlesource',
            name='source_ref_text',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='interimbooksource',
            name='editors',
            field=models.TextField(max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='interimbooksource',
            name='essay_title',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='interimbooksource',
            name='source_is_essay_in_book',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='interimbooksource',
            name='source_ref_text',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='interimothersource',
            name='source_ref_text',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='interimothersource',
            name='year',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='interimprimarysource',
            name='source_ref_text',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
