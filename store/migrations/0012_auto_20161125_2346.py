# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-25 20:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20161125_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='time_added',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 25, 20, 46, 46, 17673, tzinfo=utc)),
        ),
    ]
