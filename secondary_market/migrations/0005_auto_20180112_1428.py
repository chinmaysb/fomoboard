# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-12 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secondary_market', '0004_auto_20180112_1306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='min_price',
        ),
        migrations.AddField(
            model_name='transaction',
            name='buyer_venmo_handle',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='seller_venmo_handle',
            field=models.TextField(default='Chinmay_Borkar', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='buyer',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='seller',
            field=models.TextField(default='Chinmay', max_length=250),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
