import pandas as pd
import streamlit as st
import numpy as np



if "df" not in st.session_state:
    st.session_state.df = None

st.session_state.df = pd.read_csv('pages/todos_productos.csv')

st.title("Tiendas Online Panamá")




def search(query,df):
    # If query is a string, split it by commas into a list
    if isinstance(query, str):
        query = query.split(',')

    # Remove leading and trailing white space from each word in the query
    query = [word.strip() for word in query]

    # Join the words with '|' to create a pattern for str.contains
    query = '|'.join(query)

    # Return products where any word in the query is found in the 'name' column

    # New columns
    df['search'] = df['name'] + " " + df["brand"] + " " + df["category"]
    return df[df['search'].str.contains(query, case=False, na=False)]



tipo_de_busqueda = st.radio("Selecciona un tipo de búsqueda", ["Por nombre de producto", "Por categoría"])

if tipo_de_busqueda == "Por nombre de producto":
    producto = st.text_input("Qué producto busca?")
    if len(producto) >= 1:
        filtered_df = st.session_state.df.drop(['page', 'availability', 'time'], axis=1)
    
        if ',' in producto:
    
            filtered_df = search(producto, filtered_df)
        else:
            filtered_df = filtered_df[filtered_df['name'].str.contains(producto, case=False, na=False)]
    
        col1, col2 = st.columns(2)
    
        tiendas = col1.multiselect("Filtrar tiendas", options=filtered_df['website'].unique(), default=filtered_df['website'].unique())
    
        marcas = col2.multiselect("Filtrar Marcas", options=filtered_df['brand'].unique(), default=filtered_df['brand'].unique())
    
        categorias = st.multiselect("Filtrar Categorías", options=filtered_df['category'].unique(), default=filtered_df['category'].unique())
    
        filtered_df = filtered_df[(filtered_df['website'].isin(tiendas)) & (filtered_df['brand'].isin(marcas))& (filtered_df['category'].isin(categorias))].sort_values("original_price")
    
        st.dataframe(filtered_df,use_container_width=True)
    else:
        pass
elif tipo_de_busqueda == "Por categoría":
    col1, col2 = st.columns(2)

    categorias = col1.multiselect("Categorías", np.sort(st.session_state.df['category'].unique(),axis=None))
    tiendas = col2.multiselect("Tiendas", np.sort(st.session_state.df['website'].unique(),axis=None))
    producto = st.text_input("Características del producto")
    filtered_df = st.session_state.df.drop(['page', 'availability', 'time'], axis=1)
    if len(categorias) >= 1:
        filtered_df = filtered_df[(st.session_state.df['category'].isin(categorias))]
    if len(tiendas) >= 1:
        filtered_df = filtered_df[(st.session_state.df['website'].isin(tiendas))]
    
    if len(producto) >= 1:
        filtered_df=search(producto, filtered_df)
    else:
        pass

    st.dataframe(filtered_df.head(200),use_container_width=True)
    st.write(f"{len(filtered_df)} resultados")
    
                                  
