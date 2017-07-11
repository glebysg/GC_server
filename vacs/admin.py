# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Experiment, Vac, Command

# Register your models here.
admin.site.register(Experiment)
admin.site.register(Vac)
admin.site.register(Command)
