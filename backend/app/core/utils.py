import boto3
import pandas as pd
import os
from datetime import datetime
from app.core.config import settings

S3_BUCKET = os.getenv("S3_BUCKET_NAME")

HISTORICO_CSV_LOCAL = "/tmp/historico_acoes.csv"
HISTORICO_CSV_S3_KEY = "logs/historico_acoes.csv"
AWS_REGION=settings.AWS_REGION

def registrar_acao(user: str, action: str, status: str, object: str):
    # Garantir que o CSV tenha cabeçalho se ainda não existe
    file_exists = os.path.isfile(HISTORICO_CSV_LOCAL)
    df = pd.DataFrame([{
        "user": user,
        "action": action,
        "data": datetime.today().strftime('%Y-%m-%d'),
        "status_operation": status,
        "object": object
    }])

    df.to_csv(HISTORICO_CSV_LOCAL, mode='a', header=not file_exists, index=False)

    # Subir para S3
    s3 = boto3.client("s3", region_name=AWS_REGION)
    s3.upload_file(HISTORICO_CSV_LOCAL, S3_BUCKET, HISTORICO_CSV_S3_KEY)