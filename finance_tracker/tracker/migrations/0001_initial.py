# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Security',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127)),
                ('isin', models.CharField(max_length=12)),
                ('detail_url', models.URLField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SecurityDataPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('currency', models.CharField(default='EUR', max_length=3)),
                ('unit_value', models.DecimalField(max_digits=7, decimal_places=4)),
                ('security', models.ForeignKey(to='tracker.Security')),
            ],
        ),
        migrations.AlterIndexTogether(
            name='securitydatapoint',
            index_together=set([('security', 'timestamp')]),
        ),
    ]
