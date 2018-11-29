import sys
from vacs.models import Command, Experiment, User, Vac, Evaluation,\
        Assignment, Participant, Score, ValAssignment, Validation
from vacs.utils import Order
from django.contrib.auth import get_user_model
import csv
import numpy as np

# Get all the vacs for the experiment
experiment_id = 77
vacs = Vac.objects.filter(experiment__id=77)

# for each user
participants = Participant.objects.filter(experiment__id=experiment_id)
participants = Participant.objects.filter(experiment__id=experiment_id)
for participant in participants:
    user = participant.user
    assignments = Assignment.objects.filter(user=user)
    # for each assignment
    for assignment in assignments:
        # for each vac
        for vac in vacs:
            # get all evaluations of that user with that vac
            evaluations = Evaluation.objects.filter(
                    vac=vac,
                    assignment=assignment
                    )
            # get groups of evaluations
            eval_matrix = np.zeros((2,9,9))
            for evaluation in evaluations:
                if len(evaluation.evaluation)>5:
                    evaluation = evaluation.evaluation.split(".")
                else:
                    evaluation = list(evaluation.evaluation)
                # create evaluation matrix 9x9x2
                # The first one is for the less thans in the upper
                # triangular and greater thans in the lower trian
                # gular and  The second one is for the equals.
                # [u'9', u'<', u'5', u'<', u'8']
                for index in range(0,3,2):
                    if evaluation[index + 1] == '<':
                        m_index = 0
                    else:
                        m_index = 1
                    g1 = int(evaluation[index])
                    g2 = int(evaluation[index+2])
                    eval_matrix[m_index,g1-1,g2-1] +=1

            # Get the values for each pair (this should be
            # a dict or a array of two).
            print eval_matrix
            eval_entropy = []
            for i in range(9):
                for j in range (i+1,9):
                    pair = []
                    # append pair name
                    # get pair values for "<", ">", "="
                    gt_than = eval_matrix[0,i,j]
                    less_than = eval_matrix[0,j,i]
                    eq = eval_matrix[1,i,j]+eval_matrix[1,j,i]
                    if gt_than + less_than + eq > 1 :
                        pair.append(str(i)+"-"+str(j))
                        pair.append([gt_than + less_than + eq])
            eval_entropy.append(pair)
            print eval_entropy

            # Get the entropy for each pair

            # Get the weighted/normalized mean of the entropy

            # save in an array

        # get the mean of the  means


# make table of  less, greater, equal, and calculate entropy
# average entropies of each user
# print a table for each user
# accumululate the averages of each user and get an total average.

