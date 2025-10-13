# import serial
# import csv
# import time

# ser = serial.Serial('COM4', 9600)  # Replace 'COM3' with your Teensy's port
# csv_path = r'C:\Users\adiso\SULRE\SULREtestdata.csv'

# with open(csv_path, 'a', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['timestamp', 'data'])  # Write header if needed

#     while True:
#         line = ser.readline().decode('utf-8').strip()
#         if line:
#             writer.writerow([int(time.time()*1000), line])
#             print(f"Logged: {line}")