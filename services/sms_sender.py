"""
Módulo para enviar mensajes SMS.
"""
from core.config import settings
from twilio.rest import Client

# Cargar variables de entorno o directamente del archivo credentials.json
TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER = settings.TWILIO_PHONE_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def enviar_sms(destinatario: str, mensaje: str) -> bool:
    mensaje = mensaje[:50]
    try:
        message = client.messages.create(
            body=mensaje,
            from_=TWILIO_PHONE_NUMBER,
            to=destinatario
        )
        print(f"SMS Enviado a : {destinatario}")
        return True
    except Exception as e:
        print(f"Error al enviar SMS: {e}")
        return False
