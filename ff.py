#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

class Fo():

	def work(self, file3):

		if True:
	
			games = []
			print 'Formatting matches into series.'
			matches_py_date = {}
			matches = 0
			'''
			Read test data into simple dictionary for later use.
			'''
			with open(file3,'rb') as f:
				for row in csv.reader(f, delimiter=';'):
					if row[0] not in matches_py_date:
						matches_py_date[row[0]] = []
					matches_py_date[row[0]].append(row)

			'''
			Read dictionary values key by key sorted by date. Remove item when read.
			'''
			for item in sorted(matches_py_date.keys()):

				region = ''
				while len(matches_py_date[item]) > 0:

					for match in matches_py_date[item]:

						if match[1] == '1-0:blue':
							score = ['1-0']
							blue_red = ['blue']
						else:
							score = ['0-1']
							blue_red = ['red']

						date = match[0]
						home = match[2]
						away = match[3]

						BO = match[7]
						
						home_team = [match[4]]
						away_team = [match[5]]

						league = match[9]

						blue_side = [match[2]]
						
						try:
							region = match[8].replace(' ','')
						except IndexError:
							print 'ff error'
						
						#gold_graph = [match[9]]
						#game_time = [match[10]]
						#team1_data = [match[11]]
						#team2_data = [match[12]]

						tiedot = [date, BO, '', '', '', home, away, score, home_team, away_team, region, league, blue_side]
						break

					matches_py_date[item].remove(match)

					deletes = []
					a = True

					while a == True:

						for match2 in matches_py_date[item]:
							
							if match2[2].lower() == home.lower() and match2[3].lower() == away.lower():

								home_team.append(match2[4])
								away_team.append(match2[5])
								blue_side.append(match[2])

								#gold_graph.append(match[9])
								#game_time.append(match[10])
								#team1_data.append(match[11])
								#team2_data.append(match[12])

								if match2[1] == '1-0:blue':
									score.append('1-0')
									blue_red.append('blue')

								else:
									score.append('0-1')
									blue_red.append('red')

								deletes.append(match2)

							elif match2[3].lower() == home.lower() and match2[2].lower() == away.lower():

								home_team.append(match2[5])
								away_team.append(match2[4])
								blue_side.append(match[3])

								#gold_graph.append(match[9])
								#game_time.append(match[10])
								#team1_data.append(match[12])
								#team2_data.append(match[11])

								if match2[1] == '0-1:red':
									score.append('1-0')
									blue_red.append('red')
								else:
									score.append('0-1')
									blue_red.append('blue')

								deletes.append(match2)

						a = False

						if deletes != []:
							for match in deletes:
								matches_py_date[item].remove(match)
						
						matches += 1
						tiedot = [date, BO, '', '', '', home, away, score, home_team, away_team, region, blue_red, league, blue_side]
						
						tiedot = Fo().Format_match_data(tiedot)

						games.append([tiedot])

			print '{} series found.'.format(matches)
			print 'Writing all into single file.'

			with open(file3,'wb') as f:
				writer = csv.writer(f, delimiter=';')
				for match in games:
					writer.writerow(match[0])
			f.close()

	def format_names(self,home,away,teams):

		home = home.replace(' (League of Legends)','')
		away = away.replace(' (League of Legends)','')

		with open('team_name.csv', 'rb') as f:
			for row in csv.reader(f):
				if home == row[0]:
					home = row[1]
				if away == row[0]:
					away = row[1]
		f.close()

		ignored = []
		with open('ignored.csv', 'rb') as f:
			for row in csv.reader(f):
				ignored.append(row[0])
		f.close()
		
		if home not in teams:
			if home not in ignored:
				print home
			
		if away not in teams:
			if away not in ignored:
				print away
		
			
		return home, away

	def Format_match_data(self, tiedot):			
		date = tiedot[0]
		BO = tiedot[1]
		odds1 = tiedot[2]
		odds2 = tiedot[3]
		odds3 = tiedot[4]
		home = tiedot[5]
		away = tiedot[6]

		score = ''
		for item in tiedot[7]:
			score += item + ','
		score = score[:-1]

		home_team = ''
		away_team = ''

		for item in tiedot[8]:
			home_team += item + ':'
		home_team = home_team[:-1]

		for item in tiedot[9]:
			away_team += item + ':'
		away_team = away_team[:-1]

		region = tiedot[10]

		blue_red = ''
		for item in tiedot[11]:
			blue_red += item + ','
		blue_red = blue_red[:-1]

		league = tiedot[-2]

		blue_side = ''
		for item in tiedot[-1]:
			blue_side += item + ','
		blue_side = blue_side[:-1]
		'''
		gold_graph = ''
		for item in tiedot[10]:
			gold_graph += item + ','
		gold_graph = gold_graph[:-1]

		game_time = ''
		for item in tiedot[11]:
			game_time += item + ','
		game_time = game_time[:-1]

		team1_data = ''
		for item in tiedot[12]:
			team1_data += item + ','
		team1_data = team1_data[:-1]

		team2_data = ''
		for item in tiedot[13]:
			team2_data += item + ','
		team2_data = team2_data[:-1]
		'''

		tiedot = [date, BO, '', '', '', home, away, score, home_team, away_team, region, blue_red, league, blue_side]
						
		
		return tiedot















