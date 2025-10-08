# Documentação do Projeto: Sistema de Processamento de Reclamações

## 1. Visão Geral

Este projeto implementa um sistema de backend para processar reclamações de clientes de um banco. A solução foi projetada para ser robusta, escalável e resiliente, seguindo os princípios da **Arquitetura Limpa (Clean Architecture)**.

O fluxo principal é assíncrono, baseado no padrão **Produtor-Consumidor**:

1.  A **API (Produtor)** recebe a reclamação, a valida e a publica em uma fila de mensagens.
2.  Um **Worker (Consumidor)**, rodando em um processo separado, consome a mensagem da fila, executa a lógica de negócio (classificação, etc.) e salva o resultado.

Essa arquitetura desacopla a API do processamento pesado, permitindo que o sistema lide com altos volumes de requisições sem degradar o tempo de resposta da API.

## 2. Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Framework da API:** FastAPI
- **Servidor da API:** Uvicorn
- **Fila de Mensagens:** RabbitMQ
- **Cliente RabbitMQ:** Pika
- **Validação de Dados:** Pydantic
- **Testes:** Pytest

## 3. Como Executar o Projeto

1.  **Pré-requisito:** Ter o Docker instalado e rodando.
2.  **Iniciar o RabbitMQ:**
    ```bash
    docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
    ```
3.  **Instalar Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Iniciar a API (Terminal 1):**
    ```bash
    python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
    ```
5.  **Iniciar o Worker (Terminal 2):**
    ```bash
    python worker.py
    ```

## 4. Como Rodar os Testes

Com as dependências instaladas, execute o seguinte comando na raiz do projeto:

```bash
python -m pytest
```

## 5. Estrutura de Diretórios

```
.
├── app/
│   └── ... (código da aplicação)
├── tests/
│   ├── api/
│   │   └── test_reclamacoes_api.py
│   └── unit/
│       └── test_classification_service.py
├── classificador.py
├── requirements.txt
├── worker.py
└── DOCUMENTACAO.md
```

## 6. Análise dos Arquivos

(As seções anteriores de análise de arquivos permanecem as mesmas)

---

### `tests/unit/test_classification_service.py`

-   **Propósito:** Testa a unidade de lógica de negócio mais pura do sistema: o serviço de classificação. 
-   **Estratégia:** Como este serviço é uma classe sem dependências externas, podemos instanciá-lo diretamente e testar seu método `classificar()` com diferentes entradas de texto, verificando se a saída (a lista de categorias) é a esperada. Cobre casos de match simples, múltiplo, nenhum match e case-insensitivity.

---

### `tests/api/test_reclamacoes_api.py`

-   **Propósito:** Testa os endpoints da API, garantindo que a interface externa do sistema funcione corretamente.
-   **Estratégia:**
    -   Usa o `TestClient` do FastAPI para fazer requisições HTTP à aplicação sem a necessidade de um servidor real.
    -   Usa **Mocks** (`unittest.mock.patch`) para isolar a API de suas dependências externas (a fila e o repositório). 
    -   No teste `POST`, verificamos se o endpoint responde com `202 Accepted` e, crucialmente, se ele chama o método `publish` da fila com os dados corretos.
    -   No teste `GET`, simulamos um retorno do repositório e verificamos se a API formata e entrega esses dados corretamente.