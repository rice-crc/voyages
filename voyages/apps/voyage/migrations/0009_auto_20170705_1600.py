# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voyage', '0008_auto_20170310_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='voyage',
            name='is_intra_american',
            field=models.BooleanField(default=False,
                                      verbose_name=b'IntraAmerican Voyage'),
        ),
        migrations.AlterField(
            model_name='voyagedates',
            name='imp_length_leaving_africa_to_disembark',
            field=models.IntegerField(
                null=True,
                verbose_name=b'Voyage length from last slave embarkation '
                             b'to first disembarkation (days) (VOY2IMP)',
                blank=True),
        ),
    ]
