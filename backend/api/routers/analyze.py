# backend/api/routers/analyze.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
from pypdf import PdfReader
from services import nlp_service

router = APIRouter()

class AnalysisResponse(BaseModel):
    category: str
    suggested_response: str

@router.post("/analyze", response_model=AnalysisResponse, tags=["Análise"])
async def analyze_email_route(text: Optional[str] = Form(None), file: Optional[UploadFile] = File(None)):
    email_content = ""
    if file:
        if file.content_type == 'text/plain':
            contents = await file.read()
            email_content = contents.decode('utf-8')
        elif file.content_type == 'application/pdf':
            try:
                reader = PdfReader(file.file)
                for page in reader.pages:
                    email_content += page.extract_text() or ""
            except Exception:
                raise HTTPException(status_code=400, detail="Erro ao ler o arquivo PDF.")
        else:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado (.txt ou .pdf).")
    elif text:
        email_content = text
    else:
        raise HTTPException(status_code=400, detail="Nenhum conteúdo enviado.")

    if not email_content.strip():
        raise HTTPException(status_code=400, detail="O conteúdo do e-mail está vazio.")

    try:
        # Ordem das tarefas do especialista:
        processed_text = nlp_service.preprocess_text(email_content)
        category = nlp_service.classify_email_via_api(processed_text)
        suggested_response = nlp_service.get_suggested_response(category)
        
        return AnalysisResponse(category=category, suggested_response=suggested_response)
    
    except Exception as e:
        # Se qualquer passo falhar, retorna um erro claro
        raise HTTPException(status_code=500, detail=str(e))