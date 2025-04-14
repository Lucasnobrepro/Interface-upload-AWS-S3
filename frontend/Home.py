import streamlit as st

st.set_page_config(page_title="Home", layout="centered")
st.title("🏠 Página Inicial")

st.markdown("""
Este é um app com backend em **FastAPI** e frontend em **Streamlit**.

Use o menu lateral para:
- Fazer upload de arquivos CSV para o S3
""")
