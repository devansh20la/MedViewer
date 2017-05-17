import numpy as np 

def costfunction(hist1,hist2):
	cost = np.sum(np.nan_to_num(np.square(hist1 - hist2)/(hist1 + hist2)))
	return cost