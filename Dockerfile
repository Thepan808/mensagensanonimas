# Use a imagem base oficial do Python mais recente
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o container
COPY . .

# Expõe a porta em que a aplicação irá rodar (ajuste conforme necessário)
EXPOSE 8000

# Define o comando padrão para rodar a aplicação
CMD ["python", "app.py"]
