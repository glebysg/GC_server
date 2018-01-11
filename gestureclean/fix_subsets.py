import sys
from vacs.models import Command, Experiment, Vac, Evaluation, Assignment, Participant, Score, ValAssignment, Validation
from django.contrib.auth import get_user_model

# Get all the Validation Assignments for the experiment
experiment_id = 77
all_val_assignments = ValAssignment.objects.filter(
        user__participant__experiment__pk=experiment_id)
count = 0
error_count = 0
for assignment in all_val_assignments:
    count += 1
    scores = assignment.evaluated_scores.all()
    # Get all the validations for the scores 
    validations = Validation.objects.filter(score__in=scores).order_by('last_updated').reverse()
    # Get the smallest and the largest sets:
    all_lexicons = [map(int, validation.selected_lexicons[:-1].split('.'))+[validation.pk] for validation in validations]
    all_lexicons.sort(key=len)
    for index in range(len(all_lexicons)-1):
        current_val_pk = all_lexicons[index][-1]
        current_val = all_lexicons[index][:-1]
        next_val_pk = all_lexicons[index+1][-1]
        next_val = all_lexicons[index+1][:-1]
        if  not set(current_val).issubset(set(next_val)):
            previous_corrected_val = set([])
            for set_index in range(index, len(all_lexicons)-1):
                current_val_pk = all_lexicons[set_index][-1]
                current_val = all_lexicons[set_index][:-1]
                next_val_pk = all_lexicons[set_index+1][-1]
                next_val = all_lexicons[set_index+1][:-1]
                corrected_val = set(current_val).union(set(next_val)).union(previous_corrected_val)
                validation = Validation.objects.get(pk=next_val_pk)
                # turn the corrected val into a string
                selected_lexicons = ""
                for value in corrected_val:
                    selected_lexicons +=str(value)
                    selected_lexicons += "."
                validation.selected_lexicons = selected_lexicons
                print selected_lexicons
                previous_corrected_val = corrected_val
                validation.save()
            # print ""
            # print all_lexicon
            print "Assignment: ", assignment.pk
            print all_lexicons
            error_count += 1
            break
print "Total: ", count
print "Errors: ", error_count
