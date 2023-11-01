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
from scipy.signal import butter,filtfilt

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
p_inlet_N2_path = N2_path+"PT520"

p_tank_IPA_path = IPA_path+"PT732"
p_tank_N2O_path = N2O_path+"PT851"
p_tank_N2_path = N2_path+"PT521"

t_inlet_IPA_path = IPA_path+"TC732"
t_inlet_N2O_path = N2O_path+"TC852"

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
burn_eq_start, i_start_eq = 1.70, 132001#117001
burn_eq_end, i_end_eq = 10.0, 147001 #200001


#Example data fetch
thrust_data = h5_data_lib.run(thrust_path, burn_10s_directory)
n2_p_data = h5_data_lib.run(p_inlet_N2_path, burn_10s_directory)
N2O_p_data = h5_data_lib.run(p_inlet_N2O_path , burn_10s_directory)
N2O_tank_p_data= h5_data_lib.run(p_tank_N2O_path , burn_10s_directory)

t_IPA_inlet = h5_data_lib.run(t_inlet_IPA_path, burn_10s_directory)
t_N2O_inlet = h5_data_lib.run(t_inlet_N2O_path, burn_10s_directory)



"""
#Example equalibrium burn time analysis:
thrust_data_eq = [0,0]
#thrust_data_eq[0] = thrust_data[0][i_start_eq:i_start_eq+4000]
#thrust_data_eq[1] = thrust_data[1][i_start_eq:i_start_eq+4000]
thrust_data_eq[0] = thrust_data[0][i_start_eq:i_end_eq]
thrust_data_eq[1] = thrust_data[1][i_start_eq:i_end_eq]


#Filter for 77 Hz, calculated from thrust data
fs = 10000
nyq = 0.5*fs
cutoff = 21 #Hz
normal_cutoff = cutoff / nyq
order = 2
n = len(thrust_data_eq[0])
b, a = butter(order, normal_cutoff, btype='low', analog=False)
filtered_thrust = filtfilt(b, a, thrust_data_eq[0])
"""



listOf_Xticks = np.arange(-10, 15, 1)
listOf_Yticks = np.arange(0, 60, 2)


plt.figure(1)
plt.title("N2O Pressures")
#plt.plot(n2_p_data [1],n2_p_data [0], label ="N2 Outlet Pressure")
plt.plot(N2O_p_data[1],N2O_p_data[0], label ="N2O Inlet Pressure")
plt.plot(N2O_tank_p_data[1],N2O_tank_p_data[0], label ="N2O Tank Pressure")
plt.legend()
plt.xticks(listOf_Xticks)
plt.yticks(listOf_Yticks)
plt.xlabel("time / s")
plt.ylabel("Pressure / Bars")
plt.grid()

plt.figure(2)
plt.title("N2 Pressures")
plt.plot(n2_p_data [1],n2_p_data [0], label ="N2 Outlet Pressure")
plt.legend()

plt.xlabel("time / s")
plt.ylabel("Pressure / Bars")
plt.grid()


plt.figure(3)
plt.title("Inlet Tempuratures")
plt.plot(t_IPA_inlet[1],t_IPA_inlet[0], label ="IPA Inlet Temperature")
plt.plot(t_N2O_inlet[1],t_N2O_inlet[0], label ="N2O Inlet Temperature")
plt.xlabel("time / s")
plt.ylabel("Tempurature / Degrees Celcius")
plt.legend()
plt.grid()
plt.plot()


        










