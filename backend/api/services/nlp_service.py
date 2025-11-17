# backend/services/nlp_service.py
import os
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Chave da API da OpenAI (OPENAI_API_KEY) não foi encontrada.")

class ContentAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        
        try:
            self.stop_words = set(stopwords.words('portuguese') + stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
        except LookupError:
            print("ERRO: Pacotes NLTK não encontrados.")

    # --- PRÉ-PROCESSAMENTO ---
    def preprocess_text(self, text: str) -> str:
        text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        tokens = word_tokenize(text)
        lemmatized = [self.lemmatizer.lemmatize(word) for word in tokens if word not in self.stop_words and len(word) > 2]
        return " ".join(lemmatized)

    # --- FUNÇÕES DE IA COM OPENAI ---
    def classify_email(self, text: str) -> str:
        """Classifica o texto usando o modelo GPT da OpenAI."""
        prompt = f"""
        Analise o seguinte texto de um e-mail e classifique-o como 'Produtivo' ou 'Improdutivo'.
        'Produtivo' significa que o e-mail requer uma ação ou resposta.
        'Improdutivo' significa que é um e-mail informativo, social ou que pode ser arquivado.
        Responda APENAS com a palavra 'Produtivo' ou 'Improdutivo'.

        Texto do E-mail:
        ---
        {text}
        ---
        Classificação:"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente de classificação de e-mails."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=5
            )
            category = response.choices[0].message.content.strip().capitalize()
            
            if category not in ['Produtivo', 'Improdutivo']:
                return 'Improdutivo'
                
            return category
            
        except Exception as e:
            raise Exception(f"Falha ao se comunicar com a API da OpenAI: {e}")

    def generate_response(self, category: str) -> str:
        """Gera uma resposta padrão com base na categoria."""
        if category == 'Produtivo':
            return "Olá! Recebemos sua mensagem e já estamos analisando sua solicitação. Entraremos em contato em breve com mais informações. Atenciosamente."
        else: 
            return "Obrigado por sua mensagem! Ela foi recebida e arquivada. Nenhuma ação é necessária no momento."
