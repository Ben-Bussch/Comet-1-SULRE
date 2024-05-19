# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 14:34:39 2024

@author: Bobke
"""
import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

try: 
    print('The home directory has been saved as: ', home_directory)
except:
    home_directory = os.path.normpath(os.getcwd() + os.sep + os.pardir)    
    print('Saving the home directory as: ', home_directory)
    
data_path = home_directory+'\Data\Ablation'
results_path = home_directory+'\Data_analysis\Ablation'

os.chdir(data_path)
directories = os.listdir()
print(directories)

df = pd.read_csv('Nozzle_Ablation_Data.csv')
print(df)
#print(df.keys())
t = df["time"][100:]
height = df["height"][100:]

dt = t[101]-t[100]

nozzle_diameter = 70 - (2*height)
abaltion_rate_data = []

nd_temp = 70 - (2*df["height"][99])
for nd in nozzle_diameter:
    ablation_rate = (nd_temp - nd)/dt
    print(ablation_rate)
    nd_temp = nd
    abaltion_rate_data.append(ablation_rate)


"Averagine out data a bit"
avg = 0
count_avg = 0
abl_average = [0]
for dx in abaltion_rate_data:
    
    if count_avg < 5:
        avg += dx
        count_avg += 1
    else:
        count_avg = 0
        abl_average.append(avg/5)
        avg = 0
        
"Averagine out data a bit"
skip_res = 6
skip = slice(None, None, skip_res )
t_alt = t[skip]


os.chdir(results_path)

plt.figure(1)
plt.title("Nozzle diameter at exit versus time")
plt.plot(t, nozzle_diameter, color= "r", label = "Nozzle Diameter")
#plt.plot(turb_pr, Tmax_list, label = "Compressor Pressure Ratio")
plt.ylabel("Nozzle Diameter [mm]")
plt.xlabel("Time [s]")
plt.grid()
plt.savefig('Nozzle_ablation_stable.png', dpi = 400)
plt.show()

plt.figure(1)
plt.title("Ablation rate at Nozzle exit versus time")
plt.plot(t_alt[1:], abl_average[1:], "rx", label = "Nozzle Ablation Rate")
#plt.plot(turb_pr, Tmax_list, label = "Compressor Pressure Ratio")
plt.ylabel("Nozzle Ablation Rate [mm/s]")
plt.xlabel("Time [s]")
plt.grid()
plt.savefig('Nozzle_ablation_rate_avg.png', dpi = 400)
plt.show()