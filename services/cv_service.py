import cv2
import numpy as np
import os
from PIL import Image
from datetime import datetime
from typing import Dict, Any
from config.settings import logger

class CVService:
    def __init__(self):
        try:
            # Solução de contorno para o bug de carregamento no ambiente headless do Linux/Render
            # Força o Python a mapear e carregar explicitamente o construtor do classificador
            from cv2 import CascadeClassifier
            
            caminho_xml = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
            self.face_cascade = CascadeClassifier(caminho_xml)
            
            # Validação de segurança para garantir que o arquivo XML foi aberto com sucesso
            if self.face_cascade.empty():
                raise FileNotFoundError("Não foi possível inicializar o arquivo xml do Haar Cascade.")
                
        except (AttributeError, ImportError):
            # Fallback caso a importação direta falhe
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def analisar_imagem(self, image_bytes: bytes) -> Dict[str, Any]:
        """Executa processamento estatístico e analítico nativo na imagem capturada."""
        try:
            # Converter bytes para imagem OpenCV
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Não foi possível decodificar os bytes da imagem.")

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            height, width, _ = img.shape

            # 1. Análise de Luminosidade
            mean_brightness = np.mean(gray)
            if mean_brightness < 60:
                luminosidade = "Baixa (Escuro)"
            elif mean_brightness > 190:
                luminosidade = "Alta (Superexposto)"
            else:
                luminosidade = "Ideal (Normal)"

            # 2. Análise de Nitidez (Variância do Laplaciano)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            nitidez = "Excelente" if laplacian_var > 100 else ("Boa" if laplacian_var > 40 else "Baixa/Borrada")

            # 3. Detecção de Faces Nativas
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            num_faces = len(faces)

            # 4. Cores Predominantes (Cálculo dos canais de cores médios)
            avg_b, avg_g, avg_r = np.mean(img, axis=(0, 1))
            cores_predominantes = f"R: {int(avg_r)}, G: {int(avg_g)}, B: {int(avg_b)}"

            # 5. Pipeline Extensível estruturado
            agora = datetime.now()
            
            resultado = {
                "descricao": f"Imagem capturada localmente com resolução {width}x{height} pixels.",
                "objetos": "Análise estatística local realizada (Filtros Prontos para IA Externa)",
                "quantidade_pessoas": num_faces, # Faces correlacionadas a pessoas
                "rostos": num_faces,
                "idade": "Não Disponível (Requer Modelo Avançado)",
                "emocao": "Não Disponível (Requer Modelo Avançado)",
                "cores": cores_predominantes,
                "luminosidade": f"{luminosidade} (Média: {mean_brightness:.1f})",
                "nitidez": f"{nitidez} (Score: {laplacian_var:.1f})",
                "resolucao": f"{width}x{height}",
                "data": agora.strftime("%d/%m/%Y"),
                "horario": agora.strftime("%H:%M:%S")
            }
            return resultado

        except Exception as e:
            logger.error(f"Erro no pipeline de Visão Computacional: {str(e)}")
            raise e
