# backend/services/nlp_service.py
import os
import re
import requests
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Configuração
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("Token do Hugging Face (HF_TOKEN) não foi encontrado. ")

try:
    stop_words = set(stopwords.words("portuguese") + stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
except LookupError:
    print("ERRO: Pacotes NLTK não encontrados. Rode o script de download.")
    exit()

MODEL = "facebook/bart-large-mnli"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}


# Funções 
def preprocess_text(text: str) -> str:
    text = re.sub(r"[^a-zA-Z\s]", "", text.lower())
    tokens = word_tokenize(text)
    lemmatized = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and len(word) > 2]
    return " ".join(lemmatized)

def classify_email_via_api(text: str) -> str:
    # Chamando a API
    payload = {
        "inputs": text,
        "parameters": {"candidate_labels": ["Produtivo", "Improdutivo"], "options": {"wait_for_model": True}},
    }
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status() 
        data = response.json()
        return data["labels"][0]
    except Exception as e:
        raise Exception(f"Falha na API de classificação: {e}")


# Retorna uma resposta padrão
def get_suggested_response(category: str) -> str:

    if category == "Produtivo":
        return "Olá! Recebemos sua mensagem e já estamos analisando sua solicitação. Entraremos em contato em breve. Atenciosamente."
    else:
        return "Obrigado por sua mensagem! Ela foi recebida e arquivada. Nenhuma ação é necessária no momento."