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
import scipy.stats as stats
import matplotlib.gridspec as gridspec

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
final_mean =np.mean(consistency_means)
final_median = np.median(consistency_means)
print "////////////////////////////"
print "MEAN ENTROPY:", final_mean
print "MAX VALUE", np.max(consistency_means)
print "MEDIAN VALUE", final_median


###### Scatter plot ###############
plt.scatter(range(len(consistency_means)), consistency_means, c="#1200c9")
plt.plot([0,250],[final_mean,final_mean], 'c--', label='Entropy mean')
line = plt.plot([0,250],[final_median,final_median], dashes=[2,2,10,2], c="r", label='Entropy median')
plt.setp(line, linewidth=3)
plt.xlabel('Evaluation instances (for a command-criterion pair)')
plt.ylabel('Average entropy of each evaluation')
plt.legend()
# plt.show()
plt.savefig('entropy_scatter.png', bbox_inches='tight', dpi=300)
plt.clf()



###### HISTOGRAM ###############
n_bins = 20
cm = plt.cm.get_cmap('RdYlBu_r')

# Get the histogramp
Y,X = np.histogram(consistency_means, n_bins, normed=1)
x_span = X.max()-X.min()
C = [cm(((x-X.min())/x_span)) for x in X]

plt.bar(X[:-1],Y,color=C,width=X[1]-X[0],edgecolor='k')
plt.xlabel('Evaluations entropy value')
plt.ylabel('Number of evaluations (of a command-criterion pair)')
# plt.show()
plt.savefig('entropy_hist.png', bbox_inches='tight', dpi=300)
plt.clf()


######### PER VAC ###############
# print consistency_means_vac
matplotlib.rcParams['lines.linewidth'] = 2
vac_evals = []
index = 0
fig = plt.figure()
gs1 = gridspec.GridSpec(3, 2)
first = True
for vac in vacs:
    # get the entropies that belong to an specific vac
    print("///////////")
    filtered_consistency_means = [ent_val for vac_name, ent_val in consistency_means_vac\
            if vac_name == vac.name]
    vac_evals.append(filtered_consistency_means)
    final_mean =np.mean(filtered_consistency_means)
    final_median = np.median(filtered_consistency_means)
    print "////////////////////////////"
    print vac.name+" MEAN ENTROPY:", final_mean
    print vac.name+" MAX VALUE", np.max(filtered_consistency_means)
    print vac.name+" MEDIAN VALUE", final_median
    small_plt = fig.add_subplot(gs1[index])
    small_plt.scatter(range(len(filtered_consistency_means)), filtered_consistency_means, c="#1200c9")
    if first:
        l1 = small_plt.plot([0,42],[final_mean,final_mean], 'c--', label='Entropy mean')
        l2 = small_plt.plot([0,42],[final_median,final_median], dashes=[2,2,15,2], c="r", label='Entropy median')
        plt.setp(l2, linewidth=2)
        first = False
    else:
        l1 = small_plt.plot([0,42],[final_mean,final_mean], 'c--')
        l2 = small_plt.plot([0,42],[final_median,final_median], dashes=[2,2,15,2], c="r")
    vac_name = vac_name
    if vac_name == 'Complexity':
        vac_name = 'Simplicity'
    elif vac_name == 'Amount of movement':
        vac_name = 'Economy of movement'
    small_plt.set_title(vac.name)
    index +=1
gs1.tight_layout(fig, rect=(0,0,1,0.90))
fig.legend(loc='upper left')
# plt.show()
fig.savefig('all_entropy_scatter.png', dpi=600)
print(stats.f_oneway(*vac_evals))

