import pandas as pd
import streamlit as st
import os

# Paths
alerts_path = os.path.join("module_alerting", "alerts.csv")
behavior_path = os.path.join("module_behavior_modeling", "data", "user_behavior.csv")

# App Title
st.set_page_config(page_title="Insider Threat Detection Dashboard", layout="wide")
st.title("🚨 Insider Threat Detection Dashboard")

# Load Alerts
if os.path.exists(alerts_path):
    alerts_df = pd.read_csv(alerts_path)
    st.subheader("⚠️ Suspicious Users Flagged")
    st.dataframe(alerts_df, use_container_width=True)
    st.metric("Total Suspicious Users", len(alerts_df))
else:
    st.warning("⚠️ No alerts generated yet. Please run `generate_alerts.py` first.")

# Load User Behavior Data
if os.path.exists(behavior_path):
    behavior_df = pd.read_csv(behavior_path)
    st.subheader("📊 User Behavior Data")
    st.dataframe(behavior_df.head(20), use_container_width=True)

    # Anomaly Statistics
    if "anomaly" in behavior_df.columns:
        anomalies = behavior_df[behavior_df["anomaly"] == 1]
        st.metric("Total Anomalies Detected", len(anomalies))

        # --- LINE CHART: Anomalies Over Time ---
        st.subheader("📈 Anomalies Detected Over Time")
        if "date" in behavior_df.columns:
            behavior_df["date"] = pd.to_datetime(behavior_df["date"])
            anomalies_per_day = anomalies.groupby("date").size().reset_index(name="anomalies")
            st.line_chart(anomalies_per_day.set_index("date")["anomalies"])
        else:
            st.info("ℹ️ No date column found in data, unable to plot trend.")

        # --- BAR CHART: Off-Hours Access vs Total Actions ---
        st.subheader("📊 Off-Hours Access vs Total Actions per User")
        if "off_hours_count" in behavior_df.columns and "total_actions" in behavior_df.columns:
            # Aggregate per user
            user_activity = behavior_df.groupby("user_id").agg({
                "off_hours_count": "sum",
                "total_actions": "sum"
            }).reset_index()

            # Sort by off-hours count descending
            user_activity = user_activity.sort_values("off_hours_count", ascending=False).head(10)

            # Display bar chart
            st.bar_chart(
                user_activity.set_index("user_id")[["off_hours_count", "total_actions"]]
            )
        else:
            st.info("ℹ️ Required columns missing for bar chart.")
else:
    st.warning("⚠️ User behavior data not found. Please run `create_features.py` and `train_anomaly_model.py`.")

# Footer
st.markdown("---")
st.markdown("✅ **Insider Threat Detection Dashboard** | Built with Streamlit")
