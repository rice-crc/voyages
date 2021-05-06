# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voyage', '0002_auto_20151210_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voyagesources',
            name='short_ref',
            field=models.CharField(max_length=255,
                                   unique=True,
                                   null=True,
                                   verbose_name='Short reference',
                                   blank=True),
        ),
    ]
