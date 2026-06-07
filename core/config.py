import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TESSERACT_CMD = os.getenv("TESSERACT_CMD")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY não encontrada. Verifique o ficheiro .env")