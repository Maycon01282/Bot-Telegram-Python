# Use a imagem oficial do Python como base
FROM python:3.10-slim

# Instala as dependências necessárias para o mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para instalar as dependências
COPY requirements.txt .

# Desabilita a verificação SSL temporariamente para instalar as dependências
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -U certifi

# Instala as dependências listadas em requirements.txt
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Adicione esta linha no seu Dockerfile do python-bot, após as instruções de atualização do sistema
RUN apt-get update && apt-get install -y netcat-openbsd

# Copia o script wait-for-it.sh
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Expõe a porta 8000 (ajuste conforme a porta usada pelo seu app)
EXPOSE 8000

# Define o comando para iniciar o aplicativo
CMD ["sh", "-c", "./wait-for-it.sh db:3306 -t 30 -- python manage.py runserver 0.0.0.0:8000"]