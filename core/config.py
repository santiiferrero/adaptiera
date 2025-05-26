import os
from dotenv import load_dotenv
from pathlib import Path


# Cargar variables desde el .env
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    # Variables comunes
    FERNET_KEY = os.getenv("FERNET_KEY", "default_key_for_development")  # Valor por defecto para desarrollo
    # Convertir a bytes 
    FERNET_KEY = FERNET_KEY.encode()

    # Email settings
    EMAIL_USER = os.getenv("EMAIL_USER", "default@example.com")
    EMAIL_PASS = os.getenv("EMAIL_PASS", "default_password")

    #LLMs
    #LLM_API_KEY = os.getenv("LLM_API_KEY")

    #ENVIROMENTS
    ENVIRONMENT = os.getenv("ENV", "development")

settings = Settings()
