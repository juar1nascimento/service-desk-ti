import sys
import urllib.parse
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# 1. Caso sua senha tenha caracteres especiais (como @, ç, #, !), 
# digite ela pura aqui que o urllib vai tratar automaticamente:
SENHA_PURAS = "Metahome@2026"  # 👈 Digite sua senha exata do Postgres aqui

senha_encoded = urllib.parse.quote_plus(SENHA_PURAS)

# 2. String de conexão formatada com client_encoding=utf8
DATABASE_URL = f"postgresql://postgres:{senha_encoded}@127.0.0.1:5432/service_desk"

def testar_conexao():
    print("🔄 Tentando conectar ao PostgreSQL...")
    
    try:
        # Força o driver psycopg2 a usar UTF-8 na comunicação
        engine = create_engine(
            DATABASE_URL, 
            connect_args={
                'connect_timeout': 5,
                'options': '-c client_encoding=utf8'
            }
        )
        
        with engine.connect() as connection:
            resultado = connection.execute(text("SELECT 1;"))
            if resultado.scalar() == 1:
                print("\n✅ SUCESSO: Conexão com o PostgreSQL realizada com sucesso!")
                print(f"📍 Banco de Dados: service_desk")
                print(f"📍 Endereço: 127.0.0.1:5432")
                
    except OperationalError as e:
        print("\n❌ ERRO DE CONEXÃO: Não foi possível conectar ao banco de dados.")
        print("Verifique se o serviço do PostgreSQL está rodando e se a senha está correta.")
        print(f"\nDetalhes do erro:\n{str(e).encode('utf-8', errors='ignore').decode('utf-8')}")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Ocorreu um erro: {str(e).encode('utf-8', errors='ignore').decode('utf-8')}")
        sys.exit(1)

if __name__ == "__main__":
    testar_conexao()