import sys
from vacs.models import Command, Experiment, Vac, Evaluation, Assignment, Participant, Score
from django.contrib.auth import get_user_model
import random

# CREATE EXPERIMENT
User = get_user_model()
user = User.objects.get(username='glebys')
experiment = Experiment.objects.create(
        name='Artificial Experiment',
        student_n=10,
        expert_n=9,
        student_cmd_n=2,
        expert_cmd_n=1,
        owner=user)
experiment.save()

# CREATE VACS
for i in range(5):
    vac = Vac.objects.create(
        experiment=experiment,
        name='VAC'+str(i + 1),
        description='Description of VAC'+str(i + 1)
    )
    vac.save()

# CREATE EVALUATIONS
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
symbols = ['.=.','.<.']

participants = Participant.objects.filter(experiment__id=experiment.pk)
for participant in participants:
    assignments = Assignment.objects.filter(user=participant.user)
    for assignment in assignments:
        lexicon_order = assignment.lexicon_order
        vacs = Vac.objects.filter(experiment__id=experiment.pk)
        for vac in vacs:
            element_count = 0
            for elements in experimental_design:
                positions = [letters.index(elem) for elem in elements]
                eval_value = str(positions[0]) + random.choice(symbols) + \
                        str(positions[1]) + random.choice(symbols) + str(positions[2])
                evaluation = Evaluation.objects.create(
                        assignment = assignment,
                        vac = vac,
                        evaluation = eval_value,
                        number = element_count)
                evaluation.save()
                element_count +=1
        assignment.done = True
        assignment.save()
