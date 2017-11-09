import sys
from vacs.models import Command, Experiment, Vac, Evaluation, Assignment, Participant, Score, ValAssignment, Validation
from django.contrib.auth import get_user_model

# Get all the Validation Assignments for the experiment
experiment_id = 77
all_val_assignments = ValAssignment.objects.filter(
        user__participant__experiment__pk=experiment_id)
ever_selected = 0
final_choice = 0
for assignment in all_val_assignments:
    scores = assignment.evaluated_scores.all()
    # Get all the validations for the scores 
    validations = Validation.objects.filter(score__in=scores)\
            .order_by('last_updated').reverse()
    # Get the smallest and the largest sets:
    smallest = []
    largest = []
    first_init = True
    for validation in validations:
        lexicon_set = map(int, validation.selected_lexicons[:-1].split('.'))
        if first_init:
            smallest.append(lexicon_set)
            largest.append(lexicon_set)
            first_init = False
        if len(largest[0]) > len(lexicon_set):
           largest = [[lexicon_set]]
        elif len(smallest[0]) < len(lexicon_set):
           smallest = [[lexicon_set]]

        if len(largest[0]) == len(lexicon_set):
            largest.append(lexicon_set)
        if len(smallest[0]) == len(lexicon_set):
            smallest.append(lexicon_set)
    for elem in largest:
        if assignment.lexicon_number in elem:
            ever_selected += 1
            break
    for elem in smallest:
        # if len(elem) > 1:
            # break
        if assignment.lexicon_number in elem:
            final_choice += 1
            break
    print "/",
    print ""
    print "Ever_selected", ever_selected
    print "Final_selected", final_choice
