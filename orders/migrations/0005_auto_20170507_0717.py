# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-07 07:17
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0001_initial'),
        ('orders', '0004_auto_20170506_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='discount.Discount'),
        ),
        migrations.AddField(
            model_name='order',
            name='discount_value',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
