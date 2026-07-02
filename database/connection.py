from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import DATABASE_URL, logger

if not DATABASE_URL:
    logger.error("DATABASE_URL não configurada no ambiente.")
    raise ValueError("A variável DATABASE_URL é obrigatória.")

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db() -> None:
    """Cria as tabelas no banco de dados se não existirem."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Banco de dados inicializado/verificado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao inicializar o banco de dados: {str(e)}")
        raise e
        