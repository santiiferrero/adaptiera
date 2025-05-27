import streamlit as st
from services.email_sender import enviar_correo

def mostrar_formulario():
    st.subheader("Formulario de contacto")
    nombre = st.text_input("Nombre")
    email = st.text_input("Email")
    mensaje = st.text_area("Mensaje")

    if st.button("Enviar"):
        enviar_correo(destinatario=email, asunto=f"Mensaje de {nombre}", cuerpo=mensaje)
        st.success("Correo enviado correctamente.")
