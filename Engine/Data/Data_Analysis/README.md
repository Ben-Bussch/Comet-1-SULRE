H5 data analysis:

h5_data_analysis.py allows the user to save specific sensor data to a csv file.

Using:
1. PIP install h5py and numpy
2. Change file_path accordingly, current config assumes .h5 file exists in working directory
3. Change data_path, group names should be seperated by "/", should not include "data" or "time" at the end. Run to preview tree if necessary.
4. .csv file will be created with data_path name in working directory
5. Enjoy

Notes:
- For faster runtime remove h5_tree(hf)

Written in Python 3.11.5

Goodluck, Davide Masini
