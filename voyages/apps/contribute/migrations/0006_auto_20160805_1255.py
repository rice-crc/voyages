# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribute', '0005_auto_20160326_0850'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewrequest',
            name='decision_message',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='interimvoyage',
            name='imputed_standardized_tonnage',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
