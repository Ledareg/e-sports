# -#- coding: utf-8
import unicodecsv as csv
import datetime
import matplotlib.pyplot as plt


K1 = 40 # Vakio
K2 = K1-8 # Vakio-8 	-> 32
K3 = K2/2 # (Vakio-8)/2	-> 16

class Player():
	def __init__(self):

		self.games = 0
		self.elo = [1450]

		self.normal_elo_x = 0.5 # Variable
		self.terrain_elo1_x = 0.5 # Variable
		self.terrain_elo2_x = 0.5 # Variable
		self.terrain_elo3_x = 0.5 # Variable
		self.terrain_elo4_x = 0.5 # Variable

		#self.x = 25 # Variable
		#self.c = 0.8 # Variable
		self.min_games = 15
		self.k = 1.1

		self.elo_indoors = [1450]
		self.elo_clay = [1450]
		self.elo_hard = [1450]
		self.elo_grass = [1450]

	def Elo(self, terrain):
		if terrain == 'NaN' or terrain == 'Varioussurfaces':
			return self.elo[-1]
		elif terrain == 'indoors':
			return self.normal_elo_x*self.elo[-1] + self.terrain_elo1_x*self.elo_indoors[-1]
		elif terrain == 'clay':
			return self.normal_elo_x*self.elo[-1] + self.terrain_elo2_x*self.elo_clay[-1]
		elif terrain == 'hard':
			return self.normal_elo_x*self.elo[-1] + self.terrain_elo3_x*self.elo_hard[-1]
		elif terrain == 'grass':
			return self.normal_elo_x*self.elo[-1] + self.terrain_elo4_x*self.elo_grass[-1]
		else:
			print terrain;quit()

	def Win(self, terrain, elo):
		self.games += 1
		OA = 1/(1+10**((elo-self.elo[-1])/float(400)))
		#K = 250/(float((self.games+self.x)**self.c))

		if self.games <= self.min_games:
			K = K1
		elif self.elo[-1] <= avg*self.k:
			K = K2
		else:
			K = K3

		# Yleinen elo ja kenttäkohtanen elo
		self.elo.append(self.elo[-1] + K*(1-OA))
		if terrain == 'indoors':
			self.elo_indoors.append(self.elo_indoors[-1] + K*(1-OA))
		elif terrain == 'clay':
			self.elo_clay.append(self.elo_clay[-1] + K*(1-OA))
		elif terrain == 'hard':
			self.elo_hard.append(self.elo_hard[-1] + K*(1-OA))
		elif terrain == 'grass':
			self.elo_hard.append(self.elo_hard[-1] + K*(1-OA))


	def Lose(self, terrain, elo):
		self.games += 1
		OA = 1/(1+10**((elo-self.elo[-1])/float(400)))
		#K = 250/(float((self.games+self.x)**self.c))
		K = 24
		# Yleinen elo ja kenttäkohtanen elo
		self.elo.append(self.elo[-1] + K*(0-OA))
		if terrain == 'indoors':
			self.elo_indoors.append(self.elo_indoors[-1] + K*(0-OA))
		elif terrain == 'clay':
			self.elo_clay.append(self.elo_clay[-1] + K*(0-OA))
		elif terrain == 'hard':
			self.elo_hard.append(self.elo_hard[-1] + K*(0-OA))
		elif terrain == 'grass':
			self.elo_hard.append(self.elo_hard[-1] + K*(0-OA))

class Functions():
	def Set_winners(self, data1, data2):
		sets1 = []
		sets2 = []
		for item in data1.split('-'):
			if item != '':
				item = int(item)
				if item <= 50:
					sets1.append(item)
				else:
					sets1.append(6)
		for item in data2.split('-'):
			if item != '':
				item = int(item)
				if item <= 50:
					sets2.append(item)
				else:
					sets2.append(6)

		sets = []
		for i in range(len(sets1)):
			if sets1[i] > sets2[i]:
				sets.append(1)
			elif sets1[i] < sets2[i]:
				sets.append(2)
			else:
				sets.append(0)

		return sets

	def Top_Players(self, Players):
		Stuff = []
		for player in Players:
			Stuff.append([player,Players[player].elo[-1]])

		i = 0
		for player in reversed(sorted(Stuff, key=lambda arvo: arvo[1])):
			if i == 9:
				break
			print player
			i+=1


filename = 'tennis_data.csv'
Players = {}
hit = [0,0]
date1 = 201500000000
date2 = 201600000000
kassa = [0]
in_ = 0
out_ = 0

with open(filename, 'rb') as f:
	reader=csv.reader(f,delimiter=';')
	Games = list(reader)
f.close()


for match in Games:
	player1 = match[3]
	player2 = match[4]
	date = int(match[0])
	try:
		odds1 = float(match[7])
		odds2 = float(match[8])
	except ValueError:
		odds1='';odds2=''

	if player1 not in Players:
		Players[player1] = Player()
	if player2 not in Players:
		Players[player2] = Player()
	
	if len(match[-1].split(',')) > 1:
		terrain = match[-1].split(',')[0]
	else:
		terrain = 'NaN'

	try:
		sets = Functions().Set_winners(match[5], match[6])
	except IndexError:
		pass

	p1_elo = Players[player1].Elo(terrain)
	p2_elo = Players[player2].Elo(terrain)

	if (p1_elo > p2_elo):
		hit[0] += 1
	elif (p2_elo > p1_elo):
		hit[1] += 1

	if (date > date1 and date < date2):
		if (odds1 != '' and odds2 != ''):
			OA1 = 1/(1+10**((p2_elo-p1_elo)/float(400)))
			OA2 = 1-OA1

			if odds1 > 1/float(OA1):
				panos = 1
				kassa.append(kassa[-1]+panos*odds1-panos)
				in_+=panos
				out_+=panos*odds1-panos

			elif odds2 > 1/float(OA2):
				panos = 1
				kassa.append(kassa[-1]-panos)
				in_+=panos
			

	for game in sets:
		p1_elo = Players[player1].Elo(terrain)
		p2_elo = Players[player2].Elo(terrain)
		if game == 1:
			Players[player1].Win(terrain, p2_elo)
			Players[player2].Lose(terrain, p1_elo)
		if game == 2:
			Players[player1].Lose(terrain, p2_elo)
			Players[player2].Win(terrain, p1_elo)


#print Players['Nieminen J.'].elo[-1], Players['Nieminen J.'].games
#Functions().Top_Players(Players)

print 'Osumaprosentti: {:.2f}% ({}/{})'.format((hit[0]/float(hit[0]+hit[1]))*100,hit[0],hit[1])
print 'Kassa lopussa: {}, pelattu: {}, ulos: {} ja pal-%: {:.2f}%'.format(kassa[-1], in_, out_, out_/float(in_)*100)

#plt.plot(kassa)
#plt.show()

















	
