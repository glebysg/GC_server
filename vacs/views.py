# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.urlresolvers import reverse_lazy
from vacs.forms import ExperimentForm
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from vacs.models import Experiment

def index(request):
    template = loader.get_template('vacs/index.html')
    return HttpResponse(template.render({},request))


class ExperimentDetailView(DetailView):
    model = Experiment


class ExperimentListView(ListView):
    model = Experiment


class ExperimentView(FormView):
    template_name = 'vacs/experiment.html'
    form_class = ExperimentForm
    success_url = 'vacs/experiments'

class ExperimentCreateView(CreateView):
    model = Experiment
    success_url = reverse_lazy('experiment_list')
    fields = ['name', 'student_n', 'expert_n', 'student_cmd_n', 'expert_cmd_n']

class ExperimentUpdateView(UpdateView):
    model = Experiment
    success_url = reverse_lazy('experiment_list')
    fields = ['is_active' ]

class ExperimentDeleteView(DeleteView):
    model = Experiment
    success_url = reverse_lazy('experiment_list')
