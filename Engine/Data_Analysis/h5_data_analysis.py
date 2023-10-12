import h5py
import numpy as np
import csv

''' Change file_path accordingly, current setup assumes .h5 file exists in working directory '''
file_path = "20230704-007-release.h5"
data_path = "groups/air/PT100"

f = h5py.File(file_path, "r")

def save_data(time, data, filename):
    time_arr = np.array(time)
    data_arr = np.array(data)

    with open("%s.csv" % filename, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Time", "Sensor_Data"])
        for i in range(len(data_arr)):
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
                pass
                print(pre + '└── ' + key + ' (%d)' % len(val))
        else:
            if type(val) == h5py._hl.group.Group:
                print(pre + '├── ' + key)
                h5_tree(val, pre+'│   ')
            else:
                pass
                print(pre + '├── ' + key + ' (%d)' % len(val))
                

def search(val, search_param, pre=''):
    items = len(val)
    for key, val in val.items():
        items -= 1
        if key == search_param:
            return val
        
    raise Exception("Group or data does not exist, chech data_path")


with h5py.File(file_directory, 'r') as hf:
    
    h5_tree(hf)
    
    print("========================================================================================")
    
    relavent_groups = data_path.split("/")
    gp_fname = "_".join(relavent_groups)
    nxt_group = hf
    for group in relavent_groups:
        nxt_group = search(nxt_group, group)
    time = search(nxt_group, "time")
    data = search(nxt_group, "data")

    save_data(time, data, gp_fname)

    
