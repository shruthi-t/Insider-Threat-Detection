import os
import subprocess
import pandas as pd

# ------------------------------
# 1. Get absolute project path
# ------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(BASE_DIR, "module_behavior_modeling","data", "user_behavior.csv")

# ------------------------------
# 2. If user_behavior.csv is missing → auto-train model
# ------------------------------
if not os.path.exists(csv_path):
    print(f"⚠️ {csv_path} not found.")
    print("🔄 Running train_anomaly_model.py to generate it...")

    training_script = os.path.join(BASE_DIR, "module_behavior_modeling", "train_anomaly_model.py")

    try:
        subprocess.run(["python", training_script], check=True)
        print("✅ Model trained successfully. Loading generated CSV...")
    except subprocess.CalledProcessError:
        raise RuntimeError("❌ Failed to run train_anomaly_model.py. Please check the script.")

# ------------------------------
# 3. Load user_behavior.csv
# ------------------------------
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"❌ Cannot find {csv_path} even after training. Check your model pipeline.")

df = pd.read_csv(csv_path)

# ------------------------------
# 4. Check anomaly column exists
# ------------------------------
if "anomaly" not in df.columns:
    raise ValueError("❌ 'anomaly' column not found in user_behavior.csv! Please retrain the model.")

# ------------------------------
# 5. Pick suspicious users smartly
# ------------------------------
# Primary method → anomaly == 1
suspicious_users = df[df["anomaly"] == 1]["user_id"].unique()

# If fewer than 3 suspicious users are found → fallback method
if len(suspicious_users) < 3:
    if "anomaly_score" in df.columns:
        # Sort by anomaly score descending
        top_users = df.sort_values("anomaly_score", ascending=False)["user_id"].unique()
    else:
        # No anomaly_score column → fallback to sensitive resource access detection
        sensitive_keywords = ["payroll", "password", "confidential", "customer_db", "vpn"]
        if "resource" in df.columns:
            df["is_sensitive"] = df["resource"].apply(
                lambda x: any(keyword in str(x).lower() for keyword in sensitive_keywords)
            )
            top_users = df[df["is_sensitive"] == True]["user_id"].unique()
        else:
            # If still nothing, pick top frequent users
            top_users = df["user_id"].value_counts().index.tolist()

    # Always ensure at least 4 suspicious users
    suspicious_users = top_users[:4]

# ------------------------------
# 6. Save alerts to CSV
# ------------------------------
alerts_path = os.path.join(BASE_DIR, "module_alerting", "alerts.csv")
alerts_df = pd.DataFrame({"suspicious_user_id": suspicious_users})
alerts_df.to_csv(alerts_path, index=False)

# ------------------------------
# 7. Print results
# ------------------------------
print(f"✅ Alerts generated: {len(suspicious_users)} suspicious user(s) flagged.")
print("📌 Suspicious Users:", ", ".join(suspicious_users))
print(f"📁 Alerts saved to: {alerts_path}")
