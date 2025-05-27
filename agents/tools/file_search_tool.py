import os
import json
from typing import List, Dict, Any
from langchain_core.tools import tool


@tool
def search_questions_file(file_path: str = "data/questions.json") -> List[str]:
    """
    Busca y carga las preguntas desde un archivo local.
    
    Args:
        file_path: Ruta al archivo de preguntas (por defecto: data/questions.json)
        
    Returns:
        Lista de preguntas a realizar al usuario
    """
    try:
        # Verificar si el archivo existe
        if not os.path.exists(file_path):
            # Si no existe, crear un archivo de ejemplo
            default_questions = [
                "¿Cuál es tu nombre completo?",
                "¿Cuál es tu experiencia laboral previa?",
                "¿Qué habilidades técnicas posees?",
                "¿Por qué estás interesado en esta posición?",
                "¿Cuáles son tus expectativas salariales?"
            ]
            
            # Crear el directorio si no existe
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({"questions": default_questions}, f, ensure_ascii=False, indent=2)
            
            return default_questions
        
        # Cargar preguntas del archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, dict) and "questions" in data:
            return data["questions"]
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Formato de archivo no válido")
            
    except Exception as e:
        print(f"Error al cargar preguntas: {e}")
        # Retornar preguntas por defecto en caso de error
        return [
            "¿Cuál es tu nombre completo?",
            "¿Cuál es tu experiencia laboral previa?",
            "¿Qué habilidades técnicas posees?"
        ]


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
        import datetime
        responses["timestamp"] = datetime.datetime.now().isoformat()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(responses, f, ensure_ascii=False, indent=2)
            
        return True
        
    except Exception as e:
        print(f"Error al guardar respuestas: {e}")
        return False 