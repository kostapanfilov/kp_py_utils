class Match():
	def __init__(self):
		pass

class Bet():
	

	def __init__(self, distribution):
		self.__pdf = distribution
		self.__cdf = np.cumsum(distribution)

	def show():
		pass

	def m3(self):
		pass

	def get_pairs(self, p):
		return([p, 1 - p])