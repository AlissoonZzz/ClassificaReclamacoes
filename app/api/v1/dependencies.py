from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from app.core.config import API_KEY

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Verifica se a chave de API fornecida no cabeçalho é válida.
    """
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return api_key
