# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacs', '0016_remove_evaluation_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
