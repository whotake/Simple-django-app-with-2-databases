# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-16 18:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_auto_20161205_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='time_added',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 16, 18, 46, 43, 480400, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user_id',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='order',
            name='user_id',
            field=models.IntegerField(default=-1),
        ),
    ]
