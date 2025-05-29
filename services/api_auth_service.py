from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import HTTPException, status
import secrets
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class AuthService:
    def __init__(self):
        # Obtener credenciales de variables de entorno o usar valores por defecto
        self.api_username = os.getenv("API_USERNAME")
        self.api_password = os.getenv("API_PASSWORD")
    
    def verify_credentials(self, credentials: HTTPBasicCredentials) -> bool:
        """
        Verifica las credenciales de autenticación básica
        
        Args:
            credentials: Credenciales HTTP básicas
            
        Returns:
            bool: True si las credenciales son válidas
            
        Raises:
            HTTPException: Si las credenciales son inválidas
        """
        is_correct_username = secrets.compare_digest(
            credentials.username.encode("utf8"),
            self.api_username.encode("utf8")
        )
        is_correct_password = secrets.compare_digest(
            credentials.password.encode("utf8"),
            self.api_password.encode("utf8")
        )
        
        if not (is_correct_username and is_correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Basic"},
            )
        
        return True 