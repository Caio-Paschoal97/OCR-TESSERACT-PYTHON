# 1. Imagem base leve do Python
FROM python:3.11-slim

# 2. Impede interações no terminal que travam o deploy
ENV DEBIAN_FRONTEND=noninteractive

# 3. Instala o Tesseract e o idioma Português (CRÍTICO para o ocr_engine.py)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. Define a pasta de trabalho
WORKDIR /app

# 5. Instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia todo o código do AcadFlow
COPY . .

# 7. Expõe a porta padrão para uso local
EXPOSE 8000

# 8. Comando de inicialização inteligente para Nuvem e Local
# Ele usa a porta injetada pelo Render ($PORT) ou a 8000 se você rodar na sua máquina
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"