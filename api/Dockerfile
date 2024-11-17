FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências necessárias para construir pacotes e remover após o uso
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    python3-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências do Python sem cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código
COPY . .

# Comando padrão para iniciar o app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
