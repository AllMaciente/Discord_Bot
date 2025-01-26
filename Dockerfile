# Use uma imagem base do Python
FROM python:3.12-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo de requisitos (requirements.txt) para o contêiner
COPY requirements.txt .

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copie o arquivo .env para dentro do contêiner
COPY .env .env

# Copie o restante dos arquivos do bot para o contêiner
COPY . .

# Exponha a porta do seu bot (se necessário)
EXPOSE 8080

# Defina o comando para rodar o bot
CMD ["python", "main.py"]
