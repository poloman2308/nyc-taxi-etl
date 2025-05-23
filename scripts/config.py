import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# File path and connection details
LOCAL_CSV_PATH = os.getenv("LOCAL_CSV_PATH", "/tmp/yellow_taxi_data.csv")

POSTGRES_DB = os.getenv("POSTGRES_DB", "nyc_taxi")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_OBJECT_NAME = os.getenv("S3_OBJECT_NAME", "yellow_taxi_data.csv")

TABLE_NAME = os.getenv("TABLE_NAME", "yellow_taxi_data")
