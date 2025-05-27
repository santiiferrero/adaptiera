import streamlit as st
import sys
from pathlib import Path

# Agregar el directorio raíz al path para las importaciones
current_dir = Path(__file__).parent
root_dir = current_dir.parent
sys.path.insert(0, str(root_dir))

# Importaciones usando rutas relativas
try:
    from app.views.form import mostrar_formulario
    from app.views.chatbot import lanzar_chatbot
    from app.views.form_candidate_contact import mostrar_formulario as mostrar_formulario_candidatos
    from app.views.rrhh_agent import mostrar_agente_rrhh
except ImportError:
    # Fallback para importaciones directas si no funciona el path
    from views.form import mostrar_formulario
    from views.chatbot import lanzar_chatbot
    from views.form_candidate_contact import mostrar_formulario as mostrar_formulario_candidatos
    from views.rrhh_agent import mostrar_agente_rrhh

# Configuración de la página
st.set_page_config(
    page_title="Adaptiera - Portal Principal",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS global para mejorar la apariencia
GLOBAL_CSS = """
<style>
/* Estilos globales para toda la aplicación */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Mejorar la apariencia del sidebar */
.css-1d391kg {
    background-color: #f8f9fa;
}

/* Estilos para títulos y headers */
h1, h2, h3 {
    color: #2c3e50;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Mejorar la apariencia de los selectbox */
.stSelectbox > div > div {
    background-color: white;
    border: 2px solid #dee2e6;
    border-radius: 8px;
}

.stSelectbox > div > div:focus-within {
    border-color: #667eea;
    box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

/* Estilos para botones */
.stButton > button {
    border-radius: 8px;
    border: none;
    padding: 0.5rem 1rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Mejorar la apariencia de las columnas */
.element-container {
    margin-bottom: 1rem;
}

/* Estilos para info boxes */
.stInfo {
    background-color: #e3f2fd;
    border-left: 4px solid #2196f3;
    border-radius: 8px;
}

.stSuccess {
    background-color: #e8f5e8;
    border-left: 4px solid #4caf50;
    border-radius: 8px;
}

.stWarning {
    background-color: #fff3e0;
    border-left: 4px solid #ff9800;
    border-radius: 8px;
}

.stError {
    background-color: #ffebee;
    border-left: 4px solid #f44336;
    border-radius: 8px;
}

/* Mejorar la apariencia de las imágenes */
.stImage {
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Estilos para el pie de página */
.footer {
    text-align: center;
    padding: 20px;
    color: #6c757d;
    border-top: 1px solid #dee2e6;
    margin-top: 2rem;
}

/* Mejorar la apariencia de los expanders */
.streamlit-expanderHeader {
    background-color: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #dee2e6;
}

/* Animaciones suaves */
* {
    transition: all 0.3s ease;
}

/* Mejorar la legibilidad del texto */
.stMarkdown {
    line-height: 1.6;
}

/* Estilos para métricas */
.metric-container {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid #667eea;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

/* Contenedor principal con mejor espaciado */
.main-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Mejorar la apariencia de las pestañas */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 16px;
}
</style>
"""

# Aplicar estilos globales
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# Título principal
st.title("🚀 Adaptiera - Portal Principal")
st.markdown("### Plataforma de reclutamiento y atención al candidato")

# Menú en la barra lateral
st.sidebar.title("📋 Menú")
st.sidebar.markdown("Selecciona una opción para comenzar:")

opciones = [
    "Seleccione una opción...", 
    "Agente de RRHH - Entrevista Virtual", 
    "Formulario de Contacto de Candidato", 
    "Chatbot"
]
opcion = st.sidebar.selectbox("Opciones disponibles:", opciones, label_visibility="collapsed")

# Mostrar el contenido según la opción seleccionada
if opcion == "Seleccione una opción..." or opcion is None:
    # Pantalla de bienvenida
    st.image("https://via.placeholder.com/800x300?text=Adaptiera", use_container_width=True)
    
    st.header("Bienvenido a Adaptiera")
    st.markdown("""
    ### Plataforma integral de reclutamiento y selección
    
    Selecciona una opción del menú lateral para comenzar:
    
    - **Agente de RRHH - Entrevista Virtual**: Realiza una entrevista automatizada con nuestro agente inteligente.
    - **Formulario de Contacto de Candidato**: Invita a candidatos a participar en procesos de selección.
    - **Chatbot**: Interactúa con nuestro asistente virtual para resolver dudas.
    """)
    
    # Crear dos columnas para mostrar características
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 Entrevistas Inteligentes")
        st.markdown("""
        - **Agente de RRHH automatizado** con IA
        - Evaluación inteligente de respuestas
        - Proceso de entrevista personalizado
        - Resúmenes automáticos y reportes
        """)
    
    with col2:
        st.subheader("📋 Gestión Completa")
        st.markdown("""
        - Formularios de contacto automatizados
        - Atención 24/7 con chatbot
        - Seguimiento efectivo de candidatos
        - Experiencia optimizada
        """)
    
    # Información adicional
    st.markdown("---")
    st.info("💡 **Consejo**: Utiliza nuestro agente de RRHH para realizar entrevistas automatizadas y obtener evaluaciones detalladas de candidatos.")

elif opcion == "Agente de RRHH - Entrevista Virtual":
    mostrar_agente_rrhh()
    
elif opcion == "Formulario de Contacto de Candidato":
    st.header("📝 Formulario de Contacto de Candidato")
    st.markdown("Complete el formulario para invitar a un candidato al proceso de selección.")
    mostrar_formulario_candidatos()
    
elif opcion == "Chatbot":
    lanzar_chatbot()

# Pie de página mejorado
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>© 2025 Adaptiera. Todos los derechos reservados.</p>
    <p>Plataforma de reclutamiento inteligente con IA</p>
</div>
""", unsafe_allow_html=True)