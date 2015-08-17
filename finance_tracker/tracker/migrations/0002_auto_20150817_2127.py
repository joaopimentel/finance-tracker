# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='securitydatapoint',
            name='currency',
        ),
        migrations.AddField(
            model_name='security',
            name='currency',
            field=models.CharField(default='EUR', max_length=3),
        ),
    ]
