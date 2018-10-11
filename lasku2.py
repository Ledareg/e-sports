
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np


a = 4
x1 = np.linspace(0,a,100)
x2 = np.linspace(a,2*a,100)
q = 10

M1_x = ((q*x1**(2))/2 - 17.56*x1)
M2_x = ((q*(2*a-x2)**(2))/2 - 17.56*(2*a-x2))
x_axis_01 = 0*x1
x_axis_02 = 0*x2

plt.plot(x1,M1_x, 'b+', label='M1(x)')
plt.plot(x2,M2_x, 'g+', label='M2(x)')
plt.plot(x1,x_axis_01, 'm')
plt.plot(x2,x_axis_02, 'm')
plt.xlabel('x (m)')
plt.ylabel('M (Nm)')
plt.title('M(x)')
plt.fill_between(x2, 0, M2_x, where=M2_x >= 0, facecolor='red', alpha=0.2)
plt.fill_between(x2, 0, M2_x, where=M2_x < 0, facecolor='blue', alpha=0.2)
plt.fill_between(x1, 0, M1_x, where=M1_x >= 0, facecolor='red', alpha=0.2)
plt.fill_between(x1, 0, M1_x, where=M1_x < 0, facecolor='blue', alpha=0.2)
plt.ylim(min([min(M1_x), min(M2_x)])-1, max([max(M1_x), max(M2_x)])+1)
plt.grid()
plt.legend()
plt.show()