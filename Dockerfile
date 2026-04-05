FROM python:3.12-slim

# Define o diretório de trabalho padrão dentro do container
WORKDIR /app

# Copia as dependências e as instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# O Gunicorn é o servidor web robusto recomendado para produção no Flask
RUN pip install --no-cache-dir gunicorn

# Copia o restante dos arquivos do projeto
COPY . .

# Garante que a pasta de uploads de fotos exista
RUN mkdir -p /app/static/uploads

# Expõe a porta 5000
EXPOSE 5010

# Comando para iniciar a aplicação via gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5010", "app:app"]
