# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribute', '0018_auto_20170131_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interimvoyage',
            name='date_departure',
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile(b'^(\\d{1,2}|),(\\d{1,2}|),(\\d{4}|)$'),
                        message=b'Please type a date in the format MM,DD,YYYY '
                        b'(individual entries may be blank)',
                        code=b'invalid')
                ]),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='date_first_slave_disembarkation',
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile(b'^(\\d{1,2}|),(\\d{1,2}|),(\\d{4}|)$'),
                        message=b'Please type a date in the format MM,DD,YYYY '
                        b'(individual entries may be blank)',
                        code=b'invalid')
                ]),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='date_return_departure',
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile(b'^(\\d{1,2}|),(\\d{1,2}|),(\\d{4}|)$'),
                        message=b'Please type a date in the format MM,DD,YYYY '
                        b'(individual entries may be blank)',
                        code=b'invalid')
                ]),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='date_second_slave_disembarkation',
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile(b'^(\\d{1,2}|),(\\d{1,2}|),(\\d{4}|)$'),
                        message=b'Please type a date in the format MM,DD,YYYY '
                        b'(individual entries may be blank)',
                        code=b'invalid')
                ]),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='date_slave_purchase_began',
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile(b'^(\\d{1,2}|),(\\d{1,2}|),(\\d{4}|)$'),
                        message=b'Please type a date in the format MM,DD,YYYY '
                        b'(individual entries may be blank)',
                        code=b'invalid')
                ]),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='date_third_slave_disembarkation',
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile(b'^(\\d{1,2}|),(\\d{1,2}|),(\\d{4}|)$'),
                        message=b'Please type a date in the format MM,DD,YYYY '
                        b'(individual entries may be blank)',
                        code=b'invalid')
                ]),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='date_vessel_left_last_slaving_port',
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile(b'^(\\d{1,2}|),(\\d{1,2}|),(\\d{4}|)$'),
                        message=b'Please type a date in the format MM,DD,YYYY '
                        b'(individual entries may be blank)',
                        code=b'invalid')
                ]),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='date_voyage_completed',
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile(b'^(\\d{1,2}|),(\\d{1,2}|),(\\d{4}|)$'),
                        message=b'Please type a date in the format MM,DD,YYYY '
                        b'(individual entries may be blank)',
                        code=b'invalid')
                ]),
        ),
    ]
