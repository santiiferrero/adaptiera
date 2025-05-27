import re

def validar_email(email: str) -> bool:
    """
    Valida el formato de un correo electrónico.
    
    Args:
        email (str): Correo electrónico a validar
        
    Returns:
        bool: True si el correo tiene un formato válido, False en caso contrario
    """
    if not email:
        return False
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, email) is not None

def validar_telefono(telefono: str) -> bool:
    """
    Valida el formato de un número de teléfono.
    
    Args:
        telefono (str): Número de teléfono a validar
        
    Returns:
        bool: True si el teléfono tiene un formato válido, False en caso contrario
    """
    if not telefono:
        return False
    
    # Eliminar espacios, guiones y paréntesis
    telefono_limpio = re.sub(r'[\s\-\(\)]', '', telefono)
    
    # Formato E.164: + seguido de 10 a 15 dígitos
    return re.match(r'^\+\d{10,15}$', telefono_limpio) is not None
