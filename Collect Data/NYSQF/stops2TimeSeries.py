##### Import Libraries #####
import sqlite3 as sq
import numpy as np
import time
import datetime 

dir = "/NS/twitter-6/work/mzafar/ComputationalDiscrimination/SQF_analysis/sqlite_data"
globalConstrains = ["datestop != ' ' ", "datestop not like '%1900%' ", "timestop != ' '"]

def Stops2TimeSeries(year, constrains):

	constrains += globalConstrains
	constrains = 'AND '.join(constrains)

	db     = "%s/%d.sqlite3" % (dir,year)
	sql    = "SELECT datestop, pct FROM sqf_data_%d WHERE %s" % (year, constrains)
	connec = sq.connect(db)
	cursor = connec.execute(sql) 
	data   = cursor.fetchall()
	
	dic = {}
	for item in data:
		item=str(item[0]).strip()
		if year != 2006:
			if len(item)==7:
				day   = item[1:3].lstrip("0")
				month = item[0]
				year  = item[3:]
			else:
				day   = item[2:4].lstrip("0")
				month = item[0:2]
				year  = item[4:]
			date = "%s-%s-%s" % (year,month,day)

		else:
			date = item
		date = datetime.datetime.strptime(date,"%Y-%m-%d")
		tmp = int(time.mktime(date.timetuple()))
		if tmp in dic:
			dic[tmp] += 1
		else:
			dic[tmp] = 1

	timeSeries = [[key, val] for key, val in dic.iteritems()]
	timeSeries.sort(key=lambda x: x[0])

	startDate = datetime.datetime.fromtimestamp(float(timeSeries[0][0])).strftime("%Y-%m-%d")
	endDate   = datetime.datetime.fromtimestamp(float(timeSeries[-1][0])).strftime("%Y-%m-%d")

	fname = "NYUPD/sqf_num_stops_%s_%s" % (startDate,endDate)
	file  = open(fname, "w")
	for dataPoint in timeSeries:
		wtr = "%d %d\n" % (dataPoint[0],dataPoint[1])
		file.write(wtr)
	file.close()

def main():

	for year in (2006,2007,2008,2009,2010,2011,2012,2013,2014):
		yearConstrain = "year = %d " % (year)

		pct = [40]
		if year in (2010,2012,2013):
			pct = ["'%s'" % (str(item)) for item in pct]	
		elif year == 2006:
			pct = ["'%s'" % ((3-len(str(item)))*" "+str(item)) for item in pct]
		else:
			pct = ["'%s'" % ((4-len(str(item)))*" "+str(item)) for item in pct]
		pctConstrain = "pct IN (%s) " % (', '.join(pct))

		constrains = [yearConstrain,pctConstrain]

		Stops2TimeSeries(year, constrains)

if __name__ == "__main__":
	main()