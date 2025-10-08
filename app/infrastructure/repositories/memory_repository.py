from typing import List, Dict
import uuid
from app.domain.models import Reclamacao

class MemoryRepository:
    """Repositório em memória para armazenar e gerenciar reclamações."""

    def __init__(self):
        self._data: Dict[uuid.UUID, Reclamacao] = {}

    def save(self, reclamacao: Reclamacao) -> Reclamacao:
        """Salva ou atualiza uma reclamação."""
        self._data[reclamacao.id] = reclamacao
        return reclamacao

    def find_all(self) -> List[Reclamacao]:
        """Retorna todas as reclamações armazenadas."""
        return list(self._data.values())

reclamacao_repository_instance = MemoryRepository()
