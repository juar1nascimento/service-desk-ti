import streamlit as st
from database import engine
import models

st.set_page_config(
    page_title="Service Desk TI",
    page_icon="🛠️",
    layout="centered"
)

# Cria as tabelas chamados e historico no PostgreSQL caso ainda não existam
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    st.error("❌ Erro ao conectar ao banco de dados PostgreSQL:")
    st.code(str(e))
    st.info("Verifique se o banco de dados 'service_desk' foi criado no pgAdmin e se o serviço PostgreSQL está ativo.")
    st.stop()

st.title("🛠️ SERVICE DESK TI")
st.markdown("---")

st.write("Bem-vindo ao **Sistema de Registro de Atendimento Service Desk GTI SESA**.")
st.write("Utilize o menu lateral para navegar entre as opções:")

st.write("📋 **Registrar Chamado:** Para abrir novas solicitações de suporte.")
st.write("🔎 **Consultar Histórico:** Para pesquisar e acompanhar chamados existentes.")