from django.contrib.auth import (
    get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.urlresolvers import reverse_lazy
from vacs.forms import ExperimentForm, VacForm, EvaluationForm
from vacs.models import Experiment, Vac, Assignment, Evaluation, Participant, Command
from django.shortcuts import render, redirect, get_object_or_404
from rolepermissions.decorators import has_role_decorator, has_permission_decorator
from rolepermissions.checkers import has_permission, has_role
from django.http import HttpResponseRedirect, QueryDict
import math
import random
from django.db.models.query import QuerySet
from pprint import PrettyPrinter

def dprint(object, stream=None, indent=1, width=80, depth=None):
    """
    A small addition to pprint that converts any Django model objects to dictionaries so they print prettier.
    h3. Example usage

        >>> from toolbox.dprint import dprint
        >>> from app.models import Dummy
        >>> dprint(Dummy.objects.all().latest())
         {'first_name': u'Ben',
          'last_name': u'Welsh',
          'city': u'Los Angeles',
          'slug': u'ben-welsh',
    """
    # Catch any singleton Django model object that might get passed in
    if getattr(object, '__metaclass__', None):
        if object.__metaclass__.__name__ == 'ModelBase':
            # Convert it to a dictionary
            object = object.__dict__
    # Catch any Django QuerySets that might get passed in
    elif isinstance(object, QuerySet):
        # Convert it to a list of dictionaries
        object = [i.__dict__ for i in object]
    # Pass everything through pprint in the typical way
    printer = PrettyPrinter(stream=stream, indent=indent, width=width, depth=depth)
    printer.pprint(object)


User = get_user_model()

u=User.objects.get(username='e60_e1')
e=Experiment.objects.get(pk=u.participant.experiment.pk)
count =0
for a in Assignment.objects.filter(user=u):
    for e in Evaluation.objects.filter(assignment=a):
        print "ASSIGNMENT: ", a.pk
        print e.pk, e.evaluation
        count +=1

print "COUNT:", count


