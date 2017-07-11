# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 06:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vacs', '0011_auto_20170711_0513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vac',
            name='experiment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacs', to='vacs.Experiment'),
        ),
    ]