import csv
from bs4 import BeautifulSoup
import urllib2
import datetime

def Soup(url):
	req = urllib2.Request(url, headers = {'User-Agent' : 'Kikkeliskokkelis'})
	con = urllib2.urlopen(req)
	html = con.read()
	soup = BeautifulSoup(html, 'lxml')

	return soup

def Old_data(file_):
	OD = []
	with open(file_, 'rb') as f:
		reader = csv.reader(f, delimiter=';')
		for item in reader:
			OD.append(item[-1])
	f.close()

	return OD

def Print_game(data):
	# [DATE, BO, HOME, AWAY, SCORES, HOME_PLAYERS, AWAY_PLAYERS, MAPS, TOURNAMENT]
	print '{:s}, BO{:s}, {:s} vs. {:s}, {:s}, {:s}'.format(data[0], data[1], data[2], data[3], data[4], data[8])

def Write_game(data, OLD_DATABASE, file_):
	with open(file_, 'ab') as f:
		writer = csv.writer(f, delimiter=';')
		writer.writerow(data)
	f.close()
	OLD_DATABASE.append(data[-1])

	return OLD_DATABASE

def Bo(data):
	data = data.split('Best of ')
	return data[1][:1]

def Date(data):
	return datetime.datetime.fromtimestamp(int(data[0]['data-unix'][:10])).strftime('%Y%m%d')

def Team_names(data):
	return data[0].text.encode('utf-8'), data[1].text.encode('utf-8')

def Result(data):
	k = 0
	MAPS = []
	SCORES = []
	for item in data:
		if k == 0:
			MAPS.append(item.text.replace('\n', ''))
			k=1
		else:
			SCORES.append(item.text.replace('\n', '').split(' ')[0])
			k=0
	MAPS = MAPS[:len(SCORES)]

	return ','.join(SCORES), ','.join(MAPS)

def Players(data):
	home = []
	away = []
	id_s = []
	for guy in data:
		name = guy['href'].split('/')[2] + '-' + guy['href'].split('/')[3].encode('utf-8')
		if name.split('-')[0] not in id_s:
			id_s.append(name.split('-')[0])
			if len(home) < 5:
				home.append(name)
			else:
				away.append(name)

	return ','.join(home), ','.join(away)

def Tournament(data):
	return data[0].text.encode('utf-8')

# Get match pages
def Get_match_urls(url):
	soup = Soup(url)
	data = soup.select('body > div > div > div > div > div > div > div > div > div > a')
	links = []
	for item in data:
		url = 'https://www.hltv.org' + item['href']
		links.append(url)

	return links

def Open_game(url, OLD_DATABASE, file_):
	soup = Soup(url)
	GAME_ID =  url.split('/')[4]
	#print GAME_ID, OLD_DATABASE
	if GAME_ID not in OLD_DATABASE:
		try:
			BO = Bo(soup.select('body > div.bgPadding > div > div.colCon > div.contentCol > div.match-page > div.flexbox.fix-half-width-margin.maps > div > div > div')[0].text)
			DATE = Date(soup.select('body > div.bgPadding > div > div.colCon > div.contentCol > div.match-page > div.standard-box.teamsBox > div.timeAndEvent > div.date'))
			HOME, AWAY = Team_names(soup.select('body > div.bgPadding > div > div.colCon > div.contentCol > div.match-page > div.standard-box.teamsBox > div > div > a > div'))
			SCORES, MAPS = Result(soup.select('body > div.bgPadding > div > div.colCon > div.contentCol > div.match-page > div.flexbox.fix-half-width-margin.maps > div > div.flexbox-column > div > div'))
			try:
				HOME_PLAYERS, AWAY_PLAYERS = Players(soup.select('body > div.bgPadding > div > div.colCon > div.contentCol > div.match-page > div.lineups > div > div > div.players > table > tr > td > a'))
				TOURNAMENT = Tournament(soup.select('body > div.bgPadding > div > div.colCon > div.contentCol > div.match-page > div.standard-box.teamsBox > div.timeAndEvent > div.event.text-ellipsis > a'))
				match_data = [DATE, BO, HOME, AWAY, SCORES, HOME_PLAYERS, AWAY_PLAYERS, MAPS, TOURNAMENT, str(GAME_ID)]
				Print_game(match_data)
				OLD_DATABASE = Write_game(match_data, OLD_DATABASE, file_)
			except KeyError:
				pass
		except Exception:
			print url
			pass
		
	return OLD_DATABASE


file_lan = 'CS_data/cs_raw_lan.csv'
file_online = 'CS_data/cs_raw_online.csv'
START_URL_LAN = 'https://www.hltv.org/results?offset=0&matchType=Lan'
START_URL_ONLINE = 'https://www.hltv.org/results?offset=0&matchType=Online'

SWITCH = raw_input('ONLINE/LAN?\n')

print '\nCS Scraper. Currently downloading {} games from HLTV.\n'.format(SWITCH)

if SWITCH == 'LAN':
	START_URL = START_URL_LAN
	file_ = file_lan
	N = 10000
if SWITCH == 'ONLINE':
	START_URL = START_URL_ONLINE
	file_ = file_online
	N = 30000

OLD_DATABASE = Old_data(file_)
start = datetime.datetime.now()


for i in range(0,N,100):
	# Search urls
	links = Get_match_urls(START_URL.replace('0', str(i)))

	# Open pages
	for link in links:
		OLD_DATABASE = Open_game(link, OLD_DATABASE, file_)

	print '\n\tDownloaded {}/{}. Runtime: {}\n'.format(i+100, N, datetime.datetime.now()-start)