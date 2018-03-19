#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import csv
from bs4 import BeautifulSoup
from datetime import datetime
from URL import URL

start_url = 'http://www.gamesoflegends.com/home/home.php?region=ALL&start='


# 1. filename
file1 = 'raw_database.csv'
file2 = 'team_name.csv'
file3 = 'sorted_database.csv'
file4 = 'oddsportal_data.csv'
file5 = 'Database_odds.csv'
file6 = 'Manual_data.csv'

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

	def Elli_vaihtaa_nimet(self):
		return self.top.name.encode('utf-8')+','+self.top.champion+','+self.top.kda+','+self.top.cs+','+self.top.gold+','+self.top.dmg + ':' + self.jun.name.encode('utf-8')+','+self.jun.champion+','+self.jun.kda+','+self.jun.cs+','+self.jun.gold+','+self.jun.dmg + ':' + self.mid.name.encode('utf-8')+','+self.mid.champion+','+self.mid.kda+','+self.mid.cs+','+self.mid.gold+','+self.mid.dmg + ':' + self.adc.name.encode('utf-8')+','+self.adc.champion+','+self.adc.kda+','+self.adc.cs+','+self.adc.gold+','+self.adc.dmg + ':' + self.sup.name.encode('utf-8')+','+self.sup.champion+','+self.sup.kda+','+self.sup.cs+','+self.sup.gold+','+self.sup.dmg

	def Tomi_vaihtaa_nimet(self):
		return self.top.name.encode('utf-8') + ',' + self.jun.name.encode('utf-8') + ',' + self.mid.name.encode('utf-8') + ',' + self.adc.name.encode('utf-8') + ',' + self.sup.name.encode('utf-8')

class Open_web():

	def Return_Soup(self, url):

		req = urllib2.Request(url, headers = {'User-Agent' : 'Kikkeliskokkelis'})
		con = urllib2.urlopen(req)
		html = con.read()
		soup = BeautifulSoup(html, 'lxml')

		return soup

	def Date(self, date):

		for item in date:
			if item['class'] == ['col-xs-12', 'col-sm-4', 'text-right']:
				date = item.text
				start = date.find(' (')

				return date[:start].replace('-','')

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

	def Players(self, soup):


		team1 = TT()
		team2 = TT()

		i = 0
		N = 0
		for item in soup:

			p = PP()
			'''
			if gold_dist != []:
				p.gold = gold_dist[i].split(',')[N]
				p.dmg = dmg_dist[i].split(',')[N]
			'''
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

		#t1 = team1.Elli_vaihtaa_nimet()
		#t2 = team2.Elli_vaihtaa_nimet()
				
		t1 = team1.Tomi_vaihtaa_nimet()
		t2 = team2.Tomi_vaihtaa_nimet()
		

		return t1, t2

	def Region(self, data):
		for item in data:
			if item['class'] == ['col-xs-12', 'col-sm-4', 'text-left']:
				tournament = item.text[:item.text.find(' (')].replace('\n','')
				start = item.text.find('(')
				region = item.text[start:].replace('(','').replace(')','').replace(' ','').encode('utf-8')

				return region, tournament

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

	def BO(self, data):

		for item in data:
			if 'BO' in item.text:
				BO = item.text.replace('BO','')
				return BO
		return '1'

	def team_names(self):

		with open(file1, 'rb') as f:
			data = list(csv.reader(f,delimiter=';'))
		f.close()

		matches = []
		teams = []
		for ro in data:
			home = ro[2]
			away = ro[3]

			if home not in teams:
				teams.append(home)
			if away not in teams:
				teams.append(away)
			with open(file2, 'rb') as f:
				for row in csv.reader(f):
					if home == row[0]:
						ro[2] = row[1]
					if away == row[0]:
						ro[3] = row[1]
			f.close()

			matches.append(ro)
		#for team in teams:
		#	print team
		with open(file1, 'wb') as f:
			writer = csv.writer(f, delimiter=';')
			for match in matches:
				writer.writerow(match)
		f.close()

	def Gold_Graph(self, data, team1, team2):

		data = str(data)
		start = data.find("label: 'Gold', ")
		data = data[start:].replace(' ', '').replace('\t', '').replace('\n', '')
		end = data.find('],')
		data = data[:end]

		start = data.find('[')
		data = data[start+1:].split(',')[:-1]

		# Plots the graph
		'''
		import matplotlib.pyplot as plt
		
		title = team1 + ' - ' + team2
		plt.plot(data)
		plt.title(title)
		plt.show()
		'''
		ggraph = ''
		for item in data:
			ggraph += item.encode('utf-8') + ','
		
		return ggraph[:-1]
		

	def Time(self, data):

		time = data[0].text.split(':')
		minutes = int(time[0])
		sec = int(time[1])/float(60)
		time = minutes+sec

		return round(time,2)

	def Output(self, data):

		#info = [Date, Result, Blue_team, Red_team, Blue_players, Red_players, Gametime, BO, Region, League, Gamesoflegends_url, Lolesports]
		
		Date = data[0]
		Result = data[1]
		Score = Result.split(':')[0].encode('utf-8')
		Blue_team = data[2].decode('utf-8').encode('utf-8')					
		Red_team = data[3].decode('utf-8').encode('utf-8')					
		Blue_players = data[4].encode('utf-8')					
		Red_players = data[5].encode('utf-8')
		Gametime = data[6]
		BO = data[7].encode('utf-8')
		Region = data[8].encode('utf-8')
		League = data[9].encode('utf-8')

		
		print '\tDate: {}, {} {} {} ({}) {}'.format(Date, Blue_team, Score, Red_team, BO, League)

	def TeamData(self, data):

		data2 = []
		for item in data:
			data2.append(item.text.replace(' ', '').replace('\t', '').replace('\n', '').encode('utf-8'))

		# Split data between both teams
		half = int(len(data2)/float(2))

		team1_data = ''
		for item in data2[:half]:
			team1_data += item + ','

		tdd = list(reversed(team1_data[:-1].split(',')))

		team1_data = ''
		for item in tdd:
			team1_data += item + ','
		team1_data = team1_data[:-1]

		team2_data = ''
		for item in data2[half:]:
			team2_data += item + ','
		team2_data = team2_data[:-1]

		return team1_data, team2_data

	def Lolesports(self, data):

		for item in data:
			if item['title'] == 'Riot Match History':
				return item['href']
			
	def Graph_players_gold(self, data):

		gold_dist = []
		dmg_dist = []
		i = 0
		for item in data:

			if (i != 0 and i <= 5):
				st = item.text.replace(' ', '').replace('\t', '').replace('\n', '').replace('TOP','').replace('SUPPORT','').replace('MID','').replace('JUNGLE','').replace('ADC','').split('%')
				st = st[0].encode('utf-8') + ',' + st[1].encode('utf-8')
				gold_dist.append(st)

			elif (i != 0 and i > 6):
				st = item.text.replace(' ', '').replace('\t', '').replace('\n', '').replace('TOP','').replace('SUPPORT','').replace('MID','').replace('JUNGLE','').replace('ADC','').split('%')
				st = st[0] + ',' + st[1]
				dmg_dist.append(st)
		
			i += 1
		
		return gold_dist, dmg_dist

		

start = datetime.now()
N = 100
iteration = 0

ddate = ''
num = 0
# 
for i in range(0, N, 10):

	while True:

		try:
			database = []
			with open(file1, 'rb') as file:
				reader = csv.reader(file, delimiter=';')
				for row in reader:
					database.append(row[10])
			file.close()

			url = start_url + str(i)
			selector = 'body > div > div > div > div > div > div > table > tbody > tr > td > a'
			data = Open_web().Return_Soup(url).select(selector)

			for link in data:
				link = link['href'][2:]

				if 'gameshow' in link:

					new_url = 'http://www.gamesoflegends.com' + link

					#print 'new_url: ',new_url.replace('&page=pw','')
					#if new_url.replace('&page=pw','') not in database:

					new_url = new_url.replace('&page=pw','&page=end')
						
					BO = Open_web().BO(Open_web().Return_Soup(new_url).select('body > div > div > div > div > table > tr > td'))

					selector = 'body > div > div > div > div > table > tr > td > a'
					data = Open_web().Return_Soup(new_url).select(selector)

					for link in data:

						if 'Game' in link.text:

							game_url = 'http://www.gamesoflegends.com' + link['href'][2:]
					
							if (game_url not in database and 'stats.' not in game_url):
								
								print game_url
						
								soup = Open_web().Return_Soup(game_url)

								Blue_team, Red_team = Open_web().Teams(soup.select('body > div > div > div > div > table > tr > td > a'))
								
								#gold_graph = Open_web().Gold_Graph(soup.select('body > div > div > script'), team1, team2)
								
								Date = Open_web().Date(soup.select('body > div > div > div > div'))
								
								Region, League = Open_web().Region(soup.select('body > div > div > div > div'))
								
								if League == 'NA LCS Spring 2018':
									Date = str(int(Date)+1)

								Gametime = Open_web().Time(soup.select('#spantime'))

								Result = Open_web().Winner(soup.select('body > div > div > div > div > table > tr > td'))	

								#team1_data, team2_data = Open_web().TeamData(soup.select('body > div > div > div > div > table > tr > td > div > div > div'))

								#gold_dist, dmg_dist = Open_web().Graph_players_gold(soup.select('body > div > div > div > div > table > tr > td > div > table > tr'))

								Blue_players, Red_players = Open_web().Players(soup.select('body > div > div > div > div > table > tr > td > table > tr'))
								
								Lolesports = Open_web().Lolesports(soup.select('body > div > div > div > div > table > tr > td > a'))
								Gamesoflegends_url = game_url

								info = [Date, Result, Blue_team, Red_team, Blue_players, Red_players, Gametime, BO, Region, League, Gamesoflegends_url, Lolesports]
								#info = [date, winner, team1, team2, players1, players2, game_url, region, BO, gold_graph, gold_dist, dmg_dist, time, team1_data, team2_data, lolesports_url]

								Open_web().Output(info)
				
								with open(file1, 'ab') as file:
									writer = csv.writer(file, delimiter = ';')
									writer.writerow(info)
								file.close()

								iteration += 1
								if iteration % 20 == 0:
									print 'Runtime: {}, {}/{}'.format(datetime.now()-start,iteration,N)
			break

		except Exception:
			print '\nCrash at {}\n'.format(datetime.now()-start)
			pass
#print 'Done!';quit()

URL().All_into_same_file(file1, file3, file6)

#Open_web().team_names()

URL().Oddsportal(file3, file4, file5)
quit()
