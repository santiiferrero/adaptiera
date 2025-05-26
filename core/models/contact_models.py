from pydantic import BaseModel, EmailStr

class Contacto(BaseModel):
    nombre: str
    email: EmailStr
    mensaje: str
