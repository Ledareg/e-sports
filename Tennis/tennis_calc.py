# -#- coding: utf-8
import unicodecsv as csv
import datetime

class Player():
	def __init__(self):

		self.games = 0
		self.elo = []

		self.elo_indoors = []
		self.elo_clay = []
		self.elo_hard = []
		self.elo_grass = []




filename = 'tennis_data.csv'
Players = []

with open(filename, 'rb') as f:
	reader=csv.reader(f,delimiter=';')
	Games = list(reader)
f.close()


for match in Games:
	player1 = match[3]
	player2 = match[4]
	
	if len(match[-1].split(',')) > 1:
		terrain = match[-1].split(',')[0]
	else:
		terrain = 'NaN'

	n = 0
	for game_score in match[5]:
		if game_score <= 7:
			
		n+=1

	quit()
