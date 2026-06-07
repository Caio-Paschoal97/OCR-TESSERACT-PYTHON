import json
from google import genai
from google.genai import types
from core.config import GEMINI_API_KEY

# Inicializa o cliente com o SDK da Google
client = genai.Client(api_key=GEMINI_API_KEY)

def estruturar_dados_certificado(texto_ocr: str) -> dict:
    prompt = f"""
    Você é um assistente de extração de dados acadêmicos. 
    Leia o texto bruto de OCR de um certificado e extraia as informações essenciais.
    Retorne os dados APENAS no formato JSON exato abaixo. Não adicione crases nem formatação markdown.
    Se não encontrar um dado específico, retorne null.
    
    {{
        "nomeAlunoOcr": "nome completo do aluno",
        "nomeCursoOcr": "nome do curso, evento ou workshop",
        "cargaHorariaOcr": "apenas o número de horas",
        "dataConclusaoOcr": "DD/MM/AAAA"
    }}
    
    Texto bruto:
    {texto_ocr}
    """
    
    # chamada do SDK google-genai
    resposta = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    return json.loads(resposta.text)