# Usa uma imagem base oficial do Python.
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container.
WORKDIR /code

# Copia o arquivo de dependências para o diretório de trabalho.
COPY requirements.txt .

# Instala as dependências.
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação (a pasta 'app') para o diretório de trabalho.
COPY ./app ./app
COPY ./worker.py .

# O comando para rodar a aplicação será definido no docker-compose.yml
