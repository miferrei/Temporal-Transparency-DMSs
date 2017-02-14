# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
########## Bayesian Offline Change Point Detection ##########

#####    Methods Available:
#####    - Class Bayesian_Offline_ChangePoint
#####			- post_dist
#####			- optimal_conditional_changepoint_loc
#####			- optimal_joint_changepoint_loc_num
#####			- rank_changepoints

#####	References: 
#####   - Built on top of Github Repository https://github.com/hildensia/bayesian_changepoint_detection

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# 	Input: 
# 	- Data 
# 	- Prior Distribution on the number of change points
# 	- Prior Distribution on the change point process
# 	- Observation Log Likelihood function

# 	Methods:
#   - post_dist
#   - optimal_conditional_changepoint_loc
#   - optimal_joint_changepoint_loc_num

# 	Output: 
# 	- Optimal Number of Change Points
# 	- Optimal Change Point location given such number of change points

#####	References: Built on top of Github Repository https://github.com/hildensia/bayesian_changepoint_detection

# 	##### Code

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


##### Import library #####
from library import *

DEBUG = False

class Bayesian_Offline_ChangePoint:

	def __init__(self, data, prior_dist_num_changepoint, prior_dist_changepoint,observation_log_likelihood, params):
		self.data = data
		self.prior_dist_num_changepoint = prior_dist_num_changepoint
		self.prior_dist_changepoint = prior_dist_changepoint 
		self.observation_log_likelihood = observation_log_likelihood

		self.distance_changepoint, self.distance_start, self.distance_end, self.epsilon = params

	##### post_dist
	### Description: Compute Change Point Location Posterior Probability
	### constrained on the number of change points (according to: P. Fearnhead. 
	### Exact and efficient bayesian inference for multiple changepoint problems.
	### and to https://github.com/hildensia/bayesian_changepoint_detection) 
	### Input: - Int
	### Output: - Int, Matrix Dim=3 Np Array
	#
	def post_dist(self, num_change_points):

		if DEBUG:
			print "\n"
			print "### Start Compute Posterior", "\n"

		### Initialize Parameters

		m = num_change_points
		n = len(self.data)

		### Initialize Data Structures

		P = np.ones((n, n))*-np.inf
		Q = np.zeros((n, m+1))
		g = np.zeros(n)
		G = np.zeros(n+1)
		Pcp = np.ones((m, n, n))*-np.inf # We waste all columns of Pcp[0] except for the first one // For Version 1

		### Compute Prior Distribution - pdf and cdf

		for t in range(n):
			g[t] = np.log(self.prior_dist_changepoint.pmf(t))
			if t == 0:
				G[t] = g[t]
			else:
				G[t] = np.logaddexp(G[t-1], g[t])

		### Split into Presence or Absence of Change Point

		if m == 0:

			P[0, n-1] = self.observation_log_likelihood.pdf(self.data, 0, n-1)

			if G[n-2] < -1e-15:
				antiG = np.log(1-np.exp(G[n-2])) 
			else:
				antiG = np.log(-G[n-2])

			Q[0, 0] = P[0, n-1] + antiG
			Pcp = np.array([0.0])

		else:

			##### Compute Recursions Q and P

			### Compute Q_m(t), for j<t<n 
			if DEBUG:
				print "Started Q_" + str(m)
			for t in reversed(range(m, n-1)):
				P[t, n-1] = self.observation_log_likelihood.pdf(self.data, t, n-1)
			
				if G[n-t] < -1e-15:
					antiG = np.log(1-np.exp(G[n-t-1])) 
				else:
					antiG = np.log(-G[n-t-1])

				Q[t, m] = P[t, n-1] + antiG 

			#	print Q[t, m], n, t, P[t, n-1], antiG
			if DEBUG:
				print "Finished Q_" + str(m)

		#		print "Q - j:%d, t:%d, t:%d, s:%d, gap:%d" % (m, t, t, n-1, t-1)
		#		print t, n, Q[t, m], P[t, n-1], antiG 

			### Compute Q_j(t), row by row
			for j in reversed(range(1, m)):
				if DEBUG:
					print "Started Q_" + str(j)
				for t in reversed(range(j+1, n-m+j-1)):
					Q_tmp = -np.inf
					for s in reversed(range(t+1,n-m+j)):
						P[t, s] = self.observation_log_likelihood.pdf(self.data, t, s)
						tmp = P[t, s] + Q[s+1, j+1] + g[s-t+1]
						Q_tmp = np.logaddexp(Q_tmp, tmp)

						if tmp - Q_tmp < self.epsilon: 
							break
					# 	print "P - t:%d, s:%d, Q -  s:%d, j:%d, gap:%d " % (t, s, s+1, j+1, s-t+1), P[t, s], Q_tmp

					Q[t, j] = Q_tmp
				if DEBUG:
					print "Finished Q_" + str(j)
			# print t, j, Q[t, j]

			### Compute Q_0(t), for j<t<n-m
			Q_tmp = -np.inf
			if DEBUG:
				print "Started Q_" + str(0)
			for s in reversed(range(1, n-m-1)):
				P[0, s] = self.observation_log_likelihood.pdf(self.data, 0, s)
				tmp = P[0, s] + Q[s+1, 1] # tmp = P[0, s] + Q[s+1, 1] + g[s]
				# print s+1, Q[s+1,1]
				Q_tmp = np.logaddexp(Q_tmp, tmp)
				# print Q_tmp, tmp, s
				if tmp - Q_tmp < self.epsilon: 
					break
			if DEBUG:
				print "Finished Q_" + str(0)

			Q[0, 0] = Q_tmp

			# print Q[0, 0]

			### Compute Posterior Change Point Probability, Pcp

			### Compute Pcp_0 
			if DEBUG:
				print "Started Pcp_" + str(0)
			for s in range(1, n-m-1):
				P[0, s] = self.observation_log_likelihood.pdf(self.data, 0, s)
				Pcp[0, 0, s] = P[0, s] + Q[s+1, 1] + g[s] - Q[0, 0]
			if DEBUG:
				print "Finish Pcp_" + str(0)
				
			#	print s, Pcp[0, 0, s], P[0, s], Q[s+1, 1], g[s], Q[0,0]

			### Compute Pcp_j 0<j<m
			for j in range(1, m):
				if DEBUG:
					print "Started Pcp_" + str(j)
				for t in range(j-1, n-m+j-1):				
					for s in range(t+1, n-m+j-1):
						P[t+1, s] = self.observation_log_likelihood.pdf(self.data, t+1, s)
						Pcp[j, t, s] = P[t+1, s] + Q[s+1, j+1] + g[s-t] - Q[t+1, j]
						
			#			print j, t, s, Pcp[j, t, s], P[t+1, s], Q[s+1, j+1], Q[t+1,j]
			#			print "Pcp - j:%d, t:%d, s:%d" % (j, t, s), Pcp[j, t, s]
				if DEBUG:
					print "Finished Pcp_" + str(j)
			if DEBUG:
				print "Finished Pcp"
		
		if DEBUG:
			print "\n", "### End Compute Posterior"

		return Q[0, 0], Pcp

	##### optimal_conditional_changepoint_loc
	### Description: Dynamic Programming Solution to Compute 
	### Optimal Change Point Location
	### Input: - Matrix Dim=3 Np Array, Int
	### Output: - Matrix Dim=1 Np Array, Int
	#
	def optimal_conditional_changepoint_loc(self, Pcp, num_change_points):
			
		if DEBUG:
			print "\n", "### Started DP"
		### Notice Log Representation

		### Initialize Parameters
		m = num_change_points
		n = len(self.data)
		s = self.distance_changepoint 
		e = self.distance_start
		d = self.distance_changepoint

		# Create Memoise Data Structure
		T_max, tmp = np.zeros(n), np.zeros(n)
		T_argmax = np.zeros((n, m-1), dtype=np.int);
		# Create Output Data Structures
		T_out_arg = np.zeros(m, dtype=np.int)
		T_out_max = np.zeros(1)

		## Dynamic Programming Solution
		for j in reversed(range(m)):

			f_min, f_max = s+j*d, n-(e+(m-j-1)*d)+1
			s_min, s_max = f_min-d, f_max-d

			# print j
			# print "f_min: " + str(f_min) + ", f_max: " + str(f_max)
			# print "s_min: " + str(s_min) + ", s_max: " + str(s_max)
			# print "\n\n"

			if j == 0:
	#			print Pcp[0,0,:]
				T_max[f_min:f_max] = (tmp + Pcp[j, 0, :])[f_min:f_max]
			else:
				for start in range(s_min, s_max):

					T_max[start] = np.max((Pcp[j, start, :]+tmp)[start+d:f_max])
					T_argmax[start][j-1] = np.argmax((Pcp[j, start, :] + tmp)[start+d:f_max])+start+d 

				tmp = np.copy(T_max)

	#		print T_max
	#		print T_argmax

		## Compute Optimal Solution
		start = np.argmax(T_max[f_min:f_max])+f_min
		T_out_max = T_max[start]
		# print start, T_out_max
		T_out_arg[0] = start 
		for j in range(1, m):
			tmp = T_argmax[start][j-1]
			T_out_arg[j] = tmp
			start = tmp

		if DEBUG:
			print "### Finished DP"
			print "\n", "T Max:"
			print T_max

		### Return Optimal Solution
		return T_out_max, T_out_arg + 1

	##### optimal_joint_changepoint_loc_num
	### Description: Inference of MLE Solution for Posterior Joint Change Point Location
	### Input: - ---
	### Output: - Int, List, Matrix Dim=3 Np Array
	#
	def optimal_joint_changepoint_loc_num(self):

		## Notice Log Representation

		### Initialize Parameters
		start_M, end_M = (int(item) for item in self.prior_dist_num_changepoint.get_interval())
		if (start_M-end_M -1) % 2: end_M += 1; start_M = max(start_M, 0)
		opt_post_dist = -np.inf		
		opt_num_changepoint = None
		opt_changepoint_loc = np.array([])
		opt_post_dist_changepoint_loc = np.array([len(self.data)])

		# Infere MLE Solution for Posterior Joint Change Point Location
		for m in range(start_M, end_M):
			if DEBUG:
				print "\n", "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
				print "##### Number of Change Points:", m
			likelihood_num_changepoint, post_dist_changepoint_loc = self.post_dist(m)
			if m == 0:
				opt_post_dist_cp, cp_loc = post_dist_changepoint_loc, np.copy(opt_changepoint_loc)
			else:
				opt_post_dist_cp, cp_loc = self.optimal_conditional_changepoint_loc(post_dist_changepoint_loc, m)
			if opt_post_dist < self.prior_dist_num_changepoint.pmf(m) + likelihood_num_changepoint + opt_post_dist_cp:
				opt_post_dist = self.prior_dist_num_changepoint.pmf(m) + likelihood_num_changepoint + opt_post_dist_cp
				opt_post_dist_changepoint_loc = post_dist_changepoint_loc
				opt_changepoint_loc = cp_loc
				opt_num_changepoint = m
			if DEBUG:
				print "\n", "### Intermediate Results:"
				print "Number Cps:", m, ", Joint Prob: ", self.prior_dist_num_changepoint.pmf(m) + likelihood_num_changepoint + opt_post_dist_cp, ", Prior Num CPs:", self.prior_dist_num_changepoint.pmf(m), ", Evidence Prob:", likelihood_num_changepoint, ", Joint Post:", opt_post_dist_cp
				print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"

		return opt_num_changepoint, opt_changepoint_loc, opt_post_dist_changepoint_loc

	##### optimal_joint_changepoint_loc_num
	### Description: Compute Change Point Ranking According to their Posterior Probability of each point
	### Input: - List, Matrix Dim=3 Np Array
	### Output: - List
	#
	def rank_changepoints(self, opt_changepoint_loc, Pcp):

		##### Initialize Parameters #####
		tmp = []
		for i in range(len(opt_changepoint_loc)):
			if i == 0:
				tmp.append(Pcp[0,0,opt_changepoint_loc[0]])
			else:
				tmp.append(Pcp[i,opt_changepoint_loc[i-1],opt_changepoint_loc[i]])

		tmp = sorted(range(len(tmp)), key=lambda k: tmp[k], reverse=True)

		rank = opt_changepoint_loc[tmp]

		return rank

