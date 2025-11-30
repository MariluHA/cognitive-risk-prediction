# Configuración completa para despliegue en Render.com
# Alzheimer Risk Predictor - Aplicación ML en Producción

## 🚀 Instrucciones de Despliegue

### Paso 1: Preparar Repositorio GitHub

```bash
# En el directorio alzheimer_predictor/
git init
git add .
git commit -m "Alzheimer Predictor - Aplicación ML de predicción de riesgo"

# Conectar con tu repositorio GitHub
git branch -M main
git remote add origin https://github.com/TU-USUARIO/alzheimer-predictor.git
git push -u origin main
```

### Paso 2: Crear Servicio Web en Render

1. **Ir a [render.com](https://render.com)**
2. **Login con GitHub**
3. **Crear Nuevo Servicio:**
   - **New** → **Web Service**
   - **Connect Repository** → Seleccionar tu repositorio

### Paso 3: Configurar Servicio Web

**Configuración Básica:**
```
Name: alzheimer-predictor
Region: Oregon (US West)
Branch: main
Root Directory: (vacío)
Runtime: Python 3
```

**Build & Deploy:**
```
Build Command: pip install -r backend/requirements.txt
Start Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

### Paso 4: Variables de Entorno

**En Render Dashboard → Environment → Environment:**
```
PYTHONPATH = /app
PYTHONUNBUFFERED = 1
MODELS_DIR = /app/models
```

### Paso 5: Desplegar

1. **Click "Create Web Service"**
2. **Esperar 5-10 minutos** para build + deploy
3. **URL generada:** `https://alzheimer-predictor.onrender.com`

## ✅ Verificación Post-Despliegue

### Health Check
```bash
curl https://tu-app.onrender.com/health
```

### Probar Predicción
```bash
curl -X POST "https://tu-app.onrender.com/predict" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

## 🔧 Solución de Problemas

### Error: "Model not loaded"
- Verificar que los archivos .pkl están en la carpeta `models/`
- Verificar que los modelos tienen los nombres correctos

### Error: "Port binding failed"
- Verificar que el Start Command usa `--port $PORT`
- Render asigna el puerto dinámicamente

### Error: "CORS issues"
- La aplicación maneja CORS automáticamente
- Frontend y backend están en el mismo dominio

### Logs no muestran modelos cargados
- Verificar Build Command se ejecutó correctamente
- Revisar requirements.txt para dependencias faltantes

## 📊 Funcionalidades Verificadas

✅ **33 campos de formulario** con validación
✅ **3 modelos ML** (Random Forest, SVM, XGBoost)
✅ **31 features** en vector de características
✅ **Interpretación** de resultados clara
✅ **HTTPS automático** en producción
✅ **Logs verificables** para monitoreo
✅ **Frontend responsivo** con React + Tailwind

## 🎯 URLs Importantes

- **Aplicación:** `https://alzheimer-predictor.onrender.com`
- **API Health:** `https://alzheimer-predictor.onrender.com/health`
- **API Models:** `https://alzheimer-predictor.onrender.com/models`
- **Documentación:** `https://alzheimer-predictor.onrender.com/docs`

## 🚨 Soporte

Si hay problemas:
1. Revisar logs en Render Dashboard
2. Verificar variables de entorno
3. Probar endpoints individualmente
4. Consultar README.md para detalles técnicos

---

**¡Aplicación ML lista para producción!** 🚀