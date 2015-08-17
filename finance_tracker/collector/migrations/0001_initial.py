# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20150817_2127'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecificXMLDataSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_url', models.URLField()),
                ('security', models.ForeignKey(to='tracker.Security')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
