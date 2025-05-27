"""
Módulo para enviar correos electrónicos.
"""
from core.config import settings
import base64
import os
import pickle
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.credentials import Credentials
import smtplib
import socket
from pathlib import Path
from core.config import settings

# Obtener la ruta al directorio raíz del proyecto
ROOT_DIR = Path(__file__).resolve().parents[1]
CREDENTIALS_PATH = ROOT_DIR / "data" / "credentials.json"
TOKEN_PATH = ROOT_DIR / "data" / "token.pickle"

# Imprimir información de depuración
print(f"Directorio raíz: {ROOT_DIR}")
print(f"Ruta de credenciales: {CREDENTIALS_PATH}")
print(f"¿El archivo de credenciales existe? {CREDENTIALS_PATH.exists()}")

# Reemplazá con tu cuenta
SMTP_USER = settings.SMTP_USER

# Scopes requeridos para enviar correo - obtenidos desde settings
SCOPES = settings.get_gmail_scopes()
print(f"Usando scopes: {SCOPES}")

def obtener_token_oauth():
    creds = None
    if TOKEN_PATH.exists():
        try:
            with open(TOKEN_PATH, "rb") as token:
                creds = pickle.load(token)
            print("Token cargado correctamente")
        except Exception as e:
            print(f"Error al cargar el token: {e}")
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("Token actualizado correctamente")
            except Exception as e:
                print(f"Error al actualizar el token: {e}")
        else:
            try:
                if not CREDENTIALS_PATH.exists():
                    print(f"Error: El archivo de credenciales no existe en: {CREDENTIALS_PATH}")
                    # Buscar en rutas alternativas
                    alt_paths = [
                        ROOT_DIR / "credentials.json",
                        Path("./credentials.json"),
                        Path("./data/credentials.json")
                    ]
                    for path in alt_paths:
                        if path.exists():
                            print(f"Usando credenciales alternativas en: {path}")
                            CREDENTIALS_PATH = path
                            break
                    else:
                        print("No se encontró el archivo de credenciales")
                        return None
                
                flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
                creds = flow.run_local_server(port=0)
                print("Nuevas credenciales obtenidas")
                
                # Asegurarse de que la carpeta data exista
                TOKEN_PATH.parent.mkdir(exist_ok=True)
                
                with open(TOKEN_PATH, "wb") as token:
                    pickle.dump(creds, token)
                print(f"Token guardado en: {TOKEN_PATH}")
            except Exception as e:
                print(f"Error al obtener nuevas credenciales: {e}")
                return None
    
    return creds.token if creds else None

def generar_oauth2_string(email, access_token):
    auth_string = f"user={email}\x01auth=Bearer {access_token}\x01\x01"
    return base64.b64encode(auth_string.encode()).decode()

def test_conexion_smtp():
    """Función para probar la conectividad SMTP"""
    try:
        # Probar conexión básica
        sock = socket.create_connection(("smtp.gmail.com", 587), timeout=10)
        sock.close()
        print("✅ Conexión a smtp.gmail.com:587 exitosa")
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def enviar_correo_v1(destinatario, asunto, cuerpo):
    """Versión con OAuth2 y mejor manejo de errores"""
    try:
        # Probar conexión primero
        if not test_conexion_smtp():
            return False
            
        access_token = obtener_token_oauth()
        if not access_token:
            print("No se pudo obtener el token de acceso")
            return False
            
        auth_string = generar_oauth2_string(SMTP_USER, access_token)
        
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = destinatario
        msg['Subject'] = asunto
        msg.attach(MIMEText(cuerpo, 'plain'))
        
        # Configurar servidor con timeout más largo
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
            server.set_debuglevel(1)  # Para ver qué está pasando
            server.ehlo()
            server.starttls()
            server.ehlo()
            
            # Autenticación OAuth2
            server.docmd("AUTH", "XOAUTH2 " + auth_string)
            server.sendmail(SMTP_USER, destinatario, msg.as_string())
        
        print("✅ Correo enviado correctamente")
        return True
        
    except Exception as e:
        print("❌ Error al enviar correo:", e)
        return False

def enviar_correo_v2_gmail_api(destinatario, asunto, cuerpo):
    """Alternativa usando Gmail API directamente (recomendado)"""
    try:
        from googleapiclient.discovery import build
        from email.mime.text import MIMEText
        import base64
        
        # Obtener credenciales
        creds = None
        if TOKEN_PATH.exists():
            try:
                with open(TOKEN_PATH, "rb") as token:
                    creds = pickle.load(token)
            except Exception as e:
                print(f"Error al cargar el token: {e}")
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error al actualizar el token: {e}")
            else:
                try:
                    if not CREDENTIALS_PATH.exists():
                        print(f"Error: El archivo de credenciales no existe en: {CREDENTIALS_PATH}")
                        return False
                    
                    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
                    creds = flow.run_local_server(port=0)
                    
                    TOKEN_PATH.parent.mkdir(exist_ok=True)
                    with open(TOKEN_PATH, "wb") as token:
                        pickle.dump(creds, token)
                except Exception as e:
                    print(f"Error al obtener nuevas credenciales: {e}")
                    return False
        
        if not creds:
            print("No se pudieron obtener las credenciales")
            return False
            
        # Crear servicio Gmail API
        service = build('gmail', 'v1', credentials=creds)
        
        # Crear mensaje
        message = MIMEText(cuerpo)
        message['to'] = destinatario
        message['from'] = SMTP_USER
        message['subject'] = asunto
        
        # Codificar mensaje
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        # Enviar
        send_message = service.users().messages().send(
            userId="me", 
            body={'raw': raw_message}
        ).execute()
        
        print("✅ Correo enviado correctamente via Gmail API")
        return True
        
    except Exception as e:
        print("❌ Error al enviar correo via Gmail API:", e)
        return False

def enviar_correo_v3_password_app(destinatario, asunto, cuerpo, password_app=None):
    """Alternativa usando contraseña de aplicación (más simple)"""
    try:
        if not test_conexion_smtp():
            return False
        
        # Si no se proporciona contraseña, usar la del archivo .env
        if not password_app:
            password_app = settings.EMAIL_PASS
            if not password_app:
                print("No se proporcionó contraseña de aplicación")
                return False
            
        msg = MIMEMultipart()
        msg['From'] = 'Adaptiera Team' #SMTP_USER
        msg['To'] = destinatario
        msg['Subject'] = asunto
        msg.attach(MIMEText(cuerpo, 'plain'))
        
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
            server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, password_app)  # Usar contraseña de aplicación
            server.sendmail(SMTP_USER, destinatario, msg.as_string())
        
        print("✅ Correo enviado correctamente con contraseña de app")
        return True
        
    except Exception as e:
        print("❌ Error al enviar correo:", e)
        return False

# Función principal que prueba diferentes métodos
def enviar_correo(destinatario, asunto, cuerpo, password_app=None):
    """
    Función principal que intenta diferentes métodos de envío
    """
    print("🔄 Intentando enviar correo...")
    
    # Si estamos en modo de desarrollo, simular el envío
    if settings.ENVIRONMENT == "development" and not settings.EMAIL_PASS:
        print("📧 Modo desarrollo: simulando envío de correo")
        print(f"Para: {destinatario}")
        print(f"Asunto: {asunto}")
        print(f"Cuerpo: {cuerpo[:100]}...")
        return True
    
    # Método 1: Gmail API (recomendado)
    print("📧 Intentando con Gmail API...")
    if enviar_correo_v2_gmail_api(destinatario, asunto, cuerpo):
        return True
    
    # Método 2: OAuth2 con SMTP
    print("📧 Intentando con OAuth2 + SMTP...")
    if enviar_correo_v1(destinatario, asunto, cuerpo):
        return True
    
    # Método 3: Contraseña de aplicación
    print("📧 Intentando con contraseña de aplicación...")
    if enviar_correo_v3_password_app(destinatario, asunto, cuerpo, password_app):
        return True
    
    print("❌ Todos los métodos fallaron")
    return False

# Ejemplo de uso
if __name__ == "__main__":
    # Probar conexión
    test_conexion_smtp()
    
    # Enviar correo
    enviar_correo(
        destinatario="destinatario@email.com",
        asunto="Prueba",
        cuerpo="Este es un correo de prueba"
    )
