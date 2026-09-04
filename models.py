from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Chamado(Base):
    __tablename__ = "chamados"

    id = Column(Integer, primary_key=True, index=True)
    protocolo = Column(String(50), unique=True, index=True, nullable=False)
    nome_solicitante = Column(String(100), nullable=False)
    setor = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    telefone = Column(String(50), nullable=True)
    assunto = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=False)
    data_abertura = Column(DateTime, default=datetime.now)

    # Relação com a tabela de histórico
    historicos = relationship("Historico", back_populates="chamado", cascade="all, delete-orphan")

class Historico(Base):
    __tablename__ = "historico"

    id = Column(Integer, primary_key=True, index=True)
    chamado_id = Column(Integer, ForeignKey("chamados.id"), nullable=False)
    data_evento = Column(DateTime, default=datetime.now)
    evento = Column(String(100), nullable=False)
    observacao = Column(Text, nullable=True)

    # Relacionamento reverso
    chamado = relationship("Chamado", back_populates="historicos")