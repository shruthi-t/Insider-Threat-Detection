import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/user_behavior_anomalies.csv')

# Count normal vs suspicious
counts = df['anomaly'].value_counts().sort_index()

plt.bar(['Suspicious (-1)', 'Normal (1)'], counts)
plt.title("Anomaly Detection - User Behavior")
plt.ylabel("User Count")
plt.show()
