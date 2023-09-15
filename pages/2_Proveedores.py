# import streamlit as st
# import funciones as func
# import streamlit as st
# import time



# st.title(":mag: Proveedores")


# # session state for token


# # Google api
# google_api = func.credenciales_google()
# # Categorías:


# bform = st.form("F2")

# ubicacion = bform.selectbox("Ubicación", ["Ciudad de Panamá, Panamá", "San Miguelito,Panamá, Panamá",
#                                             "Tocumen, Panamá, Panamá", "David, Chiriquí, Panamá", "Arraiján, Panamá Oeste, Panamá",
#                                             "Colón, Colón, Panamá", "Chorrera, Panamá Oeste, Panamá", "Santiago, Veraguas, Panamá",
#                                             "Chitré, Herrera, Panamá", "Penonomé, Coclé, Panamá", "Aguadulce, Coclé, Panamá",
#                                             "Las Tablas, Los Santos, Panamá", "Pedregal, Chiriquí, Panamá", "Arraiján, Panamá",
#                                             "Capira, Panamá", "Chepo, Panamá"])
# radio = 5000

# categoria = bform.text_input("Categoría")

# boton = bform.form_submit_button("Buscar")

# if boton:
#     provs = func.get_places(api_key=google_api, location=ubicacion, radius=radio, category=categoria, region="pa")
#     token = provs[1]
#     provs = provs[0]
    
#     if 'token' not in st.session_state:
#         st.session_state['token'] = None
    
    
#     if token != None:
#         st.session_state['token'] = token
#         time.sleep(2)
#         alist = func.get_places(api_key=google_api, location=ubicacion, radius=radio, category=categoria, region="pa", token=st.session_state['token'])
#         for x in alist[0]:
#             provs.append(x)

#         atoken = alist[1]
#         if atoken is not None:
#             st.session_state['token'] = atoken
#             time.sleep(2)
#             blist = func.get_places(api_key=google_api, location=ubicacion, radius=radio, category=categoria, region="pa", token=st.session_state['token'])
#             for x in blist[0]:
#                 provs.append(x)
                
#     for key in st.session_state.keys():
#         del st.session_state[key]
     

#     provs = func.sort_dicts_by_keys(provs, ['puntaje', 'user_ratings_total'])
#     numeros = []
#     nombres = []

#     for x in provs:
#         if 'formatted_phone_number' in provs[provs.index(x)]:
#             numeros.append(x['formatted_phone_number'])
#         if 'name' in provs[provs.index(x)]:
#             nombres.append(x['name'])



#     st.download_button(label="**Descargar números**", data=func.create_csv(numeros, nombres),file_name=f'numeros_proveedores.csv', mime='text/csv')
#     for x in provs:
#         if 'name' in provs[provs.index(x)].keys():
#             st.write(f'Nombre: **{provs[provs.index(x)]["name"]}**')
#         if 'formatted_address' in provs[provs.index(x)].keys():
#             st.write(f'Dirección: {provs[provs.index(x)]["formatted_address"]}')
#         if 'formatted_phone_number' in provs[provs.index(x)].keys():
#             st.write(f'Teléfono: {provs[provs.index(x)]["formatted_phone_number"]}')
#         if 'user_ratings_total' in provs[provs.index(x)].keys():
#             st.write(f'N Reviews: {provs[provs.index(x)]["user_ratings_total"]}')
#         if 'rating' in provs[provs.index(x)].keys():
#             st.write(f'Rating: {provs[provs.index(x)]["rating"]}')
#         if 'puntaje' in provs[provs.index(x)].keys():
#             st.write(f'Puntaje: {provs[provs.index(x)]["puntaje"]}')
#         st.write('---------------------------------------------')


import streamlit as st
import funciones as func
import time

st.title(":mag: Proveedores")

# Initialize Google API credentials
google_api = func.credenciales_google()

# Create form
bform = st.form("F2")

# Location select box
ubicacion = bform.selectbox("Ubicación", [
    "Ciudad de Panamá, Panamá", "San Miguelito,Panamá, Panamá",
    "Tocumen, Panamá, Panamá", "David, Chiriquí, Panamá", 
    "Arraiján, Panamá Oeste, Panamá", "Colón, Colón, Panamá", 
    "Chorrera, Panamá Oeste, Panamá", "Santiago, Veraguas, Panamá",
    "Chitré, Herrera, Panamá", "Penonomé, Coclé, Panamá", 
    "Aguadulce, Coclé, Panamá", "Las Tablas, Los Santos, Panamá", 
    "Pedregal, Chiriquí, Panamá", "Arraiján, Panamá", 
    "Capira, Panamá", "Chepo, Panamá"
])

# Search radius and category text input
radio = 5000
categoria = bform.text_input("Categoría")

# Submit button
boton = bform.form_submit_button("Buscar")

def fetch_data(api_key, location, radius, category, region, token=None):
    # This function can be used to fetch data recursively and handle pagination.
    data, next_token = func.get_places(api_key=api_key, location=location, radius=radius, category=category, region=region, token=token)
    if next_token:
        time.sleep(2)
        next_data = fetch_data(api_key, location, radius, category, region, next_token)
        data.extend(next_data)
    return data

if boton:
    # Fetch data from Google Places API
    provs = fetch_data(api_key=google_api, location=ubicacion, radius=radio, category=categoria, region="pa")
    
    # Sort data
    provs = func.sort_dicts_by_keys(provs, ['puntaje', 'user_ratings_total'])

    # Store data in session state to retain it between interactions
    st.session_state['provs'] = provs

# If data is present in session state, display it and offer download button
if 'provs' in st.session_state:
    numeros = []
    nombres = []

    for x in st.session_state['provs']:
        if 'formatted_phone_number' in x:
            numeros.append(x['formatted_phone_number'])
        if 'name' in x:
            nombres.append(x['name'])

    if numeros and nombres:
        st.download_button(label="**Descargar números**", data=func.create_csv(numeros, nombres), file_name='numeros_proveedores.csv', mime='text/csv')
    
    for x in st.session_state['provs']:
       # Displaying each provider's details in the streamlit app
        if 'name' in x:
            st.write(f'Nombre: **{x["name"]}**')
        if 'formatted_address' in x:
            st.write(f'Dirección: {x["formatted_address"]}')
        if 'formatted_phone_number' in x:
            st.write(f'Teléfono: {x["formatted_phone_number"]}')
        if 'user_ratings_total' in x:
            st.write(f'N Reviews: {x["user_ratings_total"]}')
        if 'rating' in x:
            st.write(f'Rating: {x["rating"]}')
        if 'puntaje' in x:
            st.write(f'Puntaje: {x["puntaje"]}')
        st.write('---------------------------------------------')
