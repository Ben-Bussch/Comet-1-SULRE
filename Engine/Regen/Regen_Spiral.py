# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 23:56:45 2023

@author: Bobke
"""
import numpy as np
import matplotlib.pyplot as plt

Domain_z_min = 0 #bottom of throat, mm
Domain_z_max = 30 #TTop of throat, mm

psi1 = np.pi/2
dpsi = 0.01

z1 = 0
R1 = 0.03*(z1-12)**2 +8 #inital diameter of spiral, mm

x1 = R1
y1 = 0

x = [x1]
y = [y1]
z = [z1]
R = [R1]
psi = [psi1]
r = 1.5  #radius of piping, mm

zn = Domain_z_min
while z1 < Domain_z_max:
    throat_curve = 0.03*(z1-12)**2 +8 #Expression for spiral
    R1 = throat_curve
    R.append(R1)
    theta = np.arccos((np.pi*R1)/(np.sqrt(r**2+(np.pi**2)*R1**2)))
    #theta = 0.01
    psi0 = psi1
    psi1 = psi0 + dpsi
    
    dxdpsi = -R1*np.sin(psi1)
    
    x0 = x1
    x1 = x0 + dxdpsi
    x.append(x1)
    
    dydpsi = R1*np.cos(psi1)
    y0 = y1 
    y1 = y0 + dydpsi
    y.append(y1)
    
    dzdpsi = np.sqrt((x1-x0)**2+(y1-y0)**2)*np.tan(theta)
    z0 = z1
    z1 = z0 + (dzdpsi*dpsi)
    z.append(z1)
   

x = [n*dpsi for n in x] #Scaling Back to dimention
y = [n*dpsi for n in y] #Scaling Back to dimention

    


fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(x, y, z)


fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(z,R)
ax.set_title("Throat Profile")



