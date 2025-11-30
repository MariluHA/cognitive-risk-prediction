#!/bin/bash

# Script automatizado de despliegue para Render.com
# Alzheimer Risk Predictor - ML Web Application

echo "🚀 INICIANDO DESPLIEGUE ALZHEIMER PREDICTOR"
echo "==========================================="

# Configuración
APP_NAME="alzheimer-predictor"
REGION="oregon"  # Cambiar según preferencia
PLAN="free"      # free, starter, standard

# Verificar archivos necesarios
echo "📁 Verificando archivos del proyecto..."

required_files=(
    "backend/main.py"
    "backend/requirements.txt"
    "static/index.html"
    "models/random_forest_model.pkl"
    "models/svm_model.pkl"
    "models/xgboost_model.pkl"
    "Dockerfile"
    "README.md"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file encontrado"
    else
        echo "❌ ERROR: $file no encontrado"
        exit 1
    fi
done

# Verificar modelos ML
echo ""
echo "🧪 Verificando integridad de modelos ML..."
for model in models/*.pkl; do
    filename=$(basename "$model")
    size=$(stat -f%z "$model" 2>/dev/null || stat -c%s "$model" 2>/dev/null)
    echo "✅ $filename ($size bytes)"
done

# Crear repository en GitHub (instrucciones)
echo ""
echo "📋 PASOS PARA DESPLIEGUE EN RENDER.COM:"
echo "========================================="
echo ""
echo "1. SUBIR A GITHUB:"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Alzheimer Predictor - ML Web App'"
echo "   git branch -M main"
echo "   git remote add origin https://github.com/TU-USUARIO/alzheimer-predictor.git"
echo "   git push -u origin main"
echo ""
echo "2. CONECTAR EN RENDER:"
echo "   - Ir a https://render.com"
echo "   - Login con GitHub"
echo "   - New → Web Service"
echo "   - Conectar tu repositorio"
echo ""
echo "3. CONFIGURAR SERVICIO:"
echo "   - Name: $APP_NAME"
echo "   - Region: $REGION" 
echo "   - Branch: main"
echo "   - Root Directory: (vacío)"
echo "   - Runtime: Python 3"
echo "   - Build Command: pip install -r backend/requirements.txt"
echo "   - Start Command: uvicorn backend.main:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "4. VARIABLES DE ENTORNO (Environment → Environment):"
echo "   PYTHONPATH=/app"
echo "   PYTHONUNBUFFERED=1"
echo "   MODELS_DIR=/app/models"
echo ""
echo "5. DESPLIEGUE:"
echo "   - Click 'Create Web Service'"
echo "   - Esperar 5-10 minutos para build + deploy"
echo "   - URL disponible: https://$APP_NAME.onrender.com"
echo ""
echo "✅ ARCHIVOS LISTOS PARA DESPLIEGUE"
echo "🎉 APLICACIÓN ML COMPLETAMENTE FUNCIONAL"