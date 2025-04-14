import streamlit as st
import pandas as pd
from utils.api import create_table_api
from utils.logger import log_action

st.set_page_config(page_title="Criar Tabela Athena", layout="wide")
st.title("📊 Criar Tabela no Athena")

user = st.text_input("Nome do usuário", value="Lucas")

uploaded_file = st.file_uploader("Faça upload do CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Prévia do DataFrame")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    st.subheader("Renomear colunas")
    col_names = {}
    for col in edited_df.columns:
        new_name = st.text_input(f"Renomear '{col}'", value=col)
        col_names[col] = new_name
    renamed_df = edited_df.rename(columns=col_names)

    st.subheader("Nome da Tabela no Athena")
    table_name = st.text_input("Nome da tabela", max_chars=50)

    if st.button("🚀 Criar Tabela"):
        if not table_name:
            st.warning("Por favor, insira um nome para a tabela.")
        else:
            with st.spinner("Enviando para o backend..."):
                renamed_csv = renamed_df.to_csv(index=False)
                renamed_file = renamed_csv.encode("utf-8")
                class NamedBytesIO:
                    def __init__(self, content, name):
                        self.content = content
                        self.name = name
                    def getvalue(self): return self.content
                    @property
                    def name(self): return self._name
                    @name.setter
                    def name(self, value): self._name = value
                fake_file = NamedBytesIO(renamed_file, "uploaded.csv")
                try:
                    result = create_table_api(table_name, fake_file)
                    st.success(f"Tabela criada com sucesso: {result.get('message', '')}")
                    log_action(user, "create_table", "success")
                except Exception as e:
                    st.error(f"Erro ao criar tabela: {str(e)}")
                    log_action(user, "create_table", "error")
