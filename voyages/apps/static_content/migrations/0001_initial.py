# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ContentGroup',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Static content group',
                'verbose_name_plural': 'Static content groups',
            },
        ),
        migrations.CreateModel(
            name='ContentPage',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('title', models.TextField(max_length=50)),
                ('description', models.TextField(max_length=2000)),
                ('order', models.IntegerField()),
                ('group', models.ForeignKey(to='static_content.ContentGroup',
                                            on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Static content page',
                'verbose_name_plural': 'Static content pages',
            },
        ),
    ]
