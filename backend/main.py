"""
Aplicación Web para Predicción de Riesgo de Alzheimer
Backend FastAPI con modelos ML integrados
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import pickle
import numpy as np
import logging
from datetime import datetime
import os
import sys

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic Models para validación
class PredictionRequest(BaseModel):
    # Datos demográficos básicos
    Age: int = Field(..., description="Edad del paciente (años)")
    EducationLevel: int = Field(..., description="Nivel educativo (años)")
    Gender_1: bool = Field(..., description="Género: 1=Mujer, 0=Hombre")
    
    # Medidas físicas y médicas
    BMI: float = Field(..., description="Índice de masa corporal")
    SystolicBP: float = Field(..., description="Presión arterial sistólica")
    DiastolicBP: float = Field(..., description="Presión arterial diastólica")
    CholesterolTotal: float = Field(..., description="Colesterol total")
    
    # Condiciones médicas
    Hypertension: int = Field(..., description="Hipertensión (0/1)")
    Diabetes: int = Field(..., description="Diabetes (0/1)")
    CardiovascularDisease: int = Field(..., description="Enfermedad cardiovascular (0/1)")
    Depression: int = Field(..., description="Depresión (0/1)")
    HeadInjury: int = Field(..., description="Lesión en la cabeza (0/1)")
    
    # Factores de estilo de vida
    Smoking: int = Field(..., description="Tabaquismo (0/1)")
    AlcoholConsumption: float = Field(..., description="Consumo de alcohol (unidades/semana)")
    PhysicalActivity: float = Field(..., description="Actividad física (horas/semana)")
    DietQuality: float = Field(..., description="Calidad de dieta (1-5)")
    SleepQuality: float = Field(..., description="Calidad del sueño (1-10)")
    
    # Historia familiar
    FamilyHistoryAlzheimers: int = Field(..., description="Historia familiar de Alzheimer (0/1)")
    
    # Evaluaciones cognitivas
    MMSE: float = Field(..., description="Mini-Mental State Examination (0-30)")
    FunctionalAssessment: float = Field(..., description="Evaluación funcional (1-5)")
    ADL: float = Field(..., description="Actividades de la vida diaria (1-5)")
    
    # Síntomas y problemas
    MemoryComplaints: int = Field(..., description="Quejas de memoria (0/1)")
    BehavioralProblems: int = Field(..., description="Problemas conductuales (0/1)")
    
    # Variables del modelo
    Diagnosis: int = Field(..., description="Diagnóstico previo (0/1)")
    HighCognitiveRisk: int = Field(..., description="Alto riesgo cognitivo (0/1)")
    HealthRiskIndex: int = Field(..., description="Índice de riesgo de salud (1-5)")
    LifestyleScore: float = Field(..., description="Puntuación de estilo de vida (1-10)")
    
    # Variables categóricas
    Ethnicity_1: bool = Field(..., description="Etnia 1 (bool)")
    Ethnicity_2: bool = Field(..., description="Etnia 2 (bool)")
    Ethnicity_3: bool = Field(..., description="Etnia 3 (bool)")
    AgeGroup_70_79: bool = Field(..., description="Grupo de edad 70-79 (bool)")
    AgeGroup_80_90: bool = Field(..., description="Grupo de edad 80-90 (bool)")
    model_name: str = Field(default="random_forest", description="Modelo ML a usar para la predicción")


class PredictionResponse(BaseModel):
    prediction: str
    risk_level: str
    confidence: Optional[float] = None
    model_used: str
    timestamp: str
    interpretation: str


class ModelInfo(BaseModel):
    model_name: str
    features: List[str]
    loaded: bool
    type: str


# Inicializar FastAPI
app = FastAPI(
    title="Alzheimer Risk Predictor",
    description="Aplicación web para predicción de riesgo de Alzheimer usando ML",
    version="1.0.0"
)

# Directorio de modelos
MODELS_DIR = "/workspace/alzheimer_predictor/models"

# Variable global para modelos cargados
loaded_models = {}


def load_models():
    """Cargar todos los modelos ML al iniciar la aplicación"""
    global loaded_models
    
    model_files = {
        "random_forest": "random_forest_model.pkl",
        "svm": "svm_model.pkl", 
        "xgboost": "xgboost_model.pkl"
    }
    
    for model_name, filename in model_files.items():
        try:
            filepath = os.path.join(MODELS_DIR, filename)
            logger.info(f"Cargando modelo {model_name} desde {filepath}")
            
            with open(filepath, 'rb') as f:
                model = pickle.load(f)
            
            loaded_models[model_name] = model
            logger.info(f"✅ Modelo {model_name} cargado exitosamente")
            
        except Exception as e:
            logger.error(f"❌ Error cargando {model_name}: {e}")
            loaded_models[model_name] = None


def prepare_feature_vector(data: Dict[str, Any]) -> np.ndarray:
    """
    Preparar vector de características en el orden exacto que esperan los modelos
    Orden exacto: Age, EducationLevel, BMI, SystolicBP, DiastolicBP, CholesterolTotal,
    Hypertension, Diabetes, CardiovascularDisease, Depression, HeadInjury, Smoking,
    AlcoholConsumption, PhysicalActivity, DietQuality, SleepQuality, FamilyHistoryAlzheimers,
    MMSE, FunctionalAssessment, ADL, MemoryComplaints, BehavioralProblems,
    HighCognitiveRisk, HealthRiskIndex, LifestyleScore, Gender_1,
    Ethnicity_1, Ethnicity_2, Ethnicity_3, AgeGroup_70-79, AgeGroup_80-90
    """
    
    # Valores por defecto para campos no incluidos directamente en la predicción
    behavioral_val = data.get('BehavioralProblems', 0)
    
    feature_vector = np.array([
        data['Age'],
        data['EducationLevel'],
        data['BMI'],
        data['SystolicBP'],
        data['DiastolicBP'],
        data['CholesterolTotal'],
        data['Hypertension'],
        data['Diabetes'],
        data['CardiovascularDisease'],
        data['Depression'],
        data['HeadInjury'],
        data['Smoking'],
        data['AlcoholConsumption'],
        data['PhysicalActivity'],
        data['DietQuality'],
        data['SleepQuality'],
        data['FamilyHistoryAlzheimers'],
        data['MMSE'],
        data['FunctionalAssessment'],
        data['ADL'],
        data['MemoryComplaints'],
        behavioral_val,
        data['HighCognitiveRisk'],
        data['HealthRiskIndex'],
        data['LifestyleScore'],
        int(data['Gender_1']),
        int(data['Ethnicity_1']),
        int(data['Ethnicity_2']),
        int(data['Ethnicity_3']),
        int(data['AgeGroup_70_79']),
        int(data['AgeGroup_80_90'])
    ], dtype=np.float32)
    
    return feature_vector.reshape(1, -1)


def interpret_prediction(prediction: int, model_name: str, confidence: Optional[float] = None) -> str:
    """Interpretar la predicción para el usuario"""
    
    interpretations = {
        0: {
            "title": "Riesgo Bajo de Alzheimer",
            "message": "Basado en los datos ingresados, el modelo indica un riesgo bajo de desarrollar Alzheimer. Sin embargo, esto no constituye un diagnóstico médico y se recomienda consultar con un profesional de la salud para evaluaciones regulares.",
            "recommendations": [
                "Mantener un estilo de vida saludable",
                "Ejercicio regular y dieta balanceada",
                "Estimulación cognitiva",
                "Revisiones médicas periódicas"
            ]
        },
        1: {
            "title": "Riesgo Elevado de Alzheimer",
            "message": "El modelo indica un riesgo elevado de desarrollar Alzheimer. Es importante consultar con un neurólogo o especialista para una evaluación completa y desarrollar un plan de seguimiento.",
            "recommendations": [
                "Consulta médica inmediata",
                "Evaluación neuropsicológica completa",
                "Monitoreo regular de funciones cognitivas",
                "Implementación de estrategias de prevención"
            ]
        }
    }
    
    result = interpretations.get(prediction, interpretations[0])
    
    if confidence:
        result["message"] += f" (Confianza del modelo: {confidence:.1%})"
    
    return result


@app.on_event("startup")
async def startup_event():
    """Cargar modelos al iniciar la aplicación"""
    logger.info("🚀 Iniciando aplicación de predicción de Alzheimer")
    load_models()
    
    # Verificar que todos los modelos se cargaron
    for model_name, model in loaded_models.items():
        if model is not None:
            logger.info(f"✅ {model_name} listo")
        else:
            logger.warning(f"⚠️ {model_name} no disponible")


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Servir la página principal"""
    try:
        with open("/workspace/alzheimer_predictor/static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        logger.error(f"Error sirviendo frontend: {e}")
        return HTMLResponse(content="<h1>Error loading application</h1>")


@app.get("/models", response_model=Dict[str, ModelInfo])
async def get_models_info():
    """Obtener información de los modelos disponibles"""
    info = {}
    
    for model_name, model in loaded_models.items():
        if model is not None:
            info[model_name] = ModelInfo(
                model_name=model_name,
                features=["31 features según modelo"],
                loaded=True,
                type=str(type(model).__name__)
            )
        else:
            info[model_name] = ModelInfo(
                model_name=model_name,
                features=[],
                loaded=False,
                type="Not loaded"
            )
    
    return info


@app.post("/predict", response_model=PredictionResponse)
async def predict_alzheimer_risk(request: PredictionRequest):
    """Endpoint principal para predicción de riesgo de Alzheimer"""
    try:
        logger.info(f"📊 Recibida solicitud de predicción")
        
        # Convertir request a diccionario
        data = request.dict()
        
        # Determinar modelo (por ahora usar el primero disponible)
        model_name = "random_forest"  # Por defecto
        if request.model_name in loaded_models:
            model_name = request.model_name
        
        # Verificar que el modelo esté cargado
        if loaded_models[model_name] is None:
            raise HTTPException(status_code=503, detail=f"Modelo {model_name} no disponible")
        
        # Preparar vector de características
        feature_vector = prepare_feature_vector(data)
        logger.info(f"✅ Vector de características preparado: {feature_vector.shape}")
        
        # Realizar predicción
        model = loaded_models[model_name]
        
        if hasattr(model, 'predict_proba'):
            # Obtener probabilidades si están disponibles
            probabilities = model.predict_proba(feature_vector)[0]
            prediction = model.predict(feature_vector)[0]
            confidence = max(probabilities)
        else:
            # Solo predicción binaria
            prediction = model.predict(feature_vector)[0]
            confidence = None
        
        logger.info(f"✅ Predicción realizada: {prediction} usando {model_name}")
        
        # Interpretar resultado
        interpretation = interpret_prediction(int(prediction), model_name, confidence)
        
        # Crear respuesta
        response = PredictionResponse(
            prediction="Alto Riesgo" if prediction == 1 else "Bajo Riesgo",
            risk_level="Alto" if prediction == 1 else "Bajo",
            confidence=confidence,
            model_used=model_name,
            timestamp=datetime.now().isoformat(),
            interpretation=interpretation["message"]
        )
        
        logger.info(f"✅ Respuesta preparada para predicción: {response.risk_level}")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error en predicción: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": len([m for m in loaded_models.values() if m is not None])
    }


# Montar archivos estáticos
if os.path.exists("/workspace/alzheimer_predictor/static"):
    app.mount("/", StaticFiles(directory="/workspace/alzheimer_predictor/static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)