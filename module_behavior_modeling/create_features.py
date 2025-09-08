import os
import pandas as pd

# ----------------------------
# 1. Define absolute paths
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(BASE_DIR, "data")
os.makedirs(data_dir, exist_ok=True)

emails_path = os.path.join(data_dir, "email_processed.csv")
logs_path = os.path.join(data_dir, "logs_processed.csv")
csv_path = os.path.join(data_dir, "user_behavior.csv")

# ----------------------------
# 2. Load preprocessed data
# ----------------------------
emails = pd.read_csv(emails_path, parse_dates=["timestamp"])
logs = pd.read_csv(logs_path, parse_dates=["timestamp"])

# Ensure sentiment column is numeric
if "sentiment" not in emails.columns:
    emails["sentiment"] = 0
else:
    emails["sentiment"] = pd.to_numeric(emails["sentiment"], errors="coerce").fillna(0)

# ----------------------------
# 3. Extract date from timestamp
# ----------------------------
emails["date"] = emails["timestamp"].dt.date
logs["date"] = logs["timestamp"].dt.date

# ----------------------------
# 4. Email features
# ----------------------------
email_features = emails.groupby(["user_id", "date"]).agg(
    avg_sentiment=("sentiment", "mean"),
    neg_msg_count=("sentiment", lambda x: (x < -0.5).sum())
).reset_index()

# ----------------------------
# 5. Log features
# ----------------------------
log_features = logs.groupby(["user_id", "date"]).agg(
    off_hours_count=("off_hours", "sum"),
    total_actions=("action", "count")
).reset_index()

# ----------------------------
# 6. Merge email + log features
# ----------------------------
features = pd.merge(email_features, log_features, on=["user_id", "date"], how="inner").fillna(0)

# ----------------------------
# 7. Save final features
# ----------------------------
features.to_csv(csv_path, index=False)
print(f"✅ Feature file created: {csv_path}")
print(f"📊 Final dataset size: {features.shape[0]} rows × {features.shape[1]} columns")
