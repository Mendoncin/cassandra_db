import streamlit as st
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pandas as pd

CASSANDRA_HOSTS = ["host.docker.internal"]
KEYSPACE = "banco_cassandra"
USERNAME = "cassandra"
PASSWORD = "cassandra"

auth_provider = PlainTextAuthProvider(USERNAME, PASSWORD)
cluster = Cluster(CASSANDRA_HOSTS, auth_provider=auth_provider)
session = cluster.connect(KEYSPACE)

st.set_page_config(page_title="Consulta Alunos", layout="wide")
st.title("🔎 Consulta de Alunos - IF976")

busca_nome = st.text_input("Buscar por nome")
busca_matricula = st.text_input("Buscar por matrícula")
busca_status = st.selectbox("Status", ["", "Aprovado", "Reprovado"])

col1, col2, col3 = st.columns(3)
with col1:
    busca_media = st.number_input("Média mínima", min_value=0.0, max_value=10.0, step=0.1)
with col2:
    busca_prova = st.number_input("Nota da Prova", min_value=0.0, max_value=10.0, step=0.1)
with col3:
    busca_grupo = st.number_input("Grupo", min_value=0, step=1)

col4, col5, col6 = st.columns(3)
with col4:
    busca_projeto1 = st.number_input("Nota Projeto 1", min_value=0.0, max_value=10.0, step=0.1)
with col5:
    busca_projeto2 = st.number_input("Nota Projeto 2", min_value=0.0, max_value=10.0, step=0.1)
with col6:
    busca_seminario = st.number_input("Nota Seminário", min_value=0.0, max_value=10.0, step=0.1)

query = "SELECT * FROM IF976 ALLOW FILTERING"
try:
    rows = session.execute(query)
    dados = [row._asdict() for row in rows]
    df = pd.DataFrame(dados)

    if not df.empty:
        # Filtros aplicados no Pandas
        if busca_nome:
            df = df[df["nome"].str.contains(busca_nome, case=False, na=False)]
        if busca_matricula:
            df = df[df["matricula"].str.contains(busca_matricula, na=False)]
        if busca_status:
            df = df[df["status"] == busca_status]
        if busca_media > 0:
            df = df[df["media"] >= busca_media]
        if busca_prova > 0:
            df = df[df["prova"] >= busca_prova]
        if busca_grupo > 0:
            df = df[df["grupo"] == busca_grupo]
        if busca_projeto1 > 0:
            df = df[df["projeto1"] >= busca_projeto1]
        if busca_projeto2 > 0:
            df = df[df["projeto2"] >= busca_projeto2]
        if busca_seminario > 0:
            df = df[df["seminario"] >= busca_seminario]

        st.dataframe(df)
    else:
        st.info("Nenhum resultado encontrado.")
except Exception as e:
    st.error(f"Erro ao executar a consulta: {e}")
