# NYC Taxi ETL Pipeline 🚖

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Airflow](https://img.shields.io/badge/Airflow-2.8.1-blue)](https://airflow.apache.org/)
[![AWS S3](https://img.shields.io/badge/AWS-S3-orange)](https://aws.amazon.com/s3/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org/)

An end-to-end ETL pipeline using Apache Airflow to process and analyze NYC Yellow Taxi trip data. This project includes automated data ingestion, validation, PostgreSQL loading, and S3 archival.

---

## 📁 Project Structure

```
nyc-taxi-etl/
├── dags/                  
│   └── nyc_taxi_etl.py    
├── data/                  
│   └── yellow_taxi_data.csv  
├── scripts/               
│   ├── config.py
│   └── webserver_config.py
├── .env                   
├── .gitignore             
├── requirements.txt       
├── SETUP.md               
└── README.md           
```

---

## ⚙️ Technologies Used

- **Apache Airflow** for orchestration
- **Python 3.11** for ETL logic
- **Pandas** for data processing
- **PostgreSQL** for structured storage
- **Amazon S3** for cloud data backup
- **psycopg2** and **boto3** for database and S3 connections

---

## 🧪 ETL Pipeline Workflow

### 1. `download_data`  
Downloads NYC Yellow Taxi data (Parquet format) and converts it to CSV.

### 2. `load_to_postgres`  
Reads the CSV, performs data validation, and loads it into a PostgreSQL table.

### 3. `upload_to_s3`  
Uploads the CSV file to an Amazon S3 bucket for archival.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Apache Airflow
- PostgreSQL
- AWS account with S3 access

### 1. Clone this repository

```bash
git clone https://github.com/<your-username>/nyc-taxi-etl.git
cd nyc-taxi-etl
```

---

### 2. Set up your environment

```bash
python -m venv airflow_etl_env
source airflow_etl_env/bin/activate
pip install -r requirements.txt
```

---

### 3. Configure Airflow

```bash
export AIRFLOW_HOME=~/airflow
airflow db init
```

---

### 4. Set up environment variables
Create a .env file at the project root:

```dotenv
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
S3_BUCKET_NAME=dataeng-landing-zone-dfa23
LOCAL_CSV_PATH=/tmp/yellow_taxi_data.csv
TABLE_NAME=yellow_taxi_data
```

---

### 5. Start Airflow services

```bash
airflow scheduler
airflow webserver
```
Access the UI at: http://localhost:8080

---

## 📊 Dataset

Source: [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
Due to GitHub file size limits, the CSV is not included in the repo.
Download it manually or let the DAG download it for you.

---

## 📤 S3 Configuration

Make sure your AWS credentials are stored securely in .env. The DAG automatically uploads processed CSVs to the configured S3 bucket.

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome.
Feel free to fork this repository and submit a pull request.

---

## ✍️ Author

Derek Acevedo
[GitHub](www.github.com/poloman2308) • [LinkedIn](www.linkedin.com/in/derekacevedo86)
