import io
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
from core.config import TESSERACT_CMD

# Configura o caminho do Tesseract no Windows
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def extrair_texto_de_arquivo(conteudo_bytes: bytes, nome_ficheiro: str) -> str:
    # Trata PDF
    if nome_ficheiro.lower().endswith('.pdf'):
        doc = fitz.open(stream=conteudo_bytes, filetype="pdf")
        if len(doc) == 0:
            raise ValueError("O documento PDF parece estar vazio.")
        
        pagina = doc.load_page(0)
        pix = pagina.get_pixmap(dpi=300)
        imagem = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # Trata Imagem (JPG, PNG)
    else:
        try:
            imagem = Image.open(io.BytesIO(conteudo_bytes))
        except Exception:
            raise ValueError("O ficheiro enviado não é uma imagem ou PDF válido.")

    # Extrai o texto
    texto_extraido = pytesseract.image_to_string(imagem, lang='por')
    
    if not texto_extraido.strip():
        raise ValueError("Não foi possível detetar nenhum texto legível no arquivo.")
        
    return texto_extraido