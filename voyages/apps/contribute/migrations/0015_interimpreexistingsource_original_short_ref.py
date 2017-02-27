# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribute', '0014_interimvoyage_persisted_form_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='interimpreexistingsource',
            name='original_short_ref',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
