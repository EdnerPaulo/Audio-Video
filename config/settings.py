import os
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = os.getenv("DATABASE_URL")
UPLOAD_FOLDER = Path(os.getenv("UPLOAD_FOLDER", "assets/images"))
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")

# Garantir diretórios estruturais
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
(BASE_DIR / "logs").mkdir(parents=True, exist_ok=True)

# Configuração de Log Avançada
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(BASE_DIR / "logs" / "app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("CV_App")