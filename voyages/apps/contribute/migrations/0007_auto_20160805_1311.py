# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contribute', '0006_auto_20160805_1255'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewvoyagecontribution',
            old_name='review_interim_voyage',
            new_name='interim_voyage',
        ),
    ]
