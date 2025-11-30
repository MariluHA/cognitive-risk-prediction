# Dockerfile para Alzheimer Predictor
FROM python:3.12-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Configurar directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY backend/ ./backend/
COPY frontend/ ./static/
COPY models/ ./models/

# Crear directorios necesarios
RUN mkdir -p /app/static

# Copiar archivos estáticos
RUN cp frontend/index.html static/index.html

# Exponer puerto
EXPOSE 8000

# Variables de entorno
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Comando de inicio
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]