# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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


########################################
##############  GLOBALS  ###############
########################################
experimental_design = [
    ['a', 'b', 'c'],
    ['a', 'd', 'e'],
    ['b', 'd', 'e'],
    ['c', 'd', 'e'],
    ['a', 'f', 'g'],
    ['b', 'f', 'g'],
    ['c', 'f', 'g'],
    ['d', 'f', 'g'],
    ['e', 'f', 'g'],
    ['a', 'h', 'i'],
    ['b', 'h', 'i'],
    ['c', 'h', 'i'],
    ['d', 'h', 'i'],
    ['e', 'h', 'i'],
    ['f', 'h', 'i'],
    ['g', 'h', 'i']
]

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

########################################
############## FUNCTIONS ###############
########################################
def index(request):
    if request.user.is_authenticated():
        user = request.user
        if has_role(user,'researcher'):
            print "%%%%%%%%%%%%%%% R %%%%%%%%%%%%%%%%"
            return HttpResponseRedirect('/vacs/experiments')
        elif has_role(user,['student','expert'] ):
            print "%%%%%%%%%%%%%%% P %%%%%%%%%%%%%%%%"
            # if the current vac is null, add the first one on the list
            participant = Participant.objects.get(user=user)
            # Get the assignments that are not done
            assignments = Assignment.objects.filter(
                    user = user,
                    done = False
            )
            if assignments:
                # if not empty grab the first assignment
                assignment = assignments[0]
                # if the current vac is null, add the first one on the list
                if not assignment.current_vac:
                    vacs = Vac.objects.filter(experiment__id=participant.experiment.pk)
                    try:
                        vac = vacs[:1].get()
                    except Vac.DoesNotExist:
                        return render(request,
                            'vacs/error_message.html', {
                            'message':'Please tell the researcher to add the VACs'})
                    assignment.current_vac = vac
                    assignment.save()
                print "ABOUT TO REDIRECT"
                return redirect('evaluation_edit',
                    assignment.pk, assignment.current_vac.pk)
            else:
                # if empty redirect to validation
                # experiment.
                return redirect('validation_index')
        else:
            print "%%%%%%%%%%%%%%% N %%%%%%%%%%%%%%%%"
            return HttpResponseRedirect('/')
    else:
        template = loader.get_template('vacs/index.html')
        return HttpResponse(template.render({},request))

@has_permission_decorator('update_evaluation')
def validation_index(request):
    template = loader.get_template('vacs/validation_index.html')
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


@has_role_decorator('researcher')
def vac_list(request, e_pk, template_name='vacs/vac_list.html'):
    experiment = get_object_or_404(Experiment, pk=e_pk)
    vac = Vac.objects.filter(experiment_id=e_pk)
    data = {}
    data['object_list'] = vac
    data['experiment'] = experiment
    return render(request, template_name, data)

@has_role_decorator('researcher')
def vac_create(request, e_pk, template_name='vacs/vac_form.html'):
    experiment = get_object_or_404(Experiment, pk=e_pk)
    form = VacForm(request.POST or None)
    if form.is_valid():
        vac = form.save(commit=False)
        vac.experiment = experiment
        form.save()
        return redirect('vac_list', e_pk)
    return render(request, template_name, {'form':form, 'action':'create'})

@has_role_decorator('researcher')
def vac_update(request, e_pk, pk, template_name='vacs/vac_form.html'):
    experiment = get_object_or_404(Experiment, pk=e_pk)
    vac = get_object_or_404(Vac, pk=pk)
    form = VacForm(request.POST or None, instance=vac)
    if form.is_valid():
        form.save()
        return redirect('vac_list', e_pk)
    return render(request, template_name, {'form':form, 'action':'update'})

@has_role_decorator('researcher')
def vac_delete(request, e_pk, pk, template_name='vacs/vac_confirm_delete.html'):
    experiment = get_object_or_404(Experiment, pk=e_pk)
    vac = get_object_or_404(Vac, pk=pk)
    if request.method=='POST':
        vac.delete()
        return redirect('vac_list', e_pk)
    return render(request, template_name, {'object':vac})

#create evaluation.
@has_permission_decorator('update_evaluation')
def evaluation_update(request, a_pk, v_pk, template_name='vacs/evaluation_form.html'):
    try:
        vac = Vac.objects.get(pk=v_pk)
    except Vac.DoesNotExist:
        return render(request, 'vacs/error_message.html', {
                'message':'Please tell the researcher to add the VACs'})
    assignment = get_object_or_404(Assignment, pk=a_pk)
    evaluation, created = Evaluation.objects.get_or_create(
	assignment=assignment,
	vac=vac,
	number=assignment.current_comparison
    )
    participant = Participant.objects.get(user__id=request.user.pk)
    experiment = Experiment.objects.get(pk=participant.experiment.pk)
    form = EvaluationForm(request.POST or None, instance=evaluation)

    assignments = Assignment.objects.filter(
        user = request.user,
        done = False
    )
    if not assignments:
        return redirect('validation_index')
    else:
        print assignments

    if form.is_valid():
        form.save()
	# check if current comparison == 15
	if assignment.current_comparison == 15:
	    # reset comparison to zero
	    assignment.current_comparison = 0
	    # add the current vac to the evaluated list
	    assignment.evaluated_vacs.add(vac)
	    # look all the vacs for this experiment,
	    participant = Participant.objects.get(user=request.user)
	    possible_vacs = Vac.objects.filter(experiment__id=participant.experiment.pk)\
	    	.exclude(id__in=[o.id for o in assignment.evaluated_vacs.all()])
	    # If the list is not empty, get the first vac and add it to the assignment as current vac
	    if possible_vacs:
		new_vac = possible_vacs[0]
		assignment.current_vac = new_vac
                lexicon_order = range(1,10)
                random.shuffle(lexicon_order)
                lexicon_order = ''.join([str(l)+',' for l in lexicon_order])
                assignment.lexicon_order = lexicon_order
	    # If the list is empty, mark as done
	    else:
                print "THE ASSIGNMENT WAS MARKED AS DONE"
	    	assignment.done = True
                assignment.save()
                return redirect('index')
        else:
	    assignment.current_comparison += 1
	assignment.save()

        return redirect('evaluation_edit',
        assignment.pk, assignment.current_vac.pk)

    positions = [letters.index(elem) for elem in experimental_design[assignment.current_comparison]]
    order = assignment.lexicon_order[0].decode('utf-8')
    print str(order).split(',')
    subjects = [assignment.lexicon_order.split(',')[p] for p in positions]

    vac_number = len(experiment.vacs.all())
    evaluation_number = 0
    all_assignments = Assignment.objects.filter(user=request.user)
    for a in all_assignments:
        evaluation_number += len(Evaluation.objects.filter(assignment=a))
    if has_role(request.user,'expert'):
    	hundred_percent = experiment.expert_cmd_n*16*vac_number
    elif has_role(request.user,'student'):
    	hundred_percent = experiment.student_cmd_n*16*vac_number
    progress = int(math.floor(evaluation_number*100/hundred_percent))

    return render(request, template_name, {
        'form':form,
        'vac':vac,
        'command':assignment.command,
        'subjects': subjects,
	'progress': progress})


@has_role_decorator('researcher')
def generate_scores(request, e_pk, template_name='vacs/scores.html'):
    experiment = get_object_or_404(Experiment, pk=e_pk)
    if request.POST:
        # ADD SCORES

        # CHANGE EXPERIMENT STATUS

        # RETURN TO EXPERIMENT
        return redirect('experiment_list')
    participant_stats = []
    # Get all the participants in the experiment
    participants = Participant.objects.filter(experiment=experiment)
    for p in participants:
        username = p.user.username
        vac_number = len(experiment.vacs.all())
        evaluation_number = 0
        all_assignments = Assignment.objects.filter(user=p.user)
        for a in all_assignments:
            evaluation_number += len(Evaluation.objects.filter(assignment=a))
        if has_role(p.user,'expert'):
            hundred_percent = experiment.expert_cmd_n*16*vac_number
            role = 'Expert'
        elif has_role(p.user,'student'):
            hundred_percent = experiment.student_cmd_n*16*vac_number
            role = 'Student'
        participant_stats.append((username, evaluation_number, hundred_percent, role))
    print participant_stats
    return render(request, template_name, {'participant_stats':participant_stats})
