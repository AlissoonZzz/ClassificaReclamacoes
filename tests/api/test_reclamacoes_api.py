from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from app.main import app
from app.domain.models import Reclamacao, Canal, Status
from app.core.config import API_KEY

# Define o cabeçalho com a chave de API correta para os testes
headers = {"X-API-Key": API_KEY}

client = TestClient(app)

def test_criar_reclamacao_endpoint():
    """Testa o endpoint de criação de reclamação (POST /api/v1/reclamacoes/)."""
    with patch("app.api.v1.endpoints.reclamacoes.RabbitMQQueue") as MockRabbitMQQueue:
        mock_queue_instance = MockRabbitMQQueue.return_value
        test_payload = {"texto": "meu app deu erro", "canal": "digital"}
        
        # Envia a requisição com o cabeçalho de autenticação
        response = client.post("/api/v1/reclamacoes/", json=test_payload, headers=headers)
        
        assert response.status_code == 202
        assert response.json() == {"message": "Reclamação recebida e enfileirada para processamento."}
        mock_queue_instance.publish.assert_called_once_with({"texto": "meu app deu erro", "canal": "digital"})

def test_listar_reclamacoes_endpoint():
    """Testa o endpoint que lista as reclamações (GET /api/v1/reclamacoes/)."""
    mock_reclamacao = Reclamacao(texto_reclamacao="teste", canal=Canal.DIGITAL, status=Status.CLASSIFICADA)
    
    with patch("app.api.v1.endpoints.reclamacoes.reclamacao_repository_instance") as mock_repo:
        mock_repo.find_all.return_value = [mock_reclamacao]
        
        # Envia a requisição com o cabeçalho de autenticação
        response = client.get("/api/v1/reclamacoes/", headers=headers)
        
        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data) == 1
        assert response_data[0]["texto_reclamacao"] == "teste"
        assert response_data[0]["status"] == "classificada"

def test_endpoint_sem_api_key_falha():
    """Testa se uma requisição sem a chave de API falha com 401."""
    response = client.get("/api/v1/reclamacoes/")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}