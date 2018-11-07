
#import matplotlib.pyplot as plt

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

	def region_(self, m):
		if self.region == 'KR':
			return 0.95 # 0.05 vali
		elif self.region == 'EUW':
			return 1 # 0.05 vali
		elif self.region == 'NA':
			return 0.90 # 0.05 vali
		elif self.region == 'CN':
			return 0.98 # 0.05 vali
		elif self.region == 'TW':
			return 0.85 # 0.05 vali
		elif self.region == 'BR':
			return 0.77 # Alas
		elif self.region == 'CIS':
			return 0.65 # Alas 
		else:
			return 0.91








			