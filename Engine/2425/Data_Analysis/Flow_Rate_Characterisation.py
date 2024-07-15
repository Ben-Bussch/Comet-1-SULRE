# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 17:38:13 2023

@author: Bobke
"""

"""
LC190 (thrust), M730 (IPA mdot), M850 (N2O mdot), 
PT852/TC852 (N2O delivery pressure/temperature), 
and PT732/TC732 (IPA delivery pressure/temperature). 
The nitrous valve is XT852, 
the IPA valve is V731 if you want to see the timings.
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 
import os
import math
import h5_data_lib 

try: 
    print('The home directory has been saved as: ', home_directory)
except:
    home_directory = os.path.normpath(os.getcwd() + os.sep + os.pardir)    
    print('Saving the home directory as: ', home_directory)

#groups
IPA_path = "groups/ipa/"
N2O_path = "groups/n2o/"
chamber_path = "chamber/"
general_path = "channels/"

#File Paths
mdot_IPA_path = IPA_path+"M730"
mdot_N2O_path = N2O_path+"M850"

p_inlet_IPA_path = IPA_path+"PT732"
p_inlet_N2O_path = N2O_path+"PT852"

t_inlet_IPA_path = IPA_path+"TC852"
t_inlet_N2O_path = N2O_path+"TC732"

valve_IPA_path = IPA_path+"V731"
valve_N2O_path = N2O_path+"XT852"

thrust_path = general_path+"LC190"

burn_10s_directory = home_directory+"\Data\Hot_Fire_10s"
burn_3s_directory = home_directory+"\Data\Hot_Fire_3s"


#Example data fetch
mdot_IPA_data = h5_data_lib.run(mdot_IPA_path, burn_10s_directory)
mdot_N2O_data = h5_data_lib.run(mdot_N2O_path, burn_10s_directory)

thrust_data = h5_data_lib.run(thrust_path, burn_10s_directory)

#10-s burn time data
burn_start = 1.22
burn_end = 10.13



plt.figure(1)
plt.title("IPA mass Flowrate")
plt.plot(mdot_IPA_data[1],mdot_IPA_data[0])
plt.xlabel("time / s")
plt.ylabel("Mass Flowrate / kg s-1")

plt.figure(2)
plt.title("N2O mass Flowrate")
plt.plot(mdot_N2O_data[1],mdot_N2O_data[0])
plt.xlabel("time / s")
plt.ylabel("Mass Flowrate / kg s-1")


plt.figure(5)
plt.title("Thurst")
plt.plot(thrust_data[1],thrust_data[0])
plt.xlabel("time / s")
plt.ylabel("Thrust / N")





#plt.xaxis.set_major_locator(ticker.MultipleLocator(1))

mdot_IPA_sum = 0
mdot_N2O_sum = 0
count_IPA_avg = 0
count_N2O_avg = 0
count = 0

mdot_fe = []
mdot_oe = []
time_e = []

"""Equalibirum mdot"""
while count < len(mdot_IPA_data[1]):
    t = mdot_IPA_data[1][count]
    if  t > 2.00 and t < 10.00: 
        if not math.isnan(mdot_IPA_data[0][count]):
            mdot_IPA_temp =  mdot_IPA_data[0][count]
            mdot_IPA_sum += mdot_IPA_temp
            count_IPA_avg += 1
        if not math.isnan(mdot_N2O_data[0][count]):
            mdot_N2O_temp =  mdot_N2O_data[0][count]
            mdot_N2O_sum += mdot_N2O_temp
            count_N2O_avg += 1
        mdot_fe.append(mdot_IPA_temp)
        mdot_oe.append(mdot_N2O_temp)
        time_e.append(mdot_N2O_data[1][count])
        
        
    count += 1

mdot_IPA_avg = mdot_IPA_sum/count_IPA_avg
mdot_N2O_avg = mdot_N2O_sum/count_N2O_avg

print("IPA average mass flowrate: ",mdot_IPA_avg, "kg/s")
print("IPA average mass flowrate: ", mdot_N2O_avg, "kg/s")
print("Total average Flowrate: ", mdot_IPA_avg+mdot_N2O_avg)

#print(mdot_IPA_data[0])
#plt.plot(mdot_IPA_data[1],mdot_IPA_data[0])



Total_mass_flow = [i + j for i, j in zip(mdot_oe,mdot_fe)]
#print(Total_mass_flow )
"""plt.figure(4)
plt.title("Mass Flows ")
plt.plot(time_e, Total_mass_flow)
plt.xlabel("time / s")
plt.ylabel("Mass Flowrate [kg / s]")"""

OF = [i / j for i, j in zip(mdot_oe,mdot_fe)]
"""
plt.figure(3)
plt.title("OF ratio")
plt.plot(time_e, OF)
plt.xlabel("time / s")
plt.ylabel("O/F ratio")
"""

thrust_temp = 0
thrust = []
OF_avg = []
mf_avg = []
time = []
count = 0
count_10 = 0

OF_temp = 0
total_mass_flow_temp = 0
time_eavg = []

"""mdot, Time-averaging"""
while count < len(OF):
    OF_temp += OF[count]
    total_mass_flow_temp  += Total_mass_flow[count]
    if  count_10  == count:
        OF_10_avg = OF_temp/300
        OF_avg.append(OF_10_avg)
       
        mass_flow_avg = total_mass_flow_temp/300
        mf_avg.append(mass_flow_avg)
        
        time_eavg.append(time_e[count_10])
        OF_temp = 0
        total_mass_flow_temp = 0
        
        count_10 += 300
    count += 1
    
print(OF_avg[0], OF_avg[1])
plt.figure(3)
plt.title("Time Averaged OF ratio")
plt.plot(time_eavg, OF_avg)
plt.xlabel("time / s")
plt.ylabel("O/F ratio")
plt.grid()

plt.figure(4)
plt.title("Time Averaged Mass Flows")
plt.plot(time_eavg,  mf_avg)
plt.xlabel("time / s")
plt.ylabel("Mass Flowrate [kg / s]")
plt.grid()


"""Thrust Time-averaging"""
while count < len(thrust_data[1]):
    
    thrust_temp +=  thrust_data[0][count]
    #OF_temp += 
    if  count_10  == count:
        thrust_10_avg = thrust_temp/100
        thrust.append(thrust_10_avg)
        time.append(thrust_data[1][count_10])
        thrust_temp = 0
        #OF_avg = 
        count_10 += 100
    count += 1
    
plt.figure(5)
plt.title("Thurst, 0.1 sec avg")
plt.plot(time,thrust)
plt.xlabel("time / s")
plt.ylabel("Thrust / N") 
plt.grid()

plt.plot()









