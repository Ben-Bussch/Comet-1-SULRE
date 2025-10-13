import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import pandas as pd
import time
import glob
import os
import numpy as np

# === Auto-pick the newest CSV in your test data folder ===
FOLDER = r"C:\Users\adiso\OneDrive\Documents\SULRE\SULRE test data"
def get_latest_csv():
    csv_files = glob.glob(os.path.join(FOLDER, "*.csv"))
    if not csv_files:
        return None
    return max(csv_files, key=os.path.getctime)

CSV_PATH = get_latest_csv()
if not CSV_PATH:
    raise FileNotFoundError("No CSV file found in test data folder.")

print(f"Live plotting: {CSV_PATH}")

# === Simple 1D Kalman Filter (constant velocity model) ===
class KalmanFilter1D:
    def __init__(self, process_var=1e-3, meas_var=1e-1):
        # Process variance (Q): trust in model
        # Measurement variance (R): trust in measurements
        self.Q = process_var
        self.R = meas_var

        self.x = None  # state estimate
        self.P = None  # covariance

    def update(self, z):
        """Update filter with new measurement z"""
        if self.x is None:
            # first measurement initializes state
            self.x = z
            self.P = 1.0
        else:
            # Prediction step
            x_pred = self.x
            P_pred = self.P + self.Q

            # Update step
            K = P_pred / (P_pred + self.R)
            self.x = x_pred + K * (z - x_pred)
            self.P = (1 - K) * P_pred

        return self.x

plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))


kf_pressure = KalmanFilter1D(process_var=1e-4, meas_var=1e-2)
kf_current = KalmanFilter1D(process_var=1e-4, meas_var=1e-2)

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

while True:
    df = read_csv_data()
    if not df.empty:
        # Apply Kalman filter
        df["pressure_kf"] = [kf_pressure.update(z) for z in df["pressure"]]
        df["current_kf"] = [kf_current.update(z) for z in df["current"]]

        # Print only the latest filtered data to terminal
        latest = df.iloc[-1]
        print(f"runtime={latest['runtime']}, pressure_kf={latest['pressure_kf']:.3f}, current_kf={latest['current_kf']:.3f}")

        ax1.clear()
        ax2.clear()

        # Plot both raw and filtered data
        ax1.plot(df["runtime"], df["pressure"], 'b.', alpha=0.3, label="Raw Pressure")
        ax1.plot(df["runtime"], df["pressure_kf"], 'b-', linewidth=2, label="Filtered Pressure")
        ax1.set_title("Pressure vs Runtime (Kalman Filtered)")
        ax1.set_xlabel("Runtime (s)")
        ax1.set_ylabel("Pressure")
        ax1.grid(True)
        ax1.legend()

        ax2.plot(df["runtime"], df["current"], 'r.', alpha=0.3, label="Raw Current")
        ax2.plot(df["runtime"], df["current_kf"], 'r-', linewidth=2, label="Filtered Current")
        ax2.set_title("Current vs Runtime (Kalman Filtered)")
        ax2.set_xlabel("Runtime (s)")
        ax2.set_ylabel("Current")
        ax2.grid(True)
        ax2.legend()

        plt.tight_layout()
        plt.draw()
        plt.pause(0.005)

    time.sleep(0.005)
