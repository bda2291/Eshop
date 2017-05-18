# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-17 14:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0004_auto_20170517_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='code',
            field=models.CharField(blank=True, default='094fb9c2-36b1-4b70-a8e7-7efb10790741', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='valid_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 5, 24, 14, 3, 19, 339778)),
        ),
    ]
