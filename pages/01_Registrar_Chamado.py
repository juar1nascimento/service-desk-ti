import streamlit as st
from database import SessionLocal
from models import Chamado, Historico
from datetime import datetime

st.set_page_config(page_title="Registrar Chamado", page_icon="📋")

st.title("📋 Registrar Chamado")
st.markdown("---")

with st.form("form_novo_chamado"):
    nome = st.text_input("Nome do solicitante *")
    setor = st.text_input("Setor *")
    email = st.text_input("E-mail")
    telefone = st.text_input("Telefone")
    assunto = st.text_input("Assunto *")
    descricao = st.text_area("Descrição do atendimento *")

    submit = st.form_submit_button("REGISTRAR CHAMADO")

    if submit:
        if not nome or not setor or not assunto or not descricao:
            st.error("Por favor, preencha todos os campos obrigatórios marcados com (*).")
        else:
            db = SessionLocal()
            try:
                ano_atual = datetime.now().year
                
                # 1. Cria o chamado com um protocolo temporário
                novo_chamado = Chamado(
                    protocolo="GERANDO...", 
                    nome_solicitante=nome,
                    setor=setor,
                    email=email,
                    telefone=telefone,
                    assunto=assunto,
                    descricao=descricao
                )
                db.add(novo_chamado)
                db.flush() # Envia para o banco para gerar o ID sequencial (sem commitar)

                # 2. Atualiza o protocolo com o ID real no formato SD-2026-000001
                novo_chamado.protocolo = f"SD-{ano_atual}-{novo_chamado.id:06d}"
                
                # 3. Insere automaticamente o primeiro registro no histórico
                historico_inicial = Historico(
                    chamado_id=novo_chamado.id,
                    evento="Chamado registrado",
                    observacao="Abertura inicial do chamado registrada pelo usuário via sistema."
                )
                db.add(historico_inicial)
                
                # Confirma a transação
                db.commit()
                
                st.success("CHAMADO REGISTRADO COM SUCESSO")
                st.info(f"**Protocolo:** {novo_chamado.protocolo}\n\n**Data:** {novo_chamado.data_abertura.strftime('%d/%m/%Y %H:%M')}\n\n*Guarde este protocolo para consulta.*")
                
            except Exception as e:
                db.rollback()
                st.error(f"Ocorreu um erro ao registrar o chamado: {e}")
            finally:
                db.close()