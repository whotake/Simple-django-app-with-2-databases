# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-16 19:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_auto_20161216_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='time_added',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 16, 19, 12, 1, 951251, tzinfo=utc)),
        ),
    ]
