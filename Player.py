
#import matplotlib.pyplot as plt
import time

K1 = 40 # Vakio
K2 = K1-8 # Vakio-8 	-> 32
K3 = K2/2 # (Vakio-8)/2	-> 16


'''
50 ottelun sarja, jonka aikana lasketaan elo, ratkaise.
'''
class Player():

	def __init__(self, k, min_games, name):
		
		self.name = name

		self.k = k
		self.min_games = min_games

		self.elo = [1450]

		self.games = 0
		
	def win(self, other, avg, i):
		OA = 1/(1+10**((other-self.elo[-1])/float(400)))
			
		if self.games <= self.min_games:
			K = K1
		elif self.elo[-1] <= avg*self.k:
			K = K2
		else:
			K = K3

		self.games += 1
		self.elo.append(self.elo[-1] + K*(1-OA))


	def lose(self, other, avg, i):
		OA = 1/(1+10**((other-self.elo[-1])/float(400)))
		
		if self.games <= self.min_games:
			K = K1
		elif self.elo[-1] <= avg*self.k:
			K = K2
		else:
			K = K3

		self.games += 1
		self.elo.append(self.elo[-1] + K*(0-OA))


	def elo_plot(self):
		title = self.name + ' - elo, current: ' + str(round(self.mid_elo_(),0))
		plt.plot(self.elo)
		plt.title(title)
		plt.show()

	def max_elo(self):
		return self.elo[-1]















