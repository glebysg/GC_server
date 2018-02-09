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
lexicon_index=8
l7_scores = scores.filter(lexicon_number=lexicon_index)

write_data = [["Command", "Score"]]
with open('gestureclean/analytics/best_lexicon.csv', 'w') as filewriter:
    writer = csv.writer(filewriter)
    counter = 0.0
    over_threshold = 0.0
    for command in commands:
        command_scores = l7_scores.filter(command=command)
        score_mean = round(np.mean([1-s.score if (s.vac.name == "Complexity" or s.vac.name == "Amount of movement") else s.score 
            for s in command_scores]),2)
        if score_mean > 0.5:
            over_threshold +=1
        write_data.append([command.name,score_mean])
        counter += 1
    write_data.append(["Commands over threshold", str((over_threshold/counter)*100)+"%"])
    writer.writerows(write_data)

fid = fopen('myfile.txt','w');
for i = 1:length(fileList)
  fprintf(fid,'%s\n',fileList{i});
end
fclose(fid);
