# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from vacs.forms import ExperimentForm
from django.views.generic.edit import FormView

def index(request):
    template = loader.get_template('vacs/index.html')
    return HttpResponse(template.render({},request))


class ExperimentView(FormView):
    template_name = 'vacs/experiment.html'
    form_class = ExperimentForm
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super(ExperimentViewe, self).form_valid(form)
