import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Senha configurada para a sua conexão
SENHA_POSTGRES = "Metahome@2026"

# Converte caracteres especiais da senha (como @) para um formato seguro em URLs
senha_encoded = urllib.parse.quote_plus(SENHA_POSTGRES)

# String de conexão usando o driver psycopg 3 (postgresql+psycopg://)
DATABASE_URL = f"postgresql+psycopg://postgres:{senha_encoded}@127.0.0.1:5432/service_desk"

# Cria a engine de conexão com timeout de 10 segundos
engine = create_engine(
    DATABASE_URL,
    connect_args={
        'connect_timeout': 10
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)