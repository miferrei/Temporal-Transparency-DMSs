# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
########## Probability Distributions ##########

#######    Methods Available:
#######   - PlotSimple
#######   - PlotCumSum
#######   - PlotPreprocess
#######   - PlotChangePoints

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
########## Probability distributions Library ##########

###### Methods:
###### Likelihood Function
###### - Student T;
###### - Student T on Streaming Data;
###### Prior Distribution for Number of Change Points
###### - Discrete Laplacian Distribution
###### Prior Distribution for Change Point Location
###### - Constant
###### - Geometric Prior

###### References:
###### - https://gist.github.com/jfrelinger/2638485
###### - https://github.com/hildensia/bayesian_changepoint_detection/blob/master/bayesian_changepoint_detection/offline_changepoint_detection.py
###### - http://www.inference.phy.cam.ac.uk/cs482/publications/em_student.py
	
###### Import Libraries ######
from __future__ import division
from library import * 

DEBUG = False

########## Likelihood Functions
##### Student T Distribution 
class StudentT:

	### Notice Log Representation for P

	def __init__(self, num_data_points):
		self.P = np.ones((num_data_points, num_data_points))*-np.inf

		# Print Likelihood Function Information
		if DEBUG:
			print "\n", "##### Likelihood Function: "
			print "### Student T Distribution: ", "\n", "### Num_Data_Points: ", num_data_points

	def pdf(self, data, t, s):

		if self.P[t, s] == -np.inf:
			if t == s:
				self.P[t, s] = 0
			else:
				tmp = self.obs_log_likelihood(data, t, s)
				while np.isnan(tmp):
					#print "Bug!", tmp, t, s+1
					for i in range(t,s+1):
						if (data[t:s+1] == data[i]).sum() > 1:
							data[i] += 1; break
					tmp = self.obs_log_likelihood(data, t, s)
					while np.isnan(tmp):
						print "Bug!", tmp, t, s+1
						for i in range(t,s+1):
							if (data[t:s+1] == data[i]).sum() > 1:
								data[i] += 1; break
						tmp = self.obs_log_likelihood(data, t, s)
						if not np.isnan(tmp): print "Bug Solved!", tmp, data[t:s+1]
				self.P[t, s] = tmp

		return self.P[t, s]

 	##### Compute EM Updates for MLE Hyper Parameters of Student T distribution
 	#	  Closely follows http://www.inference.phy.cam.ac.uk/cs482/publications/em_student.py
	def obs_log_likelihood(self, data, t, s):

		s += 1
		data = data[t:s] 

		verbose = False
		# Number Iterations
		k = 50

		# Fit Normal parameters using ML
		mu = np.mean(data)
		sigma = np.std(data)
		minmax = min(data), max(data)

		# EM on student's t
		# Initialize using ML parameters for the Normal
		mu = mu
		lambd = 1/sigma
		nu = 0.1

		start = True
		if verbose: print "%3s  %15s  %15s  %15s"%("i", "mu", "lambda", "nu")
		for i in range(k):
		    # helper variables
		    u = (nu+1)/(nu+lambd*(data-mu)**2); 

		    mu_new = np.sum(data*u)/sum(u)
		    lambd_new = 1/np.mean(u * (data-mu_new)**2)

		    # Solve numerically for nu (using the ridder root finder)
		    const = 1+digamma((nu+1)/2)-np.log(nu+1)+np.mean(np.log(u)-u)
		    f = lambda nu: -digamma(nu/2) + np.log(nu) + const
		    if start:
		        nu_new = ridder(f, 10**-4, 10**4)
		        start = False
		    else:
		        factor = 2
		        minmax = [nu/2, nu*2]
		        while f(minmax[0])*f(minmax[1]) >= 0:
		            minmax[0] /= factor
		            minmax[1] *= factor
		        nu_new = ridder(f, minmax[0], minmax[1])

		    mu = mu_new
		    lambd = lambd_new
		    nu = nu_new
		    if verbose: print "%3i  %15e  %15e  %15e"%(i+1, mu, np.sqrt(1/lambd), nu)
		
		return np.sum(gammaln((nu+1)/2) - gammaln(nu/2) + 0.5*np.log(lambd/pi/nu) -((nu+1)/2)*np.log(1+lambd*(data-mu)**2/nu))


class GaussianLikelihood:

	def __init__(self, num_data_points):
		self.P = np.ones((num_data_points, num_data_points))*-np.inf

	def pdf(self, data, t, s):
		if self.P[t, s] == -np.inf:
			self.P[t, s] = self.obs_log_likelihood(data, t, s)

		return self.P[t, s]

	def obs_log_likelihood(self, data, t, s):

		s += 1
		n = s - t
		mean = data[t:s].sum(0) / n

		muT = (n * mean) / (1 + n)
		nuT = 1 + n
		alphaT = 1 + n / 2
		betaT = 1 + 0.5 * ((data[t:s] - mean) ** 2).sum(0) + ((n)/(1 + n)) * (mean**2 / 2)
		scale = (betaT*(nuT + 1))/(alphaT * nuT)

		# splitting the PDF of the student distribution up is /much/ faster.
		# (~ factor 20) using sum over for loop is even more worthwhile
		prob = np.sum(np.log(1 + (data[t:s] - muT)**2/(nuT * scale)))
		lgA = gammaln((nuT + 1) / 2) - np.log(np.sqrt(np.pi * nuT * scale)) - gammaln(nuT/2)

		return np.sum(n * lgA - (nuT + 1)/2 * prob)


########## Prior Distributions for Change Point Process
########## Offline Algorithm
##### Constant Prior
class Constant_Prior:	

	def __init__(self, l):

		self.l = l

	def pmf(self, t):

		return np.array([1.0/self.l])

##### Geometric Prior
class Geometric_Prior:

	def __init__(self, p, num_data_points):
		self.p = p
		self.g = np.zeros(num_data_points)

	def pmf(self, t):

		if self.g[t] == 0:
			self.g[t] = self.geometric_prior(t)

	def geometric_prior(self, t):

		return self.p*((1-self.p)**(t-1))

##### Negative Binomial
class Negative_Binomial_Prior:

	def __init__(self, p, k, num_data_points):

		self.p = p
		self.k = k
		self.P = np.zeros(num_data_points)

	def pmf(self, t):

		if self.P[t] == 0:
			self.P[t] = self.negative_binomial(t)

	def negative_binomial(self, t):

		return comb(t - self.k, self.k - 1) * self.p ** self.k * (1 - self.p) ** (t - self.k)

########## Prior Distributions for Number of Change Points
##### Discrete Laplacian Distribution
class Laplacian_Prior:

	def __init__(self, mu, beta, alpha):
		self.mu = mu
		self.beta = beta
		self.alpha = alpha

		# Print Prior Distribution Information
		start, end = (int(item) for item in self.get_interval())
		if DEBUG:
			print "\n", "##### Prior Distributions for Number of Change Points: "
			print "### Laplace Distribution: ", "\n", "### Mu:", mu, "### Beta:", beta, "### Alpha:", alpha
			for t in range(start, end):
				print "t:", t, "pmf:", self.pmf(t)

	def pmf(self, k):

		return dlaplace.logpmf(k, self.beta, self.mu)

	def get_interval(self):

		return dlaplace.interval(self.alpha, self.beta, self.mu)



