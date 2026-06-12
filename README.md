# Insider Threat Detection System

This project is an end-to-end Machine Learning-based cybersecurity solution that detects potential insider threats by analyzing employee behavior and communication patterns. It combines NLP-based sentiment analysis with the Isolation Forest anomaly detection algorithm to identify suspicious activities and proactively flag risky users.

The system demonstrates a complete threat detection pipeline:

Raw Employee Data → Feature Engineering → Sentiment Analysis → Isolation Forest Detection → Alert Generation → Dashboard Visualization

Project Structure

Insider Threat Detection

dashboard

* app.py

module_alerting

module_behavior_modeling

module_processing

generate_bulk_data.py

create_features.py

train_anomaly_model.py

emails.csv

access_logs.csv

email_processed.csv

requirements.txt

README.md

Setup

Create a virtual environment (optional):

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Project

Generate synthetic employee data:

```bash
python generate_bulk_data.py
```

Create behavioral features:

```bash
python create_features.py
```

Train the anomaly detection model:

```bash
python train_anomaly_model.py
```

Launch the Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

Open the dashboard in your browser:

```text
http://localhost:8501
```

Highlights

This project leverages NLP sentiment analysis and Isolation Forest anomaly detection to identify suspicious insider activities. It analyzes behavioral indicators such as email sentiment, off-hours access, and activity counts to detect anomalies. The system includes an interactive Streamlit dashboard for real-time monitoring, suspicious user identification, and anomaly trend visualization, enabling proactive threat detection and improved enterprise security monitoring.
