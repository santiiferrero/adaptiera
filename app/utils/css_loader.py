import streamlit as st
from pathlib import Path

def load_css_file(css_file_path):
    """
    Carga un archivo CSS y lo aplica en Streamlit
    
    Args:
        css_file_path (str): Ruta al archivo CSS
    """
    try:
        css_path = Path(css_file_path)
        if css_path.exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            st.markdown(f"""
            <style>
            {css_content}
            </style>
            """, unsafe_allow_html=True)
            return True
        else:
            st.warning(f"Archivo CSS no encontrado: {css_file_path}")
            return False
    except Exception as e:
        st.error(f"Error al cargar CSS: {str(e)}")
        return False

def inject_chat_styles():
    """
    Inyecta estilos CSS específicos para los mensajes de chat
    """
    css_styles = """
    <style>
    /* Estilos CSS para mensajes de chat - Adaptiera */
    
    /* MENSAJES DEL USUARIO - Fondo azul con texto blanco */
    [data-testid="chat-message-user"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 18px 18px 4px 18px !important;
        margin-left: 20% !important;
        border: none !important;
        padding: 12px 16px !important;
    }
    
    /* Todos los elementos dentro de mensajes del usuario */
    [data-testid="chat-message-user"] *,
    [data-testid="chat-message-user"] .stMarkdown,
    [data-testid="chat-message-user"] .stMarkdown *,
    [data-testid="chat-message-user"] p,
    [data-testid="chat-message-user"] div,
    [data-testid="chat-message-user"] span,
    [data-testid="chat-message-user"] strong,
    [data-testid="chat-message-user"] em {
        color: white !important;
        background-color: transparent !important;
    }
    
    /* MENSAJES DEL ASISTENTE - Fondo gris con texto negro */
    [data-testid="chat-message-assistant"] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
        color: #212529 !important;
        border-radius: 18px 18px 18px 4px !important;
        margin-right: 20% !important;
        border-left: 4px solid #28a745 !important;
        padding: 12px 16px !important;
    }
    
    /* Todos los elementos dentro de mensajes del asistente */
    [data-testid="chat-message-assistant"] *,
    [data-testid="chat-message-assistant"] .stMarkdown,
    [data-testid="chat-message-assistant"] .stMarkdown *,
    [data-testid="chat-message-assistant"] p,
    [data-testid="chat-message-assistant"] div,
    [data-testid="chat-message-assistant"] span,
    [data-testid="chat-message-assistant"] strong,
    [data-testid="chat-message-assistant"] em {
        color: #212529 !important;
        background-color: transparent !important;
    }
    
    /* Avatares */
    [data-testid="chat-message-user"] img {
        background-color: #667eea !important;
        border-radius: 50% !important;
    }
    
    [data-testid="chat-message-assistant"] img {
        background-color: #28a745 !important;
        border-radius: 50% !important;
    }
    
    /* Input del chat */
    .stChatInput textarea,
    [data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #212529 !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
    }
    
    .stChatInput textarea:focus,
    [data-testid="stChatInput"] textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25) !important;
    }
    
    /* Botón de envío */
    .stChatInput button,
    [data-testid="stChatInput"] button {
        background-color: #667eea !important;
        color: white !important;
        border-radius: 50% !important;
        border: none !important;
        width: 40px !important;
        height: 40px !important;
    }
    
    .stChatInput button:hover,
    [data-testid="stChatInput"] button:hover {
        background-color: #5a6fd8 !important;
        transform: scale(1.05) !important;
    }
    
    /* Selectores con mayor especificidad para forzar estilos */
    .stApp [data-testid="chat-message-user"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    .stApp [data-testid="chat-message-user"] * {
        color: white !important;
    }
    
    .stApp [data-testid="chat-message-assistant"] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
    }
    
    .stApp [data-testid="chat-message-assistant"] * {
        color: #212529 !important;
    }
    </style>
    """
    
    st.markdown(css_styles, unsafe_allow_html=True)

def inject_chatbot_styles():
    """
    Inyecta estilos CSS específicos para el chatbot
    """
    css_styles = """
    <style>
    /* Estilos específicos para el chatbot */
    
    /* MENSAJES DEL USUARIO - Fondo azul turquesa con texto blanco */
    [data-testid="chat-message-user"] {
        background: linear-gradient(135deg, #17a2b8 0%, #138496 100%) !important;
        color: white !important;
        border-radius: 18px 18px 4px 18px !important;
        margin-left: 15% !important;
        padding: 12px 16px !important;
        border: none !important;
    }
    
    [data-testid="chat-message-user"] *,
    [data-testid="chat-message-user"] .stMarkdown,
    [data-testid="chat-message-user"] .stMarkdown *,
    [data-testid="chat-message-user"] p,
    [data-testid="chat-message-user"] div,
    [data-testid="chat-message-user"] span,
    [data-testid="chat-message-user"] strong,
    [data-testid="chat-message-user"] em {
        color: white !important;
        background-color: transparent !important;
        font-weight: 500 !important;
    }
    
    /* MENSAJES DEL ASISTENTE - Fondo gris con texto negro */
    [data-testid="chat-message-assistant"] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
        color: #212529 !important;
        border-radius: 18px 18px 18px 4px !important;
        margin-right: 15% !important;
        border-left: 4px solid #17a2b8 !important;
        padding: 12px 16px !important;
    }
    
    [data-testid="chat-message-assistant"] *,
    [data-testid="chat-message-assistant"] .stMarkdown,
    [data-testid="chat-message-assistant"] .stMarkdown *,
    [data-testid="chat-message-assistant"] p,
    [data-testid="chat-message-assistant"] div,
    [data-testid="chat-message-assistant"] span,
    [data-testid="chat-message-assistant"] strong,
    [data-testid="chat-message-assistant"] em {
        color: #212529 !important;
        background-color: transparent !important;
    }
    
    /* Avatares del chatbot */
    [data-testid="chat-message-user"] img {
        background-color: #17a2b8 !important;
        border-radius: 50% !important;
    }
    
    [data-testid="chat-message-assistant"] img {
        background-color: #17a2b8 !important;
        border-radius: 50% !important;
    }
    
    /* Input del chatbot */
    .stChatInput textarea,
    [data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #212529 !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
        font-size: 14px !important;
    }
    
    .stChatInput textarea:focus,
    [data-testid="stChatInput"] textarea:focus {
        border-color: #17a2b8 !important;
        box-shadow: 0 0 0 0.2rem rgba(23, 162, 184, 0.25) !important;
    }
    
    .stChatInput button,
    [data-testid="stChatInput"] button {
        background-color: #17a2b8 !important;
        color: white !important;
        border-radius: 50% !important;
        border: none !important;
        width: 40px !important;
        height: 40px !important;
    }
    
    .stChatInput button:hover,
    [data-testid="stChatInput"] button:hover {
        background-color: #138496 !important;
        transform: scale(1.05) !important;
    }
    
    /* Header del chatbot */
    .chatbot-header {
        text-align: center;
        padding: 15px;
        background: linear-gradient(90deg, #17a2b8 0%, #138496 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    
    /* Forzar estilos con mayor especificidad */
    .stApp [data-testid="chat-message-user"] {
        background: linear-gradient(135deg, #17a2b8 0%, #138496 100%) !important;
    }
    
    .stApp [data-testid="chat-message-user"] * {
        color: white !important;
    }
    
    .stApp [data-testid="chat-message-assistant"] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
    }
    
    .stApp [data-testid="chat-message-assistant"] * {
        color: #212529 !important;
    }
    </style>
    """
    
    st.markdown(css_styles, unsafe_allow_html=True) 