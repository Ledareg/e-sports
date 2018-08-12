

from Function import Function
from Player import Player
from Team import Team
import roster
import numpy as np


# Filename which has every game sorted by date.
file = 'Database_odds.csv'

# Open file that contains every single game.
# Returns list of those games.
Data = Function().Open_file(file)

# Calculate player ELO's and return all players as a dictionary

k = 0.98
min_games = 12
blue = 76
m = 1
Players, Teams, bank, hit = Function().Calculate_elo(Data, k, min_games, blue, m)

print 'Bookkereiden logaritmisumma oli: ', round(np.mean(bank.log_sum_odds),4)
print 'Laskurin logaritmisumma oli: ', round(np.mean(bank.log_sum),4)

bank.Tournaments()
bank.plot()

'''
rr = []
for muuttuja in range(0, 50, 1):
	#muuttuja = muuttuja/float(100)
	k = 0.98 #0.83
	min_games = 12 #36
	blue = 76 # <- SELVITA TASAPANOKSELLA, 76
	Players, Teams, bank, hit = Function().Calculate_elo(Data, k, min_games, blue, muuttuja)

	#print 'Muuttuja: {:3.2f}'.format(muuttuja)
	#print 'Games: {:.0f} - ROI: {:5.2f}% - Profit: {:5.1f}u.'.format(bank.games, bank.ROI(), bank.profit())
	#print '---------------------'
	rr.append([muuttuja, bank.games, bank.ROI(), bank.profit(), bank.var(), hit.hitrate(), np.mean(bank.log_sum)])

#bank.plot()

for item in reversed(sorted(rr, key=lambda arvo: arvo[2])):
	print 'Muuttuja: {:3.2f} - Games: {:.0f} - Profit: {:5.1f}u - ROI: {:5.2f}%  - STD: {:5.2f} - Hitrate: {:.2f}% - Logsum: {:.3f}'.format(item[0], item[1], item[3], item[2], item[4], item[5], item[6])
print np.mean(bank.log_sum_odds)

'''
roster.Team().Excel(Players)
roster.Team().Last5(Players, file)








