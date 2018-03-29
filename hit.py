class Hit():

	def __init__(self):
		self.hit = 0
		self.mis = 0

	def hitrate(self):
		return 0#self.hit/float(self.hit+self.mis)*100

	def game(self, elo1, elo2, result):

		if result == '1-0':
			if elo1 > elo2:
				self.hit += 1
			elif elo2 > elo1:
				self.mis += 1

		elif result == '0-1':
			if elo2 > elo1:
				self.hit += 1
			elif elo1 > elo2:
				self.mis += 1

		else:
			print result;quit()