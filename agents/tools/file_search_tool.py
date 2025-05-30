import os
import json
from typing import List, Dict, Any
from langchain_core.tools import tool
import datetime


@tool
def search_questions_file(file_path: str = "data/questions.json", id_job_offer: str = None) -> List[str]:
    """
    Busca y carga las preguntas desde un archivo local basándose en el id_job_offer.
    
    Args:
        file_path: Ruta base del archivo de preguntas
        id_job_offer: ID de la oferta de trabajo para seleccionar el archivo específico
        
    Returns:
        Lista de preguntas a realizar al usuario
    """
    try:
        # Si se proporciona id_job_offer, buscar archivo específico
        if id_job_offer:
            # Construir ruta específica para la oferta de trabajo
            base_dir = os.path.dirname(file_path) if file_path else "data"
            specific_file = os.path.join(base_dir, f"questions_{id_job_offer}.json")
            
            print(f"🔍 Buscando preguntas para oferta de trabajo: {id_job_offer}")
            print(f"📁 Archivo esperado: {specific_file}")
            
            # Intentar cargar archivo específico de la oferta de trabajo
            if os.path.exists(specific_file):
                print(f"✅ Encontrado archivo específico: {specific_file}")
                with open(specific_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if isinstance(data, dict) and "questions" in data:
                    print(f"📋 Cargadas {len(data['questions'])} preguntas para oferta de trabajo {id_job_offer}")
                    return data["questions"]
                elif isinstance(data, list):
                    print(f"📋 Cargadas {len(data)} preguntas para oferta de trabajo {id_job_offer}")
                    return data
            else:
                print(f"⚠️ No se encontró archivo específico para oferta de trabajo {id_job_offer}")
                print(f"🔄 Intentando cargar archivo por defecto...")
        
        # Cargar archivo por defecto si no hay id_job_offer o no existe el específico
        default_file = file_path if file_path else "data/questions.json"
        
        # Verificar si el archivo por defecto existe
        if not os.path.exists(default_file):
            print(f"❌ No se encontró archivo de preguntas: {default_file}")
            raise FileNotFoundError(f"Archivo de preguntas no encontrado: {default_file}")
        
        # Cargar preguntas del archivo por defecto
        print(f"📂 Cargando archivo por defecto: {default_file}")
        with open(default_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, dict) and "questions" in data:
            print(f"📋 Cargadas {len(data['questions'])} preguntas del archivo por defecto")
            return data["questions"]
        elif isinstance(data, list):
            print(f"📋 Cargadas {len(data)} preguntas del archivo por defecto")
            return data
        else:
            raise ValueError("Formato de archivo no válido")
            
    except Exception as e:
        print(f"❌ Error al cargar preguntas: {e}")
        raise e


@tool
def save_user_responses(responses: Dict[str, str], file_path: str = "data/user_responses.json") -> bool:
    """
    Guarda las respuestas del usuario en un archivo local.
    
    Args:
        responses: Diccionario con las respuestas del usuario
        file_path: Ruta donde guardar las respuestas
        
    Returns:
        True si se guardó correctamente, False en caso contrario
    """
    try:
        # Crear el directorio si no existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Agregar timestamp
        responses["timestamp"] = datetime.datetime.now().isoformat()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(responses, f, ensure_ascii=False, indent=2)
            
        return True
        
    except Exception as e:
        print(f"Error al guardar respuestas: {e}")
        return False


# Versiones directas (sin @tool) para uso interno
def search_questions_file_direct(file_path: str = "data/questions.json", id_job_offer: str = None) -> List[str]:
    """
    Versión directa de search_questions_file (sin decorador @tool).
    """
    # Usar la misma lógica que la versión con @tool
    return search_questions_file.func(file_path, id_job_offer)


def save_user_responses_direct(responses: Dict[str, str], file_path: str = "data/user_responses.json") -> bool:
    """
    Versión directa de save_user_responses (sin decorador @tool).
    """
    # Usar la misma lógica que la versión con @tool
    return save_user_responses.func(responses, file_path) 