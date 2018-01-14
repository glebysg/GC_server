import sys
from vacs.models import Command, Experiment, Vac, Evaluation,\
        Assignment, Participant, Score, ValAssignment, Validation
from django.contrib.auth import get_user_model
import csv
import numpy as np


# Get all the Scores for the experiment 
experiment_id = 77
scores = Score.objects.filter(experiment__id=77)
vacs = Vac.objects.filter(experiment__id=77)
commands = Command.objects.all()

write_data = [["Lexicons"],[1],[2],[3],[4],[5],[6],[7],[8],[9]]
with open('gestureclean/analytics/avg_scores.csv', 'w') as filewriter:
    writer = csv.writer(filewriter)
    for vac in vacs:
        write_data[0].append(vac.name)
        scores_for_vac = scores.filter(vac=vac)
        for lexicon_index in range(1,10):
            scores_for_lexicon = scores_for_vac.filter(lexicon_number=lexicon_index)
            vac_mean = round(np.mean([s.score for s in scores_for_lexicon]),2)
            write_data[lexicon_index].append(vac_mean)
    writer.writerows(write_data)


for vac in vacs:
    write_data = [["Count", "Command Name",
        "L1",
        "L2",
        "L3",
        "L4",
        "L5",
        "L6",
        "L7",
        "L8",
        "L9"]]
    with open('gestureclean/analytics/'+vac.name+'_scores.csv', 'w') as filewriter:
        writer = csv.writer(filewriter)
        counter = 0
        for command in commands:
            row = []
            counter +=1
            score_vals = [-10000000]*9
            row.append(counter)
            row.append(command.name)
            scores_vac_command = scores.filter(vac=vac,command=command)
            for s in scores_vac_command:
                score_vals[s.lexicon_number-1] = s.score
            row = row + score_vals
            write_data.append(row)
        writer.writerows(write_data)
