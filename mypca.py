import numpy as np 

def sort(eigenValues,eigenVectors):
	idx = eigenValues.argsort()[::-1]
	eigenValues = eigenValues[idx]
	eigenVectors = eigenVectors[:,idx]
	return eigenValues,eigenVectors

def pcaupdate(points):
	meanshape = np.mean(points.T,axis=0)
	points = (points.T - meanshape).T
	print ("...Calculating Covariance matrix.....")
	covar = np.cov(points)
	print covar.shape
	print ("...Eigen vectors.....")
	lam,vec = np.linalg.eig(covar)
	print ("..Sorting...")
	lam,vec = sort(lam,vec)

	topvectors = (vec[:,:20]).real
	topvalues = (lam[:20]).real

	modelparam = np.matmul(topvectors.T,points[:,0])

	return modelparam,meanshape,topvectors