# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
########## Test Change Point Detection Performance ##########

#######    Functions:
#######   - CuSumCPDetection
#######   - BestCpExplain

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

##### Import Libraries #####
from __future__ import division
if __name__ == "__main__":
	import os, sys
	os.chdir(os.path.abspath(os.path.join(os.getcwd(), '..')))
	sys.path.append('driver')
from library import *

DEBUG = False

##### CuSumCPDetection
### Description: CuSum Changepoint Detection Framework given TimeSeries in a given file
### Input: - String
### Output: - ----
#
def CuSumCPDetection(fname):

	#################### Read Input Data ####################
	dates, f = ReadInputData(fname)
	PlotSimple(f,dates,fname)

	#################### Preprocessing ####################
	##### Outlier Removal
	window, threshold = 20, 0.31
	feng1, index, numOutliers = RemoveOutliers(f,window,threshold)
	dateseng = [dates[i] for i in index]

	##### 0-1 Scaling
	feng2, Lup, Llow = FeatureScaling(feng1)

	##### Smooth/Filtering Data #####
	window, degree = 11, 6
	feng2 = FilterData(feng2,window,degree)

	if DEBUG: PlotPreprocess(feng1,feng2,dateseng)

	#################### Algorithm ####################

	##### Compute Estimate Number Change Points #####
	h = 12.5
	_, locCps = CuSum(feng2,dateseng,h)

	##### Revert Preprocessing #####
	locCps = index[locCps]

	#################### Write Output Data ####################
	PlotChangePoints(f,locCps,dates,fname)
	WriteOutputData(fname,locCps,dates)


##### FUNCTION: ReadInputData 
### Description: Return optimal changepoint location given ground truth
### Input: List, List
### Output: List
def BestCpExplain(locCpTrue, locCpMeth):

		# Initicialise Parameters
		N, M = locCpTrue.size, locCpMeth.size
		dist = np.ones((N, M))*np.inf
		prev_search = []
		beta = 10

		# Create Matrix with distance between every two points that complain with the cost function
		active_row = np.ones(N, dtype = bool)
		for i in range(N):
			count = False
			for j in range(M):
				tmp = fabs(locCpTrue[i]-locCpMeth[j])
				if tmp < beta:
					dist[i, j] = tmp
					count = True
			active_row[i] = count

		# Create all possible combinations
		for i in range(dist.shape[0]):
			next_search = []
			for j in range(dist.shape[1]):
				if dist[i, j] != np.inf:
					if not prev_search:
						next_search.append([[[i,j]], int(dist[i, j])])
					else:
						for item in prev_search:
							if j not in list(zip(*item[0])[1]):
								next_search.append([item[0]+[[i,j]], int(item[1]+dist[i, j])])
			next_search += prev_search				
			prev_search = next_search[:]

		# Compute Optimal Solution
		if prev_search:
			max_len = len(max(prev_search, key = lambda x: len(x[0]))[0])
			prev_search = [item for item in prev_search if len(item[0]) == max_len]
			tmp = min(prev_search, key = lambda x: x[1])[0]

			# Fentch Optimal Solution
			res = np.ones(N)*np.inf
			res[list(zip(*tmp)[0])] = locCpMeth[list(zip(*tmp)[1])]
		else:
			res = np.array([])

		print res

		return res

def main():

	##### SET NUMBER OF TRIAL #####
	numTrials = 5
	RecallTetra = PrecisionTetra = PrecisionCuSum = RecallCuSum = 0

	for _ in range(numTrials):

		##### GENERATE SYNTHETIC DATA #####
		fname1, fname2 = syntheticData()
		
		for method in [UniOfflineCPDetection, CuSumCPDetection]:

			##### CHANGE POINT ANALYSIS ON SYNTHETIC DATA - TETRA #####
			method(fname1)

			##### OPTIMAL TRUE/DETECTED CHANGEPOINT MATCHING #####
			locCpTrue, _ = ReadCPData(fname2)
			locCpMeth, dates = ReadCPData(fname1)
			locCpOpt  = BestCpExplain(locCpTrue,locCpMeth)

			if DEBUG:

				print "\t\t "
				print "\t\t------------------------------------------------------"
				print "\t\t|\t\tTRUE CHANGE POINT LOCATION\t       |"
				print "\t\t------------------------------------------------------"
				for i in range(len(locCpTrue)):
					print "\t\t|    \t\t %d. Date : %s \t\t     |" % (i,dates[locCpTrue[i]].strftime("%Y-%m-%d"))
					print "\t\t------------------------------------------------------"
				print " "

				print "\t\t "
				print "\t\t------------------------------------------------------"
				print "\t\t|    OPTIMAL EXPLANATION CHANGE POINT LOCATION\t     |"
				print "\t\t------------------------------------------------------"
				for i in range(len(locCpOpt)):
					if locCpOpt[i] != np.inf:
						print "\t\t|    \t\t %d. Date : %s \t\t     |" % (i,dates[int(locCpOpt[i])].strftime("%Y-%m-%d"))
						print "\t\t------------------------------------------------------"
				print " "

			##### COMPUTE SCORE #####
			count=0
			for item in locCpOpt:
				if item != np.inf: count += 1

			if method.__name__ is "UniOfflineCPDetection":
				PrecisionTetra += float(count)/len(locCpMeth)*100
				RecallTetra += float(count)/len(locCpTrue)*100
			else:
				PrecisionCuSum += float(count)/len(locCpMeth)*100
				RecallCuSum += float(count)/len(locCpTrue)*100

	PrecisionTetra = PrecisionTetra/numTrials		
	RecallTetra = RecallTetra/numTrials

	PrecisionCuSum = PrecisionCuSum/numTrials		
	RecallCuSum = RecallCuSum/numTrials

	print " "
	print "\t\t------------------------------------------------------"
	print "\t\t|\t\t\tRESULTS TETRA\t\t\t|"
	print "\t\t------------------------------------------------------"
	print "\t\t|     Recall: %f  ##  Precision: %f    |" % (RecallTetra, PrecisionTetra)
	print "\t\t------------------------------------------------------"
	print "\t\t|\t\t\tRESULTS CUSUM\t\t\t|"
	print "\t\t------------------------------------------------------"
	print "\t\t|     Recall: %f  ##  Precision: %f    |" % (RecallCuSum, PrecisionCuSum)
	print "\t\t------------------------------------------------------"
	print " "

if __name__ == "__main__":
	main()


	








