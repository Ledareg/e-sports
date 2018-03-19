import csv

class Team2():
	def __init__(self, nic, top, jun, mid, adc, sup, Players):
		self.nic = nic
		self.top = top
		self.jun = jun
		self.mid = mid
		self.adc = adc
		self.sup = sup

		try:
			self.top_elo = Players[self.top].top_elo[-1]
		except KeyError:
			self.top_elo = 1450
		try:
			self.jun_elo = Players[self.jun].jun_elo[-1]
		except KeyError:
			self.jun_elo = 1450
		try:
			self.mid_elo = Players[self.mid].mid_elo[-1]
		except KeyError:
			self.mid_elo = 1450
		try:
			self.adc_elo = Players[self.adc].adc_elo[-1]
		except KeyError:
			self.adc_elo = 1450
		try:
			self.sup_elo = Players[self.sup].sup_elo[-1]
		except KeyError:
			self.sup_elo = 1450
		try:
			self.top_games = Players[self.top].top_games
		except KeyError:
			self.top_games = 0
		try:
			self.jun_games = Players[self.jun].jun_games
		except KeyError:
			self.jun_games = 0
		try:
			self.mid_games = Players[self.mid].mid_games
		except KeyError:
			self.mid_games = 0
		try:
			self.adc_games = Players[self.adc].adc_games
		except KeyError:
			self.adc_games = 0
		try:
			self.sup_games = Players[self.sup].sup_games
		except KeyError:
			self.sup_games = 0
	'''
	def Elo(self, side):
		if side == 'blue':
			return (self.top_elo_blue + self.jun_elo_blue + self.mid_elo_blue + self.adc_elo_blue + self.sup_elo_blue)/float(5)
		else:
			return (self.top_elo_red + self.jun_elo_red + self.mid_elo_red + self.adc_elo_red + self.sup_elo_red)/float(5)
	'''
	def Out(self, team):
		return [team, self.nic, self.top, int(round(self.top_elo,0)), self.top_games, self.jun, int(round(self.jun_elo,0)), self.jun_games, self.mid, int(round(self.mid_elo,0)), self.mid_games, self.adc, int(round(self.adc_elo,0)), self.adc_games, self.sup, int(round(self.sup_elo,0)), self.sup_games]	

	def Out2(self, team):
		return [team, self.nic, self.top, int(round(self.top_elo,0)), self.top_games, self.jun, int(round(self.jun_elo,0)), self.jun_games, self.mid, int(round(self.mid_elo,0)), self.mid_games, self.adc, int(round(self.adc_elo,0)), self.adc_games, self.sup, int(round(self.sup_elo,0)), self.sup_games]	
class Team():

	def Read_teams(self, Players):
		Teams = {}

		i = 0
		with open('rosters.csv', 'rb') as file:
			data = list(csv.reader(file, delimiter=';'))
		file.close()
			
		for row in data:
			if row != '':
				if row[0] == '{':
					Teams = Team().Format_data(data[i+1], data[i+2], data[i+3], data[i+4], data[i+5], data[i+6], data[i+7], Teams, Players)
			i += 1

		return Teams

	def Last5(self, Players, file):
		Teams = {}
		with open(file, 'rb') as fi:
			reader = csv.reader(fi, delimiter=';')
			for row in reader:
				home = row[5]
				away = row[6]
				if home not in Teams:
					Teams[home] = []
				if away not in Teams:
					Teams[away] = []
				i = 0
				for score in row[7].split(','):
					if score == '1-0':
						away_outcome = 'lose'
						home_outcome = 'win'
					else:
						home_outcome = 'lose'
						away_outcome = 'win'



					Teams[home].append([row[8].split(':')[i],home_outcome,away])
					Teams[away].append([row[9].split(':')[i],away_outcome,home])
					i += 1
		fi.close()

		jouk = Team().Read_teams(Players)

		data = []
		for item in jouk:
			tt = [item]
			for game in Teams[item][-5:]:
				#print 'Players: {}, outcome: {} vs. {}'.format(game[0], game[1], game[2])
				tt.append(game[0])
				tt.append(game[1])
				tt.append(game[2])
			data.append(tt)

		with open('Excel data/Team_last_game_data.csv', 'wb') as file:
			writer = csv.writer(file)
			for item in data:
				writer.writerow(item)
		file.close()

	def Match(self, team1, team2, Teams):
		blue = 0
		OA1_B = (1/(1+10**((team2.Elo('red')-(team1.Elo('blue')+blue))/float(400))))
		OA2_R = 1-OA1_B
		OA2_B = (1/(1+10**((team1.Elo('red')-(team2.Elo('blue')+blue))/float(400))))
		OA1_R = 1-OA2_B

		#bo = raw_input('BO: ')

		bo = 3

		if bo == 3:
			OA1 = OA1_B*OA1_R + OA1_B*OA2_B*OA1_B + OA2_R*OA1_R*OA1_B
			OA2 = 1-OA1
			print('{} arvio {:.1f}% raja {:.2f}'.format(team1.nic,OA1*100,1/OA1))
			print('{} arvio {:.1f}% raja {:.2f}'.format(team2.nic,OA2*100,1/OA2))
			print('{} 2-0 raja {:.2f}~{:.1f}% | +1.5 {:.2f}~{:.1f}%'.format(team1.nic,1/(OA1_B*OA1_R),OA1_B*OA1_R*100,1/(1-OA2_R*OA2_B),100*(1-OA2_R*OA2_B)))
			print('{} 2-0 raja {:.2f}~{:.1f}% | +1.5 {:.2f}~{:.1f}%'.format(team2.nic,1/(OA2_B*OA2_R),OA2_B*OA2_R*100,1/(1-OA1_R*OA1_B),100*(1-OA1_R*OA1_B)))
			#print('')
			print('Under {:.2f}~{:.1f}%, Over {:.2f}~{:.1f}%'.format(1/float(OA1_B*OA1_R+OA2_B*OA2_R),(OA1_B*OA1_R+OA2_B*OA2_R)*100,1/float(1-(OA1_B*OA1_R+OA2_B*OA2_R)),(1-(OA1_B*OA1_R+OA2_B*OA2_R))*100))
			#print('')
			print('2-0 {:.2f}~{:.1f}%, 2-1 {:.2f}~{:.1f}%, 1-2 {:.2f}~{:.1f}%, 0-2 {:.2f}~{:.1f}%'.format(1/(OA1_B*OA1_R),OA1_B*OA1_R*100,1/(OA1-(OA1_B*OA1_R)),(OA1-OA1_B*OA1_R)*100,1/(OA2-(OA2_B*OA2_R)),(OA2-OA2_B*OA2_R)*100,1/(OA2_B*OA2_R),OA2_B*OA2_R*100))
			print('---------------')



	def Format_data(self, team_name, nickname, top, jun, mid, adc, sup, Teams, Players):
		team_name = team_name[0].replace('\tTeam name: ','').split(',')[0]
		nickname = nickname[0].replace('\tNickname: ','').split(',')[0]
		top = Team().AaAaA(top[0].replace('\tTop: ','').split(','))
		jun = Team().AaAaA(jun[0].replace('\tJungle: ','').split(','))
		mid = Team().AaAaA(mid[0].replace('\tMid: ','').split(','))
		adc = Team().AaAaA(adc[0].replace('\tAdc: ','').split(','))
		sup = Team().AaAaA(sup[0].replace('\tSupport: ','').split(','))

		if team_name not in Teams:
			Teams[team_name] = Team2(nickname, top, jun, mid, adc, sup, Players)

		return Teams

	def AaAaA(self, data):
		i = 0
		nn = ''
		for item in data:
			if i == 0:
				nn += item +','
			else:
				nn += item[1:] +','
			i += 1

		return nn[:-1].split(',')[0]

	def Calculator(self, Players):
		while True:
			try:
				while True:
					Teams = Team().Read_teams(Players)

					team1 = raw_input('\nGive bluside nicname: ')
					team2 = raw_input('Give redside nicname: ')
					print '\n'

					for team in Teams:
						if Teams[team].nic == team1:
							Teams[team].Print(team, 'blue')
							team1 = team
						if Teams[team].nic == team2:
							Teams[team].Print(team, 'red')
							team2 = team

					Team().Match(Teams[team1], Teams[team2], Teams)

					if (raw_input('\nNew match? (Y/n): ')).lower() != 'y':
						break
					else:
						continue
				break
			except KeyError:
				print 'Error with name!\n'

	def Excel(self, Players):
		data = []
		with open('Excel data/Excel_data.csv', 'wb') as file:
			writer = csv.writer(file)
			Teams = Team().Read_teams(Players)
			for team in Teams:
				data.append(Teams[team].Out(team))
			for item in sorted(data, key=lambda arvo: arvo[0]):
				writer.writerow(item)
		file.close()

		#import os
		#os.system("open Kokeilu.xlsm")

	def Regions(self, Players):
		EU = ['FNC', 'G2', 'MIS', 'H2k', 'SPY', 'ROC', 'VIT', 'UoL', 'GIA', 'S04']
		with open('Excel data/EU.csv' , 'wb') as file:
			writer = csv.writer(file)
			Teams = Team().Read_teams(Players)
			for team in Teams:
				if Teams[team].Out2(team)[1] in EU:
					writer.writerow(Teams[team].Out(team))
		file.close()

		NA = ['100', 'C9', 'Clutch', 'CLG', 'FOX', 'GGS', 'OpTic', 'TL', 'TSM', 'FLY']
		with open('Excel data/NA.csv' , 'wb') as file:
			writer = csv.writer(file)
			Teams = Team().Read_teams(Players)
			for team in Teams:
				if Teams[team].Out2(team)[1] in NA:
					writer.writerow(Teams[team].Out(team))
		file.close()

		LPL = ['TOP', 'SNG', 'RNG', 'BLG', 'EDG', 'FPX', 'iG', 'JDG', 'OMG', 'LGD', 'ROG', 'SN', 'WE', 'VG']
		with open('Excel data/LPL.csv' , 'wb') as file:
			writer = csv.writer(file)
			Teams = Team().Read_teams(Players)
			for team in Teams:
				if Teams[team].Out2(team)[1] in LPL:
					writer.writerow(Teams[team].Out(team))
		file.close()

		LCK = ['AFs', 'bbq', 'JAG', 'KDX', 'KDM', 'KSV', 'KT', 'MVP', 'ROX', 'SKT']
		with open('Excel data/LCK.csv' , 'wb') as file:
			writer = csv.writer(file)
			Teams = Team().Read_teams(Players)
			for team in Teams:
				if Teams[team].Out2(team)[1] in LCK:
					writer.writerow(Teams[team].Out(team))
		file.close()

