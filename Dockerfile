FROM python:3.12-slim

# Instalar dependencias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar y instalar requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY static/ ./static/
COPY download_models.py .

# Crear carpeta de modelos
RUN mkdir -p /app/models

# ⭐ DESCARGAR MODELOS AL INICIAR
RUN python download_models.py

EXPOSE 8000

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]