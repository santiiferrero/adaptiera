import streamlit as st
from views import formulario, chatbot

st.title("Portal Principal")

formulario.mostrar_formulario()
st.markdown("---")
#chatbot.lanzar_chatbot()
