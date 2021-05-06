# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribute', '0017_auto_20170112_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='editorvoyagecontribution',
            name='ran_impute',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='deletevoyagecontribution',
            name='deleted_voyages_ids',
            field=models.CharField(
                help_text=b'The voyage_id of each Voyage being deleted by '
                b'this contribution',
                max_length=255,
                verbose_name=b'Deleted voyage ids',
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile('^[\\d,]+\\Z'),
                        'Enter only digits separated by commas.', 'invalid')
                ]),
        ),
        migrations.AlterField(
            model_name='interimpreexistingsource',
            name='voyage_ids',
            field=models.CharField(
                max_length=255,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile('^[\\d,]+\\Z'),
                        'Enter only digits separated by commas.', 'invalid')
                ]),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='date_departure',
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile('^[\\d,]+\\Z'),
                        'Enter only digits separated by commas.', 'invalid')
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
                        re.compile('^[\\d,]+\\Z'),
                        'Enter only digits separated by commas.', 'invalid')
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
                        re.compile('^[\\d,]+\\Z'),
                        'Enter only digits separated by commas.', 'invalid')
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
                        re.compile('^[\\d,]+\\Z'),
                        'Enter only digits separated by commas.', 'invalid')
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
                        re.compile('^[\\d,]+\\Z'),
                        'Enter only digits separated by commas.', 'invalid')
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
                        re.compile('^[\\d,]+\\Z'),
                        'Enter only digits separated by commas.', 'invalid')
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
                        re.compile('^[\\d,]+\\Z'),
                        'Enter only digits separated by commas.', 'invalid')
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
                        re.compile('^[\\d,]+\\Z'),
                        'Enter only digits separated by commas.', 'invalid')
                ]),
        ),
        migrations.AlterField(
            model_name='mergevoyagescontribution',
            name='merged_voyages_ids',
            field=models.CharField(
                help_text=b'The voyage_id of each Voyage being merged by this '
                b'contribution',
                max_length=255,
                verbose_name=b'Merged voyage ids',
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile('^[\\d,]+\\Z'),
                        'Enter only digits separated by commas.', 'invalid')
                ]),
        ),
    ]
