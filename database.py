import os
import urllib.parse
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if "postgres" in st.secrets:
    db_config = st.secrets["postgres"]
    user = db_config["user"]
    password = urllib.parse.quote_plus(str(db_config["password"]))
    host = db_config["host"]
    port = db_config.get("port", 5432)
    dbname = db_config["dbname"]
    
    # Injeta obrigatoriamente a opção sslmode=require para bancos em nuvem (Neon/Render)
    DATABASE_URL = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}?sslmode=require"
else:
    # Conexão Local (Fallback)
    SENHA_POSTGRES = "Metahome@2026"
    senha_encoded = urllib.parse.quote_plus(SENHA_POSTGRES)
    DATABASE_URL = f"postgresql+psycopg://postgres:{senha_encoded}@127.0.0.1:5432/service_desk"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)