clear; clc; 

load('similarity_grouping')
load('scores_mat')

num_cmds = size(scores, 1);
num_subjects = size(scores, 2);
num_vacs = size(scores, 3);

sim_ids = unique(similarity_group_ids);

% Sum the VAC axis of the scores
scores(:,:,2) = 1 - scores(:,:,2); % Complexity to simplicty
scores(:,:,6) = 1 - scores(:,:,6); % amount of movement to economy of movement
scores = mean(scores, 3);

worst_lexicons = [];
best_lexicons = [];
for sim_id = sim_ids'
   group_mean = mean(scores(similarity_group_ids == sim_id, :), 1) ;
   [~, worst_lex] = min(group_mean);
   [~, best_lex] = max(group_mean);
   worst_lexicons = [worst_lexicons, worst_lex];
   best_lexicons = [best_lexicons, best_lex];
end

best_lexicons_mat = zeros(num_cmds, 1); 
worst_lexicons_mat = zeros(num_cmds, 1); 
for idx = 1 : num_cmds
    worst_lexicons_mat(idx) = worst_lexicons(find(sim_ids == similarity_group_ids(idx)));
    best_lexicons_mat(idx) = best_lexicons(find(sim_ids == similarity_group_ids(idx)));
end

S8_scores = scores(:,8);
S8_scores = S8_scores(:);
disp(sprintf('Lexicon 8:\n'))
disp([mean(S8_scores), std(S8_scores)])

S11_scores = scores((1:9) == best_lexicons_mat);
S11_scores = S11_scores(:);
disp(sprintf('Artificial Best Lexicon:\n'))
disp([mean(S11_scores), std(S11_scores)])

% S3_scores = scores(:,3);
% S3_scores = S3_scores(:);
% mean(S3_scores)
% std(S3_scores)
% 
% S10_scores = scores((1:9) == worst_lexicons_mat);
% S10_scores = S10_scores(:);
% mean(S10_scores)
% std(S10_scores)
