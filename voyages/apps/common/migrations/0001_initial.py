# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='SavedQuery',
            fields=[
                ('id',
                 models.CharField(max_length=8,
                                  serialize=False,
                                  primary_key=True)),
                ('hash',
                 models.CharField(default=b'', max_length=255, db_index=True)),
                ('query', models.TextField()),
            ],
        ),
    ]
