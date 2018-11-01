from .bet import Bet
import numpy as np
import math
class Total(Bet):

	def __init__(self, distribution):
		self.__pdf = distribution
		self.__cdf = np.cumsum(distribution)
		self.__rng = list(map(lambda x: x+ 0.5, range(len(distribution))))

	def total(self, total):
		if(abs(total - 0.5 - math.floor(total)) < 1e-5):
			t = list(filter(lambda x: x[0] == total, zip(self.__rng, self.__cdf)))
			return(self.get_pairs(t[0][1]))
		elif(abs(total - round(total)) < 1e-5):
			return(0)
		else:
			if(1 == 1):
				pass
			elif(2 == 1):
				pass
			else:
				return('error')
