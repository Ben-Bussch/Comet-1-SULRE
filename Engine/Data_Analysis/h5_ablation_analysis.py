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

t_tank_N2O_path = N2O_path+"TC851" 

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
burn_eq_start, i_start_eq = 1.20, 125001#117001
burn_eq_end, i_end_eq = 10.0, 200001 #200001


#Example data fetch
IPA_mdot_data = h5_data_lib.run(mdot_IPA_path, burn_10s_directory)

IPA_mdot_data_eq = [0,0]
IPA_mdot_data_eq[0] = IPA_mdot_data[0][i_start_eq:i_end_eq]
IPA_mdot_data_eq[1] = IPA_mdot_data[1][i_start_eq:i_end_eq]


plt.figure(1)
plt.title("IPA mass flowrate")
plt.plot(IPA_mdot_data_eq[1],IPA_mdot_data_eq[0], label = "data")

#mdot_dot = np.polynomial.polynomial.polyfit(IPA_mdot_data_eq[1], IPA_mdot_data_eq[0], 1)
#print(mdot_dot)

grad = 0.009
m0 = 0.764
i = 2
y_list =  []
i_list = []
while i < 10:
    y_list.append(m0+grad*i)
    i_list.append(i)
    i+= 0.1
    
plt.plot(i_list,y_list, label ="Modeled Throat ablation")
plt.legend()
plt.xlabel("time / s")
plt.ylabel("Mass Flowrate / kg/s")
plt.grid()

    
        










