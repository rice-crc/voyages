# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribute', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interimarticlesource',
            name='url',
            field=models.TextField(max_length=400, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='interimbooksource',
            name='url',
            field=models.TextField(max_length=400, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='interimothersource',
            name='url',
            field=models.TextField(max_length=400, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='interimprimarysource',
            name='url',
            field=models.TextField(max_length=400, null=True, blank=True),
        ),
    ]
