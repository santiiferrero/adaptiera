import streamlit as st

def input_field(label, key):
    return st.text_input(label, key=key)
