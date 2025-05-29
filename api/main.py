from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.session_route import router as session_router

# Crear instancia de FastAPI
app = FastAPI(
    title="Adaptiera API",
    description="API para el sistema de entrevistas de Adaptiera",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(session_router) 