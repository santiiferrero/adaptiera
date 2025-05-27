import streamlit as st

def lanzar_chatbot():
    st.subheader("Chatbot")
    
    # Inicializar historial de chat en session state si no existe
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
    
    # Mostrar historial de mensajes
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])
    
    # Campo para nuevo mensaje
    if prompt := st.chat_input("Escribe tu mensaje aquí..."):
        # Agregar mensaje del usuario al historial
        st.session_state.mensajes.append({"role": "user", "content": prompt})
        
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Procesar respuesta del chatbot
        try:
            # Respuesta simple para pruebas
            user_input = prompt.lower()
            
            if "hola" in user_input or "saludos" in user_input:
                respuesta = "¡Hola! ¿En qué puedo ayudarte hoy?"
            elif "ayuda" in user_input:
                respuesta = "Estoy aquí para ayudarte. Puedes preguntarme sobre nuestros servicios, formularios o cualquier otra información."
            elif "gracias" in user_input:
                respuesta = "¡De nada! Si tienes más preguntas, no dudes en consultarme."
            else:
                respuesta = "Entiendo tu consulta. Nuestro equipo está trabajando para implementar respuestas más inteligentes. ¿Puedo ayudarte con algo más?"
            
            # Agregar respuesta al historial
            st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
            
            # Mostrar respuesta
            with st.chat_message("assistant"):
                st.markdown(respuesta)
        except Exception as e:
            st.error(f"Error al procesar tu mensaje: {str(e)}")
