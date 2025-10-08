# Documentação do Projeto: Sistema de Processamento de Reclamações

## 1. Visão Geral

Este projeto implementa um sistema de backend para processar reclamações de clientes de um banco. A solução foi projetada para ser robusta, escalável e resiliente, seguindo os princípios da **Arquitetura Limpa (Clean Architecture)**.

O fluxo principal é assíncrono, baseado no padrão **Produtor-Consumidor**:

1.  A **API (Produtor)** recebe a reclamação, a valida e a publica em uma fila de mensagens (RabbitMQ).
2.  Um **Worker (Consumidor)**, rodando em um processo separado, consome a mensagem da fila, executa a lógica de negócio (classificação por palavras-chave) e salva o resultado em um repositório em memória.

Essa arquitetura desacopla a API do processamento pesado, permitindo que o sistema lide com altos volumes de requisições sem degradar o tempo de resposta.

## 2. Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Framework da API:** FastAPI
- **Servidor da API:** Uvicorn
- **Fila de Mensagens:** RabbitMQ
- **Cliente RabbitMQ:** Pika
- **Validação de Dados:** Pydantic
- **Testes:** Pytest

## 3. Como Executar o Projeto com Docker Compose

1.  **Pré-requisito:** Ter Docker e Docker Compose instalados.
2.  Abra um terminal na raiz do projeto e execute:
    ```bash
    docker-compose up --build
    ```
3.  A aplicação estará disponível em `http://localhost:8000`.

## 4. Como Rodar os Testes

Com as dependências instaladas (`pip install -r requirements.txt`), execute o seguinte comando na raiz do projeto:

```bash
python -m pytest
```

## 5. Estrutura de Diretórios

```
.
├── app/                 # Contém todo o código fonte da aplicação
│   ├── api/             # Camada de API (endpoints)
│   ├── application/     # Lógica de aplicação (casos de uso, serviços)
│   ├── domain/          # Entidades e regras de negócio centrais
│   └── infrastructure/  # Implementações de baixo nível (fila, repositórios)
├── tests/               # Contém os testes automatizados
│   ├── api/
│   └── unit/
├── Dockerfile           # Receita para construir a imagem da aplicação
├── docker-compose.yml   # Orquestra os contêineres da aplicação
├── requirements.txt     # Dependências Python
└── worker.py            # Ponto de entrada para o processo consumidor
```

## 6. Análise dos Arquivos Principais

- **`docker-compose.yml`**: Define os três serviços principais (`rabbitmq`, `api`, `worker`), suas imagens, portas e como eles se conectam.
- **`Dockerfile`**: Constrói a imagem Python para os serviços `api` e `worker`, instalando as dependências a partir do `requirements.txt`.
- **`app/main.py`**: Ponto de entrada da API FastAPI, onde os roteadores são incluídos.
- **`app/api/v1/endpoints/reclamacoes.py`**: Define os endpoints `/reclamacoes` (POST e GET), incluindo a camada de segurança com chave de API.
- **`worker.py`**: O processo consumidor que escuta a fila do RabbitMQ, recebe as reclamações e dispara o caso de uso para processá-las.
- **`app/application/use_cases/processar_reclamacao.py`**: Orquestra as etapas de uma reclamação: cria a entidade, chama o serviço de classificação e salva no repositório.
- **`app/application/services/keyword_classification_service.py`**: Implementa a lógica de classificação baseada em uma lista de palavras-chave.
- **`app/domain/models.py`**: Define as estruturas de dados centrais (Pydantic models) como `Reclamacao`, `Canal` e `Status`.
