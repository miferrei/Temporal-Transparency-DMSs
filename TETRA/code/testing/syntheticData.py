##### Import Libraries #####
if __name__ == "__main__":
	import os, sys
	os.chdir(os.path.abspath(os.path.join(os.getcwd(), '..')))
	sys.path.append('driver')
from library import *


DEBUG = False

def CreateDates(T):
	startDate = date = datetime.datetime(1999,1,1,12,0,0)
	dates = [startDate]
	for _ in range(1, T):
		date = date + datetime.timedelta(days=1)
		dates.append(date)
	endDate = date

	startDate = startDate.strftime("%Y-%m-%d")
	endDate = endDate.strftime("%Y-%m-%d")

	return dates, startDate, endDate

def syntheticData():
	#################### SETUP EXPERIMENT ####################
	##### Number of Samples | Change Point Location #####
	T = 1000 #300 
	locCps = range(80,1000,80) #range(30,300,50) 

	##### Define Prior HyperParameters #####
	scale = 0.005
	shape = 6.0
	mu0 = 1000
	kappa0 = 1

	#################### GENERATE DATA ####################
	f = np.zeros(T)

	##### Set Inital Mean and Variance #####
	ivar = np.random.gamma(shape, scale)
	muT = mu = np.random.normal(mu0, (kappa0*ivar)**-1)

	if DEBUG:
		print 'Mean:', mu, 'Inverse Variance:', ivar**-1

	for t in range(T):

		##### Change Point #####
		if t in locCps:
			##### Update Mean and Variance #####
			ivar = np.random.gamma(shape, scale)
			muT = np.random.normal(mu0, (kappa0*ivar)**-1)
			while (30>ivar**-1 or ivar**-1>50) or fabs(muT-mu)<25:
				ivar = np.random.gamma(shape, scale)
				muT = np.random.normal(mu0, (kappa0*ivar)**-1)
			mu = muT
			if DEBUG:
				print 'Mean:', mu, 'Inverse Variance:', ivar**-1

		f[t] = np.random.normal(mu, ivar**-1)

	dates, startDate, endDate = CreateDates(T)

	#################### WRITE DATA ####################
	fname1 = "SD/numPoint%dnumCps%d_%s_%s.txt" % (T,len(locCps),startDate,endDate)
	fname2 = "SD/CpListnumPoint%dnumCps%d_%s_%s.txt" % (T,len(locCps),startDate,endDate)

	PlotSimple(f,dates,fname1)
	WriteSyntheticData(fname1,fname2,locCps,f,dates)

	return fname1, fname2

# def main():
# 	syntheticData()

# if __name__ == "__main__":
# 	main()
