# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('year', models.IntegerField()),
                ('embarked_slaves', models.FloatField(null=True, blank=True)),
                ('disembarked_slaves', models.FloatField(null=True,
                                                         blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExportArea',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('name',
                 models.CharField(max_length=200,
                                  verbose_name=b'Export area name')),
                ('order_num', models.IntegerField()),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('show_at_zoom', models.IntegerField()),
                ('show_on_map', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='ExportRegion',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('name',
                 models.CharField(max_length=200,
                                  verbose_name=b'Export region name')),
                ('order_num', models.IntegerField()),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('show_at_zoom', models.IntegerField()),
                ('show_on_map', models.BooleanField()),
                ('export_area', models.ForeignKey(to='assessment.ExportArea',
                                                  on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='ImportArea',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('name',
                 models.CharField(max_length=200,
                                  verbose_name=b'Import area name')),
                ('order_num', models.IntegerField()),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('show_at_zoom', models.IntegerField()),
                ('show_on_map', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='ImportRegion',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('name',
                 models.CharField(max_length=200,
                                  verbose_name=b'Import region name')),
                ('order_num', models.IntegerField()),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('show_at_zoom', models.IntegerField()),
                ('show_on_map', models.BooleanField()),
                ('import_area', models.ForeignKey(to='assessment.ImportArea',
                                                  on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Nation',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('name', models.CharField(max_length=200, null=True,
                                          blank=True)),
                ('order_num', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='estimate',
            name='disembarkation_region',
            field=models.ForeignKey(blank=True,
                                    to='assessment.ImportRegion',
                                    null=True,
                                    on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='estimate',
            name='embarkation_region',
            field=models.ForeignKey(blank=True,
                                    to='assessment.ExportRegion',
                                    null=True,
                                    on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='estimate',
            name='nation',
            field=models.ForeignKey(to='assessment.Nation',
                                    on_delete=models.CASCADE),
        ),
    ]
