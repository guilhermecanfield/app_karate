import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from .src.etl import gera_dados
from .models.atletas_luta_kata import AtletasLutaKata, Base
import pandas as pd

# Carregar variáveis de ambiente
load_dotenv()

# Construir a URL do DB
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"

# Criar conexão
def get_engine():
    try:
        engine = create_engine(
            DATABASE_URL,
            pool_size=5,
            max_overflow=10,
            echo=True  # Adiciona logs SQL para debug
        )
        return engine
    except SQLAlchemyError as e:
        print(f"Erro ao criar engine: {e}")
        return None

# Obter engine e criar Session
engine = get_engine()
Session = sessionmaker(bind=engine)

def limpar_tabelas():
    """
    Remove todas as tabelas do banco de dados
    """
    try:
        Base.metadata.drop_all(bind=engine)
        print("Todas as tabelas foram removidas com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao remover as tabelas: {e}")
        return False

def setup_database():
    """
    Cria/recria a tabela no banco de dados
    """
    try:
        # Tenta dropar a tabela se ela existir
        Base.metadata.drop_all(bind=engine, tables=[AtletasLutaKata.__table__], checkfirst=True)
        
        # Cria a tabela
        Base.metadata.create_all(bind=engine, tables=[AtletasLutaKata.__table__])
        print("Tabela criada com sucesso!")
        return True
    except SQLAlchemyError as e:
        print(f"Erro ao configurar banco de dados: {e}")
        return False

def inserir_dados():
    """
    Insere dados na tabela AtletasLutaKata
    """
    session = Session()
    try:
        # Ler e preparar os dados
        df = gera_dados()
        
        # Inserir em lotes para melhor performance
        batch_size = 1000
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size]
            atletas = [
                AtletasLutaKata(
                    categoria=row['categoria'],
                    faixa=row['faixa'],
                    idade=row['idade'],
                    atleta=row['atleta'],
                    sexo=row['sexo'],
                    estilo=row['estilo'],
                    academia=row['academia'],
                    local=row['local']
                ) for _, row in batch.iterrows()
            ]
            
            session.bulk_save_objects(atletas)
            session.commit()
            print(f"Lote {i//batch_size + 1} inserido com sucesso!")
            
        print("Todos os dados foram inseridos com sucesso!")
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro ao inserir dados: {e}")
        return False
    finally:
        session.close()

def ler_dados():
    """
    Lê dados da tabela AtletasLutaKata e retorna um DataFrame pandas
    """
    session = Session()
    try:
        # Executar consulta na tabela AtletasLutaKata
        query = session.query(AtletasLutaKata)
        
        # Converter os resultados da consulta para uma lista de dicionários
        resultados = [
            {
                "categoria": row.categoria,
                "faixa": row.faixa,
                "idade": row.idade,
                "atleta": row.atleta,
                "sexo": row.sexo,
                "estilo": row.estilo,
                "academia": row.academia,
                "local": row.local
            }
            for row in query
        ]

        # Criar um DataFrame a partir dos resultados
        df = pd.DataFrame(resultados)
        print("Dados lidos com sucesso!")
        return df

    except SQLAlchemyError as e:
        print(f"Erro ao ler dados: {e}")
        return pd.DataFrame()  # Retornar um DataFrame vazio em caso de erro
    finally:
        session.close()

def mostrar_ajuda():
    """
    Mostra as opções disponíveis do script
    """
    print("\nUso: python conexao_db.py [comando]")
    print("\nComandos disponíveis:")
    print("  setup       - Cria/recria a tabela no banco de dados")
    print("  inserir     - Insere dados na tabela")
    print("  ler         - Lê e mostra os dados da tabela")
    print("  limpar      - Remove todas as tabelas do banco")
    print("  ajuda       - Mostra esta mensagem de ajuda")
    print("\nExemplo: python conexao_db.py inserir")

def main():
    if not engine:
        print("Não foi possível criar a conexão com o banco de dados")
        return

    # Se nenhum argumento foi fornecido ou se o argumento é 'ajuda'
    if len(sys.argv) < 2 or sys.argv[1] == 'ajuda':
        mostrar_ajuda()
        return

    comando = sys.argv[1].lower()
    
    if comando == 'setup':
        setup_database()
    elif comando == 'inserir':
        setup_database()  # Sempre recriar a tabela antes de inserir
        inserir_dados()
    elif comando == 'ler':
        df = ler_dados()
        if not df.empty:
            print("\nPrimeiras 5 linhas dos dados:")
            print(df.head())
            print(f"\nTotal de registros: {len(df)}")
    elif comando == 'limpar':
        limpar_tabelas()
    else:
        print(f"Comando '{comando}' não reconhecido")
        mostrar_ajuda()

if __name__ == "__main__":
    main()