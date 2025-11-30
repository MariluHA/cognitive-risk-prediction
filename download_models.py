import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_from_gdrive(file_id, output_path):
    """Descargar archivo desde Google Drive"""
    
    url = f"https://drive.google.com/uc?id={file_id}&export=download"
    
    try:
        session = requests.Session()
        response = session.get(url, stream=True)
        
        # Google Drive puede requerir un token de descarga
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                params = {'id': file_id, 'confirm': value}
                response = session.get(url, params=params, stream=True)
                break
        
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=32768):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        percent = (downloaded / total_size * 100) if total_size else 0
                        logger.info(f"  Progreso: {percent:.1f}%")
            
            logger.info(f"✅ Descargado: {output_path}")
            return True
        else:
            logger.error(f"❌ Error descargando (status {response.status_code})")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False


def download_models():
    """Descargar todos los modelos"""
    
    models_dir = "/app/models"
    os.makedirs(models_dir, exist_ok=True)
    
    # ⭐ REEMPLAZA ESTOS IDS CON LOS TUYOS DE GOOGLE DRIVE
    models = {
        "random_forest_model.pkl": "1huELShO1nGgwB25RN1G1CDAEc7YWq3jy",  # CAMBIAR
        "svm_model.pkl": "1RkVQUIKIGdy4GddYsp0tabXOMvUnU9Y_",            # CAMBIAR
        "xgboost_model.pkl": "1V7NuB18OTdEXw5LCZMCCPmhmTjgsMkzV"         # CAMBIAR
    }
    
    logger.info("📥 Iniciando descarga de modelos...")
    
    for model_name, file_id in models.items():
        filepath = os.path.join(models_dir, model_name)
        
        if os.path.exists(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            logger.info(f"✅ {model_name} ya existe ({size_mb:.1f} MB)")
            continue
        
        logger.info(f"⬇️ Descargando {model_name} (ID: {file_id})")
        download_from_gdrive(file_id, filepath)
    
    logger.info("✅ Descarga completada")


if __name__ == "__main__":
    download_models()