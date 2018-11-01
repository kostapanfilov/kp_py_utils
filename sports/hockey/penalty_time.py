
from .hockey import Hockey
#from ...bets.bet import Bet, Total, Spread
from scipy.stats import poisson
import numpy as np

def multiple_convolve(array):
	pdf = array[0]
	for i in range(1, len(array)):
	    pdf = np.convolve(array[i], pdf)
	return(pdf)

class PenaltyTime(Hockey):

	__max_len = 100
	def __init__(self, s1 = None, s2 = None, tournament_type = 'NHL'):
		if(tournament_type == 'NHL'):
			self.__length = 4
			self.__correlation_vect = np.array([0,0,0,0])
			self.__ratio = np.array([0.95, 0.03, 0.01, 0.01])
			self.__pt_types = np.array([2,5,10,20])
		elif (tournament_type == 'KHL'):
			self.__length = 4
			self.__correlation_vect = np.array([0,0,0,0])
			self.__ratio = np.array([0.95, 0.03, 0.01, 0.01])
			self.__pt_types = np.array([2,5,10,20])
		else:
			self.__length = 4
			self.__correlation_vect = np.array([0,0,0,0])
			self.__ratio = np.array([0.95, 0.03, 0.01, 0.01])
			self.__pt_types = np.array([2,5,10,20])

	def __set_means__(self, s1, s2):
		if(len(s1) == 1):
			self.__s1 = s1 * self.__ratio / np.sum(self.__ratio * self.__pt_types)
		elif(len(s1) == self.__length):
			self.__s1 = s1
		else:
			self.__s1 = None

		if(len(s2) == 1):
			self.__s2 = s2 * self.__ratio / np.sum(self.__ratio * self.__pt_types)
		elif(len(s1) == self.__length):
			self.__s2 = s2
		else:
			self.__s2 = None

	def fit(self, s1, s2):
		self.__set_means__(s1,s2)
		self.pdf_total = self.__get_distribution_total()
		self.pdf_spread = self.__get_distribution_spread()
		self.pdf_team_1_total = self.__get_distribution_team_total(1)
		self.pdf_team_2_total = self.__get_distribution_team_total(2)

	def __distribution(self, pt_type, mu):
		probs = poisson.pmf(k = range(int(100 / pt_type )), mu = mu)
		zeros = [0] * ( (pt_type ) * len(probs) - 1)
		zeros[::(pt_type )] = probs
		return(zeros)

	def __get_distribution_total(self):
		values_uno = (self.__s1 + self.__s2) * (1 - self.__correlation_vect)
		values_double = 0.5 * (self.__s1 + self.__s2) * self.__correlation_vect
		pt_parts = []
		for mu, pt_type in zip(values_uno, self.__pt_types):
		    pt_parts.append(self.__distribution(pt_type, mu))

		for mu, pt_type in zip(values_double, self.__pt_types):
			pt_parts.append(self.__distribution(2 * pt_type, mu))

		out = multiple_convolve(pt_parts)[:self.__max_len]
		return(out)

	def __get_distribution_spread(self):
		s1 = self.__get_distribution_team_total(team = 1, corr_vect = self.__correlation_vect)
		s2 = self.__get_distribution_team_total(team = 2, corr_vect = self.__correlation_vect)
		out = np.convolve(s1[::-1],s2)
		return(out)

	def __get_distribution_team_total(self, team, corr_vect = 0):
		if(team == 1): s = self.__s1
		if(team == 2): s = self.__s2
		pt_parts = []
		for mu, pt_type in zip(s, self.__pt_types):
			pt_parts.append(self.__distribution(pt_type, mu))
		out = multiple_convolve(pt_parts)[:self.__max_len]
		return(out)
