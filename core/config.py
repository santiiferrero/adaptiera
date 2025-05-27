import os
import sys
from pathlib import Path
from dotenv import load_dotenv


# Obtener la ruta absoluta al directorio raíz del proyecto
ROOT_DIR = Path(__file__).resolve().parents[1]

# Imprimir información de depuración
print(f"Directorio raíz: {ROOT_DIR}")
env_path = ROOT_DIR / ".env"
print(f"Ruta del archivo .env: {env_path}")
print(f"¿El archivo .env existe? {env_path.exists()}")

# Añadir el directorio raíz al path de Python
sys.path.insert(0, str(ROOT_DIR))

# Cargar variables desde el .env
try:
    # Intentar cargar desde el directorio raíz
    load_dotenv(dotenv_path=env_path)
    print("Variables de entorno cargadas desde .env")
except Exception as e:
    print(f"Error al cargar las variables de entorno: {e}")
    # Fallback: intentar carga directa
    load_dotenv()

class Settings:
    # Variables comunes
    FERNET_KEY = os.getenv("FERNET_KEY")
    # Convertir a bytes 
    FERNET_KEY = FERNET_KEY.encode()

    # Email settings
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    SMTP_USER  = os.getenv("SMTP_USER")
    # Gmail API settings
    GMAIL_SCOPES = os.getenv("GMAIL_SCOPES")
    
    # Si GMAIL_SCOPES contiene múltiples scopes separados por comas, conviértelos en lista
    def get_gmail_scopes(self):
        if ',' in self.GMAIL_SCOPES:
            return self.GMAIL_SCOPES.split(',')
        return [self.GMAIL_SCOPES]

    # Twilio settings
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

    #LLMs
    LLM_API_KEY = os.getenv("LLM_API_KEY")

    #ENVIROMENTS
    ENVIRONMENT = os.getenv("ENV", "development")

    # API Endpoints
    ENDPOINT_VACANTES = os.getenv("ENDPOINT_VACANTES")
    ENDPOINT_MEDIOS = os.getenv("ENDPOINT_MEDIOS")

    def __init__(self):
        # Imprimir algunas variables para depuración
        print(f"EMAIL_USER: {self.EMAIL_USER}")
        print(f"ENVIRONMENT: {self.ENVIRONMENT}")
        print(f"GMAIL_SCOPES: {self.GMAIL_SCOPES}")

settings = Settings()
