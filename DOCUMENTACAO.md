# Documentação do Projeto: Sistema de Processamento de Reclamações

## 1. Visão Geral

Este projeto implementa um sistema de backend para processar reclamações de clientes, projetado para ser robusto, escalável e de fácil manutenção, utilizando os princípios da **Arquitetura Limpa (Clean Architecture)**.

O fluxo principal é assíncrono e baseado no padrão **Produtor-Consumidor**:

1.  A **API (Produtor)** recebe a reclamação, realiza uma validação inicial e a publica em uma fila de mensagens (RabbitMQ).
2.  Um **Worker (Consumidor)**, executado em um processo independente, consome a mensagem da fila, aplica a lógica de negócio (como a classificação por palavras-chave) e persiste o resultado.

Essa arquitetura desacopla o recebimento das reclamações do seu processamento, permitindo que o sistema lide com altos volumes de requisições sem degradar o tempo de resposta da API e garantindo que nenhuma reclamação seja perdida.

## 2. Arquitetura e Tecnologias

### 2.1. Arquitetura

A **Clean Architecture** foi escolhida por promover um baixo acoplamento e uma clara separação de responsabilidades, o que resulta em um sistema mais testável, compreensível e fácil de manter ou evoluir. As dependências apontam sempre para o centro (domínio), protegendo as regras de negócio de alterações em frameworks e tecnologias de infraestrutura.

### 2.2. Tecnologias Principais

-   **Linguagem:** Python 3.
-   **Framework da API:** **FastAPI** com **Uvicorn** como servidor ASGI.
    -   **Motivos:** Alto desempenho, documentação automática (Swagger/OpenAPI) e um ecossistema moderno que acelera o desenvolvimento de APIs robustas.
-   **Fila de Mensagens:** **RabbitMQ** com a biblioteca **Pika**.
    -   **Motivos:** Garante o desacoplamento entre a API e os serviços de processamento, aumenta a resiliência do sistema e permite o balanceamento de carga e a escalabilidade independente dos workers.
-   **Persistência de Dados:** **Repositório em Memória**.
    -   **Nota:** Para a simplicidade deste case, foi implementado um repositório em memória. No entanto, a arquitetura permite uma substituição fácil por um banco de dados relacional como o **PostgreSQL**, que seria a escolha ideal para um ambiente de produção devido à sua confiabilidade, robustez e recursos avançados para consultas estruturadas.
-   **Testes:** **Pytest** para testes unitários e de integração.

## 3. Atendendo aos Requisitos do Case

A solução foi projetada para endereçar os desafios propostos no `casecanais.pdf`:

-   **Suporte a Picos e Fluxo Contínuo:** O uso de RabbitMQ como buffer absorve picos de requisições, garantindo que as reclamações sejam processadas de forma assíncrona sem sobrecarregar o sistema.
-   **Rastreabilidade:** Cada reclamação recebe um ID único na API. O desacoplamento via fila permite que cada etapa (recebimento, classificação, etc.) seja monitorada, e o status da reclamação pode ser atualizado no repositório, garantindo a rastreabilidade.
-   **Integração com Sistema Legado:** O `worker` pode ser estendido para, após processar a reclamação, enviar os dados para o sistema legado através de uma chamada de API ou publicando em outra fila de mensagens dedicada a essa integração.
-   **Monitoramento de SLA (Prazo de 10 dias):** Para identificar casos próximos do vencimento, um campo `data_expiracao_sla` pode ser adicionado ao modelo de dados. Um processo agendado (ex: um CronJob) poderia consultar o repositório diariamente e gerar alertas para os casos que expiram em breve.

## 4. Proposta de Evolução: Classificação com IA

A classificação atual, baseada em palavras-chave, é funcional, mas limitada. Uma evolução natural seria substituí-la por um modelo de **Inteligência Artificial Generativa**.

-   **Vantagens:**
    -   **Compreensão de Contexto:** A IA pode interpretar o sentimento e o contexto da reclamação, superando a rigidez das palavras-chave.
    -   **Tolerância a Erros:** Lida melhor com erros de digitação, sinônimos e variações na forma de escrever.
    -   **Classificação Múltipla e Precisa:** Pode atribuir múltiplas categorias com maior precisão, reduzindo classificações equivocadas.

Essa abordagem, embora envolva um custo maior de implementação e inferência, tende a otimizar o processo, direcionando as reclamações para as equipes corretas com mais eficiência.

## 5. Como Executar o Projeto

### 5.1. Com Docker (Recomendado)

1.  **Pré-requisito:** Ter Docker e Docker Compose instalados.
2.  Na raiz do projeto, execute:
    ```bash
    docker-compose up --build
    ```
3.  A API estará disponível em `http://localhost:8000/docs` para interagir com a documentação do Swagger.

### 5.2. Rodar os Testes

1.  Certifique-se de que as dependências de desenvolvimento estão instaladas:
    ```bash
    pip install -r requirements.txt
    ```
2.  Execute o Pytest na raiz do projeto:
    ```bash
    python -m pytest
    ```

## 6. Estrutura de Diretórios

```
.
├── app/                 # Código fonte da aplicação (Clean Architecture)
│   ├── api/             # Camada de API (endpoints, DTOs)
│   ├── application/     # Lógica de aplicação (casos de uso, serviços)
│   ├── domain/          # Entidades e regras de negócio centrais
│   └── infrastructure/  # Implementações (fila, repositórios, etc.)
├── tests/               # Testes automatizados
├── Dockerfile           # Define a imagem da aplicação
├── docker-compose.yml   # Orquestra os contêineres (api, worker, rabbitmq)
├── requirements.txt     # Dependências Python
└── worker.py            # Ponto de entrada do consumidor da fila
```

## 6.1 Análise dos Arquivos Principais

- **`docker-compose.yml`**: Define os três serviços principais (`rabbitmq`, `api`, `worker`), suas imagens, portas e como eles se conectam.
- **`Dockerfile`**: Constrói a imagem Python para os serviços `api` e `worker`, instalando as dependências a partir do `requirements.txt`.
- **`app/main.py`**: Ponto de entrada da API FastAPI, onde os roteadores são incluídos.
- **`app/api/v1/endpoints/reclamacoes.py`**: Define os endpoints `/reclamacoes` (POST e GET), incluindo a camada de segurança com chave de API.
- **`worker.py`**: O processo consumidor que escuta a fila do RabbitMQ, recebe as reclamações e dispara o caso de uso para processá-las.
- **`app/application/use_cases/processar_reclamacao.py`**: Orquestra as etapas de uma reclamação: cria a entidade, chama o serviço de classificação e salva no repositório.
- **`app/application/services/keyword_classification_service.py`**: Implementa a lógica de classificação baseada em uma lista de palavras-chave.
- **`app/domain/models.py`**: Define as estruturas de dados centrais (Pydantic models) como `Reclamacao`, `Canal` e `Status`.