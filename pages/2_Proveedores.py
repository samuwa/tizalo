import streamlit as st
import funciones as func
import streamlit as st



st.title(":mag: Proveedores")


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
    provs = func.get_places(api_key=google_api, location=ubicacion, radius=radio, category=categoria, region="pa")
    token = provs[1]
    provs = provs[0]
    
    st.write(type(token))

    if token is None:
      break
     else:
       alist = func.get_places(api_key=google_api, location=ubicacion, radius=radio, category=categoria, region="pa", token=token)
       for x in alist[0]:
           provs.append(x)

#         atoken = alist[1]
#         if atoken is not None and type(atoken) == str:
#             blist = func.get_places(api_key=google_api, location=ubicacion, radius=radio, category=categoria, region="pa", token=atoken)
#             for x in blist[0]:
#                 provs.append(x)

    provs = func.sort_dicts_by_keys(provs, ['puntaje', 'user_ratings_total'])
    numeros = []

    for x in provs:
        if 'formatted_phone_number' in provs[provs.index(x)]:
            numeros.append(x['formatted_phone_number'])


    st.download_button(label="**Descargar números**", data=func.create_csv(numeros),file_name=f'numeros_proveedores.csv', mime='text/csv')
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
