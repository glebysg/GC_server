# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 01:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacs', '0009_auto_20170710_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='replications',
            field=models.TextField(blank=True),
        ),
    ]
