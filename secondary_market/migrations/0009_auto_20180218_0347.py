# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-18 03:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secondary_market', '0008_payment'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Payment',
            new_name='Payments',
        ),
    ]
