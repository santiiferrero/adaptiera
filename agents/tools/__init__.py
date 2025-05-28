"""
Herramientas disponibles para el agente de RRHH
"""

from .email_tool import send_email_summary, simulate_email_send
from .file_search_tool import search_questions_file, save_user_responses
from .json_tool import leer_json

__all__ = [
    'send_email_summary',
    'simulate_email_send', 
    'search_questions_file',
    'save_user_responses',
    'leer_json'
]
