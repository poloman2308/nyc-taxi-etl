from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
import pandas as pd
import requests
from io import BytesIO
import logging
import psycopg2
from psycopg2.extras import execute_values
import boto3
import os

# Logging
log = logging.getLogger(__name__)

# Constants
DATA_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
LOCAL_CSV_PATH = "/tmp/yellow_taxi_data.csv"
TABLE_NAME = "yellow_taxi_data"
BUCKET_NAME = "dataeng-landing-zone-dfa23"
S3_KEY = "yellow_taxi_data/yellow_tripdata_2024-01.csv"

# Default args
default_args = {
    'owner': 'derek',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def download_data():
    log.info("Downloading Parquet file...")
    response = requests.get(DATA_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to download data: {response.status_code}")

    df = pd.read_parquet(BytesIO(response.content))
    log.info(f"Downloaded {len(df)} rows. Saving to CSV...")
    df.to_csv(LOCAL_CSV_PATH, index=False)
    log.info("✅ CSV file written to local path")

def load_to_postgres():
    try:
        df = pd.read_csv(LOCAL_CSV_PATH, low_memory=False)

        expected_columns = [
            "VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime", "passenger_count",
            "trip_distance", "RatecodeID", "store_and_fwd_flag", "PULocationID", "DOLocationID",
            "payment_type", "fare_amount", "extra", "mta_tax", "tip_amount",
            "tolls_amount", "improvement_surcharge", "total_amount", "congestion_surcharge", "Airport_fee"
        ]

        log.info("Validating columns...")
        missing = set(expected_columns) - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns in CSV: {missing}")

        df = df[expected_columns].dropna()
        log.info(f"Filtered and validated {len(df)} rows for insert.")

        if df['passenger_count'].lt(0).any():
            raise ValueError("Negative passenger counts found")

        conn = psycopg2.connect(
            dbname="nyc_taxi",
            user="postgres",
            host="localhost"
        )
        cur = conn.cursor()

        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                "VendorID" INT,
                "tpep_pickup_datetime" TIMESTAMP,
                "tpep_dropoff_datetime" TIMESTAMP,
                "passenger_count" INT,
                "trip_distance" FLOAT,
                "RatecodeID" INT,
                "store_and_fwd_flag" TEXT,
                "PULocationID" INT,
                "DOLocationID" INT,
                "payment_type" INT,
                "fare_amount" FLOAT,
                "extra" FLOAT,
                "mta_tax" FLOAT,
                "tip_amount" FLOAT,
                "tolls_amount" FLOAT,
                "improvement_surcharge" FLOAT,
                "total_amount" FLOAT,
                "congestion_surcharge" FLOAT,
                "Airport_fee" FLOAT
            );
        """)
        conn.commit()

        insert_query = f"""
            INSERT INTO {TABLE_NAME} (
                "VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime", "passenger_count",
                "trip_distance", "RatecodeID", "store_and_fwd_flag", "PULocationID", "DOLocationID",
                "payment_type", "fare_amount", "extra", "mta_tax", "tip_amount",
                "tolls_amount", "improvement_surcharge", "total_amount", "congestion_surcharge", "Airport_fee"
            ) VALUES %s
        """

        data_tuples = df.values.tolist()
        log.info("Inserting data into PostgreSQL...")
        execute_values(cur, insert_query, data_tuples)
        conn.commit()
        cur.close()
        conn.close()
        log.info(f"✅ Inserted {len(data_tuples)} rows into {TABLE_NAME}.")

    except Exception as e:
        log.error(f"❌ Error in load_to_postgres: {str(e)}")
        raise

def upload_to_s3():
    s3 = boto3.client('s3')
    if not os.path.exists(LOCAL_CSV_PATH):
        raise FileNotFoundError("CSV file not found for upload")

    log.info("Uploading file to S3...")
    s3.upload_file(LOCAL_CSV_PATH, BUCKET_NAME, S3_KEY)
    log.info(f"✅ Uploaded {LOCAL_CSV_PATH} to s3://{BUCKET_NAME}/{S3_KEY}")

with DAG(
    dag_id='nyc_taxi_etl',
    default_args=default_args,
    description='ETL pipeline for NYC Taxi data',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['example']
) as dag:

    task_download = PythonOperator(
        task_id='download_data',
        python_callable=download_data
    )

    task_load_postgres = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_to_postgres
    )

    task_upload_s3 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3
    )

    task_download >> task_load_postgres >> task_upload_s3

