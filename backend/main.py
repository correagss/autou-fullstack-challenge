# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import analyze

app = FastAPI(title="API de Análise de E-mails")

origins = [
    "http://localhost:5173",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Usa as rotas da API
app.include_router(analyze.router, prefix="/api")

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "API de Análise de E-mails está no ar!"}