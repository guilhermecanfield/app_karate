from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Criar Model
class AtletasLutaKata(Base):
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
