
import matplotlib.pyplot as plt

class Team():

	def __init__(self, name):
		self.name = name
		self.games = 0
		self.matches = []
		self.region = ''

	def win(self, opponent, elo):
		self.matches.append([opponent, 'win', elo])

	def lose(self, opponent, elo):
		self.matches.append([opponent, 'lose', elo])

	def last10(self):
		for i in range(1, 11):
			print 'Opponent: {:20s}, result: {:4s} and opponent elo. {:.0f}'.format(self.matches[-i][0], self.matches[-i][1], self.matches[-i][2])

	def region_(self):
		if self.region == 'KR':
			return 1
		elif self.region == 'EUW':
			return 1
		elif self.region == 'NA':
			return 1
		elif self.region == 'CN':
			return 1
		elif self.region == 'TW':
			return 1
		elif self.region == 'BR':
			return 1
		elif self.region == 'CIS':
			return 1
		elif self.region == 'TR':
			return 1
		else:
			return 1








			