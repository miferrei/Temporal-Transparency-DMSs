# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
########## Data Visualization ##########

#######    Methods Available:
#######   - PlotSimple
#######   - PlotCumSum
#######   - PlotPreprocess
#######   - PlotChangePoints

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


##### Import Libraries #####
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# - - - - - - - - - - - - MAIN - - - - - - - - - - - - - - - - - - - - - - - - - - 

##### FUNCTION: PlotSimple 
### Description: Plots (and saves plot) Time Series Data
### Input: Np Array, List, String
### Output: -
def PlotSimple(f,dates,fname):

	fig, ax1 = plt.subplots()

	##### Set Y Axis Limits #####
	f_lim_1 = max(min(f) - int( float(min(f)) * 0.1 ), 0)
	f_lim_2 = max(f) + int( float(max(f)) * 0.1 )
	flim = [f_lim_1, f_lim_2]
	ax1.set_ylim(flim)
	ax1.set_ylabel('f(t)')

	##### Set X Axis limits #####
	dates_lim_1 = min(dates)
	dates_lim_2 = max(dates)
	dateslim = [dates_lim_1, dates_lim_2]
	ax1.set_xlim(dateslim)
	ax1.set_xlabel('t')

	ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d')) # so that we can trace the day in the interactive method	
	fig.autofmt_xdate() # so that the dates are adjusted in a way that they dont overlap

	# Plot f 
	ax1.plot_date(dates, f, "-o", color="red")
	
	plt.grid(True)

	# Save Figure
	fname=fname.replace(".txt",".pdf")
	faddress = "../input_data/"+fname
	fig.savefig(faddress)
	# Show Figure
	plt.show()

	return

##### FUNCTION: PlotCumSum
### Description: Plots given Change Points yield by the Cumulative Sum Algorithm
### Input: Np Array, Np Array, Np Array, List, String
### Output: -
def PlotCumSum(f,cps,dates):

	fig, ax1 = plt.subplots()

	##### Set Y1 Axis Limits #####
	f_lim_1 = max(min(f) - int( float(min(f)) * 0.1 ), 0)
	f_lim_2 = max(f) + int( float(max(f)) * 0.1 )
	flim = [f_lim_1, f_lim_2]
	ax1.set_ylim(flim)
	ax1.set_ylabel('f(t)')

	##### Set X Axis limits #####
	dates_lim_1 = min(dates)
	dates_lim_2 = max(dates)
	dateslim = [dates_lim_1, dates_lim_2]
	ax1.set_xlim(dateslim)
	ax1.set_xlabel('t')

	ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d')) # so that we can trace the day in the interactive method	
	fig.autofmt_xdate() # so that the dates are adjusted in a way that they dont overlap

	# Plot f 
	ax1.plot_date(dates, f, "-o", color="red")
	# Plot Change Points 
	for cp in cps:
		plt.axvline(dates[cp],color='green',linestyle="--")

	plt.grid(True)
	plt.show()

	return

##### FUNCTION: PlotPreProcess
### Description: Plots result of the Preprocessing on the given inputdata
### Input: Np Array, Np Array, List
### Output: -
def PlotPreprocess(f,feng,dates):

	fig, ax1 = plt.subplots()

	##### Set Y1 Axis Limits #####
	f_lim_1 = max(min(f) - int( float(min(f)) * 0.1 ), 0)
	f_lim_2 = max(f) + int( float(max(f)) * 0.1 )
	flim = [f_lim_1, f_lim_2]
	ax1.set_ylim(flim)
	ax1.set_ylabel('f(t)')

	##### Set Y2 Axis Limits #####
	feng_lim_1 = min(min(feng) - int( float(min(feng)) * 0.1 ), 0)
	feng_lim_2 = max(feng) + int( float(max(feng)) * 0.1 )
	fenglim = [feng_lim_1, feng_lim_2]
	ax2 = ax1.twinx()
	ax2.set_ylim(fenglim)

	##### Set X Axis limits #####
	dates_lim_1 = min(dates)
	dates_lim_2 = max(dates)
	dateslim = [dates_lim_1, dates_lim_2]
	ax1.set_xlim(dateslim)
	ax1.set_xlabel('t')

	ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d')) # so that we can trace the day in the interactive method	
	fig.autofmt_xdate() # so that the dates are adjusted in a way that they dont overlap

	# Plot f 
	ax1.plot_date(dates, f, "-o", color="red")
	# Plot feng
	ax2.plot_date(dates, feng, "-o", color="green", label = 'After Preprocessing')
	
	# Save Figure
	plt.legend(loc='upper right')
	# Show Figure
	plt.grid(True)
	plt.show()

	return

##### FUNCTION: PlotChangepoints
### Description: Plots (and saves plot) of the Change Points yield by Tetra
### Input: Np Array, List, List, String
### Output: -
def PlotChangePoints(f,locCps,dates,fname):

	fig, ax1 = plt.subplots()

	##### Set Y Axis Limits #####
	f_lim_1 = max(min(f) - int( float(min(f)) * 0.1 ), 0)
	f_lim_2 = max(f) + int( float(max(f)) * 0.1 )
	flim = [f_lim_1, f_lim_2]
	ax1.set_ylim(flim)
	ax1.set_ylabel('f(t)')

	##### Set X Axis limits #####
	dates_lim_1 = min(dates)
	dates_lim_2 = max(dates)
	dateslim = [dates_lim_1, dates_lim_2]
	ax1.set_xlim(dateslim)
	ax1.set_xlabel('t')

	ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d')) # so that we can trace the day in the interactive method	
	fig.autofmt_xdate() # so that the dates are adjusted in a way that they dont overlap

	# Plot f 
	ax1.plot_date(dates, f, "-o", color="red")
	# Plot Change Points 
	for cp in locCps:
		plt.axvline(dates[cp],color='green',linestyle="--")

	plt.grid(True)

	# Save Figure
	fname=fname.replace(".txt",".pdf")
	faddress = "../output_data/"+fname
	fig.savefig(faddress)
	# Show Figure
	plt.show()

	return