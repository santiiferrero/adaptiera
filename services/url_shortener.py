"""
Servicio para acortar URLs largas.
"""
import requests
from core.config import settings
import hashlib
import base64

def acortar_url(url_larga):
    """
    Acorta una URL larga utilizando un servicio de acortamiento o una técnica interna.
    
    Args:
        url_larga (str): La URL larga que se va a acortar
        
    Returns:
        str: La URL acortada
    """
    # Usar TinyURL API para acortar la URL
    try:
        response = requests.get(
            f"https://tinyurl.com/api-create.php?url={url_larga}",
            timeout=5
        )
        if response.status_code == 200:
            url_acortada = response.text
            print(f"URL acortada: {url_acortada}")
            return url_acortada
    except Exception as e:
        print(f"Error al acortar URL con TinyURL: {e}")
    
    # Alternativa: Si el token es muy largo, podemos generar un hash y usarlo como identificador
    try:
        # Extraer el token de la URL
        if "?token=" in url_larga:
            token_part = url_larga.split("?token=")[1]
            # Generar un hash más corto del token
            hash_object = hashlib.md5(token_part.encode())
            short_hash = base64.urlsafe_b64encode(hash_object.digest()).decode()[:10]
            # Reconstruir la URL con el token acortado
            base_url = url_larga.split("?token=")[0]
            url_acortada = f"{base_url}?token={short_hash}"
            print(f"URL acortada internamente: {url_acortada}")
            return url_acortada
    except Exception as e:
        print(f"Error al acortar URL internamente: {e}")
    
    # Si todo falla, devolver la URL original
    print("No se pudo acortar la URL, devolviendo la original")
    return url_larga

def generar_url_token(base_url, token):
    """
    Genera una URL con un token acortado.
    
    Args:
        base_url (str): La URL base
        token (str): El token (posiblemente largo)
        
    Returns:
        str: La URL completa, posiblemente acortada
    """
    url_completa = f"{base_url}?token={token}"
    return acortar_url(url_completa)


# Prueba del módulo
if __name__ == "__main__":
    url_larga = "https://chatbot-adaptiera.streamlit.app/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    url_acortada = acortar_url(url_larga)
    print(f"URL original: {url_larga}")
    print(f"URL acortada: {url_acortada}") 