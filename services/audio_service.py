import os
from typing import Optional
from faster_whisper import WhisperModel
from config.settings import logger

class AudioService:
    def __init__(self):
        # Utiliza o modelo 'tiny' otimizado para CPU, ideal para a camada gratuita do Render
        # O download ocorre em memória apenas na primeira chamada se não mapeado em cache
        self.model_size = "tiny"
        self._model = None

    @property
    def model(self):
        if self._model is None:
            logger.info("Carregando o modelo Faster-Whisper...")
            # Força o uso de CPU para compatibilidade com Render Gratuito
            self._model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
        return self._model

    def transcrever(self, audio_path: str) -> Optional[str]:
        """Transcreve arquivos de áudio locais de forma assíncrona/síncrona para texto."""
        if not os.path.exists(audio_path):
            logger.warning(f"Arquivo de áudio não encontrado: {audio_path}")
            return None
        try:
            logger.info(f"Iniciando transcrição do arquivo: {audio_path}")
            segments, info = self.model.transcribe(audio_path, beam_size=1)
            textos = [segment.text for segment in segments]
            transcricao_completa = " ".join(textos).strip()
            logger.info("Transcrição concluída com sucesso.")
            return transcricao_completa if transcricao_completa else "Áudio em branco ou incompreensível."
        except Exception as e:
            logger.error(f"Falha na transcrição do áudio: {str(e)}")
            return f"Erro na transcrição: {str(e)}"