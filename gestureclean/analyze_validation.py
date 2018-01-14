import sys
from vacs.models import Command, Experiment, Vac, Evaluation, Assignment, Participant, Score, ValAssignment, Validation
from django.contrib.auth import get_user_model
# Exclude ids that were not recoverable from the db
full_exclude_id = [2657, 2662, 2666, 2667, 2668, 2672, 2709, 2735, 2737, 2741, 2758, 2784, 2805, 2827, 2844, 2877, 2886, 2920, 2923, 2924, 2927, 2944, 2953, 2971, 3004, 3008, 3012, 3021]
exclude_id =  [2657, 2662, 2666, 2668, 2709, 2735, 2737, 2741, 2805, 2827, 2844, 2877, 2886, 2923, 2971, 3012]

# Get all the Validation Assignments for the experiment
experiment_id = 77
all_val_assignments = ValAssignment.objects.filter(
        user__participant__experiment__pk=experiment_id).exclude(id__in=exclude_id)
ever_selected = 0
final_choice = 0
count = 0

for assignment in all_val_assignments:
    count += 1
    scores = assignment.evaluated_scores.all()
    # Get all the validations for the scores 
    validations = Validation.objects.filter(score__in=scores)\
            .order_by('last_updated').reverse()
    # Get the smallest and the largest sets:
    all_lexicons = [map(int, validation.selected_lexicons[:-1].split('.')) for validation in validations]
    all_lexicons.sort(key=len)
    flat_lexicons = [item for sublist in all_lexicons for item in sublist]

    if len(all_lexicons[0]) != 1:
        full_exclude_id.append(assignment.id)
        if assignment.lexicon_number in all_lexicons[0]:
            exclude_id.append(assignment.id)
        print all_lexicons
        print assignment.lexicon_number
        print "///////////////////////"
print "Final_selected", final_choice
print "full excule", full_exclude_id
print "excule", exclude_id
