from fastapi import APIRouter, HTTPException

from core.models.session import SessionRequest, Session
from services.session_service import SessionService

router = APIRouter(prefix="/api")

# Crear instancia del servicio
session_service = SessionService()

@router.post("/session", response_model=Session)
async def create_session(session_request: SessionRequest):
    """
    Crea una nueva sesión para un usuario
    
    Args:
        session_request: Datos de la solicitud de sesión
        
    Returns:
        Session: Datos de la sesión creada
        
    Raises:
        HTTPException: Si el usuario no existe
    """
    session = session_service.create_session(session_request)
    
    if not session:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    
    return session 