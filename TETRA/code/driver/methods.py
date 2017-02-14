# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
########## TETRA Framework ##########

#######    Methods Available:
#######   - UniOfflineCPDetection

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

##### Import Libraries #####
import os, sys
sys.path.append('../visual')
from plot import *
sys.path.append('../date')
from dataManage import *
sys.path.append('../methods')
from cumsum import *
from bayesian_offline_changepoint_detection import *
from featureEng import *
sys.path.append('../stats')
from distributions import *

##### DEBUG #####
DEBUG = True

##### UniOfflineCPDetection
### Description: Changepoint Detection Framework given TimeSeries in a given file
### Input: - String
### Output: - ----
#
def UniOfflineCPDetection(fname):

	#################### Read Input Data ####################
	dates, f = ReadInputData(fname)
	if DEBUG: PlotSimple(f,dates,fname)

	#################### Preprocessing ####################
	##### Outlier Removal
	window, threshold = 20, 0.275
	feng1, index, numOutliers = RemoveOutliers(f,window,threshold)
	dateseng = [dates[i] for i in index]

	##### 0-1 Scaling
	feng2, Lup, Llow = FeatureScaling(feng1)

	##### Smooth/Filtering Data #####
	window, degree = 11, 5
	feng2 = FilterData(feng2,window,degree)

	if DEBUG: PlotPreprocess(feng1,feng2,dateseng)

	#################### Probabilistic Setup ####################

	##### Compute Estimate Number Change Points #####
	h = 10
	estimNumCps, _ = CuSum(feng2,dateseng,h)

	print "\t\t "
	print "\t\t------------------------------------------------------"
	print "\t\t|      \t\tPREPROCESSING\t\t\t     |"
	print "\t\t------------------------------------------------------"
	print "\t\t| # Number of Outliers Removed : %d \t\t     |" % (numOutliers)
	print "\t\t| # Number of Estimated Change Points : %d \t     |" % (estimNumCps)
	print "\t\t------------------------------------------------------"

	##### Priors Laplacian Distribution #####
	beta = 5 
	alpha = 0.999999 # 0.999

	##### Segment Mininum Length Constrains #####
	epsilon = -30
	distance_start = 10
	distance_end = 10
	distance_changepoint = 10
	params = [distance_changepoint, distance_start, distance_end, epsilon]

	##### Fix Probability Distribution ######
	prior_dist_numCps = Laplacian_Prior(estimNumCps, beta, alpha)
	prior_dist_Cps = Constant_Prior(len(feng2)+1)
	likelihood_function = StudentT(len(feng2))
	
	print "\t\t "
	print "\t\t------------------------------------------------------"
	print "\t\t|    \t\tPROBABILISTIC SETUP\t\t     |"
	print "\t\t------------------------------------------------------"
	print "\t\t| # Beta           : %f \t\t\t     |" % (beta)
	print "\t\t| # Alpha          : %f \t\t\t     |" % (alpha)
	print "\t\t| # Distance Start : %d \t\t\t     |" % (distance_start)
	print "\t\t| # Distance End   : %d \t\t\t     |" % (distance_end)
	print "\t\t| # Distance CP    : %d \t\t\t     |" % (distance_changepoint)
	print "\t\t------------------------------------------------------"
	
	#################### Solve MAP Problem ####################
	bayesian_offline_detection = Bayesian_Offline_ChangePoint(feng2, prior_dist_numCps, prior_dist_Cps, likelihood_function, params)

	##### Compute Optimal Parameters #####
	NumCps, locCps, Pcp = bayesian_offline_detection.optimal_joint_changepoint_loc_num()

	##### Rank Change Points #####
	RankCps = bayesian_offline_detection.rank_changepoints(locCps,Pcp)

	##### Revert Preprocessing #####
	if len(locCps) > 0:
		locCps, rankCps = index[locCps], index[RankCps]
		

	print "\t\t "
	print "\t\t------------------------------------------------------"
	print "\t\t|    \t\tCHANGE POINT LOCATION\t\t     |"
	print "\t\t------------------------------------------------------"
	for i in range(len(locCps)):
		print "\t\t|    \t\t %d. Date : %s \t\t     |" % (i,dates[locCps[i]].strftime("%Y-%m-%d"))
		print "\t\t------------------------------------------------------"


	print "\t\t "
	print "\t\t------------------------------------------------------"
	print "\t\t|\t\tRANKED CHANGE POINT LOCATION\t     |"
	print "\t\t------------------------------------------------------"
	for i in range(len(rankCps)):
		print "\t\t|    \t\t %d. Date : %s \t\t     |" % (i,dates[rankCps[i]].strftime("%Y-%m-%d"))
		print "\t\t------------------------------------------------------"
	print " "

	#################### Write Output Data ####################
	PlotChangePoints(f,locCps,dates,fname)
	WriteOutputData(fname,locCps,dates)
