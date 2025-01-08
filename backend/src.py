import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

from src.etl import gera_dados
from models.atletas_luta_kata import AtletasLutaKata

import pandas as pd

# Carregar variáveis de ambiente
load_dotenv()

# Construir a URL do DB
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"

Base = declarative_base()

# Criar conexão
def get_engine():
    try:
        engine = create_engine(DATABASE_URL)
        return engine
    except SQLAlchemyError as e:
        print(e)
        return None
    
# Obter instância da engine e criar tabela se não existir
engine = get_engine()

def sobrescrever_tabela():
    try:
        # Remover a tabela existente
        Base.metadata.drop_all(bind=engine, tables=[AtletasLutaKata.__table__])

        # Recriar a tabela
        Base.metadata.create_all(bind=engine)

        print("Tabela sobrescrita com sucesso!")
    except SQLAlchemyError as e:
        print(f"Erro ao sobrescrever tabela: {e}")

# Configurar a sessao do sqlalchemy
Session = sessionmaker(bind=engine)

# Função para inserir dados
def inserir_dados():
    """
    Insere dados na tabela AtletasLutaKata.
    """
    sobrescrever_tabela()

    session = Session()
    try:
        # Ler o arquivo CSV
        df = gera_dados()

        # Converter o DataFrame para uma lista de dicionários
        dados = df.to_dict(orient='records')

        # Criar objetos da classe SQLAlchemy e adicionar ao banco
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
            ) for row in dados
        ]

        session.add_all(atletas)

        # Confirmar as alterações
        session.commit()
        print("Dados inseridos com sucesso!")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro ao inserir dados: {e}")
    finally:
        session.close()

def ler_dados():
    """
    Lê dados da tabela AtletasLutaKata e retorna um DataFrame pandas.
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