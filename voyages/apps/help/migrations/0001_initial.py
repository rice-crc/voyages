# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField(max_length=300, verbose_name='Question')),
                ('answer', models.TextField(max_length=2000, verbose_name='Answer')),
                ('question_order', models.IntegerField()),
            ],
            options={
                'ordering': ['category', 'question_order'],
                'verbose_name': 'Frequently Asked Question (FAQ)',
                'verbose_name_plural': 'FAQs',
            },
        ),
        migrations.CreateModel(
            name='FaqCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=100, verbose_name='Category')),
                ('type_order', models.IntegerField(verbose_name=b'Category Order')),
            ],
            options={
                'ordering': ['type_order'],
                'verbose_name': 'FAQ category',
                'verbose_name_plural': 'FAQ categories',
            },
        ),
        migrations.CreateModel(
            name='Glossary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term', models.CharField(max_length=50, verbose_name='Term')),
                ('description', models.CharField(max_length=1000, verbose_name='Description')),
            ],
            options={
                'ordering': ['term'],
                'verbose_name': 'Glossary Item',
                'verbose_name_plural': 'Glossary Items',
            },
        ),
        migrations.AddField(
            model_name='faq',
            name='category',
            field=models.ForeignKey(to='help.FaqCategory'),
        ),
    ]
