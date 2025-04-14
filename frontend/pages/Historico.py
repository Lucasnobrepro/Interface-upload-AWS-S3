import streamlit as st
import boto3
import pandas as pd
import os
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

# Configurações
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
CSV_PATH = os.getenv("HISTORICO_CSV_PATH", "logs/historico_acoes.csv")

# Cliente boto3
s3 = boto3.client("s3", region_name=AWS_REGION)

def carregar_csv_s3():
    try:
        response = s3.get_object(Bucket=S3_BUCKET, Key=CSV_PATH)
        content = response["Body"].read().decode("utf-8")
        df = pd.read_csv(StringIO(content))
        return df
    except Exception as e:
        st.error(f"Erro ao carregar histórico Streamlit: {e}")
        return pd.DataFrame(columns=["user", "action", "data", "status_operation", "object"])

def main():
    st.set_page_config(page_title="Histórico de Ações", layout="wide")
    st.title("📋 Histórico de Ações")

    df = carregar_csv_s3()

    if df.empty:
        st.warning("Nenhuma ação registrada ainda.")
        return

    # Filtros
    users = df["user"].dropna().unique().tolist()
    actions = df["action"].dropna().unique().tolist()

    col1, col2 = st.columns(2)
    filtro_user = col1.selectbox("Filtrar por usuário", ["Todos"] + users)
    filtro_action = col2.selectbox("Filtrar por ação", ["Todos"] + actions)

    if filtro_user != "Todos":
        df = df[df["user"] == filtro_user]

    if filtro_action != "Todos":
        df = df[df["action"] == filtro_action]

    st.dataframe(df.sort_values("data", ascending=False), use_container_width=True)

if __name__ == "__main__":
    main()
