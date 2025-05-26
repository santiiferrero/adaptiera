import re
from typing import List, Optional

def clean_text(text: str) -> str:
    """Limpia un texto eliminando espacios extra y caracteres especiales."""
    # Eliminar espacios múltiples
    text = re.sub(r'\s+', ' ', text)
    # Eliminar caracteres especiales
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Trunca un texto a una longitud máxima."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def extract_emails(text: str) -> List[str]:
    """Extrae direcciones de email de un texto."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

def extract_phone_numbers(text: str) -> List[str]:
    """Extrae números de teléfono de un texto."""
    phone_pattern = r'\+?1?\d{9,15}'
    return re.findall(phone_pattern, text) 