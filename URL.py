#!/usr/bin/env python
# -*- coding: utf-8 -*-

######!		Lolesports scraper written by TG++ !#######

import urllib2
from bs4 import BeautifulSoup
import re
import csv
from time import strftime
import unicodecsv
from datetime import datetime
import os
import os.path
from pathlib import Path
from more_itertools import unique_everseen
import shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
import threading
import Queue
from ff import Fo

class Tournament():

	def __init__(self,url,region):
		self.url = url
		self.region = region

	def re(self,name):
		return [name,self.url,self.region]

class URL():

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
		'''
		ps = []
		with open('Players.csv', 'rb') as f:
			reader = csv.reader(f)
			for item in reader:
				ps.append(item[0])
		f.close()
	
		with open(file6, 'rb') as f:
			reader = csv.reader(f, delimiter= ';')
			for row in reader:
				if row != []:
					p1 = []
					pp1 = ''
					for item in row[4].split(','):
						p1.append(item)
						pp1+=item + ','
					p2 = []
					pp2 = ''
					for item in row[5].split(','):
						p2.append(item)
						pp2+=item+ ','
					row[4] = pp1[:-1]
					row[5] = pp2[:-1]
					p = p1+p2
					Date = row[0]
					Result = row[1]
					Blue_team = row[2]
					Red_team = row[3]
					Blue_players = row[4]
					Red_players = row[5]
					Gametime = row[12]
					Region = row[7]
					BO = row[8]
					League = ''
					Gamesoflegends_url = ''
					Lolesports = ''
					info = [Date, Result, Blue_team, Red_team, Blue_players, Red_players, Gametime, BO, Region, League, Gamesoflegends_url, Lolesports]

					games.append(info)

		f.close()
		'''
		'''
		Nimien muuttaja. Kesken!
		'''
		games = URL().Name_changer(games)

		# Kaikki pelit samaan tiedostoon oikeaan järjestykseen
		file2 = file1.replace('.csv', '') + '2' + '.csv'

		with open(file2, 'wb') as f:
			writer = csv.writer(f, delimiter=';')
			games = sorted(games, key=lambda arvo: arvo[0])
			for game in games:
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

	def Oddsportal(self, file3, file4, file5):

		Fo().work(file3)

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

		data = URL().Name_changer_team(data, 1)

		data2 = []
		with open(file4,'rb') as f:
			for row in csv.reader(f, delimiter=','):
				data2.append(row)
		f.close()

		data2 = URL().Name_changer_team(data2, 2)

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
			

	def Odds_count(self,lista):
		
		i=0
		for row in lista:
			try:
				if row[3] != '':
					i+=1
			except IndexError:
				pass
		return i

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
					print item
					quit()
				else:
					players1 += str(players[item]) + ','
		
			for item in game[5].split(','):
				if item not in players.keys():
					print item
					quit()
				else:
					players2 += str(players[item]) + ','
			players1 = players1[:-1]
			players2 = players2[:-1]
			game[4] = players1
			game[5] = players2
		
		return games

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
		#print teams;quit()

		if numm == 1:
			print 'Teams in database:',len(check)
			for game in sorted(games):
				team1 = game[5]
				team2 = game[6]

				if team1 not in teams.keys():
					print team1
				else:
					team1 = teams[team1]
				
				if team2 not in teams.keys():
					print team2
					quit()
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
					print team1
				else:
					team1 = teams[team1]
				
				if team2 not in teams.keys():
					print team2
					quit()
				else:
					team2 = teams[team2]

				game[0] = team1
				game[1] = team2

			return games


	