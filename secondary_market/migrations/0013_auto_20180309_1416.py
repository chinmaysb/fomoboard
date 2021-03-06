# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-09 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secondary_market', '0012_auto_20180218_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='icon',
            field=models.TextField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='transaction',
            name='decay_price',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='transaction',
            name='email_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='email_tries',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='transaction',
            name='payment_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='payment_tries',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='transaction',
            name='reserve_price',
            field=models.IntegerField(blank=True, default=9999),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='buyer_venmo_handle',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='exp_price',
            field=models.IntegerField(blank=True, default=9999),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.CharField(max_length=6, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='seller',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='seller_venmo_handle',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
