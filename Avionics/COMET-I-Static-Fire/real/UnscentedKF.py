import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import pandas as pd
import time
import glob
import os
import numpy as np
import datetime
import csv



FOLDER = r"C:\Users\adiso\OneDrive\Documents\SULRE\SULRE test data"
def get_latest_csv():
    csv_files = glob.glob(os.path.join(FOLDER, "*.csv"))
    if not csv_files:
        return None
    return max(csv_files, key=os.path.getctime)

CSV_PATH = get_latest_csv()
if not CSV_PATH:
    raise FileNotFoundError("No CSV file found in test data folder.")

print(f"Live plotting (EKF): {CSV_PATH}")

#=========================================================================================
FOLDER2 = r"C:\Users\adiso\OneDrive\Documents\SULRE\SULRE test data filtered"
os.makedirs(FOLDER2, exist_ok=True)

timestamp1 = time.strftime("%Y%m%d-%H%M")
runtype = input("Run number?").strip().lower()

program_starttime = time.time()
CSV_PATH2 = os.path.join(FOLDER2, f"SULREtestdatafiltered_{runtype}_{timestamp1}.csv")

#============================================================================================

def log_to_csv(response):
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    program_runtime = round(time.time() - program_starttime, 3)
    try:
        with open(CSV_PATH2, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, program_runtime, response])
    except Exception as e:
        print(f"CSV write error: {e}")

#=============================================================================================

class ExtendedKalmanFilter:
    def __init__(self, dim_x, dim_z, process_var=1e-3, meas_var=1e-1):
        self.dim_x = dim_x
        self.dim_z = dim_z
        self.Q = np.eye(dim_x) * process_var  
        self.R = np.eye(dim_z) * meas_var    
        self.x = np.zeros(dim_x)             
        self.P = np.eye(dim_x) * 1.0         

    def f(self, x):
        """Nonlinear state transition"""
        pressure, current = x
        return np.array([
            pressure + 0.01 * np.sin(current),
            current + 0.01 * np.cos(pressure)
        ])

    def F_jacobian(self, x):
        """Jacobian of f(x)"""
        pressure, current = x
        return np.array([
            [1.0, 0.01 * np.cos(current)],
            [-0.01 * np.sin(pressure), 1.0]
        ])

    def h(self, x):
        
        return x  

    def H_jacobian(self, x):
        
        return np.eye(self.dim_z)

    def predict(self):
        
        F = self.F_jacobian(self.x)
        self.x = self.f(self.x)
        self.P = F @ self.P @ F.T + self.Q

    def update(self, z):
        
        H = self.H_jacobian(self.x)
        y = z - self.h(self.x)  # residual
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.P = (np.eye(self.dim_x) - K @ H) @ self.P

        return self.x


plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ekf = ExtendedKalmanFilter(dim_x=2, dim_z=2, process_var=1e-4, meas_var=1e-2)

def read_csv_data():
    try:
        df = pd.read_csv(
            CSV_PATH,
            names=["timestamp", "runtime", "data"],
            on_bad_lines="skip"
        )
        df[["pressure", "current"]] = df["data"].str.replace('"','').str.split(",", expand=True)
        df["pressure"] = pd.to_numeric(df["pressure"], errors="coerce")
        df["current"] = pd.to_numeric(df["current"], errors="coerce")
        return df.dropna(subset=["pressure", "current"])
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return pd.DataFrame(columns=["runtime", "pressure", "current"])

# Create plot objects once
raw_pressure_plot, = ax1.plot([], [], 'b.', alpha=0.3, label="Raw Pressure")
ekf_pressure_plot, = ax1.plot([], [], 'r-', label="EKF Pressure")
raw_current_plot, = ax2.plot([], [], 'b.', alpha=0.3, label="Raw Current")
ekf_current_plot, = ax2.plot([], [], 'r-', label="EKF Current")

ax1.set_title("Pressure vs Runtime (EKF)")
ax1.set_xlabel("Runtime (s)")
ax1.set_ylabel("Pressure")
ax1.grid(True)
ax1.legend()

ax2.set_title("Current vs Runtime (EKF)")
ax2.set_xlabel("Runtime (s)")
ax2.set_ylabel("Current")
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()

while True:
    df = read_csv_data()
    if not df.empty:
        pressure_est, current_est = [], []
        for i, row in df.iterrows():
            z = np.array([row["pressure"], row["current"]])
            ekf.predict()
            est = ekf.update(z)
            pressure_est.append(est[0])
            current_est.append(est[1])

            
            filtered_response = f"{est[0]},{est[1]}"
            log_to_csv(filtered_response)

        # Update plot data instead of clearing/replotting
        raw_pressure_plot.set_data(df["runtime"], df["pressure"])
        ekf_pressure_plot.set_data(df["runtime"], pressure_est)
        raw_current_plot.set_data(df["runtime"], df["current"])
        ekf_current_plot.set_data(df["runtime"], current_est)

        ax1.relim()
        ax1.autoscale_view()
        ax2.relim()
        ax2.autoscale_view()

        plt.draw()
        plt.pause(0.005)

    time.sleep(0.005)
