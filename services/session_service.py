import json
import os
from datetime import datetime
import secrets
from pathlib import Path
from typing import Optional

from core.models.api_session import Session, SessionRequest

class SessionService:
    def __init__(self):
        self.users_file = Path("data/usuarios.json")
    
    def _load_users(self):
        """Carga los usuarios desde el archivo JSON"""
        if not self.users_file.exists():
            return {"usuarios": []}
        
        with open(self.users_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _user_exists(self, username: str) -> bool:
        """Verifica si existe el usuario"""
        data = self._load_users()
        return any(user["user"] == username for user in data.get("usuarios", []))
    
    def create_session(self, session_request: SessionRequest) -> Optional[Session]:
        """
        Crea una nueva sesión si el usuario existe
        
        Args:
            session_request: Datos de la solicitud de sesión
            
        Returns:
            Session si el usuario existe, None si no
        """
        if not self._user_exists(session_request.user):
            return None
            
        # Generar token seguro
        token = secrets.token_urlsafe(32)
        
        # Crear timestamp actual
        now = datetime.now()
        
        # Crear y retornar sesión
        return Session(
            user=session_request.user,
            id_vacancy=session_request.id_vacancy,
            token=token,
            datetime_session_init=now,
            datetime_session_lastactivity=now
        ) 