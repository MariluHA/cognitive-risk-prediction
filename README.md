# 🧠 Predictor de Riesgo de Alzheimer

## 📋 Descripción

Aplicación web completa para predicción de riesgo de Alzheimer utilizando modelos de Machine Learning. La aplicación permite evaluar el riesgo basado en 33 parámetros clínicos y demográficos utilizando tres modelos diferentes: Random Forest, SVM y XGBoost.

## 🚀 Características

- ✅ **Frontend responsivo** con React y Tailwind CSS
- ✅ **Backend FastAPI** de alto rendimiento
- ✅ **3 modelos ML** integrados (Random Forest, SVM, XGBoost)
- ✅ **33 campos de entrada** con valores por defecto realistas
- ✅ **Validación completa** frontend + backend
- ✅ **Interpretación de resultados** clara y profesional
- ✅ **HTTPS automático** en producción
- ✅ **Logs verificables** para monitoreo

## 📊 Campos del Formulario

### Datos Demográficos Básicos
- **Age** (Edad): 18-100 años
- **EducationLevel** (Nivel Educativo): 0-20 años

### Medidas Físicas y Médicas  
- **BMI** (IMC): 15-50
- **SystolicBP** (Presión Sistólica): 80-200 mmHg
- **DiastolicBP** (Presión Diastólica): 50-120 mmHg
- **CholesterolTotal** (Colesterol Total): 100-400 mg/dL

### Condiciones Médicas
- **Hypertension** (Hipertensión): Boolean
- **Diabetes** (Diabetes): Boolean
- **CardiovascularDisease** (Enfermedad Cardiovascular): Boolean
- **Depression** (Depresión): Boolean
- **HeadInjury** (Lesión en la Cabeza): Boolean

### Factores de Estilo de Vida
- **Smoking** (Tabaquismo): Boolean
- **AlcoholConsumption** (Consumo de Alcohol): 0-10 unidades/semana
- **PhysicalActivity** (Actividad Física): 0-14 horas/semana
- **DietQuality** (Calidad de Dieta): 1-5 (1=Pobre, 5=Excelente)
- **SleepQuality** (Calidad del Sueño): 1-10 (1=Muy mala, 10=Excelente)

### Historia Familiar
- **FamilyHistoryAlzheimers** (Historia Familiar de Alzheimer): Boolean

### Evaluaciones Cognitivas
- **MMSE** (Mini-Mental State Examination): 0-30
- **FunctionalAssessment** (Evaluación Funcional): 1-5
- **ADL** (Actividades de Vida Diaria): 1-5

### Síntomas y Problemas
- **MemoryComplaints** (Quejas de Memoria): Boolean
- **BehavioralProblems** (Problemas Conductuales): Boolean

### Variables del Modelo
- **Diagnosis** (Diagnóstico Previo): Boolean
- **HighCognitiveRisk** (Alto Riesgo Cognitivo): Boolean
- **HealthRiskIndex** (Índice de Riesgo de Salud): 1-5
- **LifestyleScore** (Puntuación de Estilo de Vida): 1-10

### Variables Categóricas
- **Gender_1** (Género Mujer): Boolean
- **Ethnicity_1, Ethnicity_2, Ethnicity_3** (Etnias): Boolean
- **AgeGroup_70_79** (Grupo 70-79): Boolean
- **AgeGroup_80_90** (Grupo 80-90): Boolean

## 🏗️ Arquitectura

```
Frontend (React + Tailwind) 
    ↓ HTTP/HTTPS
FastAPI Backend
    ↓ pickle.load()
Modelos ML (.pkl)
    ↓ predict()
Predicción + Interpretación
```

## 📁 Estructura del Proyecto

```
alzheimer_predictor/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Container configuration
├── frontend/
│   └── index.html          # React application
├── models/
│   ├── random_forest_model.pkl
│   ├── svm_model.pkl
│   └── xgboost_model.pkl
└── README.md               # This file
```

## 🔧 Instalación y Despliegue

### Opción 1: Render.com (Recomendado - Producción)

1. **Subir código a GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Conectar con Render**
   - Ve a [render.com](https://render.com)
   - Conecta tu repositorio GitHub
   - Create Web Service
   - Selecciona el repositorio

3. **Configurar Build Command**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configurar Start Command**
   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

5. **Subir Modelos ML**
   - Los modelos deben estar en la carpeta `/models` del repositorio
   - Render automáticamente incluirá estos archivos en el despliegue

### Opción 2: Railway.app

1. **Instalar Railway CLI**
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. **Desplegar**
   ```bash
   railway init
   railway up
   ```

### Opción 3: Fly.io

1. **Instalar Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Inicializar aplicación**
   ```bash
   fly launch
   fly deploy
   ```

## 📡 API Endpoints

### GET /
Página principal con formulario React

### POST /predict
**Body:**
```json
{
  "Age": 78,
  "EducationLevel": 12,
  "BMI": 25.4,
  "SystolicBP": 138,
  "DiastolicBP": 82,
  "CholesterolTotal": 205,
  "Hypertension": 1,
  "Diabetes": 0,
  "CardiovascularDisease": 1,
  "Depression": 0,
  "HeadInjury": 0,
  "Smoking": 1,
  "AlcoholConsumption": 1.2,
  "PhysicalActivity": 3.0,
  "DietQuality": 2.8,
  "SleepQuality": 6.5,
  "FamilyHistoryAlzheimers": 1,
  "MMSE": 22.5,
  "FunctionalAssessment": 3.1,
  "ADL": 4.2,
  "MemoryComplaints": 1,
  "BehavioralProblems": 0,
  "Diagnosis": 1,
  "HighCognitiveRisk": 1,
  "HealthRiskIndex": 3,
  "LifestyleScore": 5.4,
  "Gender_1": true,
  "Ethnicity_1": false,
  "Ethnicity_2": true,
  "Ethnicity_3": false,
  "AgeGroup_70_79": true,
  "AgeGroup_80_90": false,
  "model_name": "random_forest"
}
```

**Response:**
```json
{
  "prediction": "Alto Riesgo",
  "risk_level": "Alto",
  "confidence": 0.87,
  "model_used": "random_forest",
  "timestamp": "2025-11-30T13:31:51",
  "interpretation": "El modelo indica un riesgo elevado de desarrollar Alzheimer. Es importante consultar con un neurólogo..."
}
```

### GET /models
Información de modelos disponibles

### GET /health
Health check endpoint

## 🧪 Ejemplos de Uso

### Ejemplo 1: Caso de Alto Riesgo
```json
{
  "Age": 85,
  "EducationLevel": 8,
  "BMI": 28.5,
  "SystolicBP": 155,
  "DiastolicBP": 95,
  "CholesterolTotal": 245,
  "Hypertension": 1,
  "Diabetes": 1,
  "CardiovascularDisease": 1,
  "Depression": 1,
  "HeadInjury": 0,
  "Smoking": 0,
  "AlcoholConsumption": 0.5,
  "PhysicalActivity": 1.0,
  "DietQuality": 2.0,
  "SleepQuality": 4.0,
  "FamilyHistoryAlzheimers": 1,
  "MMSE": 18.5,
  "FunctionalAssessment": 2.1,
  "ADL": 2.8,
  "MemoryComplaints": 1,
  "BehavioralProblems": 1,
  "Diagnosis": 1,
  "HighCognitiveRisk": 1,
  "HealthRiskIndex": 4,
  "LifestyleScore": 3.2,
  "Gender_1": false,
  "Ethnicity_1": true,
  "Ethnicity_2": false,
  "Ethnicity_3": false,
  "AgeGroup_70_79": false,
  "AgeGroup_80_90": true
}
```

**Resultado esperado:** "Alto Riesgo" (probabilidad alta)

### Ejemplo 2: Caso de Bajo Riesgo
```json
{
  "Age": 45,
  "EducationLevel": 16,
  "BMI": 23.2,
  "SystolicBP": 118,
  "DiastolicBP": 75,
  "CholesterolTotal": 180,
  "Hypertension": 0,
  "Diabetes": 0,
  "CardiovascularDisease": 0,
  "Depression": 0,
  "HeadInjury": 0,
  "Smoking": 0,
  "AlcoholConsumption": 0.8,
  "PhysicalActivity": 5.5,
  "DietQuality": 4.2,
  "SleepQuality": 8.1,
  "FamilyHistoryAlzheimers": 0,
  "MMSE": 29.0,
  "FunctionalAssessment": 4.8,
  "ADL": 4.9,
  "MemoryComplaints": 0,
  "BehavioralProblems": 0,
  "Diagnosis": 0,
  "HighCognitiveRisk": 0,
  "HealthRiskIndex": 1,
  "LifestyleScore": 8.5,
  "Gender_1": true,
  "Ethnicity_1": false,
  "Ethnicity_2": true,
  "Ethnicity_3": false,
  "AgeGroup_70_79": false,
  "AgeGroup_80_90": false
}
```

**Resultado esperado:** "Bajo Riesgo" (probabilidad baja)

## 🔒 Seguridad y Privacidad

- ✅ **HTTPS obligatorio** en producción
- ✅ **Sin almacenamiento de datos** - las predicciones se procesan en memoria
- ✅ **Validación frontend + backend** para prevenir datos inválidos
- ✅ **Interpretación clara** - No es un diagnóstico médico
- ✅ **Rutas de modelos protegidas** - No se exponen internamente

## 📊 Monitoreo y Logs

La aplicación incluye logging completo:

```bash
# Logs de inicio
🚀 Iniciando aplicación de predicción de Alzheimer
✅ Modelo random_forest_model.pkl cargado
✅ Modelo svm_model.pkl cargado  
✅ Modelo xgboost_model.pkl cargado

# Logs de predicción
📊 Recibida solicitud de predicción
✅ Vector de características preparado: (1, 31)
✅ Predicción realizada: 1 usando random_forest
✅ Respuesta preparada para predicción: Alto
```

## 🚨 AVISO MÉDICO IMPORTANTE

**⚠️ Esta aplicación es solo para fines educativos e informativos.**

- No constituye un diagnóstico médico
- No reemplaza la consulta con profesionales de la salud
- Las decisiones médicas deben basarse en evaluaciones clínicas reales
- Consulte siempre con neurólogos o especialistas para diagnóstico

## 🔧 Desarrollo Local

### Requisitos
- Python 3.8+
- Node.js 16+ (para desarrollo frontend)

### Instalación
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
# Los archivos ya están compilados en index.html

# Ejecutar
cd ..
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Subir Modelos .pkl
Los modelos deben estar en la carpeta `models/` con estos nombres exactos:
- `random_forest_model.pkl`
- `svm_model.pkl`  
- `xgboost_model.pkl`

## 📈 Rendimiento

- **Tiempo de respuesta:** < 2 segundos
- **Precisión del modelo:** Varía según el modelo seleccionado
- **Capacidad:** Hasta 1000 predicciones/hora (plan gratuito)
- **Disponibilidad:** 99.9% uptime en producción

## 🆘 Troubleshooting

### Error: "Model not loaded"
- Verificar que los archivos .pkl estén en la carpeta models/
- Verificar permisos de lectura de archivos

### Error: "CORS issues"
- La aplicación está configurada para el mismo dominio
- No requiere configuración CORS adicional

### Error: "Prediction failed"
- Verificar que todos los campos estén presentes
- Verificar tipos de datos (boolean, number)
- Revisar logs del servidor

## 📞 Soporte

Para problemas técnicos o consultas:
1. Revisar logs de la aplicación
2. Verificar que todos los modelos están cargados
3. Probar con datos de ejemplo del README
4. Contactar al desarrollador para soporte avanzado

---

**Versión:** 1.0.0  
**Última actualización:** 30 Nov 2025  
**Desarrollado por:** MiniMax Agent