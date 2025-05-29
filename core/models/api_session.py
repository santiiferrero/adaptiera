from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SessionRequest(BaseModel):
    """Modelo para la solicitud de sesión"""
    user: str
    id_vacancy: int

class Session(BaseModel):
    """Modelo para la respuesta de sesión"""
    user: str
    id_vacancy: int
    token: str
    datetime_session_init: datetime
    datetime_session_lastactivity: datetime 