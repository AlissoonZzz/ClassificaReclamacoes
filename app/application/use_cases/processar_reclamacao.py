from datetime import datetime
from app.domain.models import Reclamacao, Canal, Status
from app.application.services.keyword_classification_service import KeywordClassificationService
from app.infrastructure.repositories.memory_repository import MemoryRepository

class ProcessarReclamacaoUseCase:
    def __init__(self, classification_service: KeywordClassificationService, repository: MemoryRepository):
        self._classification_service = classification_service
        self._repository = repository

    def execute(self, texto_reclamacao: str, canal: Canal) -> Reclamacao:
        reclamacao = Reclamacao(
            texto_reclamacao=texto_reclamacao,
            canal=canal
        )

        categorias = self._classification_service.classificar(reclamacao.texto_reclamacao)
        
        reclamacao.categorias = categorias
        reclamacao.status = Status.CLASSIFICADA
        reclamacao.data_atualizacao = datetime.utcnow()

        self._repository.save(reclamacao)

        # TODO: Implementar envio para o sistema legado (ex: chamada de API, etc.)

        return reclamacao
