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
final_step_selection = 0
hard_judge_selections = [[0,0] for i in range(6)]
soft_judge_selections = [[0,0] for i in range(6)]
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

    # Get the avg selection step 
    avg_selection_step.append(len(all_lexicons))

    # Get the avg number of elements in the first selection
    if len(all_lexicons) > 1:
        avg_first_size.append(len(all_lexicons[0]))

    #####################################
    ###### FOR ALL THE JUDJES ###########
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
    ###### DIVIDED BY JUDJE CRITERIA ####
    #####################################
 
    # Soft judjes 
    if len(all_lexicons) > judge_dividing_factor:
    # Rash judjes
        pass
    else:
        pass
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


    # if len(all_lexicons[0]) != 1:
        # full_exclude_id.append(assignment.id)
        # if assignment.lexicon_number in all_lexicons[0]:
            # exclude_id.append(assignment.id)
        # print all_lexicons
        # print assignment.lexicon_number
        # print "///////////////////////"
# print "Final_selected", final_choice
# print "full excule", full_exclude_id
# print "excule", exclude_id
