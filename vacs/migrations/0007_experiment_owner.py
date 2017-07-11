# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-09 20:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vacs', '0006_auto_20170705_0357'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]