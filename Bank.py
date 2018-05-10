
class Tournament():
	def __init__(self, name):
		self.name = name
		self.played = 0
		self.games = 0
		self.won = 0

class Bank():
	def __init__(self, max_betsize, date):
		self.games = 0
		self.played = 0
		self.won = 0
		self.maxOA = 130000 # %
		self.log_sum = []
		self.log_sum_odds = []
		self.kassa = [0]
		self.max_betsize = max_betsize
		self.date = date
		self.OA = []
		self.tournaments = {}

	def ROI(self):
		#return ((self.profit()-self.kassa[0])/float(self.played+self.kassa[0]))*100
		return (1+(self.profit())/float(self.played))*100

	def profit(self):
		#return self.won - self.played + self.kassa[0]
		return self.won - self.played

	def var(self):
		return self.ROI() - sum(self.OA)/float(len(self.OA))

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
		plt.plot(self.kassa)
		title = 'Kassankasvu - ROI: ' + str(round(self.ROI(),2)) + '% - games: ' + str(self.games)
		plt.title(title)
		plt.grid()
		plt.show()

	def Tournaments(self):
		tournaments = []
		for item in self.tournaments:
			tournaments.append([item, self.tournaments[item].games, self.tournaments[item].played, self.tournaments[item].won-self.tournaments[item].played])
		print '\n---------------------------------------------------------------------------------'
		for item in reversed(sorted(tournaments, key=lambda arvo: arvo[3])):
			print '| {:<31s} | games: {:<3.0f} | played: {:>7.2f} | won: {:>7.2f} |'.format(item[0], item[1], item[2], item[3])
		print '---------------------------------------------------------------------------------\n'

	def match(self, row, home_elo, away_elo, blue, kelly, Teams):
		regions = ['WR']#['EUW', 'NA', 'KR', 'CN', 'WR']
		#print row[10]
		if (row[2] != '' and row[2] != '-' and row[1] != '2' and int(row[0]) > self.date and row[10] in regions):
			
			# Kansainvalinen ottelu
			if row[10] == 'WR':
				print Teams[row[5]], Teams[row[5]].region_(), Teams[row[5]].region
				print Teams[row[6]], Teams[row[6]].region_(), Teams[row[6]].region

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

				#panos = panos * self.kassa[-1]
				#panos = 1

				self.played += panos
				self.tournaments[tournament].played += panos
				self.tournaments[tournament].games += 1
				self.OA.append(home_odds*OA1*100)

				if winner == 1:
					self.won += panos*home_odds
					self.tournaments[tournament].won += panos*home_odds

				self.kassa.append(self.profit())

				#print '{}: {:>20s} {:.2f} (x) -     {:.2f} {:20s} <> {:4.2f}% ({:.2f}) - ({:.2f}) {:4.2f}% <> Ottelun tulos: {:.0f} Kassa: {:.2f} Panos: {:.2f} OA: {:.2f}%'.format(row[0], row[5], home_odds, away_odds, row[6], OA1*100, 1/(OA1), 1/(OA2), OA2*100, winner, self.profit(), panos, home_odds*OA1*100)
				

			elif away_odds > 1/OA2:
				self.games += 1
				panos = (OA2*away_odds-1)/float(away_odds-1)/float(kelly)*100
				if panos >= self.max_betsize:
					panos = self.max_betsize

				#panos = panos * self.kassa[-1]
				#panos = 1

				self.played += panos
				self.tournaments[tournament].played += panos
				self.tournaments[tournament].games += 1
				self.OA.append(away_odds*OA2*100)

				if winner == 2:
					self.won += panos*away_odds
					self.tournaments[tournament].won += panos*away_odds

				self.kassa.append(self.profit())

				#print '{}: {:>20s} {:.2f}     - (x) {:.2f} {:20s} <> {:4.2f}% ({:.2f}) - ({:.2f}) {:4.2f}% <> Ottelun tulos: {:.0f} Kassa: {:.2f} Panos: {:.2f} OA: {:.2f}%'.format(row[0], row[5], home_odds, away_odds, row[6], OA1*100, 1/(OA1), 1/(OA2), OA2*100, winner, self.profit(), panos, away_odds*OA2*100)
				




