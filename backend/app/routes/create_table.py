from fastapi import APIRouter, UploadFile, Form, HTTPException
import boto3
import pandas as pd
import os
import time
from app.core.config import settings
from app.core.utils import registrar_acao
from app.services.athena_service import create_database_if_not_exists


router = APIRouter()

S3_BUCKET = os.getenv("S3_BUCKET_NAME")
ATHENA_DB = "playground"
S3_OUTPUT = f"s3://{S3_BUCKET}/athena-results/"
S3_CSV_UPLOAD = f"s3://{S3_BUCKET}/uploaded-csvs/"

HISTORICO_CSV_LOCAL = "/tmp/historico_acoes.csv"
HISTORICO_CSV_S3_KEY = "logs/historico_acoes.csv"

AWS_REGION=settings.AWS_REGION
LOG_FILE = "historico_acoes.csv"

@router.post("/")
async def create_table(table_name: str = Form(...), file: UploadFile = Form(...), user: str = Form(...)):
    try:
        # 1. Salvar CSV temporariamente
        contents = await file.read()
        temp_file = f"/tmp/{file.filename}"
        with open(temp_file, "wb") as f:
            f.write(contents)

        # 2. Ler com pandas e extrair colunas
        df = pd.read_csv(temp_file)
        columns = ",\n  ".join([f"`{col}` string" for col in df.columns])

        # 3. Upload para S3 (em diretório)
        s3_path = f"uploaded-csvs/{table_name}/{table_name}.csv"
        s3 = boto3.client("s3", region_name=AWS_REGION)
        s3.upload_file(temp_file, S3_BUCKET, s3_path)

        # 4. Query de criação no Athena
        query = f"""
        CREATE EXTERNAL TABLE IF NOT EXISTS {ATHENA_DB}.{table_name} (
          {columns}
        )
        ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
        WITH SERDEPROPERTIES (
           'serialization.format' = ',',
           'field.delim' = ','
        )
        LOCATION 's3://{S3_BUCKET}/uploaded-csvs/{table_name}/'
        TBLPROPERTIES ('has_encrypted_data'='false');
        """

        athena = boto3.client("athena", region_name=AWS_REGION)
        create_database_if_not_exists(athena)

        response = athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={"Database": ATHENA_DB},
            ResultConfiguration={"OutputLocation": S3_OUTPUT},
        )

        # 5. Esperar execução da query
        execution_id = response["QueryExecutionId"]
        status = "RUNNING"
        while status in ["RUNNING", "QUEUED"]:
            result = athena.get_query_execution(QueryExecutionId=execution_id)
            status = result["QueryExecution"]["Status"]["State"]
            if status in ["FAILED", "CANCELLED"]:
                reason = result["QueryExecution"]["Status"].get("StateChangeReason", "Unknown")
                registrar_acao(user, "create_table", "failed")
                raise HTTPException(status_code=500, detail=f"Athena query falhou: {reason}")
            time.sleep(2)

        # 6. Log de sucesso
        registrar_acao(user, "create_table", "success")
        return {"message": "Tabela criada com sucesso!", "tabela": f"{ATHENA_DB}.{table_name}"}

    except Exception as e:
        import traceback
        traceback.print_exc()  # <- Adicione isso para mostrar o erro no terminal
        registrar_acao(user, "create_table", "failed")
        raise HTTPException(status_code=500, detail=str(e))
