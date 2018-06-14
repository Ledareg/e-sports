
import matplotlib.pyplot as plt
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

		self.top_elo = [1450]
		self.jun_elo = [1450]
		self.mid_elo = [1450]
		self.adc_elo = [1450]
		self.sup_elo = [1450]

		self.top_games = 0
		self.jun_games = 0
		self.mid_games = 0
		self.adc_games = 0
		self.sup_games = 0
		
	def win(self, other, avg, i):

		if i == 0:
			OA = 1/(1+10**((other-self.top_elo[-1])/float(400)))
			
			if self.top_games <= self.min_games:
				K = K1
			elif self.top_elo[-1] <= avg*self.k:
				K = K2
			else:
				K = K3
			
			self.top_games += 1
			self.top_elo.append(self.top_elo[-1] + K*(1-OA))

		if i == 1:
			OA = 1/(1+10**((other-self.jun_elo[-1])/float(400)))
			
			if self.jun_games <= self.min_games:
				K = K1
			elif self.jun_elo[-1] <= avg*self.k:
				K = K2
			else:
				K = K3

			self.jun_games += 1
			self.jun_elo.append(self.jun_elo[-1] + K*(1-OA))

		if i == 2:
			OA = 1/(1+10**((other-self.mid_elo[-1])/float(400)))

			if self.mid_games <= self.min_games:
				K = K1
			elif self.mid_elo[-1] <= avg*self.k:
				K = K2
			else:
				K = K3

			self.mid_games += 1
			self.mid_elo.append(self.mid_elo[-1] + K*(1-OA))

		if i == 3:
			OA = 1/(1+10**((other-self.adc_elo[-1])/float(400)))

			if self.adc_games <= self.min_games:
				K = K1
			elif self.adc_elo[-1] <= avg*self.k:
				K = K2
			else:
				K = K3

			self.adc_games += 1
			self.adc_elo.append(self.adc_elo[-1] + K*(1-OA))

		if i == 4:
			OA = 1/(1+10**((other-self.sup_elo[-1])/float(400)))

			if self.sup_games <= self.min_games:
				K = K1
			elif self.sup_elo[-1] <= avg*self.k:
				K = K2
			else:
				K = K3
			
			self.sup_games += 1
			self.sup_elo.append(self.sup_elo[-1] + K*(1-OA))


	def lose(self, other, avg, i):
		if i == 0:
			OA = 1/(1+10**((other-self.top_elo[-1])/float(400)))
		
			if self.top_games <= self.min_games:
				K = K1
			elif self.top_elo[-1] <= avg*self.k:
				K = K2
			else:
				K = K3

			self.top_games += 1
			self.top_elo.append(self.top_elo[-1] + K*(0-OA))

		if i == 1:
			OA = 1/(1+10**((other-self.jun_elo[-1])/float(400)))
		
			if self.jun_games <= self.min_games:
				K = K1
			elif self.jun_elo[-1] <= avg*self.k:
				K = K2
			else:
				K = K3

			self.jun_games += 1
			self.jun_elo.append(self.jun_elo[-1] + K*(0-OA))

		if i == 2:
			OA = 1/(1+10**((other-self.mid_elo[-1])/float(400)))
	
			if self.mid_games <= self.min_games:
				K = K1
			elif self.mid_elo[-1] <= avg*self.k:
				K = K2
			else:
				K = K3

			self.mid_games += 1
			self.mid_elo.append(self.mid_elo[-1] + K*(0-OA))

		if i == 3:
			OA = 1/(1+10**((other-self.adc_elo[-1])/float(400)))
	
			if self.adc_games <= self.min_games:
				K = K1
			elif self.adc_elo[-1] <= avg*self.k:
				K = K2
			else:
				K = K3

			self.adc_games += 1
			self.adc_elo.append(self.adc_elo[-1] + K*(0-OA))

		if i == 4:
			OA = 1/(1+10**((other-self.sup_elo[-1])/float(400)))
		
			if self.sup_games <= self.min_games:
				K = K1
			elif self.sup_elo[-1] <= avg*self.k:
				K = K2
			else:
				K = K3
		
			self.sup_games += 1
			self.sup_elo.append(self.sup_elo[-1] + K*(0-OA))


	def elo_plot(self):
		title = self.name + ' - elo, current: ' + str(round(self.mid_elo_(),0))
		plt.plot(self.mid_elo)
		plt.title(title)
		plt.show()

	def max_elo(self):
		elo = 1000
		if self.top_elo[-1] > elo:
			elo = self.top_elo[-1]

		if self.jun_elo[-1] > elo:
			elo = self.jun_elo[-1]

		if self.mid_elo[-1] > elo:
			elo = self.mid_elo[-1]

		if self.adc_elo[-1] > elo:
			elo = self.adc_elo[-1]

		if self.sup_elo[-1] > elo:
			elo = self.sup_elo[-1]

		return elo

	def top_elo_(self):

		elo = self.top_elo
		return elo[-1]

	def jun_elo_(self):
		elo = self.jun_elo
		return elo[-1]

	def mid_elo_(self):
		elo = self.mid_elo
		return elo[-1]

	def adc_elo_(self):
		elo = self.adc_elo
		return elo[-1]

	def sup_elo_(self):
		elo = self.sup_elo
		return elo[-1]















