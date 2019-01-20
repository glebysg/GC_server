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
coefficients = vif_coeffs(vac_scores)
print coefficients, ''
index = np.argmax(coefficients)
## Eigen Decomposition
U, S, V = np.linalg.svd(vac_scores)
print 'Eigen Values'
print S.tolist()
print 'Last eigen vector'
print V[-1, :]
print '============================\n'

############################
### Ignore Largest index ###
############################
print '======= Ignore VAC with largest coefficient: '+data['vacs'][index]+' ========'
ignore_index = np.array([index])
mask = np.sum(np.arange(6).reshape(-1,1) == ignore_index.reshape(1,-1), axis = 1) == 0
new_vac_scores = vac_scores[:, mask]
## VIF
print 'VIF Coeffecients'
coefficients = vif_coeffs(new_vac_scores)
print coefficients, ''
index2 = np.argmax(coefficients)
## Eigen Decomposition
U, S, V = np.linalg.svd(new_vac_scores)
print 'Eigen values'
print S.tolist()
print 'Last eigen vector'
print V[-1, :]
print '============================\n'

if index <= index2:
    index2 += 1
else:
    index += 1

print

##########################
### Ignore 2 largest  ###
##########################
print '======= Ignore two largest coefficients: '+data['vacs'][index]+',' +data['vacs'][index2]+ ' ========'
ignore_index = np.array([index2, index])
mask = np.sum(np.arange(6).reshape(-1,1) == ignore_index.reshape(1,-1), axis = 1) == 0
new_vac_scores = vac_scores[:, mask]
## VIF
print 'VIF Coeffecients'
coefficients = vif_coeffs(new_vac_scores)
print coefficients, ''
index3 = np.argmax(coefficients)
## Eigen Decomposition
U, S, V = np.linalg.svd(new_vac_scores)
print 'Eigen values'
print S.tolist()
print 'Last eigen vector'
print V[-1, :]
print '============================\n'

