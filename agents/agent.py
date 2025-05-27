from agents.simple_agent import create_simple_rrhh_agent, SimpleRRHHAgent
from agents.langgraph_agent import create_rrhh_agent, AdaptieraRRHHAgent

# Usar la versión simplificada por defecto (más estable)
def crear_agente() -> SimpleRRHHAgent:
    """
    Crea un agente conversacional de RRHH (versión simplificada).
    
    Returns:
        Instancia del agente configurada
    """
    return create_simple_rrhh_agent()

# Función para crear la versión LangGraph (experimental)
def crear_agente_langgraph() -> AdaptieraRRHHAgent:
    """
    Crea un agente conversacional de RRHH usando LangGraph (experimental).
    
    Returns:
        Instancia del agente configurada
    """
    return create_rrhh_agent()

# Exportar las clases principales para uso directo
__all__ = [
    "crear_agente", 
    "crear_agente_langgraph",
    "SimpleRRHHAgent", 
    "AdaptieraRRHHAgent", 
    "create_simple_rrhh_agent",
    "create_rrhh_agent"
]
