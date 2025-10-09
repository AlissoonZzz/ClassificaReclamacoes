# 🚀 Sistema de Processamento de Reclamações

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103-009688?style=for-the-badge&logo=fastapi)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.9-FF6600?style=for-the-badge&logo=rabbitmq)
![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?style=for-the-badge&logo=docker)
![Pytest](https://img.shields.io/badge/Pytest-7.4-0A9B00?style=for-the-badge&logo=pytest)

Este repositório contém a implementação de um sistema de backend para processamento de reclamações de clientes, construído com foco em escalabilidade, resiliência e manutenibilidade, seguindo os princípios da **Arquitetura Limpa (Clean Architecture)**.

## 🎯 O Problema

Instituições financeiras recebem um grande volume de reclamações de clientes por múltiplos canais (digitais e físicos). Para garantir a satisfação do cliente e cumprir os SLAs (Acordos de Nível de Serviço), essas reclamações precisam ser:

1.  **Recepcionadas** de forma padronizada.
2.  **Classificadas** automaticamente por tipo de demanda.
3.  **Processadas** de forma eficiente e rastreável.
4.  **Integradas** com sistemas legados para consumo por outras áreas.

## ✨ A Solução

A solução implementada é um sistema assíncrono que utiliza o padrão **Produtor-Consumidor** para desacoplar o recebimento da reclamação do seu processamento.

### Arquitetura do Fluxo

```mermaid
graph TD
    subgraph "Canais de Entrada"
        A[Canal Digital / Sites]
        B[Canal Físico (Digitalizado)]
    end

    subgraph "Sistema de Processamento"
        A -- "POST /reclamacoes" --> C(API - FastAPI)
        B -- "Envio via API" --> C
        C -- "Publica Mensagem" --> D{Fila - RabbitMQ}
        D -- "Consome Mensagem" --> E(Worker)
        E -- "Salva Resultado" --> F[(Repositório)]
    end

    subgraph "Sistemas Externos"
        G[Sistema Legado]
    end

    E -- "Envia Dados" --> G
```

1.  **API (Produtor):** Um endpoint FastAPI recebe a reclamação, valida os dados e a publica em uma fila RabbitMQ. A resposta para o cliente é imediata.
2.  **Worker (Consumidor):** Um processo independente consome as mensagens da fila, executa a lógica de negócio (classificação por palavras-chave) e persiste o resultado.

Esta abordagem garante que a API permaneça responsiva, mesmo sob alta carga, e que nenhuma reclamação seja perdida.

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia | Justificativa |
| :--- | :--- | :--- |
| **Linguagem** | **Python 3** | Linguagem versátil e com um ecossistema robusto para aplicações web e de dados. |
| **Framework API** | **FastAPI** | Alto desempenho, documentação OpenAPI automática e sintaxe moderna. |
| **Servidor ASGI** | **Uvicorn** | Servidor rápido e leve, recomendado pelo FastAPI. |
| **Fila de Mensagens**| **RabbitMQ** | Garante o desacoplamento, a resiliência e a escalabilidade do processamento. |
| **Persistência** | **Repo. em Memória** | Simplicidade para o case. A arquitetura permite fácil troca por um DB como **PostgreSQL**. |
| **Testes** | **Pytest** | Framework de testes poderoso e flexível para garantir a qualidade do código. |
| **Containerização** | **Docker** | Facilita a configuração do ambiente e o deploy da aplicação. |

## 🚀 Como Executar o Projeto

A maneira mais simples de executar o projeto é utilizando Docker e Docker Compose.

### Pré-requisitos

-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/)

### Passos

1.  Clone este repositório:
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd <NOME_DO_DIRETORIO>
    ```

2.  Execute o Docker Compose para construir e iniciar os contêineres:
    ```bash
    docker-compose up --build
    ```

3.  Aguarde os serviços iniciarem. A API estará disponível e pronta para receber requisições.

-   **Documentação Interativa (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
-   **Health Check da API:** [http://localhost:8000/health](http://localhost:8000/health)

## 🧪 Como Rodar os Testes

Os testes foram escritos com Pytest e podem ser executados localmente.

1.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

2.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

3.  Execute os testes:
    ```bash
    python -m pytest
    ```

## 🕹️ Exemplo de Uso da API

Você pode enviar uma nova reclamação para o endpoint `/reclamacoes` usando a documentação do Swagger ou via `curl`.

**Exemplo com `curl`:**

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/reclamacoes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: fake-api-key' \
  -d 
  {
    "titulo": "Problema com o aplicativo",
    "descricao": "O aplicativo do banco está travando muito e com erro ao carregar o extrato.",
    "cliente_id": "cliente123"
  }
```

O `worker` processará a reclamação em segundo plano. Você pode verificar as reclamações processadas no endpoint `GET /reclamacoes`.

## 🗺️ Roadmap e Próximos Passos

-   [ ] **Substituir Classificador:** Trocar a classificação por palavras-chave por um modelo de **IA Generativa** para maior precisão e compreensão de contexto.
-   [ ] **Implementar Banco de Dados:** Substituir o repositório em memória por uma implementação com **PostgreSQL** ou outro banco de dados robusto.
-   [ ] **Monitoramento de SLA:** Adicionar um serviço para monitorar o tempo de vida das reclamações e alertar sobre prazos de vencimento.
-   [ ] **Autenticação e Autorização:** Implementar um sistema de autenticação mais robusto (ex: OAuth2).

---
*Projeto desenvolvido como parte de um case técnico.*
