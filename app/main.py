from fastapi import FastAPI
from app.api.v1.endpoints import reclamacoes

app = FastAPI(
    title="Sistema de Processamento de Reclamações",
    description="API para receber, classificar e gerenciar reclamações de clientes.",
    version="1.0.0"
)

# Inclui as rotas da API de reclamações
app.include_router(reclamacoes.router, prefix="/api/v1/reclamacoes", tags=["Reclamações"])

@app.get("/", tags=["Health Check"])
def read_root():
    """Endpoint raiz para verificar se a API está no ar."""
    return {"status": "ok"}
