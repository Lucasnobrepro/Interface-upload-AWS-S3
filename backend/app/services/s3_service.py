import boto3
from fastapi import UploadFile
from app.core.config import settings
import os
import pandas as pd
from datetime import datetime


S3_BUCKET = os.getenv("S3_BUCKET_NAME")
AWS_REGION = settings.AWS_REGION
HISTORICO_CSV_LOCAL = "/tmp/historico_acoes.csv"
HISTORICO_CSV_S3_KEY = "logs/historico_acoes.csv"


s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

async def upload_file_to_s3(file: UploadFile):
    content = await file.read()
    s3.put_object(Bucket=settings.S3_BUCKET_NAME, Key=file.filename, Body=content)
    url = f"https://{settings.S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{file.filename}"
    return url


def get_history():
    try:
        # Baixar CSV do S3
        s3 = boto3.client("s3", region_name=AWS_REGION)
        s3.download_file(S3_BUCKET, HISTORICO_CSV_S3_KEY, HISTORICO_CSV_LOCAL)

        # Carregar e renderizar
        df = pd.read_csv(HISTORICO_CSV_LOCAL)
        return f"<h2>Histórico de Ações</h2>{df.to_html(index=False)}"

    except Exception as e:
        return f"<h3>Erro ao carregar histórico: {str(e)}</h3>"