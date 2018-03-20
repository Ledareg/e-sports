#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Packages needed
# pip install package
import urllib2
import csv
from bs4 import BeautifulSoup
from datetime import datetime

from Scraper_functions import Scraper as Scraper

print '\nLeague of Legends scraper\n'

# Determining constant variables
# Starting url
start_url = 'http://www.gamesoflegends.com/home/home.php?region=ALL&start='

# Filenames, these will probably change in the future
file1 = 'raw_database.csv'
file2 = 'team_name.csv'
file3 = 'sorted_database.csv'
file4 = 'oddsportal_data.csv'
file5 = 'Database_odds.csv'
file6 = 'Manual_data.csv'

# -Scraper-

# Starttime saved for later use
start = datetime.now()

# What games we already have and how many are games there actually is?
database, number_of_games = Scraper().Old_database(file1)

# How many websites are we going to scrape data from?
# This should be 50-100 if last download was made max. 1 week ago.
# If database is empty this should be 25000!
N = Scraper().How_many_games()

iteration = 0

for i in range(0, N, 10):
	while True:
		try:
			url = start_url + str(i)
			selector = 'body > div > div > div > div > div > div > table > tbody > tr > td > a'
			data = Scraper().Return_Soup(url).select(selector)

			for link in data:
				link = link['href'][2:]
				if 'gameshow' in link:
					new_url = str('http://www.gamesoflegends.com' + link).replace('&page=pw','&page=end')
					BO = Scraper().BO(Scraper().Return_Soup(new_url).select('body > div > div > div > div > table > tr > td'))
					selector = 'body > div > div > div > div > table > tr > td > a'
					data = Scraper().Return_Soup(new_url).select(selector)
					for link in data:
						if 'Game' in link.text:
							game_url = 'http://www.gamesoflegends.com' + link['href'][2:]
							if (game_url not in database and 'stats.' not in game_url):		
								print game_url
								soup = Scraper().Return_Soup(game_url)
								Blue_team, Red_team = Scraper().Teams(soup.select('body > div > div > div > div > table > tr > td > a'))	
								Date = Scraper().Date(soup.select('body > div > div > div > div'))
								Region, League = Scraper().Region(soup.select('body > div > div > div > div'))
								
								# NALCS dates are fucked up for some reason.
								if League == 'NA LCS Spring 2018':
									Date = str(int(Date)+1)

								Gametime = Scraper().Time(soup.select('#spantime'))
								Result = Scraper().Winner(soup.select('body > div > div > div > div > table > tr > td'))	
								Blue_players, Red_players = Scraper().Players(soup.select('body > div > div > div > div > table > tr > td > table > tr'))	
								Lolesports = Scraper().Lolesports(soup.select('body > div > div > div > div > table > tr > td > a'))
								Gamesoflegends_url = game_url
								info = [Date, Result, Blue_team, Red_team, Blue_players, Red_players, Gametime, BO, Region, League, Gamesoflegends_url, Lolesports]
								Scraper().Output(info)
								iteration = Scraper().Write(info, iteration, file1)
			break
		except SyntaxError:
			print '\nCrash at {}\n'.format(datetime.now()-start)
			pass

# Add all games into the same file
Scraper().All_into_same_file(file1, file3, file6)

# Add odds into the database
Scraper().Oddsportal(file3, file4, file5)













