# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voyage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voyageslavesnumbers',
            name='slave_deaths_between_arrival_and_sale',
            field=models.IntegerField(
                null=True,
                verbose_name=b'Slaves death before arrival and sale '
                             b'(SLADAMER)',
                blank=True),
        ),
        migrations.AlterField(
            model_name='voyageslavesnumbers',
            name='slave_deaths_between_africa_america',
            field=models.IntegerField(
                null=True,
                verbose_name=b'Slaves death between Africa and Americas '
                             b'(SLADVOY)',
                blank=True),
        ),
    ]
