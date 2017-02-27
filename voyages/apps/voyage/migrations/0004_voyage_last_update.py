# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voyage', '0003_auto_20161023_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='voyage',
            name='last_update',
            field=models.DateTimeField(default='2016-11-27', auto_now=True),
            preserve_default=False,
        ),
    ]
