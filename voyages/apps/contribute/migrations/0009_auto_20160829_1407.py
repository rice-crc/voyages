# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribute', '0008_auto_20160808_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interimslavenumber',
            name='number',
            field=models.FloatField(verbose_name=b'Number'),
        ),
    ]
