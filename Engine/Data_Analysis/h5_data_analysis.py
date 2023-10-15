import h5py
import numpy as np
import csv
import os

try: 
    print('The home directory has been saved as: ', home_directory)
except:
    home_directory = os.path.normpath(os.getcwd() + os.sep + os.pardir)    
    print('Saving the home directory as: ', home_directory)
    
burn_10s_directory = home_directory+"\Data\Hot_Fire_10s"
burn_3s_directory = home_directory+"\Data\Hot_Fire_3s"

data_directory_path = burn_10s_directory #Set to either 3s or 10s burn respectively
data_path = "groups" #Set to the path within which all sensors will be saved, seperate with "/"
data_folder_name = "groups_data" #Set to name of folder to be created to contain files, folder must

os.chdir(data_directory_path)

h5_data = os.listdir()[0]

f = h5py.File(h5_data, "r")

def save_data(sensors, filename):
    folder_path = os.path.join(os.getcwd(), data_folder_name)
    os.mkdir(folder_path)
    os.chdir(folder_path)
    counter = 0

    for sensor in sensors:
        counter += 1
        print(counter, " out of ", len(sensors), " sensors saved")
        time_arr = np.array(sensor[1])
        data_arr = np.array(sensor[2])
        with open("%s.csv" % sensor[0], "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(["Time", "Sensor_Data"])

            for i in range(len(sensor[1])):
                writer.writerow([time_arr[i], data_arr[i]])


def h5_tree(val, pre=''):
    items = len(val)
    for key, val in val.items():
        items -= 1
        if items == 0:
            if type(val) == h5py._hl.group.Group:
                print(pre + '└── ' + key)
                h5_tree(val, pre+'    ')
            else:
                print(pre + '└── ' + key + ' (%d)' % len(val))
        else:
            if type(val) == h5py._hl.group.Group:
                print(pre + '├── ' + key)
                h5_tree(val, pre+'│   ')
            else:
                print(pre + '├── ' + key + ' (%d)' % len(val))
                

def search(val, search_param):
    items = len(val)
    for key, val in val.items():
        items -= 1
        if key == search_param:
            return val
        
    raise Exception("Group or data does not exist, check data_path")


def get_sensors(val, sensors):
    items = len(val)
    previous_group = val
    for key, val in val.items():
        if type(val) == h5py._hl.group.Group:
            get_sensors(val, sensors)
            previous_group = val
        else:
            time = search(previous_group, "time")
            data = search(previous_group, "data")

            sensor_path = "_".join(val.name.split("/"))[1:]
            sensors.append([sensor_path, time, data])
            sensor_path = ""

    return sensors


with h5py.File(h5_data, 'r') as hf:
    
    h5_tree(hf)
    
    print("==================================================================================================")
    
    relavent_groups = data_path.split("/")
    gp_fname = "_".join(relavent_groups)
    nxt_group = hf
    for group in relavent_groups:
        nxt_group = search(nxt_group, group)

    sensors = []
    sensors = get_sensors(nxt_group, sensors)

    os.chdir(home_directory+"\Data_Analysis")
    save_data(sensors, gp_fname)

    
