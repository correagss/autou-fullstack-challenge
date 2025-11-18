# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import analyze
from api.routers import home

app = FastAPI(title="API de Análise de E-mails")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Usa as rotas da API
app.include_router(analyze.router   , prefix="/api")
app.include_router(home.router      , prefix="")


