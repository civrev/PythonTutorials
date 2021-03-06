#python3 ~/PythonTutorials/ReenforcementLearning/bandits5.py
#The Multi-Arm Bandit problem
#Re-enforcement learning, epsilon-greedy strategy, with decaying epsilon
#Made from a class I got on Udemy
#"artificial intelligence reinforcement learning in python" by The LazyProgrammer

import numpy as np
import matplotlib.pyplot as plt

class Bandit:
	'''
	bandit represents a slot machine
	m is the true win rate of the machine
	we will be using the mean to calculate the win rate
	since it is hidden from us
	and N is the number of times we've tried a machine
	'''
	def __init__(self, m):
		self.m = m
		self.mean = 0
		self.N = 0

	def pull(self):
		#this is the reward given
		p = np.random.random()
		if p < self.m:
			#win
			return 1
		else:
			#lose
			return 0

	def update(self, x):
		self.N +=1
		self.mean = (1 - 1/self.N)*self.mean + (1/self.N)*x

def run_experiment(m1,m2,m3,eps,N):
	"""
	give the parameters for 3 bandits
	an epsilon function to use for
	epsilon-greedy strategy
	and N, the number of times we play the game
	"""
	bandits = [Bandit(m1),Bandit(m2),Bandit(m3)]
	
	#for PLOTTING ONLY
	#this is not needed for functioning
	data = np.empty(N)

	#play game N times
	for i in range(N):
		#epsilon-greedy here
		#random number 0-1
		#if in the epsilon % range we explore, otherwise exploit
		p = np.random.random()
		if p < 1-(eps*i):
			#explore
			#choose a random one to explore
			j = np.random.choice(3)
		else:
			#exploit
			#choose the current-best mean bandit to use
			j = np.argmax([b.mean for b in bandits])

		#pull the one we chose
		x = bandits[j].pull()

		#whether explore or exploit, we update our knowledge
		bandits[j].update(x)

		#for PLOTTING
		data[i] = x

	#this is basically the rate your agent sees at the win rate per bandit
	#once the experiment is over
	cumulative_average = np.cumsum(data)/(np.arange(N)+1)

	plt.plot(cumulative_average)

	#just lines, like grid lines
	plt.plot(np.ones(N)*m1)
	plt.plot(np.ones(N)*m2)
	plt.plot(np.ones(N)*m3)

	plt.title("Espsilon = "+str(eps))
	plt.xscale('log')
	plt.show()

	for index,b in enumerate(bandits):
		print("Esp " + str(eps) + " Bandit " + str(index) + ' ' + str(b.mean))
	
	return cumulative_average

#run experiment for differnet epsilons
# 10%
c_1 = run_experiment(0.10,0.20,0.30, 0.1, 100000)
# 5%
c_05 = run_experiment(0.10,0.20,0.30, 0.05, 100000)
# 1%
c_01 = run_experiment(0.10,0.20,0.30, 0.01, 100000)

plt.plot(c_1, label='eps = 0.1')
plt.plot(c_05, label='eps = 0.05')
plt.plot(c_01, label='eps = 0.01')
plt.legend()
plt.xscale('log')
plt.show()

#so you see as the mean of the agents approach the highest true win rate
#for all bandits, you see that the agent has at some point found through
#exploration which one was the best, and chose it every time for exploitation
#NOTE: once it was clear which one was the best, our agent still explored
#at the epsilon rate randomly which choses sub-optimal choices often, and as such
#is just sub-optimal acitons it didn't have to take

#output to console
'''
Esp 0.1 Bandit 0 0
Esp 0.1 Bandit 1 0.0
Esp 0.1 Bandit 2 0.29942299422994295
Esp 0.05 Bandit 0 0.0
Esp 0.05 Bandit 1 0.0
Esp 0.05 Bandit 2 0.3014041123289819
Esp 0.01 Bandit 0 0.0
Esp 0.01 Bandit 1 0.2777777777777778
Esp 0.01 Bandit 2 0.2985004451647083
'''
