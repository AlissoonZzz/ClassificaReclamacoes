from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.domain.models import Reclamacao, Canal
from app.api.v1.dependencies import verify_api_key
from app.infrastructure.queue.rabbitmq_queue import RabbitMQQueue
from app.infrastructure.repositories.memory_repository import reclamacao_repository_instance

# Aplica a dependência de segurança a todas as rotas deste roteador
router = APIRouter(dependencies=[Depends(verify_api_key)])

class CriarReclamacaoRequest(BaseModel):
    texto: str
    canal: Canal

@router.post("/", status_code=202) 
def criar_reclamacao(request: CriarReclamacaoRequest):
    """
    Endpoint para aceitar uma nova reclamação e enfileirá-la para processamento.
    """
    reclamacao_data = {
        "texto": request.texto,
        "canal": request.canal.value
    }
    # Cria uma nova instância e publica a mensagem
    queue = RabbitMQQueue()
    queue.publish(reclamacao_data)
    return {"message": "Reclamação recebida e enfileirada para processamento."}

@router.get("/", response_model=list[Reclamacao])
def listar_reclamacoes():
    """Endpoint para listar todas as reclamações processadas."""
    return reclamacao_repository_instance.find_all()