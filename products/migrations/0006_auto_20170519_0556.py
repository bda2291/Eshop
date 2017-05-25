# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-19 05:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20170517_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='producer',
            field=models.CharField(blank=True, db_index=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(blank=True, db_index=True, default=None, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='name',
            field=models.CharField(blank=True, db_index=True, default=None, max_length=64, null=True, unique=True),
        ),
    ]