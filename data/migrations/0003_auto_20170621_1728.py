# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20170621_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datamodel',
            name='active_trucks',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='datamodel',
            name='carrier_type',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='datamodel',
            name='dba',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='datamodel',
            name='effective_date',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='datamodel',
            name='mailing_address',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='datamodel',
            name='name',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='datamodel',
            name='phone',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='datamodel',
            name='record_url',
            field=models.URLField(default=''),
        ),
    ]
