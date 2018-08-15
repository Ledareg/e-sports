# -#- coding: utf-8

import unicodecsv as csv
import urllib2
from bs4 import BeautifulSoup
import datetime


def Soup(url):
	req = urllib2.Request(url, headers = {'User-Agent' : 'Kikkeliskokkelis'})
	con = urllib2.urlopen(req)
	html = con.read()
	soup = BeautifulSoup(html, 'lxml')

	return soup

def Old_data(file_name):
	DB = []
	i = 0
	with open(file_name, 'r') as f:
		reader = csv.reader(f, delimiter=';', encoding='utf-8')
		for item in reader:
			DB.append(str(item[-1]))
			i+=1
	f.close()
	print '{} games in database.'.format(i)

	return DB

def Sort_player_data(data, n, odds2):
	if n == 1:
		time = data[0].split(':')
		time = ''.join(time)
		name = data[1].split('(')[0]
		if name[-1] == ' ':
			name = name[:-1]
		sets = data[2]
		game1 = data[3]
		game2 = data[4]
		game3 = data[5]
		game4 = data[6]
		game5 = data[7]
		odds1 = data[8]
		odds2 = data[9]
		player = [name, sets, game1, game2, game3, game4, game5, odds1,time]

	else:
		name = data[0].split('(')[0]
		if name[-1] == ' ':
				name = name[:-1]
		sets = data[1]
		game1 = data[2]
		game2 = data[3]
		game3 = data[4]
		game4 = data[5]
		game5 = data[6]
		odds2 = odds2
		player = [name, sets, game1, game2, game3, game4, game5, odds2]

	return player, odds2

def Format_into_match(player1, player2, date, current_tournament, id_,file_name):
	player1_games = '-'.join(player1[2:6])
	player2_games = '-'.join(player2[2:6])
	match = [''.join([date,player1[8]]), player1[1], player2[1], player1[0], player2[0], player1_games, player2_games, player1[7], player2[7], current_tournament, id_]
	with open(file_name, 'ab') as f:
		csv.writer(f, delimiter=';', encoding='utf-8').writerow(match)
	f.close()

def Magic(data, date, DB, file_name):
	i = 0
	x0 = 0
	x1 = 0
	id_=u'1'
	current_tournament = ''
	player1 = []
	player2 = []
	for stuff in data:
		kama = stuff.text.replace(u'\xa0\xa0', '#').split('\n')
		if kama[1][0] == '#':
			#current_tournament = kama[1][1:]
			try:
				current_tournament = stuff.select('td > a')[0]['href']
			except IndexError:
				current_tournament = kama[1][1:]
		else:
			if i == 0:

				try:
					id_ = stuff.select('td > a')[1]['href'].split('id=')[1]
				except IndexError:
					id_ = stuff.select('td > a')[0]['href'].split('id=')[1]

				player1, odds2 = Sort_player_data(kama[1:], 1, 0)
				i = 1
			else:
				player2, a = Sort_player_data(kama[1:], 2, odds2)
				i = 0

		if (player1 != [] and player2 != []):
			#print type(id_), type(DB[0])
			#print id_ != DB[0];quit()
			if (id_ not in DB):
				Format_into_match(player1, player2, date, current_tournament, id_, file_name)
				player1 = [];player2 = [];id_=u'1';x1+=1
			x0+=1
	print '\t {} games, {} new.'.format(x0, x1)

for k in range(0, 15000, 1):
	start_time = datetime.datetime.now() - datetime.timedelta(days=k)

	start_time_url = start_time.strftime('%Y-%m-%d').split('-')
	#print start_time, start_time - datetime.timedelta(days=1);quit()
	file_name = 'raw_tennis_data.csv'
	DB = Old_data(file_name)

	'''
	Matka alkaa tästä. Aloitus url riippuu scrapperin käyttöpäivästä.
	'''
	url = 'http://www.tennisexplorer.com/results/?type=all&year=' + start_time_url[0] + '&month=' + start_time_url[1] + '&day=' + start_time_url[2]
	#url = 'http://www.tennisexplorer.com/results/?type=all&year=2018&month=07&day=11'
	print url
	date = start_time.strftime('%Y%m%d')
	'''
	Haetaan keittoa. Tätä varten tuli väsättyä ihan oma funktio
	'''
	soup = Soup(url)
	print date
	soup = soup.select('#center > ul > div.box.tbl.lGray > div > div')[0]
	#print soup.text;quit()
	if len(soup.select('table > tbody > tr > td')) > 1:

		'''
		This is where the magic happens.
		'''
		shit_data = soup.select('table > tbody > tr')# > td.t-name')
		Magic(shit_data, date, DB, file_name)
		'''
		a=True
		while a==True:
			try:
				Magic(shit_data, date, DB, file_name)
				a=False
			except IndexError:
				pass
		'''
		'''
		Kohti ääretöntä ja sen yli!
		'''
	else:
		print 'No games today.'

