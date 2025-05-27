import streamlit as st

def lanzar_chatbot():
    # Header del chatbot
    st.subheader("💬 Chatbot de Atención")
    st.markdown("¡Hola! Estoy aquí para ayudarte con cualquier consulta sobre Adaptiera.")
    
    # Inicializar historial de chat en session state si no existe
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
        # Mensaje de bienvenida inicial
        st.session_state.mensajes.append({
            "role": "assistant", 
            "content": "¡Hola! 👋 Soy el asistente virtual de Adaptiera. ¿En qué puedo ayudarte hoy? Puedes preguntarme sobre nuestros servicios, procesos de selección, o cualquier otra consulta."
        })
    
    # Mostrar historial de mensajes usando contenedores nativos
    st.markdown("### 💬 Conversación")
    
    for i, mensaje in enumerate(st.session_state.mensajes):
        if mensaje["role"] == "user":
            # Mensaje del usuario
            col1, col2 = st.columns([1, 4])
            with col2:
                st.info(f"**👤 Tú:** {mensaje['content']}")
        else:
            # Mensaje del asistente
            col1, col2 = st.columns([4, 1])
            with col1:
                st.success(f"**🤖 Asistente:** {mensaje['content']}")
    
    # Campo para nuevo mensaje
    st.markdown("### ✍️ Escribe tu mensaje:")
    user_input = st.text_area(
        "Tu mensaje:",
        height=80,
        placeholder="Escribe tu consulta aquí..."
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("📤 Enviar", type="primary"):
            if user_input.strip():
                # Agregar mensaje del usuario al historial
                st.session_state.mensajes.append({"role": "user", "content": user_input})
                
                # Procesar respuesta del chatbot
                try:
                    # Respuesta simple para pruebas
                    user_input_lower = user_input.lower()
                    
                    if "hola" in user_input_lower or "saludos" in user_input_lower or "buenos días" in user_input_lower or "buenas tardes" in user_input_lower:
                        respuesta = "¡Hola! 😊 ¿En qué puedo ayudarte hoy? Estoy aquí para resolver tus dudas sobre Adaptiera."
                    elif "ayuda" in user_input_lower or "información" in user_input_lower:
                        respuesta = """Estoy aquí para ayudarte con:
                        
• **Información sobre nuestros servicios** de reclutamiento
• **Procesos de selección** y entrevistas
• **Formularios de contacto** para candidatos
• **Dudas generales** sobre Adaptiera
                        
¿Sobre qué te gustaría saber más?"""
                    elif "servicios" in user_input_lower or "que hacen" in user_input_lower or "adaptiera" in user_input_lower:
                        respuesta = """🚀 **Adaptiera** es una plataforma integral de reclutamiento que ofrece:

• **Entrevistas virtuales** con IA
• **Formularios automatizados** para candidatos
• **Evaluación inteligente** de perfiles
• **Atención 24/7** con chatbot
• **Reportes detallados** para RRHH

¿Te interesa algún servicio en particular?"""
                    elif "entrevista" in user_input_lower or "proceso" in user_input_lower:
                        respuesta = """📋 **Nuestro proceso de entrevista virtual:**

1. **Inicio**: El candidato accede al agente de RRHH
2. **Preguntas personalizadas**: IA adapta las preguntas al perfil
3. **Evaluación automática**: Análisis inteligente de respuestas
4. **Resumen detallado**: Reporte completo para el equipo de RRHH

¿Quieres saber más sobre algún paso específico?"""
                    elif "gracias" in user_input_lower:
                        respuesta = "¡De nada! 😊 Si tienes más preguntas, no dudes en consultarme. Estoy aquí para ayudarte."
                    elif "adiós" in user_input_lower or "hasta luego" in user_input_lower:
                        respuesta = "¡Hasta luego! 👋 Que tengas un excelente día. Recuerda que siempre puedes volver si necesitas ayuda."
                    else:
                        respuesta = """Entiendo tu consulta. 🤔 

Nuestro equipo está trabajando para implementar respuestas más inteligentes. Mientras tanto, puedes:

• Explorar nuestro **Agente de RRHH** para entrevistas virtuales
• Usar el **Formulario de Contacto** para candidatos
• Contactar directamente con nuestro equipo

¿Hay algo específico en lo que pueda ayudarte?"""
                    
                    # Agregar respuesta al historial
                    st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error al procesar tu mensaje: {str(e)}")
            else:
                st.warning("Por favor, escribe un mensaje antes de enviar.")
                
    # Información adicional en la barra lateral
    with st.sidebar:
        st.markdown("### 💡 Consejos")
        st.info("""
        **Puedes preguntarme sobre:**
        - Servicios de Adaptiera
        - Proceso de entrevistas
        - Formularios de contacto
        - Información general
        """)
        
        if st.button("🗑️ Limpiar conversación"):
            st.session_state.mensajes = [{
                "role": "assistant", 
                "content": "¡Hola! 👋 Soy el asistente virtual de Adaptiera. ¿En qué puedo ayudarte hoy?"
            }]
            st.rerun()
