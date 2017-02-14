# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
########## Feature Engineering ##########

#######    Functions:
#######    - RemoveOutliers
#######    - FeatureScaling
#######    - FilterData

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

DEBUG = False

##### Import Libraries 
import numpy as np
from scipy.signal import savgol_filter
from scipy.ndimage.filters import uniform_filter

##### Remove Outilier
### Description: Outliers removal through comparison with shifted moving average
### Input: - Np Array, Int, Float
### Output: - Np Array, Np Array
#
def RemoveOutliers(f, W, thr):

	def MovingAvg(f, window):
		return uniform_filter(f, size=window, mode='mirror')

	start, end, n = 0, f.shape[0], f.shape[0]
	norm_f, _, _ = FeatureScaling(f)
	avg = MovingAvg(norm_f, W)
	outlier = [t for t in range(start, end) if np.linalg.norm(avg[t] - norm_f[t]) >= thr]
	index = np.delete(np.arange(n), outlier)
	feng = f[index]
	
	if DEBUG: print outlier

	return feng, index, len(outlier)

##### FUNCTION: FeatureScaling 
### Description: Scaling application data to [0-1]. Return Upper and Lower Limits
### Input: Np Array
### Output: - Np.array, float, float
#
def FeatureScaling(f):

	res = np.zeros_like(f, dtype=float)
	try:
		max_f, min_f = np.zeros(f.shape[1], dtype = float), np.zeros(f.shape[1], dtype = float)
		for i in range(f.shape[1]):
			max_f[i], min_f[i] = np.amax(f[:,i]), np.amin(f[:,i])
			res[:,i] = (f[:, i]-min_f[i]) /(max_f[i]-min_f[i])
	except IndexError:
		max_f, min_f = np.amax(f), np.amin(f)
		res = (f-min_f) /(max_f-min_f)

	return res, max_f, min_f

##### FUNCTION: FilterData
### Description: Filter data via Savitzky Golay Filter. Underlying assumption that the features 
#	are independent (and equaly weighted) for the sake of filtering. Degree of the 
#	polynomial and window size should be adjusted so to meet a particular distribution
### Input: Np Array, int, int,
### Output: - Np Array
#
def FilterData(f, W, deg):

	res = np.zeros_like(f)
	try:
		for i in range(f.shape[1]):
			res[:, i] = savgol_filter(f[:, i], W, deg)
	except IndexError:
		return  savgol_filter(f, W, deg)

	return res

	