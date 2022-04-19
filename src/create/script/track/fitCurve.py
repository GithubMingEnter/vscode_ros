#!/usr/bin/python
# coding=gbk
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
print os.getcwd()
wps = np.loadtxt("bufPoint.txt")
x=wps[:,0]
y=wps[:,1]

t=np.linspace(0,1,num=len(x))

f1=interp1d(t,x,kind='cubic')
f2=interp1d(t,y,kind='cubic')

newt=np.linspace(0,1,100)
nx=f1(newt)
ny=f2(newt)

#matplotlib inline

plt.scatter(x,y)
plt.plot(nx,ny)
plt.show()



# import matplotlib
# import matplotlib.pyplot as plt
# import numpy as np

# # matplotlib.get_backend()
# # print matplotlib.matplotlib_fname()
# x=np.linspace(-1,1,50)
# y=2*x+1
# plt.plot(x,y)

# plt.show()










