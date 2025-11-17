import io
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from main import app
from api.services.nlp_service import ContentAnalyzer


# ---------------------------------------------------------------------
# Fake que substitui o serviço real durante os testes
# ---------------------------------------------------------------------
class MockedAnalyzer:
    def preprocess_text(self, text: str) -> str:
        return "texto preprocessado"

    def classify_email(self, text: str) -> str:
        return "Produtivo"

    def generate_response(self, category: str) -> str:
        return "Resposta automática"


# ---------------------------------------------------------------------
# Fixture que sobrescreve o ContentAnalyzer via dependency_overrides
# ---------------------------------------------------------------------
@pytest.fixture
def mocked_analyzer():
    app.dependency_overrides[ContentAnalyzer] = lambda: MockedAnalyzer()
    yield
    app.dependency_overrides.pop(ContentAnalyzer, None)


# ---------------------------------------------------------------------
# Fixture do cliente de testes (DEVE depender do mock)
# ---------------------------------------------------------------------
@pytest.fixture
def client(mocked_analyzer):
    return TestClient(app)


# =============================================================================
# TESTE 1: Enviar TEXTO
# =============================================================================
def test_analyze_route_with_text(client: TestClient):
    response = client.post(
        "/api/analyze",
        data={"text": "Olá! Preciso de ajuda com o relatório."}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["category"] == "Produtivo"
    assert "Resposta automática" in data["suggestedResponse"]


# =============================================================================
# TESTE 2: Enviar TXT
# =============================================================================
def test_analyze_route_with_txt_file(client: TestClient):
    file_content = "Este é um email de teste.".encode("utf-8")

    response = client.post(
        "/api/analyze",
        files={"file": ("email.txt", file_content, "text/plain")}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["category"] == "Produtivo"
    assert "Resposta automática" in data["suggestedResponse"]


# =============================================================================
# TESTE 3: Enviar PDF (simulado)
# =============================================================================
@patch("api.routers.analyze.PdfReader")
def test_analyze_route_with_pdf_file(mock_pdf_reader, client: TestClient):
    # Mock da extração de texto do PDF
    mock_pdf_reader.return_value.pages = [
        MagicMock(extract_text=lambda: "Texto da página 1"),
        MagicMock(extract_text=lambda: "Texto da página 2"),
    ]

    fake_pdf_bytes = b"%PDF-1.4 Fake content"

    response = client.post(
        "/api/analyze",
        files={"file": ("email.pdf", fake_pdf_bytes, "application/pdf")}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["category"] == "Produtivo"
    assert "Resposta automática" in data["suggestedResponse"]


# =============================================================================
# TESTE 4: Nenhum conteúdo enviado
# =============================================================================
def test_analyze_route_without_text_or_file(client: TestClient):
    response = client.post("/api/analyze", data={})

    assert response.status_code == 400
    assert "Nenhum conteúdo enviado" in response.json()["detail"]


# =============================================================================
# TESTE 5: Conteúdo vazio
# =============================================================================
def test_analyze_route_empty_text(client: TestClient):
    response = client.post("/api/analyze", data={"text": "    "})

    assert response.status_code == 400
    assert "conteúdo do e-mail está vazio" in response.json()["detail"].lower()
