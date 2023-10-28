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


plt.figure(3)
plt.title("Thurst")
plt.plot(thrust_data[1],thrust_data[0])
plt.xlabel("time / s")
plt.ylabel("Thrust / N")



thrust_temp = 0
thrust = []
time = []
count = 0
count_10 = 0

"""Thrust Time-averaging"""
while count < len(thrust_data[1]):
    
    thrust_temp +=  thrust_data[0][count]
    if  count_10  == count:
        thrust_10_avg = thrust_temp/100
        thrust.append(thrust_10_avg)
        time.append(thrust_data[1][count_10])
        thrust_temp = 0
        count_10 += 100
    count += 1
    
plt.figure(3)
plt.title("Thurst, 0.1 sec avg")
plt.plot(time,thrust)
plt.xlabel("time / s")
plt.ylabel("Thrust / N") 
plt.grid()
#plt.xaxis.set_major_locator(ticker.MultipleLocator(1))

mdot_IPA_sum = 0
mdot_N2O_sum = 0
count_IPA_avg = 0
count_N2O_avg = 0
count = 0


"""Equalibirum mdot"""
while count < len(mdot_IPA_data[1]):
    t = mdot_IPA_data[1][count]
    if  t > 1.70 and t < 10.00: 
        if not math.isnan(mdot_IPA_data[0][count]):
            mdot_IPA_temp =  mdot_IPA_data[0][count]
            mdot_IPA_sum += mdot_IPA_temp
            count_IPA_avg += 1
        if not math.isnan(mdot_N2O_data[0][count]):
            mdot_N2O_temp =  mdot_N2O_data[0][count]
            mdot_N2O_sum += mdot_N2O_temp
            count_N2O_avg += 1
                
        
    count += 1

mdot_IPA_avg = mdot_IPA_sum/count_IPA_avg
mdot_N2O_avg = mdot_N2O_sum/count_N2O_avg

print("IPA average mass flowrate: ",mdot_IPA_avg, "kg/s")
print("IPA average mass flowrate: ", mdot_N2O_avg, "kg/s")
print("Total average Flowrate: ", mdot_IPA_avg+mdot_N2O_avg)

#print(mdot_IPA_data[0])
#plt.plot(mdot_IPA_data[1],mdot_IPA_data[0])
plt.plot()


        










