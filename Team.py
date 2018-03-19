
import matplotlib.pyplot as plt

class Team():

	def __init__(self, name):
		self.name = name
		self.games = 0
		self.matches = []

	def win(self, opponent, elo):
		self.matches.append([opponent, 'win', elo])

	def lose(self, opponent, elo):
		self.matches.append([opponent, 'lose', elo])

	def last10(self):
		for i in range(1, 11):
			print 'Opponent: {:20s}, result: {:4s} and opponent elo. {:.0f}'.format(self.matches[-i][0], self.matches[-i][1], self.matches[-i][2])










			