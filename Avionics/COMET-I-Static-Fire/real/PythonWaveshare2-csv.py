import serial
import threading
import time
import sys
import csv
import os
import datetime

# --- Serial setup ---
PORT = "COM7"
BAUD = 9600
ser = serial.Serial(PORT, BAUD, timeout=0.1)

polling_enabled = True  # global flag


FOLDER = r"C:\Users\adiso\OneDrive\Documents\SULRE\SULRE test data"
os.makedirs(FOLDER, exist_ok=True)

timestamp1 = time.strftime("%Y%m%d-%H%M")
runtype = input("Is this a test run or actual run? ").strip().lower()

program_starttime = time.time()
CSV_PATH = os.path.join(FOLDER, f"SULREtestdata_{runtype}_{timestamp1}.csv")


def log_to_csv(response):
    """Write timestamped response to CSV with milliseconds."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    program_runtime = round(time.time() - program_starttime, 3)
    try:
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, program_runtime, response])
    except Exception as e:
        print(f"CSV write error: {e}")


def poll_slave():
    global polling_enabled
    while True:
        if polling_enabled:
            try:
                ser.write(b"PRESS?\n")
                response = ser.readline().decode(errors='ignore').strip()
                if not response:
                    response = "<no data>"
                log_to_csv(response)
               # print(f"[Auto] {response}")  # Print to terminal
            except Exception as e:
                print(f"Polling error: {e}")
        time.sleep(0.05)  

def user_input():
    global polling_enabled
    while True:
        try:
            cmd = sys.stdin.readline().strip()
            if cmd:
                polling_enabled = False
                time.sleep(0.1)

                ser.write((cmd + "\n").encode())
                time.sleep(0.1)

                response = ser.readline().decode(errors='ignore').strip()
                if not response:
                    response = "<no data>"

                print(f"[Manual] {response}")  # Already prints manual responses
                log_to_csv(response)

                polling_enabled = True
        except Exception as e:
            print(f"Input error: {e}")

# --- Main ---
def main():
    print("Master started. Polling data. Type a command to override.")
    print(f"Logging all responses to {CSV_PATH}")

    threading.Thread(target=poll_slave, daemon=True).start()
    threading.Thread(target=user_input, daemon=True).start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
