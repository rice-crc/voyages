# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2022-07-19 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voyage', '0018_auto_20220618_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='africaninfo',
            name='possibly_offensive',
            field=models.BooleanField(default=False, help_text='Indicates that the wording used in this label might be offensive to readers'),
        ),
    ]
