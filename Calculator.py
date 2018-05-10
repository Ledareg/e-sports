
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
min_games = 27
blue = 68
Players, Teams, bank, hit = Function().Calculate_elo(Data, k, min_games, blue)

#bank.plot()
#print np.mean(bank.log_sum_odds)
#print np.mean(bank.log_sum)

bank.Tournaments()

'''
# Test variables and tune parameters
rr = []
for muuttuja in range(0, 40, 1):
	#muuttuja = muuttuja/float(100)
	k = 0.98 #0.98
	min_games = 27 #27
	blue = 68 #68
	Players, Teams, bank, hit = Function().Calculate_elo(Data, k, min_games, blue)

	#print 'Muuttuja: {:3.2f}'.format(muuttuja)
	#print 'Games: {:.0f} - ROI: {:5.2f}% - Profit: {:5.1f}u.'.format(bank.games, bank.ROI(), bank.profit())
	#print '---------------------'
	rr.append([muuttuja, bank.games, bank.ROI(), bank.profit(), bank.var(), hit.hitrate(), np.mean(bank.log_sum)])

#bank.plot();quit()

for item in reversed(sorted(rr, key=lambda arvo: arvo[2])):
	print 'Muuttuja: {:3.2f} - Games: {:.0f} - Profit: {:5.1f}u - ROI: {:5.2f}%  - Var: {:5.2f}% - Hitrate: {:.2f}% - Logsum: {:.3f}'.format(item[0], item[1], item[3], item[2], item[4], item[5], item[6])
#print np.mean(bank.log_sum_odds)
#
'''
roster.Team().Excel(Players)
roster.Team().Last5(Players, file)








