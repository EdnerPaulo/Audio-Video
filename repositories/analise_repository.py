from typing import List, Optional
from sqlalchemy.orm import Session
from models.analise import AnaliseModel
from config.settings import logger

class AnaliseRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, analise: AnaliseModel) -> AnaliseModel:
        try:
            self.db.add(analise)
            self.db.commit()
            self.db.refresh(analise)
            return analise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao salvar análise no repositório: {e}")
            raise e

    def get_all(self) -> List[AnaliseModel]:
        return self.db.query(AnaliseModel).order_by(AnaliseModel.created_at.desc()).all()

    def delete(self, analise_id: int) -> bool:
        try:
            analise = self.db.query(AnaliseModel).filter(AnaliseModel.id == analise_id).first()
            if analise:
                self.db.delete(analise)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao deletar registro {analise_id}: {e}")
            raise e

    def update_transcricao(self, analise_id: int, transcricao: Optional[str]) -> bool:
        try:
            analise = self.db.query(AnaliseModel).filter(AnaliseModel.id == analise_id).first()
            if analise:
                analise.transcricao = transcricao
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao atualizar transcrição {analise_id}: {e}")
            raise e