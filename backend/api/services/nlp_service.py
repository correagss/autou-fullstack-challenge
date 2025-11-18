# backend/services/nlp_service.py
import os
import re
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from openai import OpenAI

load_dotenv()

class ContentAnalyzer:
    """
    Classe responsável por realizar:
    - Pré-processamento de texto (tokenização, limpeza, lematização)
    - Classificação de e-mails usando modelo GPT da OpenAI
    - Geração de respostas automáticas baseadas na categoria detectada
    """

    def __init__(self):
        """
        Inicializa cliente OpenAI e componentes do NLTK.
        """
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        if not OPENAI_API_KEY:
            raise ValueError("Chave da API da OpenAI (OPENAI_API_KEY) não foi encontrada.")

        self.client = OpenAI(api_key=OPENAI_API_KEY)

        try:
            self.stop_words = set(stopwords.words('portuguese') + stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
        except LookupError:
            print("ERRO: Pacotes NLTK não encontrados. Execute: nltk.download('all')")

    # -------------------------------------------------------------------------
    # PRÉ-PROCESSAMENTO
    # -------------------------------------------------------------------------
    def preprocess_text(self, text: str) -> str:
        """
        Realiza pré-processamento básico do texto:
        - Converte para minúsculas
        - Remove caracteres especiais
        - Tokeniza
        - Remove stop words
        - Lematiza tokens

        Args:
            text (str): Texto bruto do e-mail.

        Returns:
            str: Texto limpo e lematizado.
        """
        text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        tokens = word_tokenize(text)
        lemmatized = [
            self.lemmatizer.lemmatize(word)
            for word in tokens
            if word not in self.stop_words and len(word) > 2
        ]
        return " ".join(lemmatized)

    # -------------------------------------------------------------------------
    # CLASSIFICAÇÃO VIA OPENAI
    # -------------------------------------------------------------------------
    def classify_email(self, text: str) -> str:
        """
        Classifica um texto de e-mail como 'Produtivo' ou 'Improdutivo'
        usando o modelo GPT da OpenAI.

        A lógica é baseada em prompt engineering — o modelo responde apenas
        com a palavra da categoria e o método valida a resposta.

        Args:
            text (str): Texto do e-mail a ser analisado.

        Returns:
            str: 'Produtivo' ou 'Improdutivo'.

        Raises:
            Exception: Quando ocorre falha na chamada à API.
        """
        prompt = f"""
        Analise o seguinte texto de um e-mail e classifique-o como 'Produtivo' ou 'Improdutivo'.
        'Produtivo' significa que o e-mail requer uma ação ou resposta.
        'Improdutivo' significa que é um e-mail informativo, social ou que pode ser arquivado.
        Responda APENAS com a palavra 'Produtivo' ou 'Improdutivo'.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
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

    # -------------------------------------------------------------------------
    # RESPOSTA AUTOMÁTICA
    # -------------------------------------------------------------------------
    def generate_response(self, category: str) -> str:
        """
        Gera uma resposta automática baseada na categoria classificada.

        Args:
            category (str): 'Produtivo' ou 'Improdutivo'.

        Returns:
            str: Texto de resposta padrão.
        """
        if category == 'Produtivo':
            return (
                "Olá! Recebemos sua mensagem e já estamos analisando sua solicitação. "
                "Entraremos em contato em breve com mais informações. Atenciosamente."
            )
        else:
            return (
                "Obrigado por sua mensagem! Ela foi recebida e arquivada. "
                "Nenhuma ação é necessária no momento."
            )
