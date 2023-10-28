# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 23:56:45 2023

@author: Bobke
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Domain_z_min = 0 #bottom of throat, mm
Domain_z_max = 20 #TTop of throat, mm

psi1 = 0
dpsi = 0.01 #Determines spiral resolution

z1 = 0
R1 = 0.03*(z1-10)**2 + 5 #inital diameter of spiral, mm
print(R1)

x1 = R1/dpsi #Compensate for Scale by dpsi
y1 = 0

x = [x1]
y = [y1]
z = [z1]
R = [R1]
psi = [psi1]
r = 1  #radius of piping, mm


"""Spiral Solver"""
zn = Domain_z_min
while z1 < Domain_z_max:
    throat_curve = 0.03*(z1-10)**2 + 5 #Expression for spiral
    R1 = throat_curve
    R.append(R1)
    theta = np.arccos((np.pi*R1)/(np.sqrt(r**2+(np.pi**2)*R1**2))) #some fancy math i did late at night, dont ask me about it
    
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
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
#fig.savefig('3D_Spiral_Path.png', dpi = 120)

fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(z,R)
ax.set_ylim(ymin=0)
ax.set_title("Throat Profile")
ax.set_xlabel("z")
ax.set_ylabel("Throat Radius")
#fig.savefig('Throat_Profile.png', dpi = 120)


np.savetxt('xyzSpiral.txt', [p for p in zip(x,y,z)], delimiter=',')




