# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
########## Data Management ##########

#######    Functions:
#######   - ReadInputData

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

##### Import Libraries 
import datetime
import time
import numpy as np

# - - - - - - - - - - - - MAIN - - - - - - - - - - - - - - - - - - - - - - - - - - 

##### FUNCTION: ReadInputData 
### Description: Return application data from complete file name
### Input: String
### Output: List, Np Array 
def ReadInputData(fname):
	dates, f = [], []
	faddress = "../input_data/"+fname
	file = open(faddress)
	for line in file:
		x, y = line.strip().split(' ')
		dates.append(datetime.datetime.fromtimestamp(int(x)))
		f.append(float(y))
	file.close()
	f=np.array(f, dtype=float)
	return dates, f

##### FUNCTION: WriteOutputData 
### Description: Write changepoint data to given complete file name
### Input: String, List, Np Array 
def WriteOutputData(fname,locCps,dates):
	faddress = "../output_data/"+fname
	file = open(faddress,"w")
	for i in range(len(locCps)):
		tmp = dates[locCps[i]].strftime("%Y-%m-%d") + "\n"
		file.write(tmp)
	file.close()

def WriteSyntheticData(fname1,fname2,locCps,f,dates):

	faddress = "../input_data/"+fname1
	file = open(faddress,"w")
	for date,val in zip(dates,f):
		wrt_str=("%d %d\n") % (int(time.mktime(date.timetuple())), val)
		file.write(wrt_str)
	file.close()

	faddress = "../output_data/"+fname2
	file = open(faddress,"w")
	for cp in locCps:
		tmp = dates[cp].strftime("%Y-%m-%d") + "\n"
		file.write(tmp)
	file.close()

##### FUNCTION: ReadCPData 
### Description: Read List of Changepoints from complete file name
### Input: String, List, Np Array 
def ReadCPData(fname):
	
	fobs, startDate, endDate = fname.strip().split('/')[-1][:-4].split('_') 
	startDate = datetime.datetime.strptime(startDate,"%Y-%m-%d") 
	endDate   = datetime.datetime.strptime(endDate,"%Y-%m-%d")

	locCps = []
	faddress = "../output_data/"+fname
	file = open(faddress)
	for line in file:
		date = line.strip()
		locCps.append((datetime.datetime.strptime(date,"%Y-%m-%d")-startDate).days)
	file.close()

	locCps = np.array(locCps, dtype=int)
	dates = [startDate+datetime.timedelta(i) for i in range(int((endDate-startDate).days))]

	return locCps, dates

