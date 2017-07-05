# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField
import collections

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
    is_active = models.BooleanField(default=True)
    replication1 = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict},
            blank=True)

class Vacs(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)


class Vac(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

class Evaluation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    vac = models.ForeignKey(Vac, on_delete=models.CASCADE)
    evaluation = models.CharField(max_length=100)

class Command(models.Model):
    name = models.CharField(unique=True, max_length=200)
    code = models.CharField(unique=True, max_length=4)

class Score(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    vac = models.ForeignKey(Vac, on_delete=models.CASCADE)
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

class Assignment(models.Model):
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_lexicon = models.IntegerField(default=1,
            validators=[MinValueValidator(1), MaxValueValidator(9)])
    Done = models.BooleanField(default=False)
