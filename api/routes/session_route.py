from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from core.models.api_session import SessionRequest, Session
from services.session_service import SessionService
from services.api_auth_service import AuthService

router = APIRouter(prefix="/api")

# Crear instancias de servicios
session_service = SessionService()
auth_service = AuthService()
security = HTTPBasic()

@router.post("/session", response_model=Session)
async def create_session(
    session_request: SessionRequest,
    credentials: HTTPBasicCredentials = Depends(security)
):
    """
    Crea una nueva sesión para un usuario
    
    Args:
        session_request: Datos de la solicitud de sesión
        credentials: Credenciales de autenticación básica
        
    Returns:
        Session: Datos de la sesión creada
        
    Raises:
        HTTPException: Si el usuario no existe o las credenciales son inválidas
    """
    # Verificar credenciales
    auth_service.verify_credentials(credentials)
    
    # Procesar la solicitud
    session = session_service.create_session(session_request)
    
    if not session:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    
    return session 