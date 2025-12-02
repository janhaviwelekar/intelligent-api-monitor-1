import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# ------------------------------
# Load log data
# ------------------------------
def load_logs(csv_file="logs.csv"):
    print("[INFO] Loading logs...")
    df = pd.read_csv(csv_file)

    # Convert latency to numeric (handle -1 errors)
    df['latency_ms'] = pd.to_numeric(df['latency_ms'], errors='coerce')

    # Remove rows with missing latency
    df = df.dropna(subset=['latency_ms'])

    print(f"[INFO] Loaded {len(df)} records.")
    return df


# ------------------------------
# Train Isolation Forest model
# ------------------------------
def detect_anomalies(df):
    print("[INFO] Training Isolation Forest...")

    model = IsolationForest(
        contamination=0.05,      # 5% anomalies expected
        random_state=42
    )

    df['anomaly'] = model.fit_predict(df[['latency_ms']])

    # anomaly = -1 → anomaly
    df['anomaly_label'] = df['anomaly'].apply(
        lambda x: "Anomaly" if x == -1 else "Normal"
    )

    print("[INFO] Anomaly detection complete.")
    return df


# ------------------------------
# Plot latency with anomalies
# ------------------------------
def plot_anomalies(df):
    plt.figure(figsize=(12, 6))
    plt.title("API Latency with Anomaly Detection")
    plt.xlabel("Request Index")
    plt.ylabel("Latency (ms)")

    # Plot normal points
    plt.plot(df.index, df['latency_ms'], '.', label="Normal", markersize=4)

    # Plot anomalies in red
    anomalies = df[df['anomaly'] == -1]
    plt.scatter(
        anomalies.index,
        anomalies['latency_ms'],
        color='red',
        label="Anomaly",
        s=40
    )

    plt.legend()
    plt.tight_layout()
    plt.show()


# ------------------------------
# Main program
# ------------------------------
def run_anomaly_pipeline():
    df = load_logs("../collector/api_logs.csv")   # correct path
    df = detect_anomalies(df)
    plot_anomalies(df)

    df.to_csv("api_logs_with_anomalies.csv", index=False)
    print("[INFO] Saved: api_logs_with_anomalies.csv")



if __name__ == "__main__":
    run_anomaly_pipeline()



