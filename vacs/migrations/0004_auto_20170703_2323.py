# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 23:23
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vacs', '0003_assignment_groupassignment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GroupAssignment',
        ),
        migrations.AddField(
            model_name='experiment',
            name='replication1',
            field=jsonfield.fields.JSONField(blank=True),
        ),
        migrations.AlterField(
            model_name='command',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
