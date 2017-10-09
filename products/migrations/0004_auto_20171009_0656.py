# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-09 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20170928_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattribute',
            name='main_attribute',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products', verbose_name='image of product'),
        ),
    ]
