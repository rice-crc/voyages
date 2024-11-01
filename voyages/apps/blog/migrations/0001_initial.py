# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2022-05-04 22:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import filebrowser.fields

from django.utils.text import slugify


def initialize_tags (apps, scheme_editor):
    tags = ["Author Profile","Institution Profile","News","Front Page"]
    Tag = apps.get_model("blog","Tag")

    for tag in tags:
        obj = Tag(name=tag,slug=slugify(tag))
        obj.save()


def add_generic_author (apps, scheme_editor):


    institutionName = "Voyages Team"
    Institution = apps.get_model("blog","Institution")

    institution = Institution(name=institutionName,slug=slugify(institutionName))
    institution.save()


    authorName = "Voyages Team"
    Author = apps.get_model("blog","Author")
        
    author = Author(name=authorName,slug=slugify(authorName),institution=institution, role="Team Member")
    author.save()

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.CharField(blank=True, max_length=600, null=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('role', models.CharField(max_length=200)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.CharField(blank=True, max_length=600, null=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('language', models.CharField(choices=[('en', 'English'), ('es', 'Spanish'), ('pt', 'Portuguese')], default='en', max_length=2, null=True)),
                ('subtitle', models.CharField(blank=True, max_length=200, null=True)),
                ('slug', models.SlugField(max_length=200)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.IntegerField(choices=[(0, 'Draft'), (1, 'Publish')], default=0)),
                ('thumbnail', filebrowser.fields.FileBrowseField(blank=True, max_length=300, verbose_name='Thumbnail')),                
                ('authors', models.ManyToManyField(to='blog.Author')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag'),
        ),
        migrations.AddField(
            model_name='author',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Institution'),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('slug', 'language')]),
        ),
        migrations.RunPython(initialize_tags),
        migrations.RunPython(add_generic_author),
    ]
