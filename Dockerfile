# Verwenden eines offiziellen Python-Images als Basis-Image
FROM python:3.9-slim-buster

# Setzen des Arbeitsverzeichnisses im Container
WORKDIR /app

# Kopieren der aktuellen Verzeichnisinhalte in das Arbeitsverzeichnis im Container
COPY . /app

# Installieren der benötigten Pakete
RUN pip install --no-cache-dir fastapi uvicorn requests beautifulsoup4

# Port für den FastAPI-Server
# Heroku weist dynamisch einen Port zu, daher ist EXPOSE optional
# EXPOSE $PORT

# Befehl, der beim Start des Containers ausgeführt wird
CMD uvicorn main:app --host 127.0.0.1 --port $PORT
