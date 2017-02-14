##### External Libraries
# sys.path.insert(0, "/home/mzafar/libraries/py/")

# import matplotlib 
# matplotlib.use('Agg')

##### Internal Libraries #####
import numpy as np
from math import fabs, pi, ceil
from random import random, randint
from collections import defaultdict

import datetime
import time
from datetime import timedelta

from scipy import stats
from scipy.signal import savgol_filter, butter, filtfilt
from scipy.special import digamma, gamma, gammaln, multigammaln
from scipy.misc import comb, logsumexp
from scipy.optimize import ridder
from scipy.stats import norm, binom, dlaplace, chi2, multivariate_normal
from scipy.ndimage.filters import uniform_filter

from numpy.linalg import inv, cholesky, det

from operator import itemgetter
import calendar

##### External Libraries #####
import os, sys
sys.path.append(os.getcwd()+'/visual')
sys.path.append(os.getcwd()+'/stats')
sys.path.append(os.getcwd()+'/methods')
sys.path.append(os.getcwd()+'/driver')
sys.path.append(os.getcwd()+'/data')
sys.path.append(os.getcwd()+'/testing')

from dataManage import *
from methods import *
from plot import *
from cumsum import *
from featureEng import *
from distributions import *
from syntheticData import *
from bayesian_offline_changepoint_detection import *
