#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import csv
from bs4 import BeautifulSoup
from datetime import datetime

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
	def Old_database(self, file1):
		database = []
		with open(file1, 'rb') as file:
			reader = csv.reader(file, delimiter=';')
			for row in reader:
				database.append(row[10])
		file.close()

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
	def Write(self, data, iteration, file1):
		with open(file1, 'ab') as file:
			writer = csv.writer(file, delimiter = ';')
			writer.writerow(data)
		file.close()
		iteration += 1
		if iteration % 20 == 0:
			print 'Runtime: {}, {}/{}'.format(datetime.now()-start,iteration,N)
		return iteration

	# Return lolesports match history url
	def Lolesports(self, data):
		for item in data:
			if item['title'] == 'Riot Match History':
				return item['href']






