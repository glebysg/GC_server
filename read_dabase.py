import numpy as np
from scipy.io import savemat

from vacs.models import Experiment, Vac, Participant, Command, Score, Validation, Assignment, Evaluation, ValAssignment

## Obtaining the Vacs
vacs = [str(vac.name) for vac in Vac.objects.all()]
print 'VACS: ', len(vacs), ' ', vacs

## Comamnd Names
commands_dict = {str(cmd.code):str(cmd.name) for cmd in Command.objects.all()}
commands = [str(cmd.name) for cmd in Command.objects.all()]
print 'Command Names: ', len(commands), ' ', commands

## Participants
part_ids = [str(part.user) for part in Participant.objects.all()]
print 'Participant IDs: ', len(part_ids), ' ', part_ids

total_scores = Score.objects.all()
lexicon_ids = list(set([int(score.lexicon_number) for score in total_scores]))
print 'Lexicon IDs: ', len(lexicon_ids), ' ', lexicon_ids


score_dict = {(str(score.command.name), int(score.lexicon_number), str(score.vac.name) ): float(score.score) for score in total_scores}
# print score_dict

A = np.zeros((len(commands), len(lexicon_ids), len(vacs)))

for cmd_idx in range(len(commands)):
    for lex_idx in range(len(lexicon_ids)):
        for vac_idx in range(len(vacs)):
            # print commands[cmd_idx], lexicon_ids[lex_idx], vacs[vac_idx]
            A[cmd_idx, lex_idx, vac_idx] = score_dict[commands[cmd_idx], lexicon_ids[lex_idx], vacs[vac_idx]]


final_dict = {'commands': commands, 'lexicon_ids': lexicon_ids, 'vacs': vacs, 'scores': A}
savemat('scores.mat', final_dict)
np.savez('scores.npz', commands=commands, lexicon_ids=lexicon_ids, vacs=vacs, scores=A)


# assns = Assignment.objects.all()
# assignments = [(assn.command, assn.user, assn.lexicon_order, assn.current_comparison, assn.current_vac, assn.evaluated_vacs, assn.done) for assn in assns]
# print assignments[0]

# evals = Evaluation.objects.all()
# evaluations = [(eva.assignment, eva.vac, eva.evaluation, eva.number) for eva in evals]
# print evaluations[0]

# vals = Validation.objects.all()
# validations = [ (val.score.score, val.selected_lexicons) for val in vals]
# print validations[0]

# val_assns = ValAssignment.objects.all()
# for assn in val_assns:
#     if assn.done:
#         print [(assn.command.name, assn.lexicon_number, assn.previous_validation.selected_lexicons, assn.current_score.score, assn.evaluated_scores.score) for assn in val_assns]
# print val_assignments[-1]
