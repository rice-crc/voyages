# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voyage', '0007_auto_20170302_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broadregion',
            name='value',
            field=models.IntegerField(unique=True,
                                      verbose_name=b'Numeric code'),
        ),
        migrations.AlterField(
            model_name='region',
            name='value',
            field=models.IntegerField(unique=True,
                                      verbose_name=b'Numeric code'),
        ),
    ]
