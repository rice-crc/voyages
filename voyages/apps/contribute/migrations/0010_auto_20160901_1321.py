# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voyage', '0002_auto_20151210_0937'),
        ('contribute', '0009_auto_20160829_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='interimarticlesource',
            name='created_voyage_sources',
            field=models.ForeignKey(related_name='+',
                                    to='voyage.VoyageSources',
                                    null=True,
                                    on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='interimbooksource',
            name='created_voyage_sources',
            field=models.ForeignKey(related_name='+',
                                    to='voyage.VoyageSources',
                                    null=True,
                                    on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='interimothersource',
            name='created_voyage_sources',
            field=models.ForeignKey(related_name='+',
                                    to='voyage.VoyageSources',
                                    null=True,
                                    on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='interimprimarysource',
            name='created_voyage_sources',
            field=models.ForeignKey(related_name='+',
                                    to='voyage.VoyageSources',
                                    null=True,
                                    on_delete=models.CASCADE),
        ),
    ]
