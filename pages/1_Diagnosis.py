import streamlit as st
import funciones as func
import streamlit as st






st.title(":female-scientist: Diagnosis")

aform = st.form("F1")

mensaje = aform.text_input("Qué necesita el cliente?")
st.info("Solamente indique que necesita el cliente. Ej: Plomeria, Utiles escolares, transporte terrestre, etc.")

boton = aform.form_submit_button("Preguntar")

if boton:

    respuesta = func.gpt_answer(mensaje)

    st.write(respuesta)
