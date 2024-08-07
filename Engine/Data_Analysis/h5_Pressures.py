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
import numpy as np

try: 
    print('The home directory has been saved as: ', home_directory)
except:
    home_directory = os.path.normpath(os.getcwd() + os.sep + os.pardir)    
    print('Saving the home directory as: ', home_directory)

#groups
IPA_path = "groups/ipa/"
N2O_path = "groups/n2o/"
N2_path = "groups/n2/"
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
valve_N2_path = N2_path + " XT852"

thrust_path = general_path+"LC190"


#Data Paths
burn_10s_directory = home_directory+"\Data\Hot_Fire_10s"
burn_3s_directory = home_directory+"\Data\Hot_Fire_3s"


#10-s burn time data
burn_start, i_start = 0.60, 106001 #seconds, then indicie of time
burn_end, i_end = 12.40, 224001

#roughly the times for the linear thrust data:
burn_eq_start, i_start_eq = 1.70, 117001
burn_eq_end, i_end_eq = 10.0, 200001


#Example data fetch
IPA_pressure = h5_data_lib.run(p_inlet_IPA_path, burn_10s_directory)
IPA_valve = h5_data_lib.run(valve_IPA_path, burn_10s_directory)

N2O_pressure = h5_data_lib.run(p_inlet_N2O_path, burn_10s_directory)
N2O_valve = h5_data_lib.run(valve_N2O_path, burn_10s_directory)

plt.figure(1)
plt.title("Pressure")
plt.plot(IPA_pressure[1],IPA_pressure[0], label = "IPA Pressure 23")
plt.plot(N2O_pressure[1],N2O_pressure[0], label = "N2O Pressure 23")
plt.xlabel("time / s")
plt.ylabel("Pressure / Bars")
plt.legend()
plt.grid()

plt.figure(2)
plt.title("Valves")
plt.plot(IPA_valve[1],IPA_valve[0], label = "IPA Valve 23")
plt.plot(N2O_valve[1],N2O_valve[0], label = "N2O Valve 23")
plt.xlabel("time / s")
plt.ylabel("Valve Setting / 0-1")
plt.legend()
plt.grid()

plt.plot()


        










