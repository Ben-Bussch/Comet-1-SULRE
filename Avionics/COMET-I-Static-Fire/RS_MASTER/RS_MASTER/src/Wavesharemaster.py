# import serial
# import threading
# import time
# import sys

# # Configure COM port for Waveshare USB-RS485 dongle
# PORT = "COM5"   # <-- change to your Waveshare COM port
# BAUD = 9600

# ser = serial.Serial(PORT, BAUD, timeout=0.1)

# polling_enabled = True  # global flag

# def poll_slave():
#     """Poll Teensy slave for pressure data every 50 ms."""
#     global polling_enabled
#     while True:
#         if polling_enabled:
#             try:
#                 ser.write(b"PRESS?\n")   # ask for pressure
#                 response = ser.readline().decode(errors='ignore').strip()
#                 if response:
#                     print(f"[Slave] {response}")
#             except Exception as e:
#                 print(f"Polling error: {e}")
#         time.sleep(0.05)  # 50 ms

# def user_input():
#     """Handle user input commands, pausing polling temporarily."""
#     global polling_enabled
#     while True:
#         try:
#             cmd = sys.stdin.readline().strip()
#             if cmd:
#                 polling_enabled = False
#                 ser.write((cmd + "\n").encode())
#                 time.sleep(0.05)  # let slave reply
#                 response = ser.readline().decode(errors='ignore').strip()
#                 if response:
#                     print(f"[Slave] {response}")
#                 polling_enabled = True
#         except Exception as e:
#             print(f"Input error: {e}")

# def main():
#     print("Master started. Polling every 50 ms. Type a command to override.")
#     # Start threads
#     threading.Thread(target=poll_slave, daemon=True).start()
#     threading.Thread(target=user_input, daemon=True).start()

#     # Keep alive
#     while True:
#         time.sleep(1)

# if __name__ == "__main__":
#     main()
