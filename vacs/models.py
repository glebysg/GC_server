# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Experiment(models.Model):
    subject_n = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

class Vacs(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)


