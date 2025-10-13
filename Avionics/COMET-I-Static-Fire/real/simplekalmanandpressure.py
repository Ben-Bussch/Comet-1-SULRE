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


class KalmanFilter1D:
    def __init__(self, process_var=1e-4, meas_var=1e-2):
        self.Q = process_var  # process noise
        self.R = meas_var     # measurement noise
        self.x = None         # estimate
        self.P = None         # covariance

    def update(self, z):
        if self.x is None:
            self.x = z
            self.P = 1.0
        else:
            # Prediction
            x_pred = self.x
            P_pred = self.P + self.Q
            # Update
            K = P_pred / (P_pred + self.R)
            self.x = x_pred + K * (z - x_pred)
            self.P = (1 - K) * P_pred
        return self.x


kf_pressure = KalmanFilter1D(process_var=1e-5, meas_var=1e-2)
kf_current = KalmanFilter1D(process_var=1e-5, meas_var=1e-2)

# --- CSV Logging ---
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

# --- Polling Thread ---
def poll_slave():
    global polling_enabled
    while True:
        if polling_enabled:
            try:
                ser.write(b"PRESS?\n")
                response = ser.readline().decode(errors='ignore').strip()

                if response:
                    try:
                        # Assume response is like: "pressure,current"
                        parts = response.split(",")
                        pressure = float(parts[0].replace('"', ''))
                        current = float(parts[1].replace('"', '')) if len(parts) > 1 else None

                        filtered_pressure = kf_pressure.update(pressure)
                        filtered_current = kf_current.update(current) if current is not None else None

                        print(f"[AUTO] Raw: Pressure={pressure:.3f}, Current={current:.3f} | "
                              f"Filtered: Pressure={filtered_pressure:.3f}, Current={filtered_current:.3f}")

                    except ValueError:
                        print(f"[AUTO] Invalid data: {response}")

                    log_to_csv(response)
                else:
                    print("[AUTO] No data received")

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

                print(f"[MANUAL] {response}")
                log_to_csv(response)

                polling_enabled = True
        except Exception as e:
            print(f"Input error: {e}")


def main():
    print("Master started. Polling data with Kalman filtering. Type a command to override.")
    print(f"Logging all responses to {CSV_PATH}")
    print("----------------------------------------------------")
    print("Format: [AUTO] Raw: <raw_value> | Filtered: <filtered_value>")
    print("----------------------------------------------------")

    threading.Thread(target=poll_slave, daemon=True).start()
    threading.Thread(target=user_input, daemon=True).start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
