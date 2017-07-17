# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 20:17
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacs', '0012_auto_20170711_0616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='current_lexicon',
        ),
        migrations.AddField(
            model_name='assignment',
            name='current_comparison',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(16)]),
        ),
        migrations.AddField(
            model_name='assignment',
            name='lexicon_order',
            field=models.CharField(default='1.2.3.4.5.6.7.8.9', max_length=200, unique=True),
            preserve_default=False,
        ),
    ]