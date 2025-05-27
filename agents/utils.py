import os
import json
import datetime
from typing import List, Dict, Any


def load_questions_from_file(file_path: str = "data/questions.json") -> List[str]:
    """
    Carga las preguntas desde un archivo local (versión simple sin @tool).
    
    Args:
        file_path: Ruta al archivo de preguntas
        
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


def save_responses_to_file(responses: Dict[str, str], file_path: str = "data/user_responses.json") -> bool:
    """
    Guarda las respuestas del usuario en un archivo local (versión simple sin @tool).
    
    Args:
        responses: Diccionario con las respuestas del usuario
        file_path: Ruta donde guardar las respuestas
        
    Returns:
        True si se guardó correctamente, False en caso contrario
    """
    try:
        # Crear el directorio si no existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Crear una copia para no modificar el original
        responses_copy = responses.copy()
        
        # Agregar timestamp
        responses_copy["timestamp"] = datetime.datetime.now().isoformat()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(responses_copy, f, ensure_ascii=False, indent=2)
            
        return True
        
    except Exception as e:
        print(f"Error al guardar respuestas: {e}")
        return False


def simulate_email_send_simple(user_responses: Dict[str, str]) -> bool:
    """
    Simula el envío de correo para pruebas (versión simple sin @tool).
    
    Args:
        user_responses: Diccionario con las respuestas del usuario
        
    Returns:
        Siempre True (simulación)
    """
    print("=== SIMULACIÓN DE ENVÍO DE CORREO ===")
    print("Resumen de la entrevista:")
    print("-" * 40)
    
    for question, answer in user_responses.items():
        if question != "timestamp":
            print(f"P: {question}")
            print(f"R: {answer}")
            print()
    
    if "timestamp" in user_responses:
        print(f"Fecha y hora: {user_responses['timestamp']}")
    
    print("=== FIN DE SIMULACIÓN ===")
    return True 