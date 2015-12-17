# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribute', '0003_auto_20151216_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interimvoyage',
            name='african_resistance',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Resistance', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='first_place_of_landing',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='first_place_of_slave_purchase',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='first_port_intended_disembarkation',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='first_port_intended_embarkation',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='guns_mounted',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='length_of_middle_passage',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='national_carrier',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Nationality', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='number_of_new_world_ports_called_prior_to_disembarkation',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='number_of_ports_called_prior_to_slave_purchase',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='place_of_call_before_atlantic_crossing',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='port_of_departure',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='port_voyage_ended',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='principal_place_of_slave_disembarkation',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='principal_place_of_slave_purchase',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='rig_of_vessel',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.RigOfVessel', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='second_place_of_landing',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='second_place_of_slave_purchase',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='second_port_intended_disembarkation',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='second_port_intended_embarkation',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='ship_construction_place',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='ship_registration_place',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='third_place_of_landing',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='third_place_of_slave_purchase',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.Place', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='ton_type',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.TonType', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='tonnage_of_vessel',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='voyage_outcome',
            field=models.ForeignKey(related_name='+', blank=True, to='voyage.ParticularOutcome', null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='year_ship_constructed',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='year_ship_registered',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
