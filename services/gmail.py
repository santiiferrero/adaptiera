from core.config import settings

def enviar_email(nombre, email, mensaje):
    print(f"Enviando correo a {settings.EMAIL_USER} desde {email}: {mensaje}")
