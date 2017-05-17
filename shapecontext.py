import numpy as np 

def cart2logpol(X):
	temp = np.sqrt(np.sum(np.square(X), axis=1))
	rho = np.power(temp/np.max(temp),0.67)
	theta = np.arctan2(np.sqrt(np.sum(np.square(X[:,:1]),axis=1)),X[:,2])
	phi = np.arctan2(X[:,1],X[:,0])
	points = np.zeros(np.shape(X))
	points[:,0] = rho
	points[:,1] = theta + np.pi -0.0001
	points[:,2] = phi + np.pi -0.0001
	return points

def quantangle(points,bin):
	output = np.digitize(points,bin,right=True)
	output[np.argwhere(output==0)] = 1
	output = output-1
	return output

def quantrho(points,bin):
	output = np.digitize(points, bin, right=True)
	output = output-1
	return output

def histogram(point_shape1):
	bins = np.linspace(0, 1, 9)
	bins1 = np.linspace(0, 2 * np.pi, 9)
	bins2 = np.linspace(0, 2 * np.pi, 9)
	l,m = np.shape(point_shape1)
	histo = np.zeros((l,8*8*8),dtype='float32')

	final = np.zeros((np.max(point_shape1[:,0]).astype(np.int)+1,np.max(point_shape1[:,1]).astype(np.int)+1,np.max(point_shape1[:,2]).astype(np.int)+1,(8*8*8) + 1));
	for i in range(0,l,1):
		point = point_shape1[i,:]
		temp = point_shape1 - point
		points_shape1_log = cart2logpol(np.delete(temp,i,0))
		l,m = np.shape(points_shape1_log)
		temp1 = np.zeros((l,m),dtype = 'int')
		temp1[:,0] = quantrho(points_shape1_log[:,0], bins)
		temp1[:,1] = quantangle(points_shape1_log[:,1], bins1)
		temp1[:,2] = quantangle(points_shape1_log[:,2], bins2)
		hist_matrix = np.zeros((8,8,8))
		
		for p in range(0,l,1):
			hist_matrix[temp1[p,0],temp1[p,1],temp1[p,2]] = hist_matrix[temp1[p,0],temp1[p,1],temp1[p,2]] + 1

		hist_matrix_reshaped = np.reshape(hist_matrix,[-1,8*8*8])
		hist_matrix_reshaped = np.append(1,hist_matrix_reshaped)
		# histo[i,:] = hist_matrix_reshaped
		point = point.astype(np.int)
		final[point[0],point[1],point[2],:] = hist_matrix_reshaped
	return final

