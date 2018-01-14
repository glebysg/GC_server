import sys
from vacs.models import Command, Experiment, Vac, Evaluation, Assignment, Participant, Score, ValAssignment, Validation
from django.contrib.auth import get_user_model
import numpy as np
from scipy.misc import comb
import math
# Exclude ids that were not recoverable from the db
full_exclude_id = [2657, 2662, 2666, 2667, 2668, 2672, 2709, 2735, 2737, 2741, 2758, 2784, 2805, 2827, 2844, 2877, 2886, 2920, 2923, 2924, 2927, 2944, 2953, 2971, 3004, 3008, 3012, 3021]
exclude_id =  [2657, 2662, 2666, 2668, 2709, 2735, 2737, 2741, 2805, 2827, 2844, 2877, 2886, 2923, 2971, 3012]

# Get all the Validation Assignments for the experiment
experiment_id = 77
all_val_assignments = ValAssignment.objects.filter(
        user__participant__experiment__pk=experiment_id).exclude(id__in=exclude_id)
full_selections = [[0,0] for i in range(6)]
full_lax_selections = [[0,0] for i in range(6)]
final_step_selection = 0
final_lax_step_selection = 0
soft_final_step_selection = 0
hard_final_step_selection = 0
soft_final_lax_step_selection= 0
hard_final_lax_step_selection= 0
hard_judge_selections = [[0,0] for i in range(6)]
soft_judge_selections = [[0,0] for i in range(6)]
soft_lax_selections = [[0,0] for i in range(6)]
hard_lax_selections = [[0,0] for i in range(6)]
judge_dividing_factor = 1
avg_first_size =[]
avg_selection_step =[]
for assignment in all_val_assignments:
    scores = assignment.evaluated_scores.all()
    # Get all the validations for the scores 
    validations = Validation.objects.filter(score__in=scores)\
            .order_by('last_updated').reverse()
    all_lexicons = [map(int, validation.selected_lexicons[:-1].split('.')) for validation in validations]
    all_lexicons.sort(key=len,reverse=True)
    flat_lexicons = [item for sublist in all_lexicons for item in sublist]

    # Get all the validations for the scores for the lax step 
    all_lax_lexicons = [map(int, validation.selected_lexicons[:-1].split('.'))+[validation.pk] for validation in validations]
    all_lax_lexicons.sort(key=len,reverse=True)

    ####################################################
    ################## WITH HARD STEPS #################
    ####################################################

    # Get the avg selection step 
    avg_selection_step.append(len(all_lexicons))

    # Get the avg number of elements in the first selection
    if len(all_lexicons) > 1:
        avg_first_size.append(len(all_lexicons[0]))

    #####################################
    ###### FOR ALL THE JUDGES ###########
    #####################################

    # Get all the selections per step
    lexicon_index = 0
    for lexicon in all_lexicons:
        if assignment.lexicon_number in lexicon:
            full_selections[lexicon_index][0] += 1
        full_selections[lexicon_index][1] += 1
        lexicon_index += 1

    # Get selected in the last step 
    if assignment.lexicon_number in all_lexicons[-1]:
        final_step_selection += 1

    #####################################
    ###### DIVIDED BY JUDGE CRITERIA ####
    #####################################

    # Soft judges 
    if len(all_lexicons) > judge_dividing_factor:
    # Get all the selections per step
        lexicon_index = 0
        for lexicon in all_lexicons:
            if assignment.lexicon_number in lexicon:
                soft_judge_selections[lexicon_index][0] += 1
            soft_judge_selections[lexicon_index][1] += 1
            lexicon_index += 1

        # Get selected in the last step 
        if assignment.lexicon_number in all_lexicons[-1]:
            soft_final_step_selection += 1
    # harsh judges
    else:
    # Get all the selections per step
        lexicon_index = 0
        for lexicon in all_lexicons:
            if assignment.lexicon_number in lexicon:
                hard_judge_selections[lexicon_index][0] += 1
            hard_judge_selections[lexicon_index][1] += 1
            lexicon_index += 1

        # Get selected in the last step 
        if assignment.lexicon_number in all_lexicons[-1]:
            hard_final_step_selection += 1

    ####################################################
    ################## WITH LAX STEPS ##################
    ####################################################
    lax_step = 3

    #####################################
    ###### FOR ALL THE JUDGES ###########
    #####################################

    # Get all the selections per step
    lexicon_index = 0
    for lexicon in all_lax_lexicons:
        # Get the next 3 closest to the assigned
        val = Validation.objects.get(pk=lexicon[-1])
        val_score = val.score
        all_lexicon_scores = Score.objects.filter(
                experiment=val_score.experiment,
                vac=val_score.vac,
                command=val_score.command)
        for s in all_lexicon_scores:
            s.diff_score = abs(s.score-val_score.score)
        sorted_scores = sorted(list(all_lexicon_scores), key=lambda s:s.diff_score)
        lax_set = set([s.lexicon_number for s in sorted_scores[:lax_step+1]])
        if bool(lax_set.intersection(set(lexicon[:-1]))):
            full_lax_selections[lexicon_index][0] += 1
        full_lax_selections[lexicon_index][1] += 1
        lexicon_index += 1

    # Get selected in the last step 
    # Get the next 3 closest to the assigned
    val = Validation.objects.get(pk=all_lax_lexicons[-1][-1])
    val_score = val.score
    all_lexicon_scores = Score.objects.filter(
            experiment=val_score.experiment,
            vac=val_score.vac,
            command=val_score.command)
    for s in all_lexicon_scores:
        s.diff_score = abs(s.score-val_score.score)
    sorted_scores = sorted(list(all_lexicon_scores), key=lambda s:s.diff_score)
    lax_set = set([s.lexicon_number for s in sorted_scores[:lax_step+1]])
    if bool(lax_set.intersection(set(all_lax_lexicons[-1][:-1]))):
        final_lax_step_selection += 1

    #####################################
    ###### DIVIDED BY JUDGE CRITERIA ####
    #####################################

    # Soft judges 
    if len(all_lexicons) > judge_dividing_factor:
        # Get all the selections per step
        lexicon_index = 0
        for lexicon in all_lax_lexicons:
            # Get the next 3 closest to the assigned
            val = Validation.objects.get(pk=lexicon[-1])
            val_score = val.score
            all_lexicon_scores = Score.objects.filter(
                    experiment=val_score.experiment,
                    vac=val_score.vac,
                    command=val_score.command)
            for s in all_lexicon_scores:
                s.diff_score = abs(s.score-val_score.score)
            sorted_scores = sorted(list(all_lexicon_scores), key=lambda s:s.diff_score)
            lax_set = set([s.lexicon_number for s in sorted_scores[:lax_step+1]])
            if bool(lax_set.intersection(set(lexicon[:-1]))):
                soft_lax_selections[lexicon_index][0] += 1
            soft_lax_selections[lexicon_index][1] += 1
            lexicon_index += 1

        # Get selected in the last step 
        # Get the next 3 closest to the assigned
        val = Validation.objects.get(pk=all_lax_lexicons[-1][-1])
        val_score = val.score
        all_lexicon_scores = Score.objects.filter(
                experiment=val_score.experiment,
                vac=val_score.vac,
                command=val_score.command)
        for s in all_lexicon_scores:
            s.diff_score = abs(s.score-val_score.score)
        sorted_scores = sorted(list(all_lexicon_scores), key=lambda s:s.diff_score)
        lax_set = set([s.lexicon_number for s in sorted_scores[:lax_step+1]])
        if bool(lax_set.intersection(set(all_lax_lexicons[-1][:-1]))):
            soft_final_lax_step_selection += 1


    # harsh judges
    else:
    # Get all the selections per step
        # Get all the selections per step
        lexicon_index = 0
        for lexicon in all_lax_lexicons:
            # Get the next 3 closest to the assigned
            val = Validation.objects.get(pk=lexicon[-1])
            val_score = val.score
            all_lexicon_scores = Score.objects.filter(
                    experiment=val_score.experiment,
                    vac=val_score.vac,
                    command=val_score.command)
            for s in all_lexicon_scores:
                s.diff_score = abs(s.score-val_score.score)
            sorted_scores = sorted(list(all_lexicon_scores), key=lambda s:s.diff_score)
            lax_set = set([s.lexicon_number for s in sorted_scores[:lax_step+1]])
            if bool(lax_set.intersection(set(lexicon[:-1]))):
                hard_lax_selections[lexicon_index][0] += 1
            hard_lax_selections[lexicon_index][1] += 1
            lexicon_index += 1

        # Get selected in the last step 
        # Get the next 3 closest to the assigned
        val = Validation.objects.get(pk=all_lax_lexicons[-1][-1])
        val_score = val.score
        all_lexicon_scores = Score.objects.filter(
                experiment=val_score.experiment,
                vac=val_score.vac,
                command=val_score.command)
        for s in all_lexicon_scores:
            s.diff_score = abs(s.score-val_score.score)
        sorted_scores = sorted(list(all_lexicon_scores), key=lambda s:s.diff_score)
        lax_set = set([s.lexicon_number for s in sorted_scores[:lax_step+1]])
        if bool(lax_set.intersection(set(all_lax_lexicons[-1][:-1]))):
            hard_final_lax_step_selection += 1


avg_first_size = round(np.mean(avg_first_size),2)
print "Total Selections by step:"
print full_selections
print "Total Selections in the last step:"
print final_step_selection
print "Avg First Step Selection size (if there is more than one step)"
print avg_first_size
print "random chance of choosing the right value on the second step"
print round(comb(8,math.ceil(avg_first_size-1.))/comb(9,math.ceil(avg_first_size))*1.0/math.ceil(avg_first_size),2)
print "Avg selection step"
print round(np.mean(avg_selection_step),2)

print "####################################"
print "Total Soft Selections by step:"
print soft_judge_selections
print "Total Soft Selections in the last step:"
print soft_final_step_selection
print "Total hard Selections by step:"
print hard_judge_selections
print "Total hard Selections in the last step:"
print hard_final_step_selection

print "####################################"
print "Total Lax  Selections by step:"
print full_lax_selections
print "Total Selections in the last step:"
print final_lax_step_selection

print "####################################"
print "Total Soft judge lax Selections by step:"
print soft_lax_selections
print "Total Soft judge lax Selections in the last step:"
print soft_final_lax_step_selection
print "Total hard judge lax Selections by step:"
print hard_lax_selections
print "Total hard judge lax Selections in the last step:"
print hard_final_lax_step_selection
