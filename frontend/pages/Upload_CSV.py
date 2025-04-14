import streamlit as st
st.set_page_config(page_title="Upload de CSV", page_icon="📄")

from utils.api import upload_csv

st.title("📤 Upload CSV para o S3")

user = st.text_input("Nome do usuário", value="Lucas")
file = st.file_uploader("Selecione o arquivo CSV", type=["csv"])

if file and st.button("Enviar"):
    with st.spinner("Enviando..."):
        response = upload_csv(file, user)
        if response:
            st.success("Arquivo enviado com sucesso!")
            st.markdown(f"[🔗 Acesse o arquivo no S3]({response['url']})")
        else:
            st.error("Erro no upload.")
