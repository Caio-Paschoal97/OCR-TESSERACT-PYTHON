# OCR Tesseract Python — Microserviço AcadFlow

Microserviço de extração de dados de certificados do sistema **AcadFlow**.  
Recebe uma imagem ou PDF de certificado, extrai o texto com **Tesseract OCR** e usa a **API Gemini** para estruturar os dados em JSON.

Desenvolvido com **FastAPI + Python** e hospedado no Render como parte do Projeto Integrador do curso de Desenvolvimento Mobile no SENAC.

link do render : https://ocr-tesseract-python.onrender.com
---

## Sobre o projeto

O microserviço expõe um único endpoint REST que recebe o arquivo do certificado (imagem JPG/PNG ou PDF), realiza a leitura do texto via Tesseract em português e envia esse texto para o modelo **Gemini 2.5 Flash** da Google, que retorna um JSON estruturado com os dados do certificado prontos para uso no app mobile.

---

## Como funciona

```
App mobile (React Native)
        │
        │  POST /ler-certificado  (multipart/form-data)
        ▼
┌─────────────────────────────┐
│         FastAPI (rotas.py)  │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│  ocr_engine.py              │
│  Tesseract OCR (lang=por)   │
│  Suporte: JPG, PNG, PDF     │
│  PDF → PyMuPDF → imagem     │
│         → pytesseract       │
└────────────┬────────────────┘
             │ texto bruto
             ▼
┌─────────────────────────────┐
│  gemini_parser.py           │
│  Gemini 2.5 Flash           │
│  Prompt → JSON estruturado  │
└────────────┬────────────────┘
             │
             ▼
     { sucesso: true, dadosOcr: { ... } }
```

---

## Tecnologias e dependências

| Pacote | Uso |
|---|---|
| `fastapi` | Framework web / API REST |
| `uvicorn` | Servidor ASGI |
| `pytesseract` | Interface Python para o Tesseract OCR |
| `Pillow` | Manipulação de imagens |
| `pymupdf` | Rasterização de PDFs (biblioteca `fitz`) |
| `google-genai` | SDK oficial do Google para Gemini |
| `python-dotenv` | Leitura de variáveis de ambiente do `.env` |
| `python-multipart` | Suporte a upload de arquivos no FastAPI |

**Sistema — instalado via Docker:**

| Pacote | Uso |
|---|---|
| `tesseract-ocr` | Engine de OCR |
| `tesseract-ocr-por` | Pack de idioma Português para o Tesseract |

---

## Pré-requisitos

**Para rodar localmente sem Docker:**

- Python 3.11+
- Tesseract OCR instalado no sistema
  - Windows: [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
  - Linux: `sudo apt install tesseract-ocr tesseract-ocr-por`
  - macOS: `brew install tesseract tesseract-lang`
- Chave de API do Google Gemini

**Para rodar com Docker:**

- Docker instalado (a instalação do Tesseract é feita automaticamente pelo Dockerfile)

---

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Chave da API do Google Gemini (obrigatória)
GEMINI_API_KEY=sua_chave_aqui

# Caminho do executável do Tesseract (necessário apenas no Windows)
# Exemplo: C:\Program Files\Tesseract-OCR\tesseract.exe
TESSERACT_CMD=
```

> O `.env` está no `.gitignore` e nunca deve ser commitado.  
> No Render, configure essas variáveis direto no painel de Environment Variables.

---

## Instalação e execução local

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/OCR-TESSERACT-PYTHON.git
cd OCR-TESSERACT-PYTHON

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure o .env
cp .env.example .env
# edite o .env com sua GEMINI_API_KEY

# Inicie o servidor
uvicorn main:app --reload --port 8000
```

A API estará disponível em `http://localhost:8000`.  
A documentação interativa (Swagger) estará em `http://localhost:8000/docs`.

---

## Execução com Docker

```bash
# Build da imagem
docker build -t ocr-acadflow .

# Execução passando a chave via variável de ambiente
docker run -p 8000:8000 -e GEMINI_API_KEY=sua_chave_aqui ocr-acadflow
```

O Dockerfile instala automaticamente o `tesseract-ocr` e o pacote de idioma `tesseract-ocr-por`, então não é necessário nenhuma instalação manual no host.

---

## Estrutura de pastas

```
OCR-TESSERACT-PYTHON/
├── main.py                  # Entry point — cria o app FastAPI, configura CORS e registra rotas
├── requirements.txt         # Dependências Python
├── Dockerfile               # Imagem Docker com Tesseract embutido
├── .gitignore
├── api/
│   └── rotas.py             # Define o endpoint POST /ler-certificado
├── core/
│   └── config.py            # Lê variáveis de ambiente (GEMINI_API_KEY, TESSERACT_CMD)
└── services/
    ├── ocr_engine.py        # Extração de texto com Tesseract (imagem e PDF)
    └── gemini_parser.py     # Estruturação dos dados com Gemini 2.5 Flash
```

---

## Endpoint

### `POST /ler-certificado`

Recebe o arquivo do certificado e retorna os dados extraídos estruturados.

**Content-Type:** `multipart/form-data`

**Campo do formulário:**

| Campo | Tipo | Descrição |
|---|---|---|
| `file` | `UploadFile` | Arquivo do certificado (JPG, PNG ou PDF) |

**Resposta de sucesso — `200 OK`:**

```json
{
  "sucesso": true,
  "dadosOcr": {
    "nomeAlunoOcr": "João da Silva",
    "nomeCursoOcr": "Workshop de Desenvolvimento Web",
    "cargaHorariaOcr": "40",
    "dataConclusaoOcr": "15/05/2025"
  }
}
```

> Campos não encontrados no certificado são retornados como `null`.

**Respostas de erro:**

| Status | Situação |
|---|---|
| `400` | Arquivo inválido, PDF vazio ou nenhum texto detectável |
| `500` | Erro interno (Tesseract, Gemini ou parsing do JSON) |

**Exemplo com curl:**

```bash
curl -X POST https://ocr-tesseract-python.onrender.com/ler-certificado \
  -F "file=@certificado.jpg"
```

---

### `GET /`

Health check — confirma que o serviço está online.

**Resposta:**
```json
{ "status": "Microsserviço de OCR AcadFlow está online!" }
```

---

## Módulos internos

### `main.py`

Inicializa o app FastAPI com título, descrição e versão. Configura o middleware CORS com `allow_origins=["*"]` (em produção, substituir pelo domínio do frontend). Registra o router de `api/rotas.py`.

---

### `core/config.py`

Carrega as variáveis de ambiente via `python-dotenv`. Lança `ValueError` na inicialização se `GEMINI_API_KEY` não estiver definida, impedindo o serviço de subir sem configuração.

---

### `api/rotas.py`

Define o único endpoint do serviço (`POST /ler-certificado`). Coordena as duas etapas do pipeline:

1. Chama `ocr_engine.extrair_texto_de_arquivo` com os bytes e o nome do arquivo
2. Chama `gemini_parser.estruturar_dados_certificado` com o texto bruto retornado
3. Devolve `{ sucesso, dadosOcr }` ou levanta `HTTPException` em caso de erro

---

### `services/ocr_engine.py`

Responsável pela extração de texto puro do arquivo recebido.

**Fluxo:**
- Se o arquivo for **PDF**: usa PyMuPDF (`fitz`) para abrir a primeira página, rasteriza em imagem com DPI 300 e converte para objeto `PIL.Image`
- Se for **imagem** (JPG, PNG, etc.): abre diretamente com `PIL.Image.open`
- Executa `pytesseract.image_to_string` com `lang='por'` (português)
- Lança `ValueError` se nenhum texto for detectado

> No Windows, o caminho do executável do Tesseract é configurado via `TESSERACT_CMD`. No Docker/Linux, o Tesseract está no PATH e essa variável pode ficar vazia.

---

### `services/gemini_parser.py`

Responsável por transformar o texto bruto do OCR em dados estruturados.

**Fluxo:**
- Monta um prompt instruindo o modelo a extrair apenas os quatro campos do certificado
- Chama `client.models.generate_content` com o modelo `gemini-2.5-flash` e `response_mime_type="application/json"` para garantir saída JSON pura
- Faz `json.loads` na resposta e retorna o dicionário

**Schema retornado pelo Gemini:**

```json
{
  "nomeAlunoOcr": "string | null",
  "nomeCursoOcr": "string | null",
  "cargaHorariaOcr": "string | null",
  "dataConclusaoOcr": "string | null"
}
```

---

## Deploy no Render

O projeto está configurado para deploy automático no Render via Docker.

**Configurações necessárias no painel do Render:**

| Campo | Valor |
|---|---|
| Environment | Docker |
| Dockerfile Path | `./Dockerfile` |
| Port | `8000` (o Dockerfile usa `${PORT:-8000}`) |

**Environment Variables:**

| Variável | Descrição |
|---|---|
| `GEMINI_API_KEY` | Chave da API do Google Gemini |
| `TESSERACT_CMD` | Deixar vazio (Tesseract está no PATH no container) |

O comando de inicialização no Dockerfile já lida com a porta dinâmica do Render:

```dockerfile
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"
```

---

## Observações

- O serviço está no **plano gratuito do Render**, que hiberna instâncias após inatividade. A primeira requisição após hibernação pode levar até 30 segundos. O app mobile já trata isso com retry automático (3 tentativas, 5 segundos de espera entre elas).
- O CORS está configurado com `allow_origins=["*"]`. Para produção, substituir pelo domínio real do frontend no `main.py`.
- Apenas a **primeira página** do PDF é processada.
- O Tesseract está configurado para reconhecimento em **português** (`lang='por'`). Certificados em outros idiomas podem ter qualidade de extração reduzida.
- A documentação Swagger gerada automaticamente pelo FastAPI fica disponível em `/docs` e pode ser usada para testar o endpoint diretamente pelo navegador.

- ## Equipe

Projeto Integrador — Turma de Desenvolvimento Mobile, SENAC  
Professor: Geraldo Gomes

| Nome |
|---|
| André Costa |
| Caio Victor |
| Leticia |
| Luciana |
| Priscila |
