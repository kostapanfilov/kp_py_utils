from .bet import Bet
import numpy as np
import math
class Spread(Bet):
	def __init__(self, distribution):
		n = (len(distribution) + 1) // 2
		self.__pdf = distribution
		self.__cdf = np.cumsum(distribution)
		self.__rng = list(map(lambda x: x+ 0.5, range(-n + 1, n)))

	def spread(self, spread):
		if(abs(spread - 0.5 - math.floor(spread)) < 1e-5):
			t = list(filter(lambda x: x[0] == spread, zip(self.__rng, self.__cdf)))
			return(self.get_pairs(t[0][1]))
		elif(abs(spread - round(spread)) < 1e-5):
			return(0)
		else:
			if(1 == 1):
				pass
			elif(2 == 1):
				pass
			else:
				return('error')
