import requests
import time
import csv
import datetime
import random

# -----------------------------
# SETTINGS
# -----------------------------
API_ENDPOINTS = [
    "http://127.0.0.1:5001/ping",
    "http://127.0.0.1:5001/slow",
    "http://127.0.0.1:5001/random-delay",
    "http://127.0.0.1:5001/sometimes-error"
]

LOG_FILE = "api_logs.csv"
REQUEST_INTERVAL = 3  # seconds between each API call


# -----------------------------
# Initialize CSV File
# -----------------------------
def initialize_csv():
    try:
        with open(LOG_FILE, "x", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "endpoint", "status", "latency_ms"])
        print(f"[INFO] Created new log file: {LOG_FILE}")

    except FileExistsError:
        print(f"[INFO] Using existing log file: {LOG_FILE}")


# -----------------------------
# Function to Log Data
# -----------------------------
def log_to_csv(timestamp, endpoint, status, latency_ms):
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, endpoint, status, latency_ms])


# -----------------------------
# Main Loop
# -----------------------------
def start_collecting():
    print("[INFO] Starting API Log Collector...")
    initialize_csv()

    while True:
        endpoint = random.choice(API_ENDPOINTS)
        start_time = time.time()

        try:
            response = requests.get(endpoint, timeout=5)
            latency = (time.time() - start_time) * 1000  # ms
            status = response.status_code

        except Exception as e:
            latency = -1  # error
            status = "ERROR"

        timestamp = datetime.datetime.now().isoformat()

        log_to_csv(timestamp, endpoint, status, round(latency, 2))

        print(f"[LOG] {timestamp} | {endpoint} | {status} | {latency:.2f} ms")

        time.sleep(REQUEST_INTERVAL)


if __name__ == "__main__":
    start_collecting()

