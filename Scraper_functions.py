#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import csv
from bs4 import BeautifulSoup
from datetime import datetime
from more_itertools import unique_everseen
import datetime

class PP():
	def __init__(self):
		self.name = ''
		self.kda = ''
		self.cs = ''
		self.champion = ''
		self.dmg = ''
		self.gold = ''

class TT():
	def __init__(self):
		self.top = ''
		self.jun = ''
		self.mid = ''
		self.adc = ''
		self.sup = ''

	def AddTeam(self, player):
		if self.top == '':
			self.top = player
		elif self.jun =='':
			self.jun = player
		elif self.mid == '':
			self.mid = player
		elif self.adc == '':
			self.adc = player
		elif self.sup == '':
			self.sup = player

	def Items(self):
		i = 0
		if self.top != '':
			i += 1
		if self.jun != '':
			i += 1
		if self.mid != '':
			i += 1
		if self.adc != '':
			i += 1
		if self.sup != '':
			i += 1
		
		return i

	def Name(self):
		if self.top == '':
			return '' + ',' + self.jun.name + ',' + self.mid.name + ',' + self.adc.name + ',' + self.sup.name
		elif self.jun == '':
			return self.top.name + ',' + '' + ',' + self.mid.name + ',' + self.adc.name + ',' + self.sup.name
		elif self.mid == '':
			return self.top.name + ',' + self.jun.name + ',' + '' + ',' + self.adc.name + ',' + self.sup.name
		elif self.adc == '':
			return self.top.name + ',' + self.jun.name + ',' + self.mid.name + ',' + '' + ',' + self.sup.name
		elif self.sup == '':
			return self.top.name + ',' + self.jun.name + ',' + self.mid.name + ',' + self.adc.name + ',' + ''
		else:
			return self.top.name + ',' + self.jun.name + ',' + self.mid.name + ',' + self.adc.name + ',' + self.sup.name
		
class Scraper():

	# Function which asks user how many sites he wants to be scraped.
	def How_many_games(self):
		while True:
			try:
				n = int(raw_input("How many games you want to download: "))
				break
			except TypeError:
				print 'Give integer!'	
		return n

	# Function which returns all game urls that are already in the database.
	def Old_database(self, file, x):
		database = []
		with open(file1, 'rb') as file:
			reader = csv.reader(file, delimiter=';')
			for row in reader:
				if 'id=' in row[10]:
					database.append(row[10].split('id=')[1])
				elif 'gol.gg' in row[10]:
					database.append(row[10].split('/')[5])
				else:
					print row[10];quit()
		file.close()

		if x == 0:
			print '{:d} series currently in the database.'.format(len(database))

		return database, len(database)

	# Function which returns url as soup object (or something like that?)
	def Return_Soup(self, url):
		req = urllib2.Request(url, headers = {'User-Agent' : 'Kikkeliskokkelis'})
		con = urllib2.urlopen(req)
		html = con.read()
		soup = BeautifulSoup(html, 'lxml')

		return soup

	# Game was best of what?
	def BO(self, data):
		for item in data:
			if 'BO' in item.text:
				BO = item.text.replace('BO','')
				return BO
		return '1'

	# Return encoded team names
	def Teams(self,data):
		t1 = ''
		t2 = ''
		for item in data:
			if 'teams' in item['href']:

				if t1 == '':
					t1 = item.text

				else:
					t2 = item.text

		return t1.encode('utf-8'), t2.encode('utf-8')

	# Return date of the game
	def Date(self, date):
		for item in date:
			if item['class'] == ['col-xs-12', 'col-sm-4', 'text-right']:
				date = item.text
				start = date.find(' (')

				return date[:start].replace('-','')

	# Return region and league
	def Region(self, data):
		for item in data:
			if item['class'] == ['col-xs-12', 'col-sm-4', 'text-left']:
				tournament = item.text[:item.text.find(' (')].replace('\n','').encode('utf-8')
				start = item.text.find('(')
				region = item.text[start:].replace('(','').replace(')','').replace(' ','').encode('utf-8')

				return region, tournament

	# Return how long the game lasted
	def Time(self, data):
		time = data[0].text.split(':')
		minutes = int(time[0])
		sec = int(time[1])/float(60)
		time = minutes+sec

		return round(time,2)

	# Who won the game?
	def Winner(self,data):
		for item in data:
			if item.find(alt = "Victory") != None:
				string = str(item)
				game_time_index = string.find('spantime')
				victory_index = string.find('victory_icon.png')
				if game_time_index > victory_index:
					return '1-0:blue'
				else:
					return '0-1:red'

	# Return player names.
	def Players(self, soup):
		team1 = TT()
		team2 = TT()
		i = 0
		N = 0
		for item in soup:
			p = PP()
			i += 1
			if i == 5:
				i = 0
				N = 1
			items = item.select('td')
			for section in items:
				if section.select('a') != []:
					if 'players' in section.select('a')[0]['href']:
						p.name = section.select('a')[0].text.encode('utf-8')
					else:
						p.champion = section.select('a')[0]['title'].replace(' stats', '').encode('utf-8')
				elif (section.text != '' and section.text != ' '.decode('utf-8')):
					if '/' in section.text:
						p.kda = section.text.replace(' ', '').replace('\t', '').replace('\n', '').encode('utf-8')
					else:
						p.cs = section.text.replace(' ', '').replace('\t', '').replace('\n', '').encode('utf-8')
			if team1.Items() < 5:
				team1.AddTeam(p)

			else:
				team2.AddTeam(p)		
		t1 = team1.Name()
		t2 = team2.Name()
		
		return t1, t2

	# Return all the data in a single string
	def Output(self, data):
		Date = data[0]
		Result = data[1]
		Score = Result.split(':')[0]
		Blue_team = data[2]			
		Red_team = data[3]					
		Blue_players = data[4]				
		Red_players = data[5]
		Gametime = data[6]
		BO = data[7]
		Region = data[8]
		League = data[9]
		
		print '\tDate: {}, {} {} {} ({}) {}'.format(Date, Blue_team, Score, Red_team, BO, League)

	# Write data into file
	def Write(self, data, iteration, file1, start, N):
		with open(file1, 'ab') as file:
			writer = csv.writer(file, delimiter = ';')
			writer.writerow(data)
		file.close()
		iteration += 1
		if iteration % 20 == 0:
			print 'Runtime: {}, {}/{}'.format(datetime.datetime.now()-start,iteration,N)
		return iteration

	# Return lolesports match history url
	def Lolesports(self, data):
		for item in data:
			if item['title'] == 'Riot Match History':
				return item['href']

	# All games into same file in chronological order
	def All_into_same_file(self, file1, file3, file6):
		player = []
		games = []
		with open(file1, 'rb') as f:
			reader = csv.reader(f, delimiter= ';')
			for row in reader:
				for item in row[4].split(','):
					if item not in player:
						player.append(item)
				for item in row[5].split(','):
					if item not in player:
						player.append(item)
				games.append(row)
		f.close()
		games = Scraper().Name_changer(games)
		file2 = file1.replace('.csv', '') + '2' + '.csv'
		with open(file2, 'wb') as f:
			writer = csv.writer(f, delimiter=';')
			games = sorted(games, key=lambda arvo: arvo[0])
			for game in games:
				if game[2] != '':
					if game[2][0] == ' ':
						game[2] = game[2][1:]
					if game[2][-1] == ' ':
						game[2] = game[2][:-1]
					if game[3][0] == ' ':
						game[3] = game[3][1:]
					if game[3][-1] == ' ':
						game[3] = game[3][:-1]
				writer.writerow(game)
		f.close()
		with open(file2,'rb') as f, open(file3,'wb') as out_file:
			out_file.writelines(unique_everseen(f))
		out_file.close()

	# Change player names to match current state
	def Name_changer(self, games):
		num = 0
		players = {}
		check = []
		with open('Player.csv', 'rb') as file:
			reader = list(csv.reader(file,delimiter=';'))
			for row in reader:
				if row[0] == '{':
					if reader[num+1][0].replace('\tName: ' ,'') != '':
						if reader[num+1][0].replace('\tName: ' ,'') not in check:
							check.append(reader[num+1][0].replace('\tName: ' ,''))
						else:
							print 'Error:',reader[num+1][0].replace('\tName: ' ,'');quit()
						if len(reader[num+3][0].replace('\tAlternatives: ' ,'').split(',')) == 1:
							players[reader[num+3][0].replace('\tAlternatives: ' ,'')] = reader[num+1][0].replace('\tName: ' ,'')
						else:
							nn = 0
							for item in reader[num+3][0].replace('\tAlternatives: ' ,'').split(','):
								players[item] = reader[num+1][0].replace('\tName: ' ,'')
								nn += 1
				num+=1
		print 'Players in database:',len(check)
		for game in sorted(games):
			players1 = ''
			players2 = ''
			for item in game[4].split(','):
				if item not in players.keys():
					print 'Player: {:s} not in database.'.format(item)
				else:
					players1 += str(players[item]) + ','
			for item in game[5].split(','):
				if item not in players.keys():
					print 'Player: {:s} not in database.'.format(item)
				else:
					players2 += str(players[item]) + ','
			players1 = players1[:-1]
			players2 = players2[:-1]
			game[4] = players1
			game[5] = players2
		
		return games

	# Change team names
	def Name_changer_team(self, games, numm):
		num = 0
		teams = {}
		check = []
		with open('Team.csv', 'rb') as file:
			reader = list(csv.reader(file,delimiter=';'))
			for row in reader:
				if row[0] == '{':
					if reader[num+1][0].replace('\tName: ' ,'') != '':
						if reader[num+1][0].replace('\tName: ' ,'') not in check:
							check.append(reader[num+1][0].replace('\tName: ' ,''))
						else:
							print 'Error:',reader[num+1][0].replace('\tName: ' ,'');quit()
						if len(reader[num+3][0].replace('\tAlternatives: ' ,'').split(',')) == 1:
							teams[reader[num+3][0].replace('\tAlternatives: ' ,'')] = reader[num+1][0].replace('\tName: ' ,'')
						else:
							nn = 0
							for item in reader[num+3][0].replace('\tAlternatives: ' ,'').split(','):
								teams[item] = reader[num+1][0].replace('\tName: ' ,'')
								nn += 1
				num+=1
		if numm == 1:
			print 'Teams in database:',len(check)
			for game in sorted(games):
				team1 = game[5]
				team2 = game[6]
				if team1 not in teams.keys():
					print 'Team: {:s} not in database.'.format(team1)
				else:
					team1 = teams[team1]
				
				if team2 not in teams.keys():
					print 'Team: {:s} not in database.'.format(team2)
				else:
					team2 = teams[team2]
				aa = ''
				for item in game[-1].split(','):
					if item not in teams.keys():
						print item
					else:
						item = teams[item]
						aa += item + ','
				game[-1] = aa[:-1]
				game[5] = team1
				game[6] = team2
			return games
		else:
			for game in sorted(games):
				team1 = game[0]
				team2 = game[1]
				if team1 not in teams.keys():
					print team1, 'row369'
				else:
					team1 = teams[team1]			
				if team2 not in teams.keys():
					print team2, 'row373'
					#quit()
				else:
					team2 = teams[team2]
				game[0] = team1
				game[1] = team2
			return games

	# Function which adds odds into the database.
	def Oddsportal(self, file3, file4, file5):
		Scraper().work(file3)
		mat = []
		tiims = []
		with open(file3,'rb') as f:
			for row in csv.reader(f, delimiter=';'):
				if row[5] not in tiims:
					tiims.append(row[5])
				if row[6] not in tiims:
					tiims.append(row[6])
		f.close()
		with open(file3,'rb') as f:
			data = list(csv.reader(f, delimiter=';'))
		f.close()
		data = Scraper().Name_changer_team(data, 1)
		data2 = []
		with open(file4,'rb') as f:
			for row in csv.reader(f, delimiter=','):
				data2.append(row)
		f.close()
		data2 = Scraper().Name_changer_team(data2, 2)
		odds_data = {}
		for row in data2:
			if row[2] not in odds_data:
				odds_data[row[2]] = []
			odds_data[row[2]].append(row)
		for match in data:
			if match[0] in odds_data:	
				for game in odds_data[match[0]]:
					odds_home_name = game[0]
					odds_away_name = game[1]
					odds_home = game[4]
					odds_draw = game[5]
					odds_away = game[6]
					if match[5].lower() == odds_home_name.lower() and match[6].lower() == odds_away_name.lower():
						match[2] = odds_home
						match[3] = odds_draw
						match[4] = odds_away
					elif match[6].lower() == odds_home_name.lower() and match[5].lower() == odds_away_name.lower():			
						match[4] = odds_home
						match[3] = odds_draw
						match[2] = odds_away
			mat.append(match)
		mat = unique_everseen(mat)
		num = 0
		with open(file5, 'wb') as f:
			writer = csv.writer(f,delimiter=';')
			for match in mat:
				writer.writerow(match)
				#print match
				if match[2] != '':
					num += 1
		f.close()
		print '{} series odds in database.'.format(num)

	# Format games itno series
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

						if (league == 'NA LCS Summer 2018'):
							date = date[:4] + '/' + str(int(date[4:6])) + '/' + str(int(date[6:8]))
							date_1 = datetime.datetime.strptime(date, "%Y/%m/%d")
							date = date_1 + datetime.timedelta(days=1)
							date = date.strftime("%Y%m%d")

						tiedot = [date, BO, '', '', '', home, away, score, home_team, away_team, region, blue_red, league, blue_side]			
						tiedot = Scraper().Format_match_data(tiedot)
						games.append([tiedot])
						
			'''
			Ramove all possible dublicates
			'''
			new_list = []
			for i in games:
				if i not in new_list:
					new_list.append(i)
			games = new_list
			
			print '{} series found.'.format(len(games))
			print 'Writing all into single file.'

			
			with open(file3,'wb') as f:
				writer = csv.writer(f, delimiter=';')
				for match in games:
					writer.writerow(match[0])
			f.close()

	# Return single string of the series data
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
		tiedot = [date, BO, '', '', '', home, away, score, home_team, away_team, region, blue_red, league, blue_side]						
		
		return tiedot