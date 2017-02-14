# "Temporal Transparency in Black-Box DMS's" 

Project directory of **"Temporal Transparency in Black-Box DMS's"**. The repository contains the following eight directories: 
- **TETRA**: Change Point Detection Framework.
- **Datasets**: Raw files of the datasets analysed.
- **Collect Data**: Code for collecting and building time series of data from the datasets available.
- **Submissions**: Project Submissions.

**Dependencies**: numpy, matplotlib, scipy, math, collection, calender, random, operator

## TETRA - Change Point Detection Framework for Black-Box DMS's 

### Goal 

The goal of **TETRA** is to detect significant policy change events in real-world DMS's. The framework consists of an Offline Change Point Detection Framework built on top of the work of P.Fearnhead in "Exact and Efficient Bayesian Inference of Multiple Changepoint Problems".

---

> Nevertheless, we further generalised the Framework to support Streaming - having considered Online Change Point Detection - and Multivariate Data).

### Structure

**TETRA** comprises three working directories:
- **code** - Application Source Code
- **input_data** - Application Input Data
- **output_data** - Application Output Data

### Usage

Consider running the framework over a given unidimensional time series of data of size _n_, _( (t<sub>1</sub>,f(t<sub>1</sub>)),...,(t<sub>n</sub>,f(t<sub>n</sub>)) )_. Start by building a file, call it `fileIn.txt`, with the following format 

```shell 
	timestamp(t1) f(t1)
	...
	timestamp(tn) f(tn)
```

and place it in the directory `input_data/` through `path_to_FileIn/fileIn.txt`.

In order to compute the Change Points for the given time series of data, consider executing the following commands:

```shell
	$ cd code
	$ python -W ignore main.py Uni Offline path_to_FileIn/fileIn.txt
```

A brief summary of the steps taken by **TETRA** will be provided during execution. The output files, concerning the set of _k_ detected Change Points (along with their relative ranking) under the format

```shell
	date(cp1) rank(cp1) 
	...
	date(cpk) rank(cpk)
```

and a _.pdf_ plot of the time series of data and its Change Points, will be available in the directory `output_data/` at `path_to_FileIn/`.

--- 

> Before usage, **TETRA** must be fined tuned to the time series of data in hand. Follow the example below to understand how.

## Example - Detecting Policy Change Events in NYSQF data in the year of 2010

### 0. Visualize Time Series

Time series of data yield by the NYSQF dataset when considering the number of stops in all of New York City's precincts in the year of 2010:

![sqf_num_stops_2010-01-01__2010-12-31_pct_all.pdf](https://github.com/miferrei/Temporal-Transparency/files/772667/sqf_num_stops_2010-01-01__2010-12-31_pct_all.pdf)

### 1. Fine Tuning 

Open the file `driver/methods.py` and fine tune **TETRA** by appropriately selecting the values for the variables presented below. We refer to the _Section 2_ in _[1.]_ for more on the _tuning parameters_. Please consider using the debugging mode (set ```Debug=True```) and the console information to infer the changes in the preprocessing implied by the fine tuning proposed.

```python
	##### Outlier Removal
	window, threshold = 20, 0.31
	... 
	##### Smooth/Filtering Data #####
	window, degree = 11, 6
	...
	##### Compute Estimate Number Change Points #####
	h = 12.5
	...
	##### Priors Laplacian Distribution #####
	beta, alpha = 5, 0.999999
```

By default, we consider a minimum segment length of _10_ data points.

```python
	distance_changepoint = 10
```

</br>
The Effect of Preprocessing:

![fig1.pdf](https://github.com/miferrei/Temporal-Transparency/files/772671/fig1.pdf)

Estimation of the Number of Change Points through the Two-sided CUMSUM Algorithm:
![fig2.pdf](https://github.com/miferrei/Temporal-Transparency/files/772676/fig2.pdf)

### 2. Results

```shell

		----------------------------------------------
		|    		CHANGE POINT LOCATION		     |
		----------------------------------------------
		|    		 0. Date : 2010-04-07 		     |
		----------------------------------------------
		|    		 1. Date : 2010-05-30 		     |
		----------------------------------------------
		|    		 2. Date : 2010-10-06 		     |
		----------------------------------------------
		|    		 3. Date : 2010-12-04 		     |
		----------------------------------------------
		|    		 4. Date : 2010-12-22 		     |
		----------------------------------------------
		
		----------------------------------------------
		|		RANKED CHANGE POINT LOCATION	     |
		----------------------------------------------
		|    		 0. Date : 2010-05-30 		     |
		----------------------------------------------
		|		     1. Date : 2010-12-04		       |
		----------------------------------------------
		|    		 2. Date : 2010-10-06 		     |
		----------------------------------------------
		|    		 3. Date : 2010-12-22 		     |
		----------------------------------------------
		|    		 4. Date : 2010-04-07 		     |
		----------------------------------------------
```

</br>
Change Points outputted by **TETRA**:

![sqf_num_stops_2010-01-01__2010-12-31_pct_all.pdf](https://github.com/miferrei/Temporal-Transparency/files/772771/sqf_num_stops_2010-01-01__2010-12-31_pct_all.pdf)

## Available Dataset and Results

### NYSQF (New York City Stop-and-Frisk) Dataset 

<ul>
<li> The complete NYSQF dataset (from years 2003 to 2014) can be found in the directory <i>'Datasets/NYSQF/'</i> in the form of yearly <i>'year.sqlite3'</i> sqlite3 files (consult http://www.nyc.gov/html/nypd/html/analysis_and_planning/stop_question_and_frisk_report.shtml for more details on the dataset structure). </li>
<li> Example files on how to build time series of data from the NYUSQF dataset can be found in the directory <i>'Collect Data/NYSQF'</i>. </li>
<li> Time series of data for the years <i>2006</i> to <i>2014</i>, sorted by <i>Borough</i> and by <i>Precinct</i>, can be found in <b>TETRA</b>'s <i>'input_data/NYSQF'</i> directory. The respective output files can be found in <b>TETRA</b>'s <i>'output_data/NYSQF'</i> directory. </li>
</ul>

### Synthetic Dataset 

<ul>
<li> Synthetic Data was generated as specified in <b>TETRA</b>'s <i>'code/testing/SyntheticData.py'</i>. We refer to the <i>Section 2</i> in <i>[1.]</i> for more details. </li>
<li> Examples of time series of data used in the experiments can be found in <b>TETRA</b>'s <i>'input_data/SD'</i> directory. The respective output files can be found in <b>TETRA</b>'s <i>'output_data/SD'</i> directory. </li>
</ul>

## References

* **The Case for Temporal Transparency: Detecting Policy Change Events in Black-Box Decision Making Systems**. Miguel Ferreira, Kristina Gligoric, Muhammad Bilal Zafar, Krishna P. Gummadi. https://arxiv.org/abs/1610.10064
