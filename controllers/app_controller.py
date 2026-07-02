import os
import uuid
from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from repositories.analise_repository import AnaliseRepository
from models.analise import AnaliseModel
from services.cv_service import CVService
from services.audio_service import AudioService
from config.settings import UPLOAD_FOLDER, logger

class AppController:
    def __init__(self):
        self.cv_service = CVService()
        self.audio_service = AudioService()

    def _get_repo(self, db: Session) -> AnaliseRepository:
        return AnaliseRepository(db)

    def processar_captura(self, image_bytes: bytes, audio_bytes: Optional[bytes] = None) -> Tuple[bool, str]:
        """Orquestra o salvamento físico, a execução do pipeline analítico e persistência de dados."""
        db = SessionLocal()
        repo = self._get_repo(db)
        try:
            # 1. Salvar arquivo físico da Imagem
            filename = f"cap_{uuid.uuid4().hex}.jpg"
            full_path = os.path.join(UPLOAD_FOLDER, filename)
            with open(full_path, "wb") as f:
                f.write(image_bytes)

            # 2. Executar Visão Computacional
            res_analise = self.cv_service.analisar_imagem(image_bytes)

            # 3. Processar áudio se fornecido no momento da captura
            transcricao_texto = ""
            if audio_bytes:
                audio_filename = f"audio_{uuid.uuid4().hex}.wav"
                audio_path = os.path.join(UPLOAD_FOLDER, audio_filename)
                with open(audio_path, "wb") as f:
                    f.write(audio_bytes)
                transcricao_texto = self.audio_service.transcrever(audio_path)
                # Remove o áudio temporário após transcrição
                if os.path.exists(audio_path):
                    os.remove(audio_path)

            # 4. Salvar no banco mapeado pelo ORM
            model_inst = AnaliseModel(
                image_path=full_path,
                descricao=res_analise["descricao"],
                objetos=res_analise["objetos"],
                quantidade_pessoas=res_analise["quantidade_pessoas"],
                rostos=res_analise["rostos"],
                idade=res_analise["idade"],
                emocao=res_analise["emocao"],
                cores=res_analise["cores"],
                luminosidade=res_analise["luminosidade"],
                nitidez=res_analise["nitidez"],
                transcricao=transcricao_texto,
                json_resultado=res_analise
            )
            repo.save(model_inst)
            return True, "Captura processada e arquivada com sucesso!"
        except Exception as e:
            logger.error(f"Falha operacional no fluxo do Controller: {e}")
            return False, f"Erro interno do servidor: {str(e)}"
        finally:
            db.close()

    def listar_historico(self) -> List[Dict[str, Any]]:
        db = SessionLocal()
        repo = self._get_repo(db)
        try:
            dados = repo.get_all()
            registros = []
            for d in dados:
                registros.append({
                    "id": d.id,
                    "created_at": d.created_at,
                    "image_path": d.image_path,
                    "descricao": d.descricao,
                    "objetos": d.objetos,
                    "quantidade_pessoas": d.quantidade_pessoas,
                    "rostos": d.rostos,
                    "idade": d.idade,
                    "emocao": d.emocao,
                    "cores": d.cores,
                    "luminosidade": d.luminosidade,
                    "nitidez": d.nitidez,
                    "transcricao": d.transcricao,
                    "json_resultado": d.json_resultado
                })
            return registros
        finally:
            db.close()

    def deletar_registro(self, analise_id: int) -> bool:
        db = SessionLocal()
        repo = self._get_repo(db)
        try:
            # Opcional: deletar arquivo físico associado
            analise = db.query(AnaliseModel).filter(AnaliseModel.id == analise_id).first()
            if analise and os.path.exists(analise.image_path):
                try:
                    os.remove(analise.image_path)
                except Exception as ex:
                    logger.error(f"Não foi possível remover arquivo físico: {ex}")
            return repo.delete(analise_id)
        finally:
            db.close()

    def gerenciar_audio_registro(self, analise_id: int, audio_bytes: Optional[bytes], acao: str) -> bool:
        db = SessionLocal()
        repo = self._get_repo(db)
        try:
            if acao == "vincular" and audio_bytes:
                audio_filename = f"audio_vinc_{uuid.uuid4().hex}.wav"
                audio_path = os.path.join(UPLOAD_FOLDER, audio_filename)
                with open(audio_path, "wb") as f:
                    f.write(audio_bytes)
                texto = self.audio_service.transcrever(audio_path)
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                return repo.update_transcricao(analise_id, texto)
            elif acao == "excluir":
                return repo.update_transcricao(analise_id, "")
            return False
        finally:
            db.close()