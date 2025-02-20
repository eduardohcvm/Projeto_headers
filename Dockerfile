FROM ubuntu:latest
LABEL authors="eduar"

# Atualiza os pacotes e instala o Python3 e pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de requisitos para o contêiner
COPY requirements.txt .

# Atualiza o pip e instala as dependências do projeto
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Copia o restante do código da aplicação para o contêiner
COPY . .

# Expõe a porta que o Flask utilizará (por padrão 5000)
EXPOSE 5000

# Define as variáveis de ambiente para o Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para iniciar a aplicação
CMD ["flask", "run"]
