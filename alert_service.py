# alert_service.py
import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
import requests

# =========================================================
# LOAD ANOMALIES FROM anomalies.csv
# =========================================================
def load_anomalies():
    if not os.path.exists("anomalies.csv"):
        print("⚠️ anomalies.csv not found. Run Step 4 first.")
        return pd.DataFrame()
    
    df = pd.read_csv("anomalies.csv")
    anomalies = df[df["anomaly"] == 1]
    return anomalies


# =========================================================
# SLACK ALERT
# =========================================================
def send_slack_alert(message):
    # Replace with your Slack webhook URL
    SLACK_WEBHOOK = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"

    payload = {"text": message}

    try:
        response = requests.post(SLACK_WEBHOOK, json=payload)
        if response.status_code == 200:
            print("✔ Slack alert sent!")
        else:
            print("❌ Slack error:", response.text)
    except Exception as e:
        print("❌ Slack Exception:", e)


# =========================================================
# EMAIL ALERT  (Gmail SMTP)
# =========================================================
def send_email_alert(message):
    EMAIL = "your_email@gmail.com"
    PASSWORD = "your_app_password"   # Gmail App Password (not your login password)
    TO = "recipient@example.com"

    msg = MIMEText(message)
    msg["Subject"] = "🚨 API Latency Anomaly Detected"
    msg["From"] = EMAIL
    msg["To"] = TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, TO, msg.as_string())
        print("✔ Email alert sent!")
    except Exception as e:
        print("❌ Email error:", e)


# =========================================================
# MAIN ALERT CHECKER
# =========================================================
def run_alert_service():
    anomalies = load_anomalies()

    if anomalies.empty:
        print("👍 No anomalies detected. System healthy.")
        return

    # Build readable text message
    message = "🚨 *API Latency Anomalies Detected*\n\n"

    for _, row in anomalies.iterrows():
        message += (
            f"• **Timestamp:** {row['timestamp']} \n"
            f"  API: {row['api_endpoint']} \n"
            f"  Latency: {row['latency_ms']} ms\n\n"
        )

    print("Sending alerts...\n")
    
    # ---- choose what you want to enable ----
    send_slack_alert(message)       # comment if not using Slack
    # send_email_alert(message)      # uncomment if using email

    print("✔ Alert service completed.")


if __name__ == "__main__":
    run_alert_service()
