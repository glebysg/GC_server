# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 05:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacs', '0010_auto_20170710_0114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacs',
            name='experiment',
        ),
        migrations.DeleteModel(
            name='Vacs',
        ),
    ]
