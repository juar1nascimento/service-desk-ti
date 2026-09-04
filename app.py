import streamlit as st
from database import engine
import models

# 1. Configuração das Páginas do Menu Lateral
page_registrar = st.Page(
    "pages/01_Registrar_Chamado.py", 
    title="Registrar Chamado", 
    icon="📋", 
    default=True
)

page_historico = st.Page(
    "pages/02_Historico_Chamados.py", 
    title="Consultar Histórico", 
    icon="🔎"
)

# 2. Montagem do Menu de Navegação
pg = st.navigation({
    "Menu Principal": [page_registrar, page_historico]
})

# 3. Configuração da Página e da Barra Lateral (Força a exibição aberta)
st.set_page_config(
    page_title="Service Desk TI",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 4. Inicialização do Banco de Dados
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    st.error("❌ Erro ao conectar ao banco de dados PostgreSQL:")
    st.code(str(e))
    st.stop()

# 5. Executa a tela selecionada no menu
pg.run()