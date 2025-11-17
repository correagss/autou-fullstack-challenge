from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from pypdf import PdfReader

from api.services import nlp_service
from api.models.analyze import AnalysisResponse

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse, tags=["Análise"])
async def analyze_email_route(text: Optional[str] = Form(None), file: Optional[UploadFile] = File(None)):
    email_content = ""
    if file:
        if file.content_type == 'text/plain':
            contents = await file.read()
            email_content = contents.decode('utf-8', errors='ignore')
        elif file.content_type == 'application/pdf':
            try:
                reader = PdfReader(file.file)
                email_content = " ".join([page.extract_text() or "" for page in reader.pages])
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Erro ao ler o arquivo PDF: {e}")
        else:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado (.txt ou .pdf).")
    elif text:
        email_content = text
    else:
        raise HTTPException(status_code=400, detail="Nenhum conteúdo enviado.")

    if not email_content.strip():
        raise HTTPException(status_code=400, detail="O conteúdo do e-mail está vazio.")
    
    try:
        processed_text = nlp_service.preprocess_text(email_content)
        category = nlp_service.classify_email(processed_text)
        
        # --- A CHAMADA CORRETA ---
        suggested_response = nlp_service.generate_response(category=category)
        
        return AnalysisResponse(category=category, suggested_response=suggested_response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))