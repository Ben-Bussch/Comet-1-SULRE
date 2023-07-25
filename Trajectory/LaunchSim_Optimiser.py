# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 12:11:53 2023

@author: Bobke
"""
import numpy as np
import matplotlib.pyplot as plt

def gravity(m, h):
    """Computes force of gravity at given height and mass for solver"""
    G = 6.674*10**(-11)
    M = 5.972*10**(24)
    R0 = 6371140
    Fg = -G*m*M/((R0+h)**2)
    return(Fg)

def drag(rho, v, s, Cd):
    """Computes drag at given height and speed for solver"""
    Fd = -.5*rho*v**2*s*Cd
    return Fd

def density(h):
    """Computes air density at given height for solver"""
    p0 = 101325     #Pa
    T0 = 288.15     #K
    g0 = 9.80665    #m/s/s
    L = 0.0065      #temperature lapse rate K/m
    R = 8.31446     #Universal Gas Constant
    M = 0.0289652   #kg/mol (molar mass of dry air)
    rho = ((p0*M)/(R*T0))*(1-L*h/T0)**(((g0*M)/(R*L))-1)
    return rho
    
    

def terminate(h1, h0, dt):
    """Terminating command for solver, currently set to apogee of trajectory"""
    run = True
    hdot = (h1 - h0)/dt
    if hdot <= 0:
        run = False
    return run

def solver(tb, mdot, ms, Ft, s, Cd, dt):
    """Main launch solver"""
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
    rail = True
    while run:
        """Numerical solver for trajectory using trapezium rule, 
        starting with sum of forces and building up"""
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
        
        if h[count] > 11.9 and rail:
            """Saves rail exit velocity"""    
            vrail = v[count]
            rail = False
            #print("v: ", v[count], "h: ", h[count])         
        
        
        #print("Time: ",t," Force: ",Fsum," Acc: ", a1," v: ", v1, " h: ", h1, " Mass: ", m1 )
        run = terminate(h[count+1], h[count], dt)
        
        count = count + 1
    #print("Time: ",t," Force: ",Fsum," Acc: ", a1," v: ", v1, " h: ", h1, " Mass: ", m1 )    
    return m,h,v,a,F,rho,time,vrail

def burn_time_change(mdot, ms, thrust, s, Cd, dt, tmin, tmax, dt2):
    """Computes the max altitude for burn times between tmim and tmax"""
    h = []
    t = []
    burn_time = tmin
    while burn_time < tmax:
        hmax = solver(burn_time, mdot, ms, thrust, s, Cd, dt)[1][-1]
        h.append(hmax)
        t.append(burn_time)
        burn_time += dt2
    
    return h,t

def structural_mass_change(bt_min, mdot, mmin, mmax, thrust, s, Cd, h_a, dt, dt2):
    """Computes the necessary burn time to reach a specific altitude 
    for variying structural masses"""
    
    ms_list = []
    bt = []
    vr = []
    ms = mmin
    
    while ms <= mmax:
        
        hmax = 0
        burn_time = bt_min
        
        while hmax < h_a:
            burn_time += dt2
            m,h,v,a,F,rho,t,vrail = solver(burn_time, mdot, ms, thrust, s, Cd, dt)
            hmax = h[-1]
    
        bt.append(burn_time)
        vr.append(vrail)
        ms_list.append(ms)
        print("Structural Mass: ",ms, " Burn Time: ",bt, " Rail Velocity: ",vrail)
        
        ms += dt2
        
                
    return bt, ms_list, vr
        
        
    
          
        
"""Rocket Parameters"""
thrust = 1500   #N
mdot = 0.785    #kg/s
ms = 15         #kg
s = np.pi*(.075**2)
Cd = 0.75
dt = 0.005 #time step, s

ms_min = 10
ms_max = 30
burn_time_min = 5
h_apogee = 4500
dt2 = 0.05

bt, mStruc, vrail = structural_mass_change(burn_time_min, mdot, ms_min,ms_max, thrust, s, Cd, h_apogee, dt, dt2)

plt.figure(1)
plt.clf()

plt.plot(mStruc, bt)
plt.grid(1)
plt.title("Burn Time to Reach "+str(h_apogee)+" m Apogee for Different Structural Masses")
plt.xlabel("Structural Mass [kg]")
plt.ylabel("Burn Time [s]")
plt.savefig('Burn_time_vs_Structural_mass_h'+str(h_apogee)+'.png', dpi=300)

plt.figure(2)
plt.clf()

plt.plot(mStruc, vrail)
plt.grid(1)
plt.title("Rail exit Velocity for different Structural masses for a "+str(h_apogee)+" m Apogee")
plt.xlabel("Structural Mass [kg]")
plt.ylabel("Launch Rail Velocity [m/s]")
plt.savefig('launchrail_velocity_vs_Structural_mass_h'+str(h_apogee)+'.png', dpi=300)


"""
burn_time_min = 10  #s 
burn_time_max = 25 #s

dt2 = 0.2

h,bt = burn_time_change(mdot, ms, thrust, s, Cd, dt,burn_time_min, burn_time_max, dt2)

plt.figure(1)
plt.clf()

plt.plot(bt, h)

plt.grid(1)
plt.xlabel("Burn Time [s]")
plt.ylabel("Altitude [m]")
plt.savefig('Altitude_vs_burn_time.png', dpi=300)
"""


    




    
    
    