# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.urlresolvers import reverse_lazy
from vacs.forms import ExperimentForm, VacForm, EvaluationForm, ValidationForm
from vacs.models import Experiment, Vac, Assignment, ValAssignment, Evaluation, Participant, Command, Score, Validation
from django.shortcuts import render, redirect, get_object_or_404
from rolepermissions.decorators import has_role_decorator, has_permission_decorator
from rolepermissions.checkers import has_permission, has_role
from django.http import HttpResponseRedirect, QueryDict
import math
import random
import pprint as pp
import json
import copy
from vacs.utils import Order, get_critical_score


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

command_code = {
    1:2,
    2:2,
    3:2,
    4:2,
    5:4,
    6:4,
    7:2,
    8:2,
    9:2,
    10:4,
    11:2,
}

########################################
############## FUNCTIONS ###############
########################################
def create_replication():
    random_groups = range(1,12)
    random.shuffle(random_groups)
    random_commands = []
    for index in random_groups:
        sub_commands = range(1,command_code[index]+1)
        random.shuffle(sub_commands)
        commands = []
        for sc in sub_commands:
            lexicons = range(1,10)
            random.shuffle(lexicons)
            lexicon_group = []
            for l in lexicons:
                lexicon_item = {'code': str(index) + '_'+str(sc) + '_'+ str(l),
                        'pk': -1}
                lexicon_group.append(lexicon_item)
            commands.append(lexicon_group)
        random_commands.append(commands)
    return random_commands

########################################
##############   VIEWS   ###############
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
            elif participant.experiment.in_validation:
                # if experiment ready for validation
                val_assignments = ValAssignment.objects.filter(
                        user = user,
                        done = False
                )
                if val_assignments:
                    # if not empty grab the first assignment
                    val_assignment = val_assignments[0]
                    # if the current score is null, add the vac that is closest to the list 
                    if not val_assignment.current_score:
                        vacs = Score.objects.filter(experiment__id=participant.experiment.pk)
                        try:
                            vac = vacs[:1].get()
                        except Vac.DoesNotExist:
                            return render(request,
                                'vacs/error_message.html', {
                                'message':'Please tell the researcher to add the VACs'})
                        # Get the current score
                        scores = Score.objects.filter(experiment=experiment,
                                command=val_assignment.command, lexicon_number=val_assignment.lexicon_number)
                        score = get_critical_score(scores)
                        val_assignment.current_score = score
                        val_assignment.save()
                    return redirect('validation_edit',
                        val_assignment.pk, val_assignment.current_score.pk)
                else:
                    return redirect('finished')

            else:
                # if empty but not in validation
                # redirect to waiting mesage
                "ENTRÉ EN ESTA MIERDA"
                return redirect('validation_index')
        else:
            print "%%%%%%%%%%%%%%% N %%%%%%%%%%%%%%%%"
            return HttpResponseRedirect('/')
    else:
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
        return redirect('index')
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
    participant_stats = []
    # Get all the participants in the experiment
    participants = Participant.objects.filter(experiment=experiment)
    not_complete = False
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
        if hundred_percent > evaluation_number:
            not_complete = True
        participant_stats.append((username, evaluation_number, hundred_percent, role))
    if request.POST:
        if not_complete:
            return render(request, template_name, {
                'participant_stats':participant_stats,
                'experiment': experiment,
                'error':'Every subject needs to complete the task before starting part II'})
        # ADD SCORES
        names_list = ['1','2','3','4', '5', '6', '7', '8', '9']
        for p in participants:
            username = p.user.username
            all_vacs = experiment.vacs.all()
            all_assignments = Assignment.objects.filter(user=p.user)
            for a in all_assignments:
                for v in all_vacs:
                    evaluations = Evaluation.objects.filter(assignment=a, vac=v)
                    evaluation_list = []
                    for e in evaluations:
                        clean_evaluation = e.evaluation.replace(".", "")
                        evaluation_list.append(clean_evaluation)
                    ord = Order(names_list, evaluation_list)
                    [global_order, ineq, scores] = ord.get_all()
                    # Create Scores
                    for index in range(len(global_order)):
                        lexicon_number = int(global_order[index])
                        score, created = Score.objects.get_or_create(
                            experiment = experiment,
                            vac = v,
                            command = a.command,
                            score = scores[index],
                            lexicon_number = lexicon_number
                        )
                        score.save()
        # CHANGE EXPERIMENT STATUS
        experiment.in_validation = True

        # CREATE PHASE II ASIGNMENTS
	# Assign the gestures to the experts
	replications = [create_replication(),create_replication(),create_replication()]
        replications_del = copy.deepcopy(replications)
	assigned = 0
	counter = 0
	replication = 0
	user_counter = 0
	total_assignments = experiment.expert_n*experiment.expert_cmd_n*9 +\
			    experiment.student_n*experiment.student_cmd_n*9

        print "ASSIGNING USERS FOR VALIDATION"
        print "Total assignments: ", total_assignments
        print "#################################"
	while (assigned <total_assignments):
	    user = participants[user_counter].user
	    if has_role(user,'expert'):
		command_n= experiment.expert_cmd_n*9
	    else:
		command_n= experiment.student_cmd_n*9
	    command_counter = 0
	    while(command_counter < command_n):
                # print "assigned: " + str(assigned)
                # print "user counter: " + str(user_counter)
                # print "counter: " + str(counter)
                # print "command_counter: " + str(command_counter)
                # print "replications: " + str(replication)
                # print "***************************************"
                # print "***************************************"
		group_index = counter%11
		assignment_created = False
                # Search for the sub-command that has the least assignments
                sub_cds_len = [len(sc) for sc in replications_del[replication][group_index]]
                max_len = max(sub_cds_len)
                if max_len != 0:
                    i_del = sub_cds_len.index(max_len)
                    full_code = replications_del[replication][group_index][i_del][0]['code']
                    split_code = full_code.split('_')
                    code_del = split_code[0]+"_"+split_code[1]
                    lexicon_index = None
                    for i, item in enumerate(replications[replication][group_index][i_del]):
                        if item['code'] == full_code:
                            lexicon_index = i
                            break
                    # create the assignment for validation 
                    command = Command.objects.get(code=code_del)
                    assignment = ValAssignment.objects.create(
                        command = command,
                        lexicon_number = split_code[2],
                        user = user)
                    assignment.save()
                    del replications_del[replication][group_index][i_del][0]
                    # Assign in the replication
                    replications[replication][group_index][i_del][lexicon_index]['pk'] = assignment.pk
                    assigned += 1
                    command_counter +=1
                    replication = assigned/(28*9)
                counter += 1
	    user_counter += 1
	experiment.val_replications = json.dumps(replications)
        # print "#################################"
        # pp.pprint(replications)
        # print "#################################"
        # pp.pprint(replications_del)
        experiment.save()

        # RETURN TO EXPERIMENT
        return redirect('experiment_list')
    print participant_stats
    return render(request, template_name, {'participant_stats':participant_stats,
        'experiment':experiment})

@has_permission_decorator('update_evaluation')
def validation_update(request, a_pk, s_pk, template_name='vacs/validation_form.html'):
    template = loader.get_template(template_name)
    assignment = ValAssignment.objects.get(pk=a_pk)
    score = Score.objects.get(pk=s_pk)
    participant = Participant.objects.get(user__id=request.user.pk)
    experiment = Experiment.objects.get(pk=participant.experiment.pk)
    last_vac = False
    if not experiment.in_validation:
        val_indextemplate = loader.get_template('vacs/validation_index.html')
        return HttpResponse(val_indextemplate.render({},request))
    validation, created = Validation.objects.get_or_create(
	score=score,
    )
    form = ValidationForm(request.POST or None, instance=validation)
    assignments = ValAssignment.objects.filter(
        user = request.user,
        done = False
    )
    if not assignments:
        return redirect('index')
    else:
        print assignments

    if form.is_valid():
        saved_validation = form.save()
        # Add the just saved Validation to the
        # previous validation in the Assignment
        assignment.previous_validation = saved_validation
        # Add the curret score to the val assigment
        assignment.evaluated_scores.add(score)
        assignment.save()

        # get all the non-validated scores associated with the val assignment
        scores_to_validate = Score.objects.filter(
            experiment = experiment,
            command = assignment.command,
            lexicon_number = assignment.lexicon_number
            ).exclude(id__in=[o.id for o in assignment.evaluated_scores.all()])

        # if its not empty
        if scores_to_validate:
            # Associate the most critical score that has not
            # been validated
            new_score = get_critical_score(scores_to_validate)
            assignment.current_score = new_score
            assignment.save()
            #delete
            print "New SCORE first", new_score
            redirect_assignment = assignment

        # if there are no scores
        else:
            # mark assignment as done
            assignment.done = True
            # get the first assignment that is not 
            # done associated with the user
            assignments = ValAssignment.objects.filter(
                user = request.user,
                done = False
            )
            redirect_assignment = assignments[0]
            # Associate the most critical score that has not
            # been validated
            scores = Score.objects.filter(
                experiment = experiment,
                command = redirect_assignment.command,
                lexicon_number = redirect_assignment.lexicon_number
                ).exclude(id__in=[o.id for o in redirect_assignment.evaluated_scores.all()])
            new_score = get_critical_score(scores)
            #delete
            print "New SCORE", new_score
            redirect_assignment.current_score = new_score
            redirect_assignment.save()
        # Redirect to the valdation with a new assignment
        # and its current score
        return redirect('validation_edit',
        redirect_assignment.pk, redirect_assignment.current_score.pk)


    vac_number = len(Vac.objects.filter(experiment=experiment))
    all_assignments = ValAssignment.objects.filter(user=request.user)
    validation_number = 0
    if len(assignment.evaluated_scores.all()) == vac_number -1:
            last_vac = True
    for a in all_assignments:
        if a.done:
            validation_number += vac_number
        else:
            validation_number += len(a.evaluated_scores.all())
    if has_role(request.user,'expert'):
    	hundred_percent = experiment.expert_cmd_n*9*vac_number
    elif has_role(request.user,'student'):
    	hundred_percent = experiment.student_cmd_n*9*vac_number
    progress = int(math.floor(validation_number*100/hundred_percent))

    # Decide on the Range:
    if assignment.previous_validation:
        str_numbers = assignment.previous_validation.selected_lexicons.split('.')
        subjects = []
        for elem in str_numbers[:-1]:
            # delete
            print "ELEM", elem
            subjects.append(int(elem))
    else:
        subjects = range(1,10)

    return render(request, template_name, {
        'form':form,
        'assignment':assignment,
        'command': assignment.command,
        'score': score,
        'vac': score.vac,
        'range': subjects,
        'thermometer_value': score.score*100,
        'last_vac': last_vac,
        'progress': progress})

@has_permission_decorator('update_evaluation')
def validation_index(request):
    template = loader.get_template('vacs/validation_index.html')
    return HttpResponse(template.render({},request))

@has_permission_decorator('update_evaluation')
def finished(request):
    template = loader.get_template('vacs/finished.html')
    return HttpResponse(template.render({},request))
