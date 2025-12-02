# 🚀 Intelligent API Performance Monitor

A real-time **API performance monitoring dashboard** built with **Python and Streamlit**, designed to detect latency anomalies and provide interactive insights into API performance.

---


## **Introduction**

APIs are critical in modern applications, and monitoring their performance is essential.  
This dashboard provides:

- Real-time monitoring of API requests  
- Detection of latency anomalies  
- Endpoint-wise performance analytics  
- Exportable logs for further analysis  

---

## **Features**

- **Auto-refresh:** Updates every 5 seconds for live monitoring  
- **Endpoint filter:** View logs for specific APIs  
- **KPIs:** Total requests, average latency, anomalies, max/median/95th percentile latency  
- **Latency Over Time Plot:** Visualizes all requests with anomalies highlighted in red  
- **Endpoint Latency Comparison:** Table and bar chart of average latency per endpoint  
- **Anomalies Over Time:** Detect trends in anomaly occurrences  
- **Recent Alerts Table:** Shows the 10 most recent anomalies  
- **Raw Data Tabs:** View all logs or anomaly logs  
- **CSV Download:** Export filtered logs or anomalies  

---

## **Data Sources**

1. **API Logs:** `api_logs.csv`  
   - Contains timestamped request data with latency, status, and endpoint information.  

2. **Anomalies:** `api_logs_with_anomalies.csv`  
   - Logs labeled with detected anomalies.  

> Both CSV files are read into the dashboard using **Pandas**.

---

## **Technical Stack**

- **Python** – Core programming language  
- **Streamlit** – Interactive dashboard UI  
- **Pandas** – Data manipulation and filtering  
- **Matplotlib** – Data visualization  
- **streamlit_autorefresh** *(optional)* – For non-blocking auto-refresh  

---

## **Setup & Installation**

1. **Clone the repository**

```bash
git clone https://github.com/janhaviwelekar/intelligent-api-monitor-1.git
cd intelligent-api-monitor-1/dashboard
