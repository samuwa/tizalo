import streamlit as st
import funciones as func
import streamlit as st
import time



st.title(":mag: Proveedores")

# Session state for provs

if "provs" not in st.session_state:
  st.session_state.provs = None
# session state for token


# Google api
google_api = func.credenciales_google()
# Categorías:


bform = st.form("F2")

ubicacion = bform.selectbox("Ubicación", ["Ciudad de Panamá, Panamá", "San Miguelito,Panamá, Panamá",
                                            "Tocumen, Panamá, Panamá", "David, Chiriquí, Panamá", "Arraiján, Panamá Oeste, Panamá",
                                            "Colón, Colón, Panamá", "Chorrera, Panamá Oeste, Panamá", "Santiago, Veraguas, Panamá",
                                            "Chitré, Herrera, Panamá", "Penonomé, Coclé, Panamá", "Aguadulce, Coclé, Panamá",
                                            "Las Tablas, Los Santos, Panamá", "Pedregal, Chiriquí, Panamá", "Arraiján, Panamá",
                                            "Capira, Panamá", "Chepo, Panamá"])
radio = 5000

categoria = bform.text_input("Categoría")

boton = bform.form_submit_button("Buscar")

if boton:
    st.session_state.provs = func.get_places(api_key=google_api, location=ubicacion, radius=radio, category=categoria, region="pa")
    token = st.session_state.provs[1]
    st.session_state.provs = st.session_state.provs[0]
    
    if 'token' not in st.session_state:
        st.session_state['token'] = None
    
    
    if token != None:
        st.session_state['token'] = token
        time.sleep(2)
        alist = func.get_places(api_key=google_api, location=ubicacion, radius=radio, category=categoria, region="pa", token=st.session_state['token'])
        for x in alist[0]:
            st.session_state.provs.append(x)

        atoken = alist[1]
        if atoken is not None:
            st.session_state['token'] = atoken
            time.sleep(2)
            blist = func.get_places(api_key=google_api, location=ubicacion, radius=radio, category=categoria, region="pa", token=st.session_state['token'])
            for x in blist[0]:
                st.session_state.provs.append(x)
                
    for key in st.session_state.keys():
        del st.session_state[key]
     

    st.session_state.provs = func.sort_dicts_by_keys(st.session_state.provs, ['puntaje', 'user_ratings_total'])
    numeros = []
    nombres = []

    for x in st.session_state.provs:
        if 'formatted_phone_number' in st.session_state.provs[st.session_state.provs.index(x)]:
            numeros.append(x['formatted_phone_number'])
        if 'name' in st.session_state.provs[st.session_state.provs.index(x)]:
            nombres.append(x['name'])



    st.download_button(label="**Descargar números**", data=func.create_csv(numeros, nombres),file_name=f'numeros_proveedores.csv', mime='text/csv')
    for x in st.session_state.provs:
        if 'name' in st.session_state.provs[st.session_state.provs.index(x)].keys():
            st.write(f'Nombre: **{st.session_state.provs[st.session_state.provs.index(x)]["name"]}**')
        if 'formatted_address' in st.session_state.provs[st.session_state.provs.index(x)].keys():
            st.write(f'Dirección: {st.session_state.provs[st.session_state.provs.index(x)]["formatted_address"]}')
        if 'formatted_phone_number' in st.session_state.provs[st.session_state.provs.index(x)].keys():
            st.write(f'Teléfono: {st.session_state.provs[st.session_state.provs.index(x)]["formatted_phone_number"]}')
        if 'user_ratings_total' in st.session_state.provs[st.session_state.provs.index(x)].keys():
            st.write(f'N Reviews: {st.session_state.provs[st.session_state.provs.index(x)]["user_ratings_total"]}')
        if 'rating' in st.session_state.provs[st.session_state.provs.index(x)].keys():
            st.write(f'Rating: {st.session_state.provs[st.session_state.provs.index(x)]["rating"]}')
        if 'puntaje' in st.session_state.provs[st.session_state.provs.index(x)].keys():
            st.write(f'Puntaje: {st.session_state.provs[st.session_state.provs.index(x)]["puntaje"]}')
        st.write('---------------------------------------------')
