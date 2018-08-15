# -#- coding: utf-8
import csv
import datetime
import urllib2
from bs4 import BeautifulSoup

def Soup(url):
	req = urllib2.Request(url, headers = {'User-Agent' : 'Kikkeliskokkelis'})
	con = urllib2.urlopen(req)
	html = con.read()
	soup = BeautifulSoup(html, 'lxml')

	return soup



def Tournament_search(file_name):
	Old = []
	file_name2 = 'tennis_tournaments.csv'
	with open(file_name2, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			Old.append(row[0])
	f.close()
	
	tournaments = []
	with open(file_name, 'rb') as f:
		reader=csv.reader(f, delimiter=';')
		for row in reader:
			if (row[-2] not in Old and row[-2] not in tournaments):
				tournaments.append(row[-2])
	f.close()

	print '{} tournaments in database.'.format(len(tournaments))
	
	#tournaments = ['/cincinnati-wta/2018/wta-women/']

	for item1 in tournaments:
		link = 'http://www.tennisexplorer.com' + item1
		try:
			soup = Soup(link)
			
			data = soup.select('#center > div.box.boxBasic.lGray')
			name = soup.select('#center > h1')[0].text

			for item in data[:3]:
				court = item.text.split(',')[-2].replace(' ','')
				print 'Court: {} - {}'.format(court, name)
				break	

			with open(file_name2, 'ab') as f:
				csv.writer(f).writerow([item1, court, name])
			f.close()
		except Exception:
			pass

file_name = 'raw_tennis_data.csv'
Tournament_search(file_name)