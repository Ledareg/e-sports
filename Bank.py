
import numpy as np

class Tournament():
	def __init__(self, name):
		self.name = name
		self.played = 0
		self.games = 0
		self.won = 0

class Bank():
	def __init__(self, max_betsize, date, cash, kelly, tasapanos):
		self.games = 0
		self.played = 0
		self.won = 0
		self.maxOA = 130000 # %
		self.log_sum = []
		self.log_sum_odds = []
		self.kassa = [1]
		self.kassa_cum_start = cash
		self.kassa_cum = [self.kassa_cum_start]
		self.max_betsize = max_betsize
		self.date = date
		self.OA = []
		self.tournaments = {}
		self.kelly = kelly
		self.EV = [0]
		self.EV_cum = [self.kassa_cum_start]
		self.pal5 = [0]
		self.pal5_ = 1.07
		self.tasapanos = tasapanos

	# Muuntaa ajanjakson jarkevaksi
	def Date(self):
		import datetime
		start_date = str(self.date)[:4] + '/' + str(int(str(self.date)[4:6]))# + '/' + str(int(str(self.date)[6:8]))
		start_date = datetime.datetime.strptime(start_date, "%Y/%m").date()
		date = datetime.datetime.now().date()

		return str(start_date) + ' - ' + str(date)

	def ROI(self):
		#return ((self.profit()-self.kassa[0])/float(self.played+self.kassa[0]))*100
		return (1+(self.profit())/float(self.played))*100

	def profit(self):
		#return self.won - self.played + self.kassa[0]
		return self.won - self.played

	# This function returns variance between EV and actual bank
	def var(self):
		# sigma = (bank[i]-EV[i])^2
		sigma = 0
		for i in range(0, len(self.kassa)):
			sigma = sigma + (self.kassa[i]-self.EV[i])**2

		return np.sqrt(sigma/float(i))

	def winner(self, row):
		score = [0, 0]
		for item in row[7].split(','):
			if item.split('-')[0] > item.split('-')[1]:
				score[0] += 1
			else:
				score[1] += 1

		if score[0] > score[1]:
			return 1
		else:
			return 2

	def plot(self):
		import matplotlib.pyplot as plt
		import pylab

		t1 = np.array(self.kassa)
		t2 = np.array(self.kassa_cum)
		t3 = np.array(self.EV)
		t4 = np.array(self.pal5)

		x = np.arange(0,len(self.kassa))

		plt.figure(1)
		plt.subplot(221)
		plt.plot(x,t1,label='Tasapanos')
		#plt.plot(x,t3,'m--',label='EV')
		plt.plot(x,t4,'m--',label='107% palautus')
		plt.legend(loc=2)
		plt.title('Kassankasvu - pal-%: ' + str(round(self.ROI(),2)) + '% - games: ' + str(self.games) + '\n Ajanjakso: ' + self.Date())
		plt.fill_between(x, t1, t4, where=t4 <= t1, facecolor='green', interpolate=True)
		plt.fill_between(x, t1, t4, where=t4 >= t1, facecolor='red', interpolate=True)
		plt.grid()

		plt.subplot(222)
		plt.plot(t2)
		#plt.plot(t4)
		plt.title('Kelly: ' + str(self.kelly) + '\nMaksimipanos: ' + str(self.max_betsize) + '% \nAloituskassa: ' + str(round(self.kassa_cum_start,-1)) + '. Lopussa: '+ str(round(self.kassa_cum[-1],-1)) + '. ROI: ' + str(round((self.kassa_cum[-1]-self.kassa_cum_start)/(self.kassa_cum_start)*100,2)) + '%.')
		plt.grid()

		plt.subplot(223)
		plt.plot(t2, 'o')
		z = np.polyfit(x, t2, 4)
		p = np.poly1d(z)
		pylab.plot(x, p(x), "r--")

		plt.show()
		
		'''
		plt.plot(self.kassa)
		title = 'Kassankasvu - ROI: ' + str(round(self.ROI(),2)) + '% - games: ' + str(self.games)
		plt.title(title)
		plt.grid()
		plt.show()
		'''

	def Tournaments(self):
		tournaments = []
		for item in self.tournaments:
			tournaments.append([item, self.tournaments[item].games, self.tournaments[item].played, self.tournaments[item].won-self.tournaments[item].played])
		print '\n---------------------------------------------------------------------------------'
		for item in reversed(sorted(tournaments, key=lambda arvo: arvo[3])):
			print '| {:<31s} | games: {:<3.0f} | played: {:>7.2f} | won: {:>7.2f} |'.format(item[0], item[1], item[2], item[3])
		print '---------------------------------------------------------------------------------\n'

	def match(self, row, home_elo, away_elo, blue, kelly, Teams, muuttuja):
		regions = ['EUW', 'NA', 'KR', 'CN']#, 'WR', 'TW', 'CIS', 'BR'
		if (row[2] != '' and row[2] != '-' and row[1] != '2' and int(row[0]) > self.date and row[10] in regions):

			# Kansainvalinen ottelu
			if row[10] == 'WR':
				home_elo = home_elo*Teams[row[5]].region_(muuttuja)
				away_elo = away_elo*Teams[row[6]].region_(muuttuja)

			home_odds = float(row[2])
			away_odds = float(row[4])
			winner = self.winner(row)

			OA1_B = (1/(1+10**(((away_elo-(home_elo+blue)))/float(400))))
			OA2_R = 1-OA1_B
			OA2_B = (1/(1+10**(((home_elo-(away_elo+blue)))/float(400))))
			OA1_R = 1-OA2_B

			tournament = row[-2]
			if tournament not in self.tournaments:
				self.tournaments[tournament] = Tournament(tournament)

			# Best of 1
			if (row[1] == '1' or row[1] == ''):
				OA1 = OA1_B
				OA2 = OA2_R

			# Best of 3
			elif row[1] == '3':
				OA1 = OA1_B*OA1_R + OA1_B*OA2_B*OA1_B + OA2_R*OA1_R*OA1_B
				OA2 = 1-OA1

			# Best of 5
			elif row[1] == '5':
				OA1 = OA1_B*OA1_R*OA1_B + OA1_B*OA2_B*OA1_B*OA1_R + OA2_R*OA1_R*OA1_B*OA1_R + OA1_B*OA1_R*OA2_R*OA1_R + OA1_B*OA1_R*OA2_R*OA2_B*OA1_B + OA1_B*OA2_B*OA1_B*OA2_B*OA1_B + OA2_R*OA2_B*OA1_B*OA1_R*OA1_B + OA2_R*OA1_R*OA2_R*OA1_R*OA1_B + OA2_R*OA1_R*OA1_B*OA2_B*OA1_B + OA1_B*OA2_B*OA2_R*OA1_R*OA1_B
				OA2 = OA2_R*OA2_B*OA2_R + OA2_R*OA1_R*OA2_R*OA2_B + OA1_B*OA2_B*OA2_R*OA2_B + OA2_R*OA2_B*OA1_B*OA2_B + OA2_R*OA2_B*OA1_B*OA1_R*OA2_R + OA2_R*OA1_R*OA2_R*OA1_R*OA2_R + OA1_B*OA1_R*OA2_R*OA2_B*OA2_R + OA1_B*OA2_B*OA1_B*OA2_B*OA2_R + OA1_B*OA2_B*OA2_R*OA1_R*OA2_R + OA2_R*OA1_R*OA1_B*OA2_B*OA2_R

			if winner == 1:
				self.log_sum.append(abs(OA1))
				self.log_sum_odds.append(abs(1/home_odds))
			else:
				self.log_sum.append(abs(OA1))
				self.log_sum_odds.append(abs(1/away_odds))
			
			if home_odds > 1/OA1:
				self.games += 1
				panos = (OA1*home_odds-1)/float(home_odds-1)/float(kelly)*100
				if panos >= self.max_betsize:
					panos = self.max_betsize

				panos_cum = panos/100 * self.kassa_cum[-1]
				if self.tasapanos == 1:
					panos = 1

				self.played += panos
				self.tournaments[tournament].played += panos
				self.tournaments[tournament].games += 1
				self.OA.append(home_odds*OA1*100)
				self.EV.append(self.EV[-1]+(OA1*(panos*home_odds-panos)-(OA2*panos)))
				self.EV_cum.append(self.EV_cum[-1]+(OA1*(panos_cum*home_odds-panos_cum)-(OA2*panos_cum)))
				self.pal5.append(self.pal5[-1]+(panos*self.pal5_-panos))

				if winner == 1:
					self.won += panos*home_odds
					self.tournaments[tournament].won += panos*home_odds
					self.kassa_cum.append((panos_cum*home_odds + self.kassa_cum[-1] - panos_cum))

				else:
					self.kassa_cum.append(self.kassa_cum[-1] - panos_cum)
		
				self.kassa.append(self.profit())
				print '{}: {:>20s} {:.2f} (x) -     {:.2f} {:20s} <> {:4.2f}% ({:.2f}) - ({:.2f}) {:4.2f}% <> Ottelun tulos: {:.0f} Kassa: {:.2f} Panos: {:.2f} OA: {:.2f}% EV: {:.2f}'.format(row[0], row[5], home_odds, away_odds, row[6], OA1*100, 1/(OA1), 1/(OA2), OA2*100, winner, self.profit(), panos, home_odds*OA1*100, self.EV[-1])
				

			elif away_odds > 1/OA2:
				self.games += 1
				panos = (OA2*away_odds-1)/float(away_odds-1)/float(kelly)*100
				if panos >= self.max_betsize:
					panos = self.max_betsize

				panos_cum = panos/100 * self.kassa_cum[-1]
				if self.tasapanos == 1:
					panos = 1

				self.played += panos
				self.tournaments[tournament].played += panos
				self.tournaments[tournament].games += 1
				self.OA.append(away_odds*OA2*100)
				self.EV.append(self.EV[-1]+(OA2*(panos*away_odds-panos)-(OA1*panos)))
				self.EV_cum.append(self.EV_cum[-1]+(OA2*(panos_cum*away_odds-panos_cum)-(OA1*panos_cum)))
				self.pal5.append(self.pal5[-1]+(panos*self.pal5_-panos))

				if winner == 2:
					self.won += panos*away_odds
					self.tournaments[tournament].won += panos*away_odds
					self.kassa_cum.append((panos_cum*away_odds + self.kassa_cum[-1] - panos_cum))

				else:
					self.kassa_cum.append(self.kassa_cum[-1] - panos_cum)

				self.kassa.append(self.profit())
				print '{}: {:>20s} {:.2f}     - (x) {:.2f} {:20s} <> {:4.2f}% ({:.2f}) - ({:.2f}) {:4.2f}% <> Ottelun tulos: {:.0f} Kassa: {:.2f} Panos: {:.2f} OA: {:.2f}%, EV: {:.2f}'.format(row[0], row[5], home_odds, away_odds, row[6], OA1*100, 1/(OA1), 1/(OA2), OA2*100, winner, self.profit(), panos, away_odds*OA2*100, self.EV[-1])
				




