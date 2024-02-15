# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 12:11:53 2023

@author: Bobke
"""
import numpy as np
import matplotlib.pyplot as plt

def gravity(m, h):
    G = 6.674*10**(-11)
    M = 5.9722*10**(24)
    R0 = 6375140
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
    
    hs = 125        #Start height above sea level, m
    rho = ((p0*M)/(R*T0))*(1-L*(h+hs)/T0)**(((g0*M)/(R*L))-1)
    return rho
    
    

def terminate(h2, h1, h0, dt):
    run = True
    """
    hdot = (h2 - h1)/dt
    if hdot <= 0:
        run = False
    """
    if h1 < h0:
        run = False 
    
    return run

def solver(tb, mdot, ms, Ft, s, Cd, theta0, dt):
    """Solving 2D launch, assuming rocket will always point prograde (passively stable)"""
    """Launch Parameters"""
    h0 = 160      #m
    v0 = 0      #m/s
    t  = 0      #s
    
    mf = mdot*tb #initial fuel mass
    m0 = mf+ms
    F0 = gravity(m0, h0) + drag(1.225, v0, s, Cd)
    a0 = F0 / m0
    print(gravity(m0, h0)/m0)
    
    #Arrays
    m = [m0]
    h = [h0]
    d = [0]
    theta = [theta0]
    vx, vy, v = [v0],[v0], [v0]
    ax, ay = [a0],[a0]
    Fx, Fy = [np.cos(theta0)*F0],[np.sin(theta0)*F0]
    rho = [density(h[0])]
    time = [t]
    
    
    
    run = True
    count = 0
    rail = True
    while run:
        
        "Solving Forces"
        Fxsum = np.cos(theta[count])*drag(rho[count], v[count], s, Cd)
        Fysum = gravity(m[count], h[count]) + np.sin(theta[count])*drag(rho[count], v[count], s, Cd)
        
        if m[count] > ms:
            #print("cos:", np.cos(theta[count]))
            #print("sin:", np.sin(theta[count]))
            Fxsum += np.cos(theta[count])*Ft
            Fysum += np.sin(theta[count])*Ft
            m1 = m[count] - mdot*dt
            
            
        else:
            m1 = m[count]
            
        #print("Fx:", Fxsum, " Fy:", Fysum)    
        m.append(m1)
        Fx.append(Fxsum)
        Fy.append(Fysum)
        
        "Solving Accelerations"
        axi = Fxsum/m[count]
        ax.append(axi)
        ayi = Fysum/m[count]
        ay.append(ayi)
        
        "Solving Velocities"
        vxi = vx[count] + (ax[count+1]+ax[count])*dt*0.5
        vx.append(vxi)
        vyi = vy[count] + (ay[count+1]+ay[count])*dt*0.5
        vy.append(vyi)
        
        vi = (vx[count+1]**2 + vy[count+1]**2)**0.5
        v.append(vi)
        
        "Solving Distances"
        hi = h[count] + (vy[count+1]+vy[count])*dt*0.5
        h.append(hi)
        
        di = d[count] + (vx[count+1]+vx[count])*dt*0.5
        d.append(di)
        
        
        #print("Vx:", vx[count+1], "Vy: ", vy[count+1])
        if h[count+1]-h0 < np.sin(theta0)*11.9:
            thetai = theta0
        else: 
            thetai = np.arctan(abs(vy[count+1]/vx[count+1]))
        
        theta.append(thetai)
        #print("Angle:", np.degrees(thetai))
        
        rho1 = density(h[count])
        rho.append(rho1)
        
        t = t + dt
        time.append(t)
        #print("Time: ",t," Force: ",Fsum, " Mass: ", m1)
        if h[count+1]-h0 > np.sin(theta0)*11.9 and rail:
            """Saves rail exit velocity"""    
            vrail = v[count]
            rail = False
            print("v: ", v[count], "h: ", h[count])
        
        #print("Time: ",t," Force: ",Fsum," Acc: ", a1," v: ", v1, " h: ", h1, " Mass: ", m1 )
        run = terminate(h[count+1], h[count], h0, dt)
        
        count = count + 1
    #print("Time: ",t," Force: ",(Fxsum**2 + Fysum**2)**0.5," vy: ", vy, " h: ", hi, " Mass: ", m1 ) 
    print("Fx: ", Fxsum, "Vx: ", vxi, "Hmax: ", hi)
    return m, h, d, vx, vy, v, ax, ay, Fx, Fy, rho,theta, time
        
"""Rocket Parameters"""
thrust = 1493   #N
mdot = 0.797    #kg/s
ms = 20         #kg
s = np.pi*(.075**2)
Cd1 = 0.75
Cd2 = 0.575
Cd3 = 0.4

burn_time = 6.5  #s 
lanch_angle_deg = 84 #degrees from horizontal
dt = 0.001 #time step, s

lanch_angle_rad = np.radians(lanch_angle_deg)
#print(lanch_angle_rad)
#tb, mdot, ms, Ft, s, Cd, dt
m, h1, d1, vx, vy, v1, ax, ay, Fx, Fy, rho, theta, t1= solver(burn_time, mdot, ms, thrust, s, Cd1, lanch_angle_rad, dt)
m, h2, d2, vx, vy, v2, ax, ay, Fx, Fy, rho, theta, t2= solver(burn_time, mdot, ms, thrust, s, Cd2, lanch_angle_rad, dt)
m, h3, d3, vx, vy, v3, ax, ay, Fx, Fy, rho, theta, t3= solver(burn_time, mdot, ms, thrust, s, Cd3, lanch_angle_rad, dt)

plt.figure(1)
plt.clf()

plt.plot(t1, v1, label = "vmag CD = 0.750")
plt.plot(t2, v2, label = "vmag CD = 0.575")
plt.plot(t3, v3, label = "vmag CD = 0.400")

plt.grid(1)
plt.xlabel("time [s]")
plt.ylabel("Velocity [m/s]")
plt.legend()
plt.savefig('Velocity_vs_time.png', dpi=300)


plt.figure(6)
plt.clf()
plt.plot(d1, h1, label = "CD = 0.750")
plt.plot(d2, h2, label = "CD = 0.575")
plt.plot(d3, h3, label = "CD = 0.400")
plt.grid(1)
plt.xlabel("Horizontal Distance (x) [m]")
plt.ylabel("Vertical Distance (y) [m]")
plt.ylim(ymin=0) 
plt.legend()
plt.savefig('Height_vs_Distance.png', dpi=300)






    
    
    