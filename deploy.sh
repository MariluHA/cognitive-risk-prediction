#!/bin/bash

# Script de despliegue para Render.com
# Alzheimer Risk Predictor

echo "🚀 Iniciando despliegue de Alzheimer Predictor..."

# Verificar que los modelos estén presentes
echo "📊 Verificando modelos ML..."
for model in models/*.pkl; do
    if [ -f "$model" ]; then
        echo "✅ $(basename $model) encontrado"
    else
        echo "❌ $(basename $model) no encontrado"
        exit 1
    fi
done

# Verificar dependencias Python
echo "🔧 Verificando dependencias..."
python3 -c "import fastapi, uvicorn, scikit-learn, xgboost" || {
    echo "❌ Dependencias no instaladas"
    exit 1
}

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r backend/requirements.txt

# Verificar estructura de archivos
echo "📁 Verificando estructura..."
required_files=(
    "backend/main.py"
    "static/index.html" 
    "models/random_forest_model.pkl"
    "models/svm_model.pkl"
    "models/xgboost_model.pkl"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file encontrado"
    else
        echo "❌ $file no encontrado"
        exit 1
    fi
done

# Probar carga de modelos
echo "🧪 Probando carga de modelos..."
python3 -c "
import pickle
import os
models_dir = 'models'
for model_name in ['random_forest_model', 'svm_model', 'xgboost_model']:
    filepath = os.path.join(models_dir, f'{model_name}.pkl')
    try:
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
        print(f'✅ {model_name} cargado correctamente')
    except Exception as e:
        print(f'❌ Error cargando {model_name}: {e}')
        exit(1)
"

echo "✅ Todos los modelos cargados correctamente"
echo "🎉 Despliegue preparado exitosamente"
echo "📍 Aplicación lista en puerto 8000"
echo "🌐 Para usar: uvicorn backend.main:app --host 0.0.0.0 --port \$PORT"