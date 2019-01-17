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
from matplotlib import colors
from matplotlib.ticker import PercentFormatter

# Get all the vacs for the experiment
experiment_id = 77
vacs = Vac.objects.filter(experiment__id=77)

# for each user
participants = Participant.objects.filter(experiment__id=experiment_id)
participants = Participant.objects.filter(experiment__id=experiment_id)
consistency_means=[]
consistency_means_vac=[]
test_means = []
for participant in participants:
    within_user_consistency_means = []
    within_user_consistency_means_vac = []
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

            consistency_means.append(sum([(sum(val_list)*entr)/15.0 \
                     for pair, val_list, entr in eval_entropy]))
            consistency_means_vac.append((vac.name, sum([(sum(val_list)*entr)/15.0 \
                     for pair, val_list, entr in eval_entropy])))

consistency_means = np.array(consistency_means)
print("///////////")
# exit()
flattened_means = reduce(lambda x,y:x+y , consistency_means)
final_mean =np.mean(flattened_means)
final_median = np.median(flattened_means)
print "////////////////////////////"
print "MEAN ENTROPY:", final_mean
print "MAX VALUE", np.max(flattened_means)
print "MEDIAN VALUE", final_median


###### Scatter plot ###############
plt.scatter(range(len(flattened_means)), flattened_means, c="#1200c9")
plt.plot([0,250],[final_mean,final_mean], 'r--', label='Entropy mean')
plt.xlabel('Evaluation instances (for a command-criteron pair)')
plt.ylabel('Average entntropy of each evaluation')
plt.legend()
plt.savefig('entropy_scatter.png', bbox_inches='tight', dpi=300)
plt.clf()



###### Comparative plot plot ###############
plt.scatter(range(len(test_means)), test_means, c="#1200c9")
plt.plot([0,250],[final_mean,final_mean], 'r--', label='Entropy mean')
plt.xlabel('Evaluation instances (for a command-criteron pair)')
plt.ylabel('Average entntropy of each evaluation')
plt.legend()
plt.savefig('test_scatter.png', bbox_inches='tight', dpi=300)
plt.clf()

###### HISTOGRAM ###############
n_bins = 20
# N is the count in each bin, bins is the lower-limit of the bin
N, bins, patches = plt.hist(flattened_means, bins=n_bins)
# We'll color code by height, but you could use any scalar
fracs = N / N.max()
# we need to normalize the data to 0..1 for the full range of the colormap
norm = colors.Normalize(fracs.min(), fracs.max())
# Now, we'll loop through our objects and set the color of each accordingly
for thisfrac, thispatch in zip(fracs, patches):
    color = plt.cm.viridis(norm(thisfrac))
    thispatch.set_facecolor(color)
plt.xlabel('Evaluations entropy value')
plt.ylabel('Number of evaluations (of a command-criteron pair)')

plt.savefig('entropy_hist.png', bbox_inches='tight', dpi=300)
plt.clf()


######### PER VAC ###############
# print consistency_means_vac
for vac in vacs:
    # get the entropies that belong to an specific vac
    print("///////////")
    filtered_consistency_means = [ent_val for vac_name, ent_val in consistency_means_vac\
            if vac_name == vac.name]
    final_mean =np.mean(filtered_consistency_means)
    final_median = np.median(filtered_consistency_means)
    print "////////////////////////////"
    print vac_name+"MEAN ENTROPY:", final_mean
    print vac_name+"MAX VALUE", np.max(filtered_consistency_means)
    print vac_name+"MEDIAN VALUE", final_median
