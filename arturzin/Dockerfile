# Imagem base Python
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Copia requisitos e instala dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação
COPY . /app

# Expõe porta
EXPOSE 5000

# Comando de entrada
CMD ["python", "app.py"]