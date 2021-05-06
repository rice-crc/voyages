# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribute', '0012_auto_20160914_1030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editorvoyagecontribution',
            name='final_decision',
        ),
        migrations.RemoveField(
            model_name='editorvoyagecontribution',
            name='published',
        ),
        migrations.AddField(
            model_name='reviewrequest',
            name='created_voyage_id',
            field=models.IntegerField(
                help_text=b'The voyage id that should be used for the newly '
                b'created voyage (in case of new or merged contributions)',
                null=True),
        ),
    ]
