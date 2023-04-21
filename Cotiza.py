import streamlit as st


st.set_page_config(
    page_title="Cotiza :mechanical_arm:",
    page_icon=":mechanical_arm:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": "https://github.com/streamlit/streamlit/issues/new/choose"
    },
    metadata={
        "google-site-verification": "google6ac22868640d7e2c.html"
    }
)

st.title("Cotiza :mechanical_arm:")

st.markdown('''

MVP descubrimiento y organizador de cotizaciones.

    Diagnosis: Encontrar posibles soluciones a un problema y entender los paramentros necesarios para cotizar cada solución.
    
    Proveedores: Encontrar proveedores relevantes para cada solución.

''')
