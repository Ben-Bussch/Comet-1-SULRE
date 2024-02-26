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
    
    hdot = (h2 - h1)/dt
    if hdot <= 0:
        run = False
    """
    if h1 < h0:
        run = False 
    """
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
            print("v launchrail: ", v[count], "h from ground: ", h[count]-h0 )
        
        #print("Time: ",t," Force: ",Fsum," Acc: ", a1," v: ", v1, " h: ", h1, " Mass: ", m1 )
        run = terminate(h[count+1], h[count], h0, dt)
        
        count = count + 1
    #print("Time: ",t," Force: ",(Fxsum**2 + Fysum**2)**0.5," vy: ", vy, " h: ", hi, " Mass: ", m1 ) 
    print("Fx: ", Fxsum, "Vx: ", vxi, "Hmax: ", hi)
    return m, h, d, vx, vy, v, ax, ay, Fx, Fy, rho,theta, time
        
"""Rocket Parameters"""
thrust = 1493   #N
mdot = 0.797    #kg/s
ms = 25         #kg
Outer_Diameter =  160 #mm (very important value to keep updated!)
s = np.pi*((Outer_Diameter/2000)**2) 
Cd = 0.38

burn_time = 6.5 #s 
lanch_angle_deg = 84 #degrees from horizontal
dt = 0.001 #time step, s

lanch_angle_rad = np.radians(lanch_angle_deg)
#print(lanch_angle_rad)
#tb, mdot, ms, Ft, s, Cd, dt
m, h, d, vx, vy, v, ax, ay, Fx, Fy, rho, theta, t= solver(burn_time, mdot, ms, thrust, s, Cd, lanch_angle_rad, dt)

F = []
a = []
for i in range(len(t)):
    F.append((Fx[i]**2 + Fy[i]**2)**0.5)
    a.append((ax[i]**2 + ay[i]**2)**0.5)

plt.figure(1)
plt.clf()
plt.title("Ms (kg): "+str(ms)+" Diameter (mm): "+str(Outer_Diameter) +" Burn Time: "+str(burn_time) +" CD: "+str(Cd))
plt.plot(t, v, label = "vmag")
plt.plot(t, vx, label = "vx")
plt.plot(t, vy, label = "vy")

plt.grid(1)
plt.xlabel("time [s]")
plt.ylabel("Velocity [m/s]")
plt.legend()
plt.savefig('Velocity_vs_time.png', dpi=300)

plt.figure(2)
plt.clf()
plt.title("Ms (kg): "+str(ms)+" Diameter (mm): "+str(Outer_Diameter) +" Burn Time: "+str(burn_time) +" CD: "+str(Cd))

plt.plot(t, F, label = "Fmag")
plt.plot(t, Fx, label = "Fx")
plt.plot(t, Fy, label = "Fy")

plt.grid(1)
plt.xlabel("time [s]")
plt.ylabel("Force [N]")
plt.legend()
plt.savefig('Force_vs_time.png', dpi=300)

plt.figure(3)
plt.clf()
plt.title("Ms (kg): "+str(ms)+" Diameter (mm): "+str(Outer_Diameter) +" Burn Time: "+str(burn_time) +" CD: "+str(Cd))

plt.plot(t, h, label = "Height")
plt.plot(t, d, label = "Distance")

plt.grid(1)
plt.xlabel("time [s]")
plt.ylabel("Height [m]")
plt.legend()
plt.savefig('Height_vs_time.png', dpi=300)

plt.figure(4)
plt.clf()
plt.title("Ms (kg): "+str(ms)+" Diameter (mm): "+str(Outer_Diameter) +" Burn Time: "+str(burn_time) +" CD: "+str(Cd))

plt.plot(t, a, label = "amag")
plt.plot(t, ax, label = "ax")
plt.plot(t, ay, label = "ay")

plt.grid(1)
plt.xlabel("time [s]")
plt.ylabel("Acceleration [m/s^2]")
plt.legend()
plt.savefig('Acceleration_vs_time.png', dpi=300)


plt.figure(5)
plt.clf()
plt.title("Ms (kg): "+str(ms)+" Diameter (mm): "+str(Outer_Diameter) +" Burn Time: "+str(burn_time) +" CD: "+str(Cd))

plt.plot(h, rho)

plt.grid(1)
plt.xlabel("height [m]")
plt.ylabel("Atmospheric Density [kg/m^3]")
plt.legend()
plt.savefig('Density_vs_height.png', dpi=300)


plt.figure(6)
plt.clf()
plt.title("Ms (kg): "+str(ms)+" Diameter (mm): "+str(Outer_Diameter) +" Burn Time: "+str(burn_time) +" CD: "+str(Cd))

plt.plot(d, h)
plt.grid(1)
plt.xlabel("Horizontal Distance (x) [m]")
plt.ylabel("Vertical Distance (y) [m]")
plt.ylim(ymin=0) 
plt.savefig('Height_vs_Distance.png', dpi=300)

plt.figure(7)
plt.clf()
plt.title("Ms (kg): "+str(ms)+" Diameter (mm): "+str(Outer_Diameter) +" Burn Time: "+str(burn_time) +" CD: "+str(Cd))

plt.plot(t, np.degrees(theta))
plt.grid(1)
plt.xlabel("Time [s]")
plt.ylabel("Angle from horizontal [degrees]")
plt.ylim(ymin=0) 
plt.savefig('Angle_vs_time.png', dpi=300)

plt.figure(8)
plt.clf()
plt.title("Ms (kg): "+str(ms)+" Diameter (mm): "+str(Outer_Diameter) +" Burn Time: "+str(burn_time) +" CD: "+str(Cd))

plt.plot(t, m)
plt.grid(1)
plt.xlabel("Time [s]")
plt.ylabel("Rocket Mass")
plt.ylim(ymin=0) 
plt.savefig('Mass_vs_time.png', dpi=300)

    




    
    
    