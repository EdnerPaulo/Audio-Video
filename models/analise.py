from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from database.connection import Base

class AnaliseModel(Base):
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    image_path = Column(String(500), nullable=False)
    descricao = Column(Text, nullable=True)
    objetos = Column(Text, nullable=True)
    quantidade_pessoas = Column(Integer, default=0)
    rostos = Column(Integer, default=0)
    idade = Column(String(50), nullable=True)
    emocao = Column(String(50), nullable=True)
    cores = Column(String(200), nullable=True)
    luminosidade = Column(String(50), nullable=True)
    nitidez = Column(String(50), nullable=True)
    transcricao = Column(Text, nullable=True)
    json_resultado = Column(JSON, nullable=True)