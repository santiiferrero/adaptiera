import streamlit as st
from services.gmail import enviar_email

def mostrar_formulario():
    st.subheader("Formulario de contacto")
    nombre = st.text_input("Nombre")
    email = st.text_input("Email")
    mensaje = st.text_area("Mensaje")

    if st.button("Enviar"):
        enviar_email(nombre, email, mensaje)
        st.success("Correo enviado correctamente.")
