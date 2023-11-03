# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 11:59:29 2023

@author: robbi
"""

import numpy as np
import matplotlib.pyplot as plot
import scipy.optimize as opt

def func_ex(t,x,Nx,Qx,Ex):
    return (t**2)*(Nx-2*Qx+Ex) + t*(2*Qx-2*Nx) + Nx - x


def solve_param_ex(x,Nx,Qx,Ex,Ny,Qy,Ey):
    t = opt.fsolve(func_ex,x,args=(x,Nx,Qx,Ex))
    
    
    y = ((1-t)**2)*Ny + 2*(1-t)*t*Qy +(t**2)*Ey
    
    return y
    
def throat_profile(x,rt,theta_t,theta_i,Nx,Qx,Ex,Ny,Qy,Ey):
    
    r1 = 0.382*rt
    r2 = 1.5*rt
    
    theta_i = np.radians(theta_i)
    theta_t = np.radians(theta_t)
    
    
    if (x > Nx and x < Ex):
       r = sum(solve_param_ex(x,Nx,Qx,Ex,Ny,Qy,Ey))
   
    if (x > Nx-r1*np.sin(theta_t) and x <= Nx):
        r = r1+rt-np.sqrt((r1**2)-(x+r1*np.sin(theta_t)-Nx)**2)
    
    if (x > Nx-r1*np.sin(theta_t)-r2*np.sin(theta_i) and x <= Nx-r1*np.sin(theta_t)):
        r = r2+rt-np.sqrt((r2**2)-(x+r1*np.sin(theta_t)-Nx)**2)
    
    return r

def throat_profile_offset(th,x,rt,theta_t,theta_i,Nx,Qx,Ex,Ny,Qy,Ey,dx = 0.1):
    
    xs = [x-dx, x, x+dx]
    rs = [throat_profile(x,rt,theta_t,theta_i,Nx,Qx,Ex,Ny,Qy,Ey) for x in xs]
    
    drdx = np.gradient(rs,dx)[1]
    inc = np.sqrt((th**2)/(1+drdx**2))
    
    new_r = rs[1]+inc
    new_x = x - drdx*inc
    
    return [new_r, new_x]

def plotty(th = 3,z_range = [-20,20], res = 2000, dx = 0.1):
    
    xvals = np.linspace(z_range[0], z_range[1], res)
    
    yvals = [throat_profile(i,11.2,22.4089,45,0,18.864,37.5,11.52307555,19.3,23.76) for i in xvals]
    xvals_mod = [throat_profile_offset(th,i,11.2,22.4089,45,0,18.864,37.5,11.52307555,19.3,23.76,dx)[1] for i in xvals]
    yvals_mod = [throat_profile_offset(th,i,11.2,22.4089,45,0,18.864,37.5,11.52307555,19.3,23.76,dx)[0] for i in xvals]
    #yvals = [i**2/40 + 20 for i in xvals]
    
    print(yvals)
    
    plot.show()
    plot.figure(figsize=(12,6))
    plot.title("Throat contour")
    plot.xlabel("Z-direction")
    plot.ylabel("Radius")
    plot.plot(xvals,yvals)
    plot.plot(xvals_mod,yvals_mod)




def spiral(n= 3,th = 3,z = 1,rt = 11, t_off = 1.630985915):
    
    [r,z_new] =  throat_profile_offset(th,z,11.2,22.4089,45,0+t_off,18.864+t_off,37.5+t_off,11.52,19.3,23.76)
    
    z = z_new
    
    #print('r =',r)
    
    theta = np.arccos(rt/r)
    #print('theta =',theta)
    
    p = np.tan(theta)/r
    #print('p =',p)
    
        
    x = [r*np.cos(p*z+(i*2*np.pi)/n) for i in range(n)]
    y = [np.sign(z)*r*np.sin(p*z+(i*2*np.pi)/n) for i in range(n)]
        
    #print('x =',x)
    
    return [x,y,z]


def plot_3d(n,d,z_range = [-20,20], rt = 20, res = 2000):
    
    z = np.linspace(z_range[0],z_range[1],res)
    xi = [spiral(n,d,i,rt)[0] for i in z]
    print('xi =',xi)
    yi = [spiral(n,d,i,rt)[1] for i in z]
    zs = [spiral(n,d,i,rt)[2] for i in z]
    xs = []
    ys = []
    
    for i in range(n):
        tempx = [xi[a][i] for a in range(len(xi))]
        print(tempx)
        tempy = [yi[a][i] for a in range(len(yi))]
        xs.append(tempx)
        ys.append(tempy)
        
    
    print('xs =', xs)
    
    ax = plot.axes(projection ='3d')
    ax.set_title('Evenly spaced cooling channels')
    plot.show()
    for i in range(len(xs)):
        
        ax.plot3D(xs[i], ys[i], zs, 'green')
    
    
       
    
    