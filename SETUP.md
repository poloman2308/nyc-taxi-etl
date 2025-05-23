
# NYC Taxi ETL Pipeline

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/poloman2308/nyc-taxi-etl.git
cd nyc-taxi-etl
```

### 2. Create Virtual Environment
```bash
python3 -m venv airflow_py311_venv
source airflow_py311_venv/bin/activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Initialize Airflow
```bash
export AIRFLOW_HOME=$(pwd)
airflow db init
```

### 5. Start Airflow
```bash
airflow webserver --port 8080
airflow scheduler
```

### 6. Access Airflow UI
Go to [http://localhost:8080](http://localhost:8080) and trigger the `nyc_taxi_etl` DAG.
