# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-18 12:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0005_auto_20170517_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='code',
            field=models.CharField(blank=True, default='2badff26-12c0-4bb6-8049-91f37425b3ce', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='valid_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 5, 25, 12, 31, 44, 704313)),
        ),
    ]
