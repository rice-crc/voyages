# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='BroadRegion',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('broad_region',
                 models.CharField(max_length=255,
                                  verbose_name=b'Broad region (Area) name')),
                ('longitude',
                 models.DecimalField(null=True,
                                     verbose_name=b'Longitude of point',
                                     max_digits=10,
                                     decimal_places=7,
                                     blank=True)),
                ('latitude',
                 models.DecimalField(null=True,
                                     verbose_name=b'Latitude of point',
                                     max_digits=10,
                                     decimal_places=7,
                                     blank=True)),
                ('value', models.IntegerField(verbose_name=b'Numeric code')),
                ('show_on_map', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['value'],
                'verbose_name': 'Broad region (area)',
                'verbose_name_plural': 'Broad regions (areas)',
            },
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('value', models.IntegerField()),
            ],
            options={
                'ordering': ['value'],
                'verbose_name': 'Nationality',
                'verbose_name_plural': 'Nationalities',
            },
        ),
        migrations.CreateModel(
            name='OwnerOutcome',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('label',
                 models.CharField(max_length=200,
                                  verbose_name=b'Outcome label')),
                ('value',
                 models.IntegerField(verbose_name=b'Code of outcome')),
            ],
            options={
                'ordering': ['value'],
            },
        ),
        migrations.CreateModel(
            name='ParticularOutcome',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('label',
                 models.CharField(max_length=200,
                                  verbose_name=b'Outcome label')),
                ('value',
                 models.IntegerField(verbose_name=b'Code of outcome')),
            ],
            options={
                'ordering': ['value'],
                'verbose_name': 'Fate (particular outcome of voyage)',
                'verbose_name_plural':
                'Fates (particular outcomes of voyages)',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('place', models.CharField(max_length=255)),
                ('value',
                 models.IntegerField(unique=True,
                                     verbose_name=b'Numeric code')),
                ('longitude',
                 models.DecimalField(null=True,
                                     verbose_name=b'Longitude of point',
                                     max_digits=10,
                                     decimal_places=7,
                                     blank=True)),
                ('latitude',
                 models.DecimalField(null=True,
                                     verbose_name=b'Latitude of point',
                                     max_digits=10,
                                     decimal_places=7,
                                     blank=True)),
                ('show_on_main_map', models.BooleanField(default=True)),
                ('show_on_voyage_map', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['value'],
                'verbose_name': 'Place (Port or Location)',
                'verbose_name_plural': 'Places (Ports or Locations)',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('region',
                 models.CharField(
                     max_length=255,
                     verbose_name=b'Specific region (country or colony)')),
                ('longitude',
                 models.DecimalField(null=True,
                                     verbose_name=b'Longitude of point',
                                     max_digits=10,
                                     decimal_places=7,
                                     blank=True)),
                ('latitude',
                 models.DecimalField(null=True,
                                     verbose_name=b'Latitude of point',
                                     max_digits=10,
                                     decimal_places=7,
                                     blank=True)),
                ('value', models.IntegerField(verbose_name=b'Numeric code')),
                ('show_on_map', models.BooleanField(default=True)),
                ('show_on_main_map', models.BooleanField(default=True)),
                ('broad_region', models.ForeignKey(to='voyage.BroadRegion',
                                                   on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['value'],
            },
        ),
        migrations.CreateModel(
            name='Resistance',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('label',
                 models.CharField(max_length=255,
                                  verbose_name=b'Resistance label')),
                ('value',
                 models.IntegerField(verbose_name=b'Code of resistance')),
            ],
            options={
                'ordering': ['value'],
            },
        ),
        migrations.CreateModel(
            name='RigOfVessel',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('label', models.CharField(max_length=25)),
                ('value', models.IntegerField()),
            ],
            options={
                'ordering': ['value'],
                'verbose_name': 'Rig of vessel',
                'verbose_name_plural': 'Rigs of vessel',
            },
        ),
        migrations.CreateModel(
            name='SlavesOutcome',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('label',
                 models.CharField(max_length=200,
                                  verbose_name=b'Outcome label')),
                ('value',
                 models.IntegerField(verbose_name=b'Code of outcome')),
            ],
            options={
                'ordering': ['value'],
            },
        ),
        migrations.CreateModel(
            name='TonType',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('value', models.IntegerField()),
            ],
            options={
                'ordering': ['value'],
                'verbose_name': 'Type of tons',
                'verbose_name_plural': 'Types of tons',
            },
        ),
        migrations.CreateModel(
            name='VesselCapturedOutcome',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('label',
                 models.CharField(max_length=200,
                                  verbose_name=b'Outcome label')),
                ('value',
                 models.IntegerField(verbose_name=b'Code of outcome')),
            ],
            options={
                'ordering': ['value'],
            },
        ),
        migrations.CreateModel(
            name='Voyage',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('voyage_id',
                 models.IntegerField(unique=True, verbose_name=b'Voyage ID')),
                ('voyage_in_cd_rom',
                 models.BooleanField(default=False,
                                     max_length=1,
                                     verbose_name=b'Voyage in 1999 CD-ROM?')),
            ],
            options={
                'ordering': ['voyage_id'],
                'verbose_name': 'Voyage',
                'verbose_name_plural': 'Voyages',
            },
        ),
        migrations.CreateModel(
            name='VoyageCaptain',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('name',
                 models.CharField(max_length=255,
                                  verbose_name=b"Captain's name")),
            ],
        ),
        migrations.CreateModel(
            name='VoyageCaptainConnection',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('captain_order', models.IntegerField()),
                ('captain',
                 models.ForeignKey(related_name='captain_name',
                                   to='voyage.VoyageCaptain',
                                   on_delete=models.CASCADE)),
                ('voyage',
                 models.ForeignKey(related_name='voyage',
                                   to='voyage.Voyage',
                                   on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Voyage captain information',
                'verbose_name_plural': 'Voyage captain information',
            },
        ),
        migrations.CreateModel(
            name='VoyageCrew',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('crew_voyage_outset',
                 models.IntegerField(null=True,
                                     verbose_name=b'Crew at voyage outset',
                                     blank=True)),
                ('crew_departure_last_port',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Crew at departure from last port of slave '
                                  b'purchase',
                     blank=True)),
                ('crew_first_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Crew at first landing of slaves',
                     blank=True)),
                ('crew_return_begin',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Crew when return voyage begin',
                     blank=True)),
                ('crew_end_voyage',
                 models.IntegerField(null=True,
                                     verbose_name=b'Crew at end of voyage',
                                     blank=True)),
                ('unspecified_crew',
                 models.IntegerField(null=True,
                                     verbose_name=b'Number of crew '
                                                  b'unspecified',
                                     blank=True)),
                ('crew_died_before_first_trade',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Crew died before first place of trade in '
                                  b'Africa',
                     blank=True)),
                ('crew_died_while_ship_african',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Crew died while ship was on African coast',
                     blank=True)),
                ('crew_died_middle_passage',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Crew died during Middle Passage',
                     blank=True)),
                ('crew_died_in_americas',
                 models.IntegerField(null=True,
                                     verbose_name=b'Crew died in the Americas',
                                     blank=True)),
                ('crew_died_on_return_voyage',
                 models.IntegerField(null=True,
                                     verbose_name=b'Crew died on return '
                                                  b'voyage',
                                     blank=True)),
                ('crew_died_complete_voyage',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Crew died during complete voyage',
                     blank=True)),
                ('crew_deserted',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Total number of crew deserted',
                     blank=True)),
                ('voyage',
                 models.ForeignKey(related_name='voyage_name_crew',
                                   blank=True,
                                   to='voyage.Voyage',
                                   null=True,
                                   on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Crew',
                'verbose_name_plural': 'Crews',
            },
        ),
        migrations.CreateModel(
            name='VoyageDates',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('voyage_began',
                 models.CommaSeparatedIntegerField(
                     help_text=b'Date in format: MM,DD,YYYY',
                     max_length=10,
                     null=True,
                     verbose_name=b'Date that voyage began (DATEDEPB,A,C)',
                     blank=True)),
                ('slave_purchase_began',
                 models.CommaSeparatedIntegerField(
                     help_text=b'Date in format: MM,DD,YYYY',
                     max_length=10,
                     null=True,
                     verbose_name=b'Date that slave purchase began '
                                  b'(D1SLATRB,A,C)',
                     blank=True)),
                ('vessel_left_port',
                 models.CommaSeparatedIntegerField(
                     help_text=b'Date in format: MM,DD,YYYY',
                     max_length=10,
                     null=True,
                     verbose_name=b'Date that vessel left last slaving port '
                                  b'(DLSLATRB,A,C)',
                     blank=True)),
                ('first_dis_of_slaves',
                 models.CommaSeparatedIntegerField(
                     help_text=b'Date in format: MM,DD,YYYY',
                     max_length=10,
                     null=True,
                     verbose_name=b'Date of first disembarkation of slaves '
                                  b'(DATARR33,32,34)',
                     blank=True)),
                ('date_departed_africa',
                 models.CommaSeparatedIntegerField(
                     help_text=b'Date in format: MM,DD,YYYY',
                     max_length=10,
                     null=True,
                     verbose_name=b'Date vessel departed Africa (DATELEFTAFR)',
                     blank=True)),
                ('arrival_at_second_place_landing',
                 models.CommaSeparatedIntegerField(
                     help_text=b'Date in format: MM,DD,YYYY',
                     max_length=10,
                     null=True,
                     verbose_name=b'Date of arrival at second place of '
                                  b'landing (DATARR37,36,38)',
                     blank=True)),
                ('third_dis_of_slaves',
                 models.CommaSeparatedIntegerField(
                     help_text=b'Date in format: MM,DD,YYYY',
                     max_length=10,
                     null=True,
                     verbose_name=b'Date of third disembarkation of slaves '
                                  b'(DATARR40,39,41)',
                     blank=True)),
                ('departure_last_place_of_landing',
                 models.CommaSeparatedIntegerField(
                     help_text=b'Date in format: MM,DD,YYYY',
                     max_length=10,
                     null=True,
                     verbose_name=b'Date of departure from last place of '
                                  b'landing (DDEPAMB,*,C)',
                     blank=True)),
                ('voyage_completed',
                 models.CommaSeparatedIntegerField(
                     help_text=b'Date in format: MM,DD,YYYY',
                     max_length=10,
                     null=True,
                     verbose_name=b'Date on which slave voyage completed '
                                  b'(DATARR44,43,45)',
                     blank=True)),
                ('length_middle_passage_days',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Length of Middle Passage in (days) '
                                  b'(VOYAGE)',
                     blank=True)),
                ('imp_voyage_began',
                 models.CommaSeparatedIntegerField(
                     help_text=b'Date in format: MM,DD,YYYY',
                     max_length=10,
                     null=True,
                     verbose_name=b'Year voyage began',
                     blank=True)),
                ('imp_departed_africa',
                 models.CommaSeparatedIntegerField(
                     help_text=b'Date in format: MM,DD,YYYY',
                     max_length=10,
                     null=True,
                     verbose_name=b'Year departed Africa',
                     blank=True)),
                ('imp_arrival_at_port_of_dis',
                 models.CommaSeparatedIntegerField(
                     help_text=b'Date in format: MM,DD,YYYY',
                     max_length=10,
                     null=True,
                     verbose_name=b'Year of arrival at port of '
                                  b'disembarkation (YEARAM)',
                     blank=True)),
                ('imp_length_home_to_disembark',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Voyage length from home port to '
                                  b'disembarkation (days) (VOY1IMP)',
                     blank=True)),
                ('imp_length_leaving_africa_to_disembark',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Voyage length from leaving Africa to '
                                  b'disembarkation (days) (VOY2IMP)',
                     blank=True)),
                ('voyage',
                 models.ForeignKey(related_name='voyage_name_dates',
                                   blank=True,
                                   to='voyage.Voyage',
                                   null=True,
                                   on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Date',
                'verbose_name_plural': 'Dates',
            },
        ),
        migrations.CreateModel(
            name='VoyageGroupings',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('label', models.CharField(max_length=30)),
                ('value', models.IntegerField()),
            ],
            options={
                'verbose_name':
                    'Grouping for estimating imputed slaves',
                'verbose_name_plural':
                    'Groupings for estimating imputed slaves',
            },
        ),
        migrations.CreateModel(
            name='VoyageItinerary',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('ports_called_buying_slaves',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of ports of call prior to buying '
                                  b'slaves (NPPRETRA)',
                     blank=True)),
                ('number_of_ports_of_call',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of ports of call in Americas prior '
                                  b'to sale of slaves (NPPRIOR)',
                     blank=True)),
                ('broad_region_of_return',
                 models.ForeignKey(
                     related_name='broad_region_of_return',
                     verbose_name=b'Broad region of return (RETRNREG1)',
                     blank=True,
                     to='voyage.BroadRegion',
                     null=True,
                     on_delete=models.CASCADE)),
                ('first_landing_place',
                 models.ForeignKey(
                     related_name='first_landing_place',
                     verbose_name=b'First place of slave landing (SLA1PORT)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('first_landing_region',
                 models.ForeignKey(
                     related_name='first_landing_region',
                     verbose_name=b'First region of slave landing (REGDIS1)',
                     blank=True,
                     to='voyage.Region',
                     null=True,
                     on_delete=models.CASCADE)),
                ('first_place_slave_purchase',
                 models.ForeignKey(
                     related_name='first_place_slave_purchase',
                     verbose_name=b'First place of slave purchase (PLAC1TRA)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('first_region_slave_emb',
                 models.ForeignKey(
                     related_name='first_region_slave_emb',
                     verbose_name=b'First region of embarkation of slaves '
                                  b'(REGEM1)',
                     blank=True,
                     to='voyage.Region',
                     null=True,
                     on_delete=models.CASCADE)),
                ('imp_broad_region_of_slave_purchase',
                 models.ForeignKey(
                     related_name='imp_broad_region_of_slave_purchase',
                     verbose_name=b'Imputed principal broad region of slave '
                                  b'purchase (MAJBYIMP1)',
                     blank=True,
                     to='voyage.BroadRegion',
                     null=True,
                     on_delete=models.CASCADE)),
                ('imp_broad_region_slave_dis',
                 models.ForeignKey(
                     related_name='imp_broad_region_slave_dis',
                     verbose_name=b'Imputed broad region of slave '
                                  b'disembarkation (MJSELIMP1)',
                     blank=True,
                     to='voyage.BroadRegion',
                     null=True,
                     on_delete=models.CASCADE)),
                ('imp_broad_region_voyage_begin',
                 models.ForeignKey(
                     related_name='imp_broad_region_voyage_begin',
                     verbose_name=b'Imputed broad region where voyage began '
                                  b'(DEPTREGIMP1)',
                     blank=True,
                     to='voyage.BroadRegion',
                     null=True,
                     on_delete=models.CASCADE)),
                ('imp_port_voyage_begin',
                 models.ForeignKey(
                     related_name='imp_port_voyage_begin',
                     verbose_name=b'Imputed port where voyage began '
                                  b'(PTDEPIMP)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('imp_principal_place_of_slave_purchase',
                 models.ForeignKey(
                     related_name='imp_principal_place_of_slave_purchase',
                     verbose_name=b'Imputed principal place of slave purchase '
                                  b'(MJBYPTIMP)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('imp_principal_port_slave_dis',
                 models.ForeignKey(
                     related_name='imp_principal_port_slave_dis',
                     verbose_name=b'Imputed principal port of slave '
                                  b'disembarkation (MJSLPTIMP)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('imp_principal_region_of_slave_purchase',
                 models.ForeignKey(
                     related_name='imp_principal_region_of_slave_purchase',
                     verbose_name=b'Imputed principal region of slave '
                                  b'purchase (MAJBYIMP)',
                     blank=True,
                     to='voyage.Region',
                     null=True,
                     on_delete=models.CASCADE)),
                ('imp_principal_region_slave_dis',
                 models.ForeignKey(
                     related_name='imp_principal_region_slave_dis',
                     verbose_name=b'Imputed principal region of slave '
                                  b'disembarkation (MJSELIMP)',
                     blank=True,
                     to='voyage.Region',
                     null=True,
                     on_delete=models.CASCADE)),
                ('imp_region_voyage_begin',
                 models.ForeignKey(
                     related_name='imp_region_voyage_begin',
                     verbose_name=b'Imputed region where voyage began '
                                  b'(DEPTREGIMP)',
                     blank=True,
                     to='voyage.Region',
                     null=True,
                     on_delete=models.CASCADE)),
                ('int_first_port_dis',
                 models.ForeignKey(
                     related_name='int_first_port_dis',
                     verbose_name=b'First intended port of disembarkation '
                                  b'(ARRPORT)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('int_first_port_emb',
                 models.ForeignKey(
                     related_name='int_first_port_emb',
                     verbose_name=b'First intended port of embarkation '
                                  b'(EMBPORT)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('int_first_region_purchase_slaves',
                 models.ForeignKey(
                     related_name='int_first_region_purchase_slaves',
                     verbose_name=b'First intended region of purchase of '
                                  b'slaves (EMBREG)',
                     blank=True,
                     to='voyage.Region',
                     null=True,
                     on_delete=models.CASCADE)),
                ('int_first_region_slave_landing',
                 models.ForeignKey(
                     related_name='int_first_region_slave_landing',
                     verbose_name=b'First intended region of slave landing '
                                  b'(REGARR)',
                     blank=True,
                     to='voyage.Region',
                     null=True,
                     on_delete=models.CASCADE)),
                ('int_second_place_region_slave_landing',
                 models.ForeignKey(
                     related_name='int_second_region_slave_landing',
                     verbose_name=b'Second intended region of slave landing '
                                  b'(REGARR2)',
                     blank=True,
                     to='voyage.Region',
                     null=True,
                     on_delete=models.CASCADE)),
                ('int_second_port_dis',
                 models.ForeignKey(
                     related_name='int_second_port_dis',
                     verbose_name=b'Second intended port of disembarkation '
                                  b'(ARRPORT2)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('int_second_port_emb',
                 models.ForeignKey(
                     related_name='int_second_port_emb',
                     verbose_name=b'Second intended port of embarkation '
                                  b'(EMBPORT2)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('int_second_region_purchase_slaves',
                 models.ForeignKey(
                     related_name='int_second_region_purchase_slaves',
                     verbose_name=b'Second intended region of purchase of '
                                  b'slaves (EMBREG2)',
                     blank=True,
                     to='voyage.Region',
                     null=True,
                     on_delete=models.CASCADE)),
                ('place_voyage_ended',
                 models.ForeignKey(
                     related_name='place_voyage_ended',
                     verbose_name=b'Place at which voyage ended (PORTRET)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('port_of_call_before_atl_crossing',
                 models.ForeignKey(
                     related_name='port_of_call_before_atl_crossing',
                     verbose_name=b'Port of call before Atlantic crossing '
                                  b'(NPAFTTRA)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('port_of_departure',
                 models.ForeignKey(related_name='port_of_departure',
                                   verbose_name=b'Port of departure (PORTDEP)',
                                   blank=True,
                                   to='voyage.Place',
                                   null=True,
                                   on_delete=models.CASCADE)),
                ('principal_place_of_slave_purchase',
                 models.ForeignKey(
                     related_name='principal_place_of_slave_purchase',
                     verbose_name=b'Principal place of slave purchase '
                                  b'(MAJBUYPT)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('principal_port_of_slave_dis',
                 models.ForeignKey(
                     related_name='principal_port_of_slave_dis',
                     verbose_name=b'Principal port of slave disembarkation '
                                  b'(MAJSELPT)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('region_of_return',
                 models.ForeignKey(related_name='region_of_return',
                                   verbose_name=b'Region of return (RETRNREG)',
                                   blank=True,
                                   to='voyage.Region',
                                   null=True,
                                   on_delete=models.CASCADE)),
                ('second_landing_place',
                 models.ForeignKey(
                     related_name='second_landing_place',
                     verbose_name=b'Second place of slave landing (ADPSALE1)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('second_landing_region',
                 models.ForeignKey(
                     related_name='second_landing_region',
                     verbose_name=b'Second region of slave landing (REGDIS2)',
                     blank=True,
                     to='voyage.Region',
                     null=True,
                     on_delete=models.CASCADE)),
                ('second_place_slave_purchase',
                 models.ForeignKey(
                     related_name='second_place_slave_purchase',
                     verbose_name=b'Second place of slave purchase (PLAC2TRA)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('second_region_slave_emb',
                 models.ForeignKey(
                     related_name='second_region_slave_emb',
                     verbose_name=b'Second region of embarkation of '
                                  b'slaves (REGEM2)',
                     blank=True,
                     to='voyage.Region',
                     null=True,
                     on_delete=models.CASCADE)),
                ('third_landing_place',
                 models.ForeignKey(
                     related_name='third_landing_place',
                     verbose_name=b'Third place of slave landing (ADPSALE2)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('third_landing_region',
                 models.ForeignKey(
                     related_name='third_landing_region',
                     verbose_name=b'Third region of slave landing (REGDIS3)',
                     blank=True,
                     to='voyage.Region',
                     null=True,
                     on_delete=models.CASCADE)),
                ('third_place_slave_purchase',
                 models.ForeignKey(
                     related_name='third_place_slave_purchase',
                     verbose_name=b'Third place of slave purchase (PLAC3TRA)',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('third_region_slave_emb',
                 models.ForeignKey(
                     related_name='third_region_slave_emb',
                     verbose_name=b'Third region of embarkation '
                                  b'of slaves (REGEM3)',
                     blank=True,
                     to='voyage.Region',
                     null=True,
                     on_delete=models.CASCADE)),
                ('voyage',
                 models.ForeignKey(related_name='voyage_name_itinerary',
                                   blank=True,
                                   to='voyage.Voyage',
                                   null=True,
                                   on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Itinerary',
                'verbose_name_plural': 'Itineraries',
            },
        ),
        migrations.CreateModel(
            name='VoyageOutcome',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('outcome_owner',
                 models.ForeignKey(verbose_name=b'Owner Outcome',
                                   blank=True,
                                   to='voyage.OwnerOutcome',
                                   null=True,
                                   on_delete=models.CASCADE)),
                ('outcome_slaves',
                 models.ForeignKey(verbose_name=b'Slaves Outcome',
                                   blank=True,
                                   to='voyage.SlavesOutcome',
                                   null=True,
                                   on_delete=models.CASCADE)),
                ('particular_outcome',
                 models.ForeignKey(verbose_name=b'Particular Outcome',
                                   blank=True,
                                   to='voyage.ParticularOutcome',
                                   null=True,
                                   on_delete=models.CASCADE)),
                ('resistance',
                 models.ForeignKey(verbose_name=b'Resistance',
                                   blank=True,
                                   to='voyage.Resistance',
                                   null=True,
                                   on_delete=models.CASCADE)),
                ('vessel_captured_outcome',
                 models.ForeignKey(verbose_name=b'Vessel Captured Outcome',
                                   blank=True,
                                   to='voyage.VesselCapturedOutcome',
                                   null=True,
                                   on_delete=models.CASCADE)),
                ('voyage',
                 models.ForeignKey(related_name='voyage_name_outcome',
                                   blank=True,
                                   to='voyage.Voyage',
                                   null=True,
                                   on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Outcome',
                'verbose_name_plural': 'Outcomes',
            },
        ),
        migrations.CreateModel(
            name='VoyageShip',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('ship_name',
                 models.CharField(max_length=255,
                                  null=True,
                                  verbose_name=b'Name of vessel',
                                  blank=True)),
                ('tonnage',
                 models.IntegerField(null=True,
                                     verbose_name=b'Tonnage of vessel',
                                     blank=True)),
                ('guns_mounted',
                 models.IntegerField(null=True,
                                     verbose_name=b'Guns mounted',
                                     blank=True)),
                ('year_of_construction',
                 models.IntegerField(
                     null=True,
                     verbose_name=b"Year of vessel's construction",
                     blank=True)),
                ('registered_year',
                 models.IntegerField(
                     null=True,
                     verbose_name=b"Year of vessel's registration",
                     blank=True)),
                ('tonnage_mod',
                 models.DecimalField(
                     null=True,
                     verbose_name=b'Tonnage standardized on British '
                                  b'measured tons, 1773-1870',
                     max_digits=8,
                     decimal_places=1,
                     blank=True)),
                ('imputed_nationality',
                 models.ForeignKey(related_name='imputed_nationality',
                                   blank=True,
                                   to='voyage.Nationality',
                                   null=True,
                                   on_delete=models.CASCADE)),
                ('nationality_ship',
                 models.ForeignKey(related_name='nationality_ship',
                                   blank=True,
                                   to='voyage.Nationality',
                                   null=True,
                                   on_delete=models.CASCADE)),
                ('registered_place',
                 models.ForeignKey(
                     related_name='registered_place',
                     verbose_name=b'Place where vessel registered',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('registered_region',
                 models.ForeignKey(
                     related_name='registered_region',
                     verbose_name=b'Region where vessel registered',
                     blank=True,
                     to='voyage.Region',
                     null=True,
                     on_delete=models.CASCADE)),
                ('rig_of_vessel',
                 models.ForeignKey(blank=True,
                                   to='voyage.RigOfVessel',
                                   null=True,
                                   on_delete=models.CASCADE)),
                ('ton_type',
                 models.ForeignKey(blank=True, to='voyage.TonType', null=True,
                                   on_delete=models.CASCADE)),
                ('vessel_construction_place',
                 models.ForeignKey(
                     related_name='vessel_construction_place',
                     verbose_name=b'Place where vessel constructed',
                     blank=True,
                     to='voyage.Place',
                     null=True,
                     on_delete=models.CASCADE)),
                ('vessel_construction_region',
                 models.ForeignKey(
                     related_name='vessel_construction_region',
                     verbose_name=b'Region where vessel constructed',
                     blank=True,
                     to='voyage.Region',
                     null=True,
                     on_delete=models.CASCADE)),
                ('voyage',
                 models.ForeignKey(related_name='voyage_name_ship',
                                   blank=True,
                                   to='voyage.Voyage',
                                   null=True,
                                   on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Ship',
                'verbose_name_plural': 'Ships',
            },
        ),
        migrations.CreateModel(
            name='VoyageShipOwner',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='VoyageShipOwnerConnection',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('owner_order', models.IntegerField()),
                ('owner',
                 models.ForeignKey(related_name='owner_name',
                                   to='voyage.VoyageShipOwner',
                                   on_delete=models.CASCADE)),
                ('voyage',
                 models.ForeignKey(related_name='voyage_related',
                                   to='voyage.Voyage',
                                   on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='VoyageSlavesNumbers',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('slave_deaths_before_africa',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Slaves death before leaving '
                                  b'Africa (SLADAFRI)',
                     blank=True)),
                ('slave_deaths_between_africa_america',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Slaves death before arrival and '
                                  b'sale (SLADAMER)',
                     blank=True)),
                ('num_slaves_intended_first_port',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of slaves intended from first port '
                                  b'of purchase (SLINTEND)',
                     blank=True)),
                ('num_slaves_intended_second_port',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of slaves intended from second '
                                  b'port of purchase (SLINTEN2)',
                     blank=True)),
                ('num_slaves_carried_first_port',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of slaves carried from first port '
                                  b'of purchase (NCAR13)',
                     blank=True)),
                ('num_slaves_carried_second_port',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of slaves carried from second port '
                                  b'of purchase (NCAR15)',
                     blank=True)),
                ('num_slaves_carried_third_port',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of slaves carried from third port '
                                  b'of purchase (NCAR17)',
                     blank=True)),
                ('total_num_slaves_purchased',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Total slaves purchased (TSLAVESP)',
                     blank=True)),
                ('total_num_slaves_dep_last_slaving_port',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Total slaves on board at departure from '
                                  b'last slaving port (TSLAVESD)',
                     blank=True)),
                ('total_num_slaves_arr_first_port_embark',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Total slaves arrived at first port '
                                  b'of disembarkation (SLAARRIV)',
                     blank=True)),
                ('num_slaves_disembark_first_place',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of slaves disembarked '
                                  b'at first place (SLAS32)',
                     blank=True)),
                ('num_slaves_disembark_second_place',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of slaves disembarked '
                                  b'at second place (SLAS36)',
                     blank=True)),
                ('num_slaves_disembark_third_place',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of slaves disembarked '
                                  b'at third place (SLAS39)',
                     blank=True)),
                ('imp_total_num_slaves_embarked',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Total slaves embarked imputed * (slaximp)',
                     blank=True)),
                ('imp_total_num_slaves_disembarked',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Total slaves disembarked '
                                  b'imputed * (SLAMIMP)',
                     blank=True)),
                ('imp_jamaican_cash_price',
                 models.DecimalField(
                     null=True,
                     verbose_name=b'Sterling cash price in Jamaica* (imputed)',
                     max_digits=10,
                     decimal_places=4,
                     blank=True)),
                ('imp_mortality_during_voyage',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Imputed number of slave deaths '
                                  b'during Middle Passage (VYMRTIMP)',
                     blank=True)),
                ('num_men_embark_first_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of men (MEN1) embarked at first '
                                  b'port of purchase',
                     blank=True)),
                ('num_women_embark_first_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of women (WOMEN1) embarked at '
                                  b'first port of purchase',
                     blank=True)),
                ('num_boy_embark_first_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of boys (BOY1) embarked at first '
                                  b'port of purchase',
                     blank=True)),
                ('num_girl_embark_first_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of girls (GIRL1) embarked at first '
                                  b'port of purchase',
                     blank=True)),
                ('num_adult_embark_first_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of adults (gender unspecified) '
                                  b'(ADULT1) embarked at first port '
                                  b'of purchase',
                     blank=True)),
                ('num_child_embark_first_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of children (gender unspecified) '
                                  b'(CHILD1) embarked at first port '
                                  b'of purchase',
                     blank=True)),
                ('num_infant_embark_first_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of infants (INFANT1) embarked at '
                                  b'first port of purchase',
                     blank=True)),
                ('num_males_embark_first_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of males (age unspecified) (MALE1) '
                                  b'embarked at first port of purchase',
                     blank=True)),
                ('num_females_embark_first_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of females (age unspecified) '
                                  b'(FEMALE1) embarked at first port '
                                  b'of purchase',
                     blank=True)),
                ('num_men_died_middle_passage',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of men '
                                  b'(MEN2) died on Middle Passage',
                     blank=True)),
                ('num_women_died_middle_passage',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of women (WOMEN2) '
                                  b'died on Middle Passage',
                     blank=True)),
                ('num_boy_died_middle_passage',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of boys '
                                  b'(BOY2) died on Middle Passage',
                     blank=True)),
                ('num_girl_died_middle_passage',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of girls '
                                  b'(GIRL2) died on Middle Passage',
                     blank=True)),
                ('num_adult_died_middle_passage',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of adults (gender unspecified) '
                                  b'(ADULT2) died on Middle Passage',
                     blank=True)),
                ('num_child_died_middle_passage',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of children (gender unspecified) '
                                  b'(CHILD2) died on Middle Passage',
                     blank=True)),
                ('num_infant_died_middle_passage',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of infants '
                                  b'(INFANT2) died on Middle Passage',
                     blank=True)),
                ('num_males_died_middle_passage',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of males (age unspecified) '
                                  b'(MALE2) died on Middle Passage',
                     blank=True)),
                ('num_females_died_middle_passage',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of females (age unspecified) '
                                  b'(FEMALE2) died on Middle Passage',
                     blank=True)),
                ('num_men_disembark_first_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of men (MEN3) disembarked at '
                                  b'first place of landing',
                     blank=True)),
                ('num_women_disembark_first_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of women (WOMEN3) disembarked at '
                                  b'first place of landing',
                     blank=True)),
                ('num_boy_disembark_first_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of boys (BOY3) disembarked at '
                                  b'first place of landing',
                     blank=True)),
                ('num_girl_disembark_first_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of girls (GIRL3) disembarked at '
                                  b'first place of landing',
                     blank=True)),
                ('num_adult_disembark_first_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of adults (gender unspecified) '
                                  b'(ADULT3) disembarked at first place '
                                  b'of landing',
                     blank=True)),
                ('num_child_disembark_first_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of children (gender unspecified) '
                                  b'(CHILD3) disembarked at first place '
                                  b'of landing',
                     blank=True)),
                ('num_infant_disembark_first_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of infants (INFANT3) disembarked '
                                  b'at first place of landing',
                     blank=True)),
                ('num_males_disembark_first_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of males (age unspecified) (MALE3) '
                                  b'disembarked at first place of landing',
                     blank=True)),
                ('num_females_disembark_first_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of females (age unspecified) '
                                  b'(FEMALE3) disembarked at first place '
                                  b'of landing',
                     blank=True)),
                ('num_men_embark_second_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of men (MEN4) embarked at second '
                                  b'port of purchase',
                     blank=True)),
                ('num_women_embark_second_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of women (WOMEN4) embarked at '
                                  b'second port of purchase',
                     blank=True)),
                ('num_boy_embark_second_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of boys (BOY4) embarked at second '
                                  b'port of purchase',
                     blank=True)),
                ('num_girl_embark_second_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of girls (GIRL4) embarked at '
                                  b'second port of purchase',
                     blank=True)),
                ('num_adult_embark_second_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of adults (gender unspecified) '
                                  b'(ADULT4) embarked at second port '
                                  b'of purchase',
                     blank=True)),
                ('num_child_embark_second_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of children (gender unspecified) '
                                  b'(CHILD4) embarked at second port '
                                  b'of purchase',
                     blank=True)),
                ('num_infant_embark_second_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of infants (INFANT4) embarked at '
                                  b'second port of purchase',
                     blank=True)),
                ('num_males_embark_second_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of males (age unspecified) (MALE4) '
                                  b'embarked at second port of purchase',
                     blank=True)),
                ('num_females_embark_second_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of females (age unspecified) '
                                  b'(FEMALE4) embarked at second port '
                                  b'of purchase',
                     blank=True)),
                ('num_men_embark_third_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of men (MEN5) embarked at third '
                                  b'port of purchase',
                     blank=True)),
                ('num_women_embark_third_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of women (WOMEN5) embarked at '
                                  b'third port of purchase',
                     blank=True)),
                ('num_boy_embark_third_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of boys (BOY5) embarked at third '
                                  b'port of purchase',
                     blank=True)),
                ('num_girl_embark_third_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of girls (GIRL5) embarked at third '
                                  b'port of purchase',
                     blank=True)),
                ('num_adult_embark_third_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of adults (gender unspecified) '
                                  b'(ADULT5) embarked at third port '
                                  b'of purchase',
                     blank=True)),
                ('num_child_embark_third_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of children (gender unspecified) '
                                  b'(CHILD5) embarked at third port '
                                  b'of purchase',
                     blank=True)),
                ('num_infant_embark_third_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of infants (INFANT5) embarked at '
                                  b'third port of purchase',
                     blank=True)),
                ('num_males_embark_third_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of males (age unspecified) (MALE5) '
                                  b'embarked at third port of purchase',
                     blank=True)),
                ('num_females_embark_third_port_purchase',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of females (age unspecified) '
                                  b'(FEMALE5) embarked at third port '
                                  b'of purchase',
                     blank=True)),
                ('num_men_disembark_second_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of men (MEN6) disembarked at '
                                  b'second place of landing',
                     blank=True)),
                ('num_women_disembark_second_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of women (WOMEN6) disembarked at '
                                  b'second place of landing',
                     blank=True)),
                ('num_boy_disembark_second_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of boys (BOY6) disembarked at '
                                  b'second place of landing',
                     blank=True)),
                ('num_girl_disembark_second_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of girls (GIRL6) disembarked at '
                                  b'second place of landing',
                     blank=True)),
                ('num_adult_disembark_second_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of adults (gender unspecified) '
                                  b'(ADULT6) disembarked at second place '
                                  b'of landing',
                     blank=True)),
                ('num_child_disembark_second_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of children (gender unspecified) '
                                  b'(CHILD6) disembarked at second place '
                                  b'of landing',
                     blank=True)),
                ('num_infant_disembark_second_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of infants (INFANT6) disembarked '
                                  b'at second place of landing',
                     blank=True)),
                ('num_males_disembark_second_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of males (age unspecified) '
                                  b'(MALE6) disembarked at second place '
                                  b'of landing',
                     blank=True)),
                ('num_females_disembark_second_landing',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of females (age unspecified) '
                                  b'(FEMALE6) disembarked at second place '
                                  b'of landing',
                     blank=True)),
                ('imp_num_adult_embarked',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Imputed number of adults embarked '
                                  b'(ADLT1IMP)',
                     blank=True)),
                ('imp_num_children_embarked',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Imputed number of adults embarked '
                                  b'(CHIL1IMP)',
                     blank=True)),
                ('imp_num_male_embarked',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Imputed number of males embarked '
                                  b'(MALE1IMP)',
                     blank=True)),
                ('imp_num_female_embarked',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Imputed number of females embarked '
                                  b'(FEML1IMP)',
                     blank=True)),
                ('total_slaves_embarked_age_identified',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Total slaves embarked with age identified '
                                  b'(SLAVEMA1)',
                     blank=True)),
                ('total_slaves_embarked_gender_identified',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Total slaves embarked with gender '
                                  b'bidentified (SLAVEMX1)',
                     blank=True)),
                ('imp_adult_death_middle_passage',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Imputed number of adults who died on '
                                  b'Middle Passage (ADLT2IMP)',
                     blank=True)),
                ('imp_child_death_middle_passage',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Imputed number of children who died on '
                                  b'Middle Passage (CHIL2IMP)',
                     blank=True)),
                ('imp_male_death_middle_passage',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Imputed number of males who died on '
                                  b'Middle Passage (MALE2IMP)',
                     blank=True)),
                ('imp_female_death_middle_passage',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Imputed number of females who died on '
                                  b'Middle Passage (FEML2IMP)',
                     blank=True)),
                ('imp_num_adult_landed',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Imputed number of adults landed '
                                  b'(ADLT3IMP)',
                     blank=True)),
                ('imp_num_child_landed',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Imputed number of children landed '
                                  b'(CHIL3IMP)',
                     blank=True)),
                ('imp_num_male_landed',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Imputed number of males landed (MALE3IMP)',
                     blank=True)),
                ('imp_num_female_landed',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Imputed number of females landed '
                                  b'(FEML3IMP)',
                     blank=True)),
                ('total_slaves_landed_age_identified',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Total slaves identified by age among '
                                  b'landed slaves (SLAVEMA3)',
                     blank=True)),
                ('total_slaves_landed_gender_identified',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Total slaves identified by gender among '
                                  b'landed slaves (SLAVEMX3)',
                     blank=True)),
                ('total_slaves_dept_or_arr_age_identified',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Total slaves identified by age at '
                                  b'departure or arrival (SLAVEMA7)',
                     blank=True)),
                ('total_slaves_dept_or_arr_gender_identified',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Total slaves identified by gender at '
                                  b'departure or arrival(SLAVEMX7)',
                     blank=True)),
                ('imp_slaves_embarked_for_mortality',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Imputed number of slaves embarked for '
                                  b'mortality calculation (TSLMTIMP)',
                     blank=True)),
                ('imp_num_men_total',
                 models.IntegerField(null=True,
                                     verbose_name=b'Number of men (MEN7)',
                                     blank=True)),
                ('imp_num_women_total',
                 models.IntegerField(null=True,
                                     verbose_name=b'Number of women (WOMEN7) ',
                                     blank=True)),
                ('imp_num_boy_total',
                 models.IntegerField(null=True,
                                     verbose_name=b'Number of boys (BOY7)',
                                     blank=True)),
                ('imp_num_girl_total',
                 models.IntegerField(null=True,
                                     verbose_name=b'Number of girls (GIRL7)',
                                     blank=True)),
                ('imp_num_adult_total',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of adults (gender unspecified) '
                                  b'(ADULT7)',
                     blank=True)),
                ('imp_num_child_total',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of children (gender unspecified) '
                                  b'(CHILD7)',
                     blank=True)),
                ('imp_num_males_total',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of males (age unspecified) (MALE7)',
                     blank=True)),
                ('imp_num_females_total',
                 models.IntegerField(
                     null=True,
                     verbose_name=b'Number of females (age unspecified) '
                                  b'(FEMALE7) ',
                     blank=True)),
                ('percentage_men',
                 models.FloatField(null=True,
                                   verbose_name=b'Percentage men on voyage',
                                   blank=True)),
                ('percentage_women',
                 models.FloatField(null=True,
                                   verbose_name=b'Percentage women on voyage',
                                   blank=True)),
                ('percentage_boy',
                 models.FloatField(null=True,
                                   verbose_name=b'Percentage boy on voyage',
                                   blank=True)),
                ('percentage_girl',
                 models.FloatField(null=True,
                                   verbose_name=b'Percentage girl on voyage',
                                   blank=True)),
                ('percentage_male',
                 models.FloatField(null=True,
                                   verbose_name=b'Percentage male on voyage',
                                   blank=True)),
                ('percentage_child',
                 models.FloatField(
                     null=True,
                     verbose_name=b'Percentage children on voyage',
                     blank=True)),
                ('percentage_adult',
                 models.FloatField(null=True,
                                   verbose_name=b'Percentage adult on voyage',
                                   blank=True)),
                ('percentage_female',
                 models.FloatField(null=True,
                                   verbose_name=b'Percentage female on voyage',
                                   blank=True)),
                ('imp_mortality_ratio',
                 models.FloatField(null=True,
                                   verbose_name=b'Imputed mortality ratio',
                                   blank=True)),
                ('voyage',
                 models.ForeignKey(
                     related_name='voyage_name_slave_characteristics',
                     to='voyage.Voyage',
                     on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Slaves Characteristic',
                'verbose_name_plural': 'Slaves Characteristics',
            },
        ),
        migrations.CreateModel(
            name='VoyageSources',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('short_ref',
                 models.CharField(max_length=255,
                                  null=True,
                                  verbose_name='Short reference',
                                  blank=True)),
                ('full_ref',
                 models.CharField(max_length=2550,
                                  null=True,
                                  verbose_name='Full reference',
                                  blank=True)),
            ],
            options={
                'ordering': ['short_ref', 'full_ref'],
                'verbose_name': 'Source',
                'verbose_name_plural': 'Sources',
            },
        ),
        migrations.CreateModel(
            name='VoyageSourcesConnection',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('source_order', models.IntegerField()),
                ('text_ref',
                 models.CharField(max_length=255,
                                  null=True,
                                  verbose_name='Text reference(citation)',
                                  blank=True)),
                ('group',
                 models.ForeignKey(related_name='group', to='voyage.Voyage',
                                   on_delete=models.CASCADE)),
                ('source',
                 models.ForeignKey(related_name='source',
                                   blank=True,
                                   to='voyage.VoyageSources',
                                   null=True,
                                   on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='VoyageSourcesType',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('group_id', models.IntegerField()),
                ('group_name', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['group_id'],
                'verbose_name': 'Sources type',
                'verbose_name_plural': 'Sources types',
            },
        ),
        migrations.AddField(
            model_name='voyagesources',
            name='source_type',
            field=models.ForeignKey(to='voyage.VoyageSourcesType', null=True,
                                    on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='voyage',
            name='voyage_captain',
            field=models.ManyToManyField(
                help_text=b'Voyage Captain',
                to='voyage.VoyageCaptain',
                through='voyage.VoyageCaptainConnection',
                blank=True),
        ),
        migrations.AddField(
            model_name='voyage',
            name='voyage_crew',
            field=models.ForeignKey(related_name='voyage_crew',
                                    blank=True,
                                    to='voyage.VoyageCrew',
                                    null=True,
                                    on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='voyage',
            name='voyage_dates',
            field=models.ForeignKey(related_name='voyage_dates',
                                    blank=True,
                                    to='voyage.VoyageDates',
                                    null=True,
                                    on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='voyage',
            name='voyage_groupings',
            field=models.ForeignKey(blank=True,
                                    to='voyage.VoyageGroupings',
                                    null=True,
                                    on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='voyage',
            name='voyage_itinerary',
            field=models.ForeignKey(related_name='voyage_itinerary',
                                    blank=True,
                                    to='voyage.VoyageItinerary',
                                    null=True,
                                    on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='voyage',
            name='voyage_ship',
            field=models.ForeignKey(related_name='voyage_ship',
                                    blank=True,
                                    to='voyage.VoyageShip',
                                    null=True,
                                    on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='voyage',
            name='voyage_ship_owner',
            field=models.ManyToManyField(
                help_text=b'Voyage Ship Owner',
                to='voyage.VoyageShipOwner',
                through='voyage.VoyageShipOwnerConnection',
                blank=True),
        ),
        migrations.AddField(
            model_name='voyage',
            name='voyage_slaves_numbers',
            field=models.ForeignKey(related_name='voyage_slaves_numbers',
                                    blank=True,
                                    to='voyage.VoyageSlavesNumbers',
                                    null=True,
                                    on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='voyage',
            name='voyage_sources',
            field=models.ManyToManyField(
                related_name='voyage_sources',
                through='voyage.VoyageSourcesConnection',
                to='voyage.VoyageSources',
                blank=True),
        ),
        migrations.AddField(
            model_name='place',
            name='region',
            field=models.ForeignKey(to='voyage.Region',
                                    on_delete=models.CASCADE),
        ),
    ]
