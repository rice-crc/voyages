# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('voyage', '0002_auto_20151210_0937'),
        ('contribute', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContributionNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=255, verbose_name=b'Tag given to the note/comment')),
                ('note', models.TextField(max_length=1024, verbose_name=b'The note/comment')),
            ],
        ),
        migrations.CreateModel(
            name='DeleteVoyageContribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(help_text=b'Indicates whether the contribution is still being edited, committed, discarded etc', verbose_name=b'Status')),
                ('deleted_voyages_ids', models.CommaSeparatedIntegerField(help_text=b'The voyage_id of each Voyage being deleted by this contribution', max_length=255, verbose_name=b'Deleted voyage ids')),
                ('contributor', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('notes', models.ManyToManyField(help_text=b'Notes for the contribution', related_name='_deletevoyagecontribution_notes_+', to='contribute.ContributionNote')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EditVoyageContribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(help_text=b'Indicates whether the contribution is still being edited, committed, discarded etc', verbose_name=b'Status')),
                ('edited_voyage_id', models.IntegerField(help_text=b'The voyage_id of the Voyage edited by this contribution', verbose_name=b'Edited voyage id')),
                ('contributor', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InterimArticleSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('authors', models.TextField(max_length=1000, null=True, blank=True)),
                ('article_title', models.CharField(max_length=255, null=True, blank=True)),
                ('journal', models.CharField(max_length=255, null=True, blank=True)),
                ('volume_number', models.CharField(max_length=20, null=True, blank=True)),
                ('year', models.IntegerField(null=True)),
                ('page_start', models.IntegerField(null=True)),
                ('page_end', models.IntegerField(null=True)),
                ('information', models.TextField(max_length=1000, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='InterimBookSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('authors', models.TextField(max_length=1000, null=True, blank=True)),
                ('book_title', models.CharField(max_length=255, null=True, blank=True)),
                ('publisher', models.CharField(max_length=255, null=True, blank=True)),
                ('place_of_publication', models.CharField(max_length=20, null=True, blank=True)),
                ('year', models.IntegerField(null=True)),
                ('page_start', models.IntegerField(null=True)),
                ('page_end', models.IntegerField(null=True)),
                ('information', models.TextField(max_length=1000, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='InterimOtherSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('location', models.CharField(max_length=255, null=True, blank=True)),
                ('page', models.CharField(max_length=20, null=True, blank=True)),
                ('information', models.TextField(max_length=1000, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='InterimPrimarySource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_of_library_or_archive', models.CharField(max_length=255, null=True, blank=True)),
                ('location_of_library_or_archive', models.CharField(max_length=255, null=True, blank=True)),
                ('series_or_collection', models.CharField(max_length=255, null=True, blank=True)),
                ('volume_or_box_or_bundle', models.CharField(max_length=255, null=True, blank=True)),
                ('document_detail', models.CharField(max_length=255, null=True, blank=True)),
                ('information', models.TextField(max_length=1000, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='InterimSlaveNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('var_name', models.CharField(max_length=20, verbose_name=b'Slave number code-book variable name')),
                ('number', models.IntegerField(verbose_name=b'Number')),
            ],
        ),
        migrations.CreateModel(
            name='InterimVoyage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_of_vessel', models.CharField(max_length=255, null=True, blank=True)),
                ('year_ship_constructed', models.IntegerField(null=True)),
                ('year_ship_registered', models.IntegerField(null=True)),
                ('tonnage_of_vessel', models.IntegerField(null=True)),
                ('guns_mounted', models.IntegerField(null=True)),
                ('first_ship_owner', models.CharField(max_length=255, null=True, blank=True)),
                ('second_ship_owner', models.CharField(max_length=255, null=True, blank=True)),
                ('additional_ship_owners', models.TextField(max_length=1000, null=True, blank=True)),
                ('number_of_ports_called_prior_to_slave_purchase', models.IntegerField(null=True)),
                ('number_of_new_world_ports_called_prior_to_disembarkation', models.IntegerField(null=True)),
                ('date_departure', models.CommaSeparatedIntegerField(max_length=10, null=True, blank=True)),
                ('date_slave_purchase_began', models.CommaSeparatedIntegerField(max_length=10, null=True, blank=True)),
                ('date_vessel_left_last_slaving_port', models.CommaSeparatedIntegerField(max_length=10, null=True, blank=True)),
                ('date_first_slave_disembarkation', models.CommaSeparatedIntegerField(max_length=10, null=True, blank=True)),
                ('date_second_slave_disembarkation', models.CommaSeparatedIntegerField(max_length=10, null=True, blank=True)),
                ('date_third_slave_disembarkation', models.CommaSeparatedIntegerField(max_length=10, null=True, blank=True)),
                ('date_return_departure', models.CommaSeparatedIntegerField(max_length=10, null=True, blank=True)),
                ('date_voyage_completed', models.CommaSeparatedIntegerField(max_length=10, null=True, blank=True)),
                ('length_of_middle_passage', models.IntegerField(null=True)),
                ('first_captain', models.CharField(max_length=255, null=True, blank=True)),
                ('second_captain', models.CharField(max_length=255, null=True, blank=True)),
                ('third_captain', models.CharField(max_length=255, null=True, blank=True)),
                ('african_resistance', models.ForeignKey(related_name='+', to='voyage.Resistance', null=True)),
                ('first_place_of_landing', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('first_place_of_slave_purchase', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('first_port_intended_disembarkation', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('first_port_intended_embarkation', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('national_carrier', models.ForeignKey(related_name='+', to='voyage.Nationality', null=True)),
                ('place_of_call_before_atlantic_crossing', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('port_of_departure', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('port_voyage_ended', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('principal_place_of_slave_disembarkation', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('principal_place_of_slave_purchase', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('rig_of_vessel', models.ForeignKey(related_name='+', to='voyage.RigOfVessel', null=True)),
                ('second_place_of_landing', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('second_place_of_slave_purchase', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('second_port_intended_disembarkation', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('second_port_intended_embarkation', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('ship_construction_place', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('ship_registration_place', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('third_place_of_landing', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('third_place_of_slave_purchase', models.ForeignKey(related_name='+', to='voyage.Place', null=True)),
                ('ton_type', models.ForeignKey(related_name='+', to='voyage.TonType', null=True)),
                ('voyage_outcome', models.ForeignKey(related_name='+', to='voyage.ParticularOutcome', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MergeVoyagesContribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(help_text=b'Indicates whether the contribution is still being edited, committed, discarded etc', verbose_name=b'Status')),
                ('merged_voyages_ids', models.CommaSeparatedIntegerField(help_text=b'The voyage_id of each Voyage being merged by this contribution', max_length=255, verbose_name=b'Merged voyage ids')),
                ('contributor', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('interim_voyage', models.ForeignKey(related_name='+', to='contribute.InterimVoyage')),
                ('notes', models.ManyToManyField(help_text=b'Notes for the contribution', related_name='_mergevoyagescontribution_notes_+', to='contribute.ContributionNote')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NewVoyageContribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(help_text=b'Indicates whether the contribution is still being edited, committed, discarded etc', verbose_name=b'Status')),
                ('contributor', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('interim_voyage', models.ForeignKey(related_name='+', to='contribute.InterimVoyage')),
                ('notes', models.ManyToManyField(help_text=b'Notes for the contribution', related_name='_newvoyagecontribution_notes_+', to='contribute.ContributionNote')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='institution',
            field=models.CharField(max_length=255),
        ),
        migrations.AddField(
            model_name='interimslavenumber',
            name='interim_voyage',
            field=models.ForeignKey(related_name='slave_numbers', to='contribute.InterimVoyage'),
        ),
        migrations.AddField(
            model_name='interimprimarysource',
            name='interim_voyage',
            field=models.ForeignKey(related_name='primary_sources', to='contribute.InterimVoyage'),
        ),
        migrations.AddField(
            model_name='interimothersource',
            name='interim_voyage',
            field=models.ForeignKey(related_name='other_sources', to='contribute.InterimVoyage'),
        ),
        migrations.AddField(
            model_name='interimbooksource',
            name='interim_voyage',
            field=models.ForeignKey(related_name='book_sources', to='contribute.InterimVoyage'),
        ),
        migrations.AddField(
            model_name='interimarticlesource',
            name='interim_voyage',
            field=models.ForeignKey(related_name='article_sources', to='contribute.InterimVoyage'),
        ),
        migrations.AddField(
            model_name='editvoyagecontribution',
            name='interim_voyage',
            field=models.ForeignKey(related_name='+', to='contribute.InterimVoyage'),
        ),
        migrations.AddField(
            model_name='editvoyagecontribution',
            name='notes',
            field=models.ManyToManyField(help_text=b'Notes for the contribution', related_name='_editvoyagecontribution_notes_+', to='contribute.ContributionNote'),
        ),
    ]
