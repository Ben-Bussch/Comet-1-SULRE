# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 12:11:53 2023

@author: Bobke
"""
import numpy as np
import matplotlib.pyplot as plt

def gravity(m, h):
    G = 6.674*10**(-11)
    M = 5.972*10**(24)
    R0 = 6371140
    Fg = -G*m*M/((R0+h)**2)
    return(Fg)

def drag(rho, v, s, Cd):
    Fd = -.5*rho*v**2*s*Cd
    return Fd

def density(h):
    p0 = 101325     #Pa
    T0 = 288.15     #K
    g0 = 9.80665    #m/s/s
    L = 0.0065      #temperature lapse rate K/m
    R = 8.31446     #Universal Gas Constant
    M = 0.0289652   #kg/mol (molar mass of dry air)
    rho = ((p0*M)/(R*T0))*(1-L*h/T0)**(((g0*M)/(R*L))-1)
    return rho
    
    

def terminate(h1, h0, dt):
    run = True
    hdot = (h1 - h0)/dt
    if hdot <= 0:
        run = False
    return run

def solver(tb, mdot, ms, Ft, s, Cd, dt):
    """Launch Parameters"""
    h0 = 0      #m
    v0 = 0      #m/s
    t  = 0      #s
    
    mf = mdot*tb #initial fuel mass
    m0 = mf+ms
    F0 = gravity(m0, h0) + drag(1.225, v0, s, Cd)
    a0 = F0 / m0
    
    
    #Arrays
    m = [m0]
    h = [h0]
    v = [v0]
    a = [a0]
    F = [F0]
    rho = [density(h[0])]
    time = [t]
    
    
    
    run = True
    count = 0
    while run:
        
        Fsum = gravity(m[count], h[count]) + drag(rho[count], v[count], s, Cd)
        if m[count] > ms:
            Fsum += Ft
            m1 = m[count] - mdot*dt
            
        else:
            m1 = m[count]
            
        m.append(m1)
        F.append(Fsum)
        
        a1 = Fsum/m[count]
        a.append(a1)
        
        v1 = v[count] + (a[count+1]+a[count])*dt*0.5
        v.append(v1)
        
        h1 = h[count] + (v[count+1]+v[count])*dt*0.5
        h.append(h1)
        
        rho1 = density(h[count])
        rho.append(rho1)
        
        t = t + dt
        time.append(t)
        #print("Time: ",t," Force: ",Fsum, " Mass: ", m1)
        """
        if h[count] > 11.8 and h[count] < 12.2:
            print("v: ", v[count], "h: ", h[count])
        """
        
        #print("Time: ",t," Force: ",Fsum," Acc: ", a1," v: ", v1, " h: ", h1, " Mass: ", m1 )
        run = terminate(h[count+1], h[count], dt)
        
        count = count + 1
    #print("Time: ",t," Force: ",Fsum," Acc: ", a1," v: ", v1, " h: ", h1, " Mass: ", m1 )    
    return h[count]

def burn_time_change(mdot, ms, thrust, s, Cd, dt, tmin, tmax, dt2):
    h = []
    t = []
    burn_time = tmin
    while burn_time < tmax:
        h.append(solver(burn_time, mdot, ms, thrust, s, Cd, dt))
        t.append(burn_time)
        burn_time += dt2
    
    return h,t
        
    
        
"""Rocket Parameters"""
thrust = 1500   #N
mdot = 0.785    #kg/s
ms = 15         #kg
s = np.pi*(.075**2)
Cd = 0.75

burn_time_min = 10  #s 
burn_time_max = 25 #s
dt = 0.005 #time step, s
dt2 = 0.2

h,bt = burn_time_change(mdot, ms, thrust, s, Cd, dt,burn_time_min, burn_time_max, dt2)



plt.figure(1)
plt.clf()

plt.plot(bt, h)

plt.grid(1)
plt.xlabel("Burn Time [s]")
plt.ylabel("Altitude [m]")
plt.savefig('Altitude_vs_burn_time.png', dpi=300)



    




    
    
    