import os
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# ------------------------------
# 1. Set correct paths
# ------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(BASE_DIR, "module_behavior_modeling", "data")
os.makedirs(data_dir, exist_ok=True)

csv_path = os.path.join(data_dir, "user_behavior.csv")
model_dir = os.path.join(BASE_DIR, "module_behavior_modeling", "models")
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "iforest_model.pkl")

# ------------------------------
# 2. Load dataset
# ------------------------------
if not os.path.exists(csv_path):
    raise FileNotFoundError(
        f"❌ Missing file: {csv_path}\nPlease run create_features.py first."
    )

df = pd.read_csv(csv_path)

# Keep numeric features only
numeric_df = df.select_dtypes(include=['number'])

# Store user IDs for later mapping
user_ids = df['user_id']

# ------------------------------
# 3. Train Isolation Forest
# ------------------------------
model = IsolationForest(
    n_estimators=200,
    contamination=0.1,
    random_state=42
)
model.fit(numeric_df)

# ------------------------------
# 4. Predict anomalies & scores
# ------------------------------
df['anomaly'] = model.predict(numeric_df)  # -1 = anomaly, 1 = normal
df['anomaly'] = df['anomaly'].apply(lambda x: 1 if x == -1 else 0)
df['anomaly_score'] = -model.decision_function(numeric_df)

# ------------------------------
# 5. Save updated CSV & model
# ------------------------------
df.to_csv(csv_path, index=False)
joblib.dump(model, model_path)

print("✅ Model trained and predictions saved!")
print(f"📄 Updated CSV: {csv_path}")
print(f"🤖 Model saved: {model_path}")
print(f"⚠️ Total anomalies flagged: {df['anomaly'].sum()}")
