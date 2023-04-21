import streamlit as st
import funciones as func
import streamlit as st



st.title(":mag: Proveedores")


# Google api
google_api = func.credenciales_google()
# Categorías:


bform = st.form("F2")

ubicacion = bform.text_input("Ubicación")
radio = 20000

categoria = bform.text_input("Categoría")

boton = bform.form_submit_button("Buscar")

if boton:
    provs = func.get_places(google_api, categoria, ubicacion, radio)
    for x in provs:
        if 'name' in provs[provs.index(x)].keys():
            st.write(f'Nombre: **{provs[provs.index(x)]["name"]}**')
        if 'formatted_address' in provs[provs.index(x)].keys():
            st.write(f'Dirección: {provs[provs.index(x)]["formatted_address"]}')
        if 'formatted_phone_number' in provs[provs.index(x)].keys():
            st.write(f'Teléfono: {provs[provs.index(x)]["formatted_phone_number"]}')
        if 'user_ratings_total' in provs[provs.index(x)].keys():
            st.write(f'N Reviews: {provs[provs.index(x)]["user_ratings_total"]}')
        if 'rating' in provs[provs.index(x)].keys():
            st.write(f'Rating: {provs[provs.index(x)]["rating"]}')
        if 'puntaje' in provs[provs.index(x)].keys():
            st.write(f'Puntaje: {provs[provs.index(x)]["puntaje"]}')
            st.write('---------------------------------------------')

    st.write(provs)
