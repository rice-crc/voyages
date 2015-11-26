# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminFaq',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField(max_length=1000)),
                ('answer', models.TextField(max_length=1000)),
            ],
            options={
                'ordering': ['question'],
                'db_table': 'contribute_adminfaq',
                'verbose_name': 'Frequently Asked Question For Admins',
                'verbose_name_plural': 'Frequently Asked Question For Admins',
            },
        ),
    ]
