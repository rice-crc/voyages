# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contribute', '0004_auto_20160309_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='deletevoyagecontribution',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 11, 18, 57, 50, 791734, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='editvoyagecontribution',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 11, 18, 57, 56, 267083, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mergevoyagescontribution',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 11, 18, 58, 10, 926648, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newvoyagecontribution',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 11, 18, 58, 16, 743608, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
