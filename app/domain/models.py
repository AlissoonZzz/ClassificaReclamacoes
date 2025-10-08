from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class Canal(str, Enum):
    """Enum para os canais de origem da reclamação."""
    DIGITAL = "digital"
    FISICO = "fisico"

class Status(str, Enum):
    """Enum para o status do processamento da reclamação."""
    RECEBIDA = "recebida"
    CLASSIFICADA = "classificada"
    ENVIADA_LEGADO = "enviada_legado"

class Reclamacao(BaseModel):
    """Representa a entidade principal de uma reclamação de cliente."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    texto_reclamacao: str
    canal: Canal
    status: Status = Status.RECEBIDA
    categorias: Optional[List[str]] = []
    data_criacao: datetime = Field(default_factory=datetime.utcnow)
    data_atualizacao: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
