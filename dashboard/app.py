import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(page_title="API Performance Monitor", layout="wide")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    logs = pd.read_csv("../collector/api_logs.csv")  # Update path if needed
    anomalies = pd.read_csv("../model/api_logs_with_anomalies.csv")  # Update path if needed
    
    logs["timestamp"] = pd.to_datetime(logs["timestamp"])
    anomalies["timestamp"] = pd.to_datetime(anomalies["timestamp"])
    
    return logs, anomalies

logs, anomalies = load_data()

# -------------------------------
# Sidebar Controls
# -------------------------------
st.sidebar.header("Controls")

# Auto-refresh checkbox
auto_refresh = st.sidebar.checkbox("Auto Refresh (every 5 sec)", value=False)
if auto_refresh:
    st_autorefresh(interval=5000, key="datarefresh")  # 5000ms = 5 sec

# Endpoint filter
selected_endpoint = st.sidebar.selectbox(
    "Filter by Endpoint",
    ["All"] + sorted(logs["endpoint"].unique())
)

# Filter by endpoint
if selected_endpoint != "All":
    logs = logs[logs["endpoint"] == selected_endpoint]
    anomalies = anomalies[anomalies["endpoint"] == selected_endpoint]

# -------------------------------
# Dashboard Header
# -------------------------------
st.title("🚀 Intelligent API Performance Monitor")
st.write("Real-time monitoring • Latency anomaly detection • API performance analytics")

# -------------------------------
# Key Performance Indicators
# -------------------------------
st.subheader("📊 Key Metrics")
col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Total Requests", len(logs))
col2.metric("Average Latency (ms)", round(logs["latency_ms"].mean(), 2))
col3.metric("Detected Anomalies", len(anomalies[anomalies["anomaly_label"] == "Anomaly"]))
col4.metric("Max Latency", logs["latency_ms"].max())
col5.metric("Median Latency", logs["latency_ms"].median())
col6.metric("95th Percentile", logs["latency_ms"].quantile(0.95))

# -------------------------------
# Download CSV Buttons
# -------------------------------
st.subheader("💾 Download Data")
st.download_button(
    label="Download Filtered Logs as CSV",
    data=logs.to_csv(index=False),
    file_name='filtered_logs.csv',
    mime='text/csv'
)
st.download_button(
    label="Download Anomaly Logs as CSV",
    data=anomalies.to_csv(index=False),
    file_name='anomaly_logs.csv',
    mime='text/csv'
)

# -------------------------------
# Latency Over Time Plot
# -------------------------------
st.subheader("📈 Latency Over Time")
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(logs["timestamp"], logs["latency_ms"], label="Latency", marker=".", linestyle="")
# Highlight anomalies
anomaly_points = anomalies[anomalies["anomaly_label"] == "Anomaly"]
ax.scatter(
    anomaly_points["timestamp"],
    anomaly_points["latency_ms"],
    color="red",
    s=60,
    label="Anomaly"
)
ax.set_xlabel("Time")
ax.set_ylabel("Latency (ms)")
ax.legend()
st.pyplot(fig)

# -------------------------------
# Endpoint Latency Comparison
# -------------------------------
st.subheader("📊 Endpoint Latency Comparison")
endpoint_summary = logs.groupby("endpoint")["latency_ms"].agg(["count", "mean", "max", "min"])
st.dataframe(endpoint_summary)
st.bar_chart(endpoint_summary["mean"])

# -------------------------------
# Anomalies Over Time
# -------------------------------
st.subheader("🚨 Anomalies Over Time")
if not anomaly_points.empty:
    anomaly_count = anomaly_points.groupby(anomaly_points["timestamp"].dt.floor("H")).size()
    st.line_chart(anomaly_count.rename("Anomaly Count"))
else:
    st.info("No anomalies detected.")

# -------------------------------
# Recent Alerts Table
# -------------------------------
st.subheader("🚨 Recent Alerts (Detected Anomalies)")
recent_alerts = anomaly_points.tail(10)
st.table(recent_alerts[["timestamp", "endpoint", "latency_ms"]])

# -------------------------------
# Raw Data Tabs
# -------------------------------
tab1, tab2 = st.tabs(["Raw Logs", "Anomaly Logs"])
with tab1:
    st.dataframe(logs.tail(100))
with tab2:
    st.dataframe(anomalies.tail(100))


