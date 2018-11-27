from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
import numpy as np
import sys

## Apply vif on every column of the matrix M
def vif_coeffs(M):
	'''
	Description:
		Compute VIF on every column of the matrix M
	Input arugments:
		* M: 2D np.ndarray
	Return:
		* A list of VIF for each column. Size of list is equal to no. of columns.
	'''
	return [vif(M, idx) for idx in range(M.shape[1])]


## Load the scores.npz file
data = np.load('scores.npz')
print 'Full List of VACS: '
print data['vacs'].tolist(), '\n'

## Load VAC scores matrix
vac_scores = data['scores'] # 28 x 9 x 6
## Reshape into 252 x 6
vac_scores = vac_scores.reshape(-1, 6)

###################
### All indices ###
###################
print '======= ALL COLUMNS ========'
print 'VIF Coeffecients'
print vif_coeffs(vac_scores), ''
## Eigen Decomposition
U, S, V = np.linalg.svd(vac_scores)
print 'Eigen Values'
print S.tolist()
print 'Last eigen vector'
print V[-1, :]
print '============================\n'

########################
### Ignore 5th index ###
########################
print '======= Ignore 5th VAC ========'
ignore_index = np.array([4])
mask = np.sum(np.arange(6).reshape(-1,1) == ignore_index.reshape(1,-1), axis = 1) == 0
new_vac_scores = vac_scores[:, mask]
## VIF
print 'VIF Coeffecients'
print vif_coeffs(new_vac_scores)
## Eigen Decomposition
U, S, V = np.linalg.svd(new_vac_scores)
print 'Eigen values'
print S.tolist()
print 'Last eigen vector'
print V[-1, :]
print '============================\n'

##########################
### Ignore 3 & 5 index ###
##########################
print '======= Ignore 3 & 5 VAC ========'
ignore_index = np.array([2, 4])
mask = np.sum(np.arange(6).reshape(-1,1) == ignore_index.reshape(1,-1), axis = 1) == 0
new_vac_scores = vac_scores[:, mask]
## VIF
print 'VIF Coeffecients'
print vif_coeffs(new_vac_scores)
## Eigen Decomposition
U, S, V = np.linalg.svd(new_vac_scores)
print 'Eigen values'
print S.tolist()
print 'Last eigen vector'
print V[-1, :]
print '============================\n'
