# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-11 06:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secondary_market', '0019_auto_20180311_0610'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Email',
            new_name='SendMail',
        ),
    ]