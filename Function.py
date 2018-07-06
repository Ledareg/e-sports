
import csv
from Player import Player
from Team import Team
from Bank import Bank
from hit import Hit


class Function():

	def Open_file(self, filename):

		with open(filename, 'rb') as file:
			data = list(csv.reader(file, delimiter = ';'))
		file.close()

		return data

	def Calculate_elo(self, data, k, min_games, blue, m):

		Players = {}
		Teams = {}

		k = k
		min_games = min_games
		blue = blue
		kelly = 12
		max_betsize = 1
		date = 20180000

		bank = Bank(max_betsize, date)
		hit = Hit()

		for series in data:
			i = 0
			home = series[5] # Home team
			away = series[6] # Away team
			game_scores = series[7].split(',')
			region = series[10]
			winning_sides = series[11].split(',')
			league = series[12]
			blue_side_team = series[13].split(',')

			players1 = series[8].split(':')
			players2 = series[9].split(':')

			for result in game_scores:
				winning_side = winning_sides[i]
				home_players = players1[i].split(',')
				away_players = players2[i].split(',')

				for player in (home_players+away_players):
					if player not in Players:
						Players[player] = Player(k, min_games, player)
				
				# Determine team regions
				for team in [home, away]:
					if team not in Teams:
						Teams[team] = Team(team)
					if region != 'WR':
						Teams[team].region = region
				
				avg = Function().avg(Players)
				home_elo = Function().team_avg(home_players, Players)
				away_elo = Function().team_avg(away_players, Players)

				'''
				if blue_side_team[i] == home:
					hit.game(home_elo+blue, away_elo, result)
				else:
					hit.game(home_elo, away_elo+blue, result)
				'''
				if (i == 0 and Function().Min_games(home_players, away_players, 0, Players) == True):
					bank.match(series, home_elo, away_elo, blue, kelly, Teams, m)

				if result == '1-0':
					#Teams[home].win(away, away_elo)
					#Teams[away].lose(home, home_elo)
					n = 0
					for player in home_players:
						Players[player].win(away_elo, avg, n)
						n += 1
					n = 0
					for player in away_players:
						Players[player].lose(home_elo, avg, n)
						n += 1

				elif result == '0-1':
					#Teams[home].lose(away, away_elo)
					#Teams[away].win(home, home_elo)
					n = 0
					for player in home_players:
						Players[player].lose(away_elo, avg, n)
						n += 1
					n = 0
					for player in away_players:
						Players[player].win(away_elo, avg, n)
						n += 1
				else:
					print series;quit()

				i += 1


		return Players, Teams, bank, hit

	def avg(self, Players):
		summ = 0
		count = 0
		for player in Players:
			summ += Players[player].max_elo()
			count += 1
		
		return summ/float(count)

	def team_avg(self, team_players, Players):
		summ = 0
		count = 0

		for player in team_players:
			if count == 0:
				summ += Players[player].elo[-1]
			if count == 1:
				summ += Players[player].elo[-1]
			if count == 2:
				summ += Players[player].elo[-1]
			if count == 3:
				summ += Players[player].elo[-1]
			if count == 4:
				summ += Players[player].elo[-1]
			count += 1

		return summ/float(count)



	def Min_games(self, home_players, away_players, n, Players):
		i = 1
		for item in (home_players+away_players):
			if i == 1:
				if Players[item].games < n:
					return False
			elif i == 2:
				if Players[item].games < n:
					return False
			elif i == 3:
				if Players[item].games < n:
					return False
			elif i == 4:
				if Players[item].games < n:
					return False
			elif i == 5:
				if Players[item].games < n:
					return False
				i = 0
			i+=1
		return True












