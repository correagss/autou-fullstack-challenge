import pytest
from unittest.mock import MagicMock, patch
from api.services.nlp_service import ContentAnalyzer


@pytest.fixture
def analyzer():
    return ContentAnalyzer()

def test_preprocess_text(analyzer: ContentAnalyzer):
    text = "Olá!!! Isso é um TESTE, certo?"
    processed = analyzer.preprocess_text(text)

    assert isinstance(processed, str)
    assert "test" in processed  # lematizado
    assert "olá" not in processed.lower()  # stopword removida


@patch("api.services.nlp_service.OpenAI")
def test_classify_email_produtivo(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Produtivo"))]

    mock_client.chat.completions.create.return_value = mock_response
    
    analyzer = ContentAnalyzer()

    result = analyzer.classify_email("Por favor, revise o documento.")

    assert result == "Produtivo"


@patch("api.services.nlp_service.OpenAI")
def test_classify_email_invalid_response_returns_default(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="banana"))]

    mock_client.chat.completions.create.return_value = mock_response

    analyzer = ContentAnalyzer()
    result = analyzer.classify_email("Texto irrelevante")

    assert result == "Improdutivo"

def test_generate_response_produtivo(analyzer: ContentAnalyzer):
    response = analyzer.generate_response("Produtivo")
    assert "analisando sua solicitação" in response

def test_generate_response_improdutivo(analyzer: ContentAnalyzer):
    response = analyzer.generate_response("Improdutivo")
    assert "Nenhuma ação é necessária" in response
