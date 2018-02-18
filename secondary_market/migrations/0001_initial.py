# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-12 12:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('face_value', models.FloatField()),
                ('event_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.TextField(blank=True, max_length=20)),
                ('venmo_handle', models.TextField(blank=True, max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('exp_price', models.FloatField()),
                ('min_price', models.FloatField()),
                ('buyer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='buyer_id', to=settings.AUTH_USER_MODEL)),
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seller_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
