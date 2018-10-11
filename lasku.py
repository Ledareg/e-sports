#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np



# Input data
l = 16
x = np.linspace(0,16,50)
q = 1



# Plotting arch geometry

y = x*(1-x/float(l))

plt.plot(x, y, 'o-r')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.ylim(min(y)-1, max(y)+1)
plt.title('Arch geometry')
plt.grid()
plt.show()

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

# Moment graphs
x1 = np.linspace(0,8,50)
x2 = np.linspace(8,16,50)
M1_x = -((-q*x1**2)/float(2) + (3*q*l*x1)/float(8) - 0.25048*q*l*x1*(1-x1/float(l)))
M2_x = -(((q*l)*(l-x2))/float(8) - 0.25048*q*l*x2*(1-x2/float(l)))

M01_x = ((3*q*l*x1)/float(8) - (q*x1**2)/float(2))
M02_x = (((q*l**2)/float(8))*(1-x2/float(l)))

plt.ylim(min([min(M01_x), min(M02_x), min(M1_x), min(M2_x)])-1, max([max(M01_x), max(M02_x), max(M1_x), max(M2_x)])+1)
plt.xlabel('x (m)')
plt.ylabel('M (Nm)')
plt.title('M(x)')
plt.plot(x1, M1_x, 'b+', label='M1(x)')
plt.plot(x2, M2_x, 'm+', label='M2(x)')
plt.plot(x1, M01_x, label='M01(x)')
plt.plot(x2, M02_x, label='M02(x)')
plt.fill_between(x2, 0, M2_x, where=M2_x >= 0, facecolor='blue', alpha=0.2)
plt.fill_between(x2, 0, M2_x, where=M2_x < 0, facecolor='red', alpha=0.2)
plt.fill_between(x1, 0, M1_x, where=M1_x >= 0, facecolor='blue', alpha=0.2)
plt.fill_between(x1, 0, M1_x, where=M1_x < 0, facecolor='red', alpha=0.2)
plt.legend()
plt.grid()

plt.show()


# N
tan1 = 1 - 2*x1/l
tan2 = 1 - 2*x2/l

sin1 = tan1/np.sqrt(1+tan1**2)
sin2 = tan2/np.sqrt(1+tan2**2)

cos1 = 1/np.sqrt(1+tan1**2)
cos2 = 1/np.sqrt(1+tan2**2)

H1 = -0.25048*q*l
H2 = -0.25048*q*l

V1 = (3*q*l)/8 - q*x1
V2 = -(q*l)/8


N1_x = (H1*cos1-V1*sin1)
N2_x = (H2*cos2-V2*sin2)


plt.plot(x1, N1_x, 'b+', label='N1(x)')
plt.plot(x2, N2_x, 'm+', label='N1(x)')
plt.title('N(x)')
plt.xlabel('x (m)')
plt.ylabel('N (kN)')
plt.legend()
plt.grid()
plt.fill_between(x2, 0, N2_x, where=N2_x >= 0, facecolor='blue', alpha=0.2)
plt.fill_between(x2, 0, N2_x, where=N2_x < 0, facecolor='red', alpha=0.2)
plt.fill_between(x1, 0, N1_x, where=N1_x >= 0, facecolor='blue', alpha=0.2)
plt.fill_between(x1, 0, N1_x, where=N1_x < 0, facecolor='red', alpha=0.2)
plt.ylim(min([min(N1_x), min(N2_x)])-1, max([max(N1_x), max(N2_x)])+1)
plt.show()

# Q

Q1_x = (H1*sin1 + V1*cos1)
Q2_x = (H2*sin2 + V2*cos2)

plt.plot(x1, Q1_x, 'b+', label='Q1(x)')
plt.plot(x2, Q2_x, 'm+', label='Q2(x)')
plt.title('Q(x)')
plt.xlabel('x (m)')
plt.ylabel('Q (kN)')
plt.legend()
plt.grid()
plt.fill_between(x1, 0, Q1_x, where=Q1_x >= 0, facecolor='blue', alpha=0.2)
plt.fill_between(x1, 0, Q1_x, where=Q1_x < 0, facecolor='red', alpha=0.2)
plt.fill_between(x2, 0, Q2_x, where=Q2_x >= 0, facecolor='blue', alpha=0.2)
plt.fill_between(x2, 0, Q2_x, where=Q2_x < 0, facecolor='red', alpha=0.2)
plt.ylim(min([min(Q1_x), min(Q2_x)])-1, max([max(Q1_x), max(Q2_x)])+1)

plt.show()













