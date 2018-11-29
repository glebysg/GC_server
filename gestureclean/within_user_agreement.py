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
                evaluation = evaluation.split(".")
                # create evaluation matrix 9x9x2
                # The first one is for the less thans and
                # The second one os for the equals.
                eval_matrix = np.zeros((9,9,2))
                # Get the values for each pair (this should be
                # a dict or a array of two).

                # Get the entropy for each pair

                # Get the weighted/normalized mean of the entropy

                # save in an array

            # get the mean of the  means


                print evaluation.evaluation
# make table of  less, greater, equal, and calculate entropy
# average entropies of each user
# print a table for each user
# accumululate the averages of each user and get an total average.

