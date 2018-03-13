# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-13 16:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secondary_market', '0028_auto_20180313_0518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2018, 3, 27, 16, 30, 13, 493842)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.FloatField(blank=True, default=9999),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='decay_rate',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='exec_price',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='reserve_price',
            field=models.FloatField(blank=True, default=9999),
        ),
    ]