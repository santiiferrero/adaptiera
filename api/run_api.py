"""
Script para ejecutar la API REST de Adaptiera.
Para ejecutar usar: python -m api.run_api
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    ) 