from langchain_core.messages import HumanMessage, AIMessage
import os

def get_response(user_input):
    """
    Función simple para generar respuestas del chatbot.
    
    Args:
        user_input (str): Mensaje del usuario
        
    Returns:
        str: Respuesta del chatbot
    """
    # En una implementación real, aquí conectarías con tu LLM o agente
    # Por ahora, devolvemos respuestas predefinidas basadas en palabras clave
    
    user_input = user_input.lower()
    
    if "hola" in user_input or "saludos" in user_input:
        return "¡Hola! ¿En qué puedo ayudarte hoy?"
    
    elif "ayuda" in user_input:
        return "Estoy aquí para ayudarte. Puedes preguntarme sobre nuestros servicios, formularios o cualquier otra información."
    
    elif "gracias" in user_input:
        return "¡De nada! Si tienes más preguntas, no dudes en consultarme."
    
    else:
        return "Entiendo tu consulta. Nuestro equipo está trabajando para implementar respuestas más inteligentes. ¿Puedo ayudarte con algo más?" 