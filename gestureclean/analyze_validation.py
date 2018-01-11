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
    all_lexicons = [map(int, validation.selected_lexicons[:-1].split('.')) for validation in validations]
    all_lexicons.sort(key=len)
    if len(all_lexicons[0]) != 1:
        final_choice += 1


    # print all_lexicons
    # if len(all_lexicons) == 1:
        # if assignment.lexicon_number in all_lexicons[0]:
            # ever_selected += 1
            # final_choice += 1
        # continue
    # smallest = [[all_lexicons[0]]]
    # largest = [[all_lexicons[-1]]]
    # for selection in all_lexicons[1:-1]:
        # if len(largest[0]) == len(selection):
            # largest.append(selection)
        # if len(smallest[0]) == len(selection):
            # smallest.append(selection)
    # for elem in largest:
        # if assignment.lexicon_number in elem:
            # ever_selected += 1
            # break
    # for elem in smallest:
        # if len(elem) > 1:
            # break
        # if assignment.lexicon_number in elem:
            # final_choice += 1
            # break
# print "Ever_selected", ever_selected
print "Final_selected", final_choice
