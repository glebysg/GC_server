# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
# @python_2_unicode_compatible
class Experiment(models.Model):
    name = models.CharField(max_length=200)
    student_n = models.IntegerField(default=0,
            validators=[MinValueValidator(0)])
    expert_n = models.IntegerField(default=0,
            validators=[MinValueValidator(0)])
    student_cmd_n  = models.IntegerField(default=2,
            validators=[MinValueValidator(2)])
    expert_cmd_n  = models.IntegerField(default=1,
            validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=False)

# @python_2_unicode_compatible
class Vacs(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
