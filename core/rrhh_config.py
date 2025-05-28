# Configuración del Agente de RRHH para Streamlit

# Configuración de la interfaz
INTERFACE_CONFIG = {
    "title": "🤖 Agente de RRHH - Entrevista Virtual con IA",
    "subtitle": "Entrevista automatizada con inteligencia artificial avanzada",
    "welcome_message": """
    ¡Bienvenido a nuestra entrevista virtual! Soy el asistente de RRHH de Adaptiera.
    Te haré algunas preguntas para conocerte mejor. Responde con sinceridad y naturalidad.
    
    🧠 **Powered by Groq**: Este sistema utiliza inteligencia artificial avanzada para evaluar tus respuestas.
    """,
    "completion_message": "🎉 ¡Entrevista completada! Gracias por tu tiempo.",
    "error_message": "❌ Error al procesar tu respuesta. Por favor, intenta de nuevo.",
    "groq_required": "🔧 Este sistema requiere configuración de Groq para funcionar correctamente.",
}

# Configuración de botones
BUTTONS_CONFIG = {
    "start": {
        "text": "🚀 Iniciar Entrevista",
        "type": "primary"
    },
    "restart": {
        "text": "🔄 Reiniciar",
        "type": "secondary"
    },
    "download": {
        "text": "📄 Descargar Resumen",
        "type": "secondary"
    }
}

# Configuración de mensajes de ayuda
HELP_CONFIG = {
    "info_title": "ℹ️ Información sobre la entrevista",
    "expectations": """
    **¿Qué puedes esperar?**
    
    - 📝 **Preguntas personalizadas**: El agente te hará preguntas relevantes sobre tu perfil profesional
    - 🤖 **Evaluación inteligente**: Tus respuestas serán evaluadas automáticamente usando IA
    - 🔄 **Clarificaciones**: Si una respuesta necesita más detalles, el agente te lo pedirá amablemente
    - 📊 **Resumen automático**: Al final recibirás un resumen completo de la entrevista
    - 📧 **Notificación**: Se enviará un resumen por correo al equipo de RRHH
    """,
    "tips": """
    **Consejos para una mejor experiencia:**
    - Responde con naturalidad y sinceridad
    - No te preocupes por errores de ortografía
    - Puedes ser breve, pero trata de ser específico
    - Si necesitas aclarar algo, el agente te ayudará
    - Tómate tu tiempo para pensar las respuestas
    """
}

# Configuración de métricas y progreso
METRICS_CONFIG = {
    "progress_label": "Progreso de la Entrevista",
    "questions_label": "Preguntas Respondidas",
    "total_label": "Total de Preguntas",
    "messages_label": "Mensajes Intercambiados"
}

# Configuración del archivo de descarga
DOWNLOAD_CONFIG = {
    "filename": "resumen_entrevista_adaptiera.txt",
    "header": "RESUMEN DE ENTREVISTA - ADAPTIERA",
    "separator": "=" * 50,
    "mime_type": "text/plain"
} 