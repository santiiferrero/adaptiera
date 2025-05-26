from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"],
    responses={404: {"description": "No encontrado"}},
)

class Mensaje(BaseModel):
    contenido: str
    tipo: str = "usuario"

class ChatResponse(BaseModel):
    mensaje: str
    sugerencias: List[str] = []

@router.post("/mensaje")
async def procesar_mensaje(mensaje: Mensaje):
    try:
        # Aquí iría la lógica del chatbot
        return ChatResponse(
            mensaje="He recibido tu mensaje",
            sugerencias=["Opción 1", "Opción 2", "Opción 3"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 