import funciones as func
import streamlit as st


st.title(":mag: Recotizar")

uploaded = st.file_uploader("Agregar cotizacion existente")

if uploaded != None:
    st.write(func.summarize_pdf(st.secrets[GPT_API],uploaded))
