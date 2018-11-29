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
            for evaluation in evaluations:
                evaluation = evaluation.evaluation.split(".")
                # create evaluation matrix 9x9x2
                # The first one is for the less thans in the upper
                # triangular and greater thans in the lower trian
                # gular and  The second one is for the equals.
                eval_matrix = np.zeros((2,9,9))
                # [u'9', u'<', u'5', u'<', u'8']
                for index in range(2):
                    if evaluation[index + 1] == '<':
                        m_index = 0
                    else:
                        m_index = 1
                    # Save in the upper triangular if its in order
                    g1 = int(evaluation[index])
                    g2 = int(evaluation[index+2])
                    if g1 < g2:
                        eval_matrix[m_index,g1-1,g2-1] +=1
                    # Save in the lower triangular if its in reverse
                    # order because we are dealing with a "greater than"
                    else:
                        eval_matrix[m_index,g2-1,g1-1] +=1
                # Get the values for each pair (this should be
                # a dict or a array of two).
                

                # Get the entropy for each pair

                # Get the weighted/normalized mean of the entropy

                # save in an array

            # get the mean of the  means


# make table of  less, greater, equal, and calculate entropy
# average entropies of each user
# print a table for each user
# accumululate the averages of each user and get an total average.

