from fastapi import APIRouter, UploadFile, File, HTTPException
from services.ocr_engine import extrair_texto_de_arquivo
from services.gemini_parser import estruturar_dados_certificado

router = APIRouter()

@router.post("/ler-certificado")
async def ler_certificado(file: UploadFile = File(...)):
    try:
        # 1. Lê os bytes do arquivo
        conteudo = await file.read()
        
        # 2. Manda para o serviço de extração visual (Tesseract)
        texto_bruto = extrair_texto_de_arquivo(conteudo, file.filename)
        
        # 3. Manda para o serviço de inteligência (Gemini)
        dados_estruturados = estruturar_dados_certificado(texto_bruto)
        
        # 4. Devolve exatamente a estrutura que o PWA espera!
        return {
            "sucesso": True,
            "dadosOcr": dados_estruturados
        }
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(f"Erro na rota OCR: {str(e)}") 
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")