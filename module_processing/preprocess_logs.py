import pandas as pd
import os

# ✅ Use the correct relative path
logs_path = os.path.join("data", "access_logs.csv")
logs = pd.read_csv(logs_path)

# ✅ Explicit timestamp parsing
logs['timestamp'] = pd.to_datetime(logs['timestamp'], format="%Y-%m-%d %H:%M:%S", errors="coerce")

# Drop invalid timestamps (if any)
logs = logs.dropna(subset=['timestamp'])

# Extract hour of access
logs['hour'] = logs['timestamp'].dt.hour

# Flag off-hours access → before 7 AM or after 8 PM
logs['off_hours'] = logs['hour'].apply(lambda x: x < 7 or x > 20)

# Save processed logs
output_path = os.path.join("data", "logs_processed.csv")
logs.to_csv(output_path, index=False)

print("✅ Logs preprocessed successfully!")
print(logs.head())
