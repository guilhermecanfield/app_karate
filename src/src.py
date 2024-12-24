import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Text, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker
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

# Criar Model
class AtletasKata(Base):
    __tablename__='atletas_kata'
    chave = Column(Integer, autoincrement=True, primary_key=True)
    categoria = Column(Integer) 
    faixa = Column(String(100))
    idade = Column(String(100))
    atleta = Column(String(100))
    sexo = Column(String(20))
    estilo = Column(String(5))
    academia = Column(String(100))
    local = Column(String(12))

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
        Base.metadata.drop_all(bind=engine, tables=[AtletasKata.__table__])

        # Recriar a tabela
        Base.metadata.create_all(bind=engine)

        print("Tabela sobrescrita com sucesso!")
    except SQLAlchemyError as e:
        print(f"Erro ao sobrescrever tabela: {e}")

# Configurar a sessao do sqlalchemy
Session = sessionmaker(bind=engine)

# Função para inserir dados
def inserir_dados():
    sobrescrever_tabela()

    session = Session()
    try:
        # Ler o arquivo CSV
        df = pd.read_csv('df_completo.csv')
        df = df.fillna("Nao Informado")

        # Converter o DataFrame para uma lista de dicionários
        dados = df.to_dict(orient='records')

        # Criar objetos da classe SQLAlchemy e adicionar ao banco
        atletas = [
            AtletasKata(
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

# Executar a inserção
if engine:
    inserir_dados()