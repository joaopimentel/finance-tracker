# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20150817_2127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('units', models.DecimalField(max_digits=7, decimal_places=4)),
                ('portfolio', models.ForeignKey(to='tracker.Portfolio')),
                ('security', models.ForeignKey(to='tracker.Security')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.AlterIndexTogether(
            name='position',
            index_together=set([('portfolio', 'timestamp')]),
        ),
    ]
