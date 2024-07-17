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

pt_path = "groups/pt/"



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

chamber_pt = pt_path + "PT100"

thrust_path = general_path+"LC190"


#Data Paths
burn_directory = home_directory+"\Data\Hot_Fire"






#Example data fetch
thrust_data = h5_data_lib.run(thrust_path, burn_directory)

p_inlet_IPA = h5_data_lib.run(p_inlet_IPA_path , burn_directory)
p_inlet_N2O = h5_data_lib.run(p_inlet_N2O_path , burn_directory)

p_chamber = h5_data_lib.run(chamber_pt , burn_directory)



plt.figure(1)
plt.title("Thurst")
plt.plot(thrust_data[1],thrust_data[0])
plt.xlabel("time / s")
plt.ylabel("Thrust / N")
plt.grid()

plt.figure(2)
plt.title("Pressures")
plt.plot(p_inlet_IPA[1],p_inlet_IPA[0])
plt.plot(p_inlet_N2O[1],p_inlet_N2O[0])
plt.xlabel("time / s")
plt.ylabel("Thrust / Bar")
plt.grid()


plt.plot()


        










