from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.rotas import router

app = FastAPI(
    title="Microsserviço de OCR - AcadFlow",
    description="Extração de dados de certificados utilizando Tesseract e Gemini",
    version="1.0.0"
)

# Configuração do CORS (Libera acesso do Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, substitua "*" pela URL do seu PWA
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas
app.include_router(router)

@app.get("/")
def root():
    return {"status": "Microsserviço de OCR AcadFlow está online!"}