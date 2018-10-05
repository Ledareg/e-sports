#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np



# Input data
l = 16
x = np.linspace(0,16,100)

y = x*(1-x/float(l))


# Plotting arch geometry
'''
plt.plot(x, y, 'o-g')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.ylim(min(y)-1, max(y)+1)
plt.title('Arch geometry')
plt.show()
'''
# Calculating arch length
x1 = 0
y1 = 0
sum_L = 0

for i in range(0,len(x),1):
	L = np.sqrt((x[i]-x1)**2 + (y[i]-y1)**2)
	sum_L += L	
	x1 = x[i]
	y1 = y[i]


print 'Arch length is: {:.2f}m'.format(sum_L)

#

