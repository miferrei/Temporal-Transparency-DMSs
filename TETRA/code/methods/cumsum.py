# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
########## SubOptimal Two-Sided CUSUM Algorithm ##########

#######    Methods Available:
#######   - CUSUM Algorithm

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


##### Import Libraries #####
from __future__ import division
from math import exp
import numpy as np 
from dataManage import *
from plot import PlotCumSum

DEBUG = True

##### Remove Outilier
### Description: SubOptimal Two-sided CuSum Algorithm Outputting Number and Set of Change Points  
### Input: - Np Array, List, Int
### Output: - Int, List
#
def CuSum(x,dates,h):

	##### Initicialize Data Structures #####
	cp = []
	sp, sm = np.zeros(len(x), dtype=float), np.zeros(len(x), dtype=float)
	Sp, Sm = np.zeros(len(x), dtype=float), np.zeros(len(x), dtype=float)
	Gp, Gm = np.zeros(len(x), dtype=float), np.zeros(len(x), dtype=float)


	##### Set Initial Parameters #####
	### Set Decision Threholds ###
	delta = float(0.2)
	mu = float(0.4)
	nu = float(0.01)

	i, j = 0, -1
	while i<len(x):
		##### MLE Sequentical Estimates #####
		k=i-j
		if k>1:
			nu = (k-1)/k*nu + (k-1)/(k**2)*(x[i-1]-mu)**2
			mu = mu + 1/k*(x[i-1]-mu)

		sp[i], sm[i] = delta/nu*(x[i]-mu-delta/2), -delta/nu*(x[i]-mu+delta/2)
		Sp[i], Sm[i] = Sp[i-1] + sp[i], Sm[i-1] + sm[i]
		Gp[i], Gm[i] = max(Gp[i-1]+sp[i],0), max(Gm[i-1]+sm[i],0)
		if (Gp[i]>h or Gm[i]>h):
			if (Gp[i]>h):
				i = np.argmin(Sp)
				cp.append(i)
			else:
				j = np.argmin(Sm)
				cp.append(i)
			sp, sm = np.zeros(len(x), dtype=float), np.zeros(len(x), dtype=float)
			Sp, Sm = np.zeros(len(x), dtype=float), np.zeros(len(x), dtype=float)
			Gp, Gm = np.zeros(len(x), dtype=float), np.zeros(len(x), dtype=float)
			mu,nu = float(0.4), float(0.01)
			j = i
		i += 1


	print "\t\t "
	print "\t\t------------------------------------------------------"
	print "\t\t|\t\tCUMSUM CHANGE POINT LOCATION\t     |"
	print "\t\t------------------------------------------------------"
	for i in range(len(cp)):
		print "\t\t|    \t\t %d. Date : %s \t\t     |" % (i,dates[cp[i]].strftime("%Y-%m-%d"))
		print "\t\t------------------------------------------------------"
	print " "

	if DEBUG: PlotCumSum(x,cp,dates)
	

	return len(cp), cp
