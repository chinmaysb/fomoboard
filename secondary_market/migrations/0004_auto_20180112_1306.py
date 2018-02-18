# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-12 13:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('secondary_market', '0003_transaction_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seller_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
