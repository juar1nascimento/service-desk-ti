import streamlit as st
from database import SessionLocal
from models import Chamado, Historico
import pandas as pd

st.set_page_config(page_title="Histórico de Chamados", page_icon="🔎", layout="wide")

st.title("🔎 Histórico de Chamados")
st.markdown("---")

db = SessionLocal()

# Filtros simples de pesquisa
col1, col2 = st.columns(2)
with col1:
    filtro_protocolo = st.text_input("Pesquisar por Protocolo (Ex: SD-2026-000001):")
with col2:
    filtro_nome = st.text_input("Pesquisar por Nome do Solicitante:")

# Montagem da Query com base nos filtros
query = db.query(Chamado)
if filtro_protocolo:
    query = query.filter(Chamado.protocolo.ilike(f"%{filtro_protocolo}%"))
if filtro_nome:
    query = query.filter(Chamado.nome_solicitante.ilike(f"%{filtro_nome}%"))

chamados = query.order_by(Chamado.data_abertura.desc()).all()

if not chamados:
    st.warning("Nenhum chamado encontrado.")
else:
    # Preparando dados para exibição no Streamlit Dataframe
    dados = []
    for c in chamados:
        dados.append({
            "PROTOCOLO": c.protocolo,
            "SOLICITANTE": c.nome_solicitante,
            "ASSUNTO": c.assunto,
            "DATA": c.data_abertura.strftime("%d/%m/%Y")
        })
    
    df = pd.DataFrame(dados)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("### 👁️ Visualizar Detalhes do Chamado")
    chamado_selecionado = st.selectbox("Selecione o protocolo para expandir:", [""] + df["PROTOCOLO"].tolist())

    if chamado_selecionado:
        detalhe = db.query(Chamado).filter(Chamado.protocolo == chamado_selecionado).first()
        
        st.markdown(f"#### CHAMADO: {detalhe.protocolo}")
        
        col_det1, col_det2 = st.columns(2)
        with col_det1:
            st.write(f"**Solicitante:** {detalhe.nome_solicitante}")
            st.write(f"**Setor:** {detalhe.setor}")
            st.write(f"**E-mail:** {detalhe.email or 'N/A'}")
            st.write(f"**Telefone:** {detalhe.telefone or 'N/A'}")
        with col_det2:
            st.write(f"**Data do Registro:** {detalhe.data_abertura.strftime('%d/%m/%Y %H:%M:%S')}")
            st.write(f"**Assunto:** {detalhe.assunto}")
        
        st.write("**Descrição:**")
        st.text_area("Descrição (Apenas Leitura)", detalhe.descricao, disabled=True, label_visibility="collapsed")
        
        # Histórico de Eventos
        st.markdown("---")
        st.markdown("#### 📜 Histórico de Eventos")
        historicos = db.query(Historico).filter(Historico.chamado_id == detalhe.id).order_by(Historico.data_evento.asc()).all()
        
        for h in historicos:
            st.markdown(f"**{h.data_evento.strftime('%d/%m/%Y %H:%M')}** - {h.evento}")
            if h.observacao:
                st.caption(f"↳ {h.observacao}")

db.close()