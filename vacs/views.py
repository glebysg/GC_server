# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.urlresolvers import reverse_lazy
from vacs.forms import ExperimentForm
from vacs.models import Experiment
from django.shortcuts import render, redirect, get_object_or_404
from rolepermissions.decorators import has_role_decorator

def index(request):
    template = loader.get_template('vacs/index.html')
    return HttpResponse(template.render({},request))

@has_role_decorator('researcher')
def experiment_list(request, template_name='vacs/experiment_list.html'):
    experiments = Experiment.objects.all()
    data = {}
    data['object_list'] = experiments
    return render(request, template_name, data)

@has_role_decorator('researcher')
def experiment_create(request, template_name='vacs/experiment_form.html'):
    form = ExperimentForm(request.POST or None)
    if form.is_valid():
        experiment = form.save(commit=False)
        experiment.owner = request.user
        form.save()
        return redirect('experiment_list')
    return render(request, template_name, {'form':form, 'action':'create'})

@has_role_decorator('researcher')
def experiment_update(request, pk, template_name='vacs/experiment_form.html'):
    experiment = get_object_or_404(Experiment, pk=pk)
    form = ExperimentForm(request.POST or None, instance=experiment)
    if form.is_valid():
        form.save()
        return redirect('experiment_list')
    return render(request, template_name, {'form':form, 'action':'update'})

@has_role_decorator('researcher')
def experiment_delete(request, pk, template_name='vacs/experiment_confirm_delete.html'):
    experiment = get_object_or_404(Experiment, pk=pk)
    if request.method=='POST':
        experiment.delete()
        return redirect('experiment_list')
    return render(request, template_name, {'object':experiment})
