import sys
from vacs.models import Command, Experiment, User, Vac, Evaluation,\
        Assignment, Participant, Score, ValAssignment, Validation
from vacs.utils import Order
from django.contrib.auth import get_user_model
import csv
import numpy as np
from scipy.stats import entropy
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Get all the vacs for the experiment
experiment_id = 77
vacs = Vac.objects.filter(experiment__id=77)

# for each user
participants = Participant.objects.filter(experiment__id=experiment_id)
participants = Participant.objects.filter(experiment__id=experiment_id)
consistency_means=[]
user_consistency = []
for participant in participants:
    within_user_consistency = []
    within_user_consistency_means = []
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
                # do the last comparison
                if evaluation[1] == '<' or evaluation[3] == '<':
                    m_index = 0
                else:
                    m_index = 1
                g1 = int(evaluation[0])
                g2 = int(evaluation[4])
                eval_matrix[m_index,g1-1,g2-1] +=1

            # Get the values for each pair (this should be
            # a dict or a array of two).
            eval_entropy = []
            for i in range(9):
                for j in range (i+1,9):
                    # append pair name
                    # get pair values for "<", ">", "="
                    gt_than = eval_matrix[0,i,j]
                    less_than = eval_matrix[0,j,i]
                    eq = eval_matrix[1,i,j]+eval_matrix[1,j,i]
                    if gt_than + less_than + eq > 1:
                        pair = []
                        pair.append(str(i)+"-"+str(j))
                        pair.append([gt_than , less_than, eq])
                        # Get the entropy for each pair
                        pair.append( entropy(pair[-1]))
                        eval_entropy.append(pair)
            within_user_consistency.append(eval_entropy)
            # Get the weighted/normalized mean of the entropy
            # Per evaluation
            within_user_consistency_means.append(np.mean([(sum(val_list)*entr)/15.0 \
                     for pair, val_list, entr in eval_entropy]))
            # print eval_entropy
    # Get the mean of all evaluations
    consistency_means.append(within_user_consistency_means)
consistency_means = np.array(consistency_means)
flattened_means = reduce(lambda x,y:x+y , consistency_means)
print flattened_means
print "////////////////////////////"
print "MEAN ENTROPY:", np.mean(flattened_means)
print "MAX VALUE", np.max(flattened_means)
print "MEDIAN VALUE", np.median(flattened_means)
plt.scatter(range(len(flattened_means)), flattened_means)
plt.show()

# Get the mean of all users
