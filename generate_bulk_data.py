import os
import random
import pandas as pd
from datetime import datetime, timedelta

# ----------------------------
# 1. Setup paths
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(BASE_DIR, "module_behavior_modeling", "data")
os.makedirs(data_dir, exist_ok=True)

emails_path = os.path.join(data_dir, "email_processed.csv")
logs_path = os.path.join(data_dir, "logs_processed.csv")

# ----------------------------
# 2. Generate users & dates
# ----------------------------
users = [f"U{100 + i}" for i in range(1, 201)]  # 200 users
start_date = datetime(2025, 7, 1)
end_date = datetime(2025, 7, 30)
date_range = pd.date_range(start_date, end_date).tolist()

# ----------------------------
# 3. Generate random emails
# ----------------------------
email_data = []
for user in users:
    for _ in range(random.randint(2, 5)):  # 2 to 5 emails per user
        ts = random.choice(date_range)
        sentiment = round(random.uniform(-1, 1), 2)
        email_data.append([user, ts, sentiment])

emails_df = pd.DataFrame(email_data, columns=["user_id", "timestamp", "sentiment"])

# ----------------------------
# 4. Generate random logs
# ----------------------------
log_data = []
actions = ["login", "logout", "file_download", "db_access", "vpn"]
for user in users:
    for _ in range(random.randint(2, 5)):  # 2 to 5 logs per user
        ts = random.choice(date_range)
        action = random.choice(actions)
        off_hours = random.choice([0, 1])
        log_data.append([user, ts, action, off_hours])

logs_df = pd.DataFrame(log_data, columns=["user_id", "timestamp", "action", "off_hours"])

# ----------------------------
# 5. Inject suspicious users
# ----------------------------
suspicious_users = random.sample(users, 5)
for user in suspicious_users:
    for _ in range(3):
        ts = random.choice(date_range)
        logs_df = pd.concat([
            logs_df,
            pd.DataFrame([[user, ts, "confidential_access", 1]], columns=logs_df.columns)
        ], ignore_index=True)

# ----------------------------
# 6. Save both datasets
# ----------------------------
emails_df.to_csv(emails_path, index=False)
logs_df.to_csv(logs_path, index=False)

print(f"✅ Successfully generated {len(emails_df)} emails and {len(logs_df)} access logs!")
print(f"📌 Suspicious users injected: {', '.join(suspicious_users)}")
print(f"📁 Emails saved to: {emails_path}")
print(f"📁 Logs saved to: {logs_path}")
