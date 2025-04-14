import os

S3_BUCKET = os.getenv("S3_BUCKET_NAME")
ATHENA_DB = "playground"
S3_OUTPUT = f"s3://{S3_BUCKET}/athena-results/"


def create_database_if_not_exists(athena_client):
    create_db_query = f"CREATE DATABASE IF NOT EXISTS {ATHENA_DB}"
    athena_client.start_query_execution(
        QueryString=create_db_query,
        ResultConfiguration={"OutputLocation": S3_OUTPUT},
    )