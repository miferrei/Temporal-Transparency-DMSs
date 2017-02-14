# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
########## File Format ##########
## fobserved_start-date_end-date.txt
########## Data Format ##########
## Date: x, Array of Timestamp ; Observed Function: f, Array of Floats
## [[x1, f1], ..., [xn, fn]]
########## Usage ##########
## python -W ignore main.py Uni Offline <file location in input_data folder>
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

##### Import Libraries
import os, sys
sys.path.append('driver')
from library import *

def main():
	if len(sys.argv)==4:
		if (sys.argv[1]=="Uni" and sys.argv[2]=="Offline"):
			UniOfflineCPDetection(sys.argv[3])
		else: print "---- Invalid Operation ----"
	else: print "---- Invalid Operation ----"

if __name__ == "__main__":
	main()
