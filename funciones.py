import openai
import googlemaps
from googlemaps.exceptions import ApiError
import streamlit as st
import requests
import PyPDF2
from io import StringIO
import warnings
import pandas as pd
import re

# Credenciales

def gpt_answer(prompt):
    openai_key = st.secrets['GPT_API']

    openai.api_key = openai_key
    model_engine = "text-davinci-003"

    prompt = prompt

    max_tokens = 1024

    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return completion.choices[0].text





def credenciales_google():
    api_key = st.secrets['google_api']
    return api_key


# Determinar el puntaje en base a la cantidad de reviews que tiene


def puntos_extra(user_ratings_total):
    if int(user_ratings_total) >= 6 and int(user_ratings_total) <= 10:
        return 1
    elif int(user_ratings_total) >= 11 and int(user_ratings_total) <= 20:
        return 2
    elif int(user_ratings_total) >= 21:
        return 3
    else:
        return 0


# Ordenar proveedores

def sort_dicts_by_keys(dicts, keys, default_values=None, reverse=True):
    if default_values is None:
        default_values = [-float('inf') if reverse else float('inf')] * len(keys)

    # Custom sorting key function that handles missing keys
    def sort_key_func(item):
        return [item.get(key, default_value) for key, default_value in zip(keys, default_values)]

    return sorted(dicts, key=sort_key_func, reverse=reverse)# Conseguir Proveedores
# Conseguir Proveedores

def get_places(api_key, categories, location, radius, results_per_page=20):
    adict_list = []
    categories = categories.split(',')

    gmaps = googlemaps.Client(api_key, timeout=10)
    geocode_result = gmaps.geocode(location, region='pa')
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    location = f"{lat},{lng}"

    for category in categories:
        category = category.strip()
        try:
            places_result = gmaps.places(query=category, location=location, radius=radius, region='pa', language="es")
            while True:
                for place in places_result['results']:
                    if 'rating' in place and place['rating'] >= 3.7:
                        adict = {}
                        adict['name'] = place.get('name', None)
                        adict['formatted_address'] = place.get('formatted_address', None)
                        adict['formatted_phone_number'] = place.get('formatted_phone_number', None)
                        adict['user_ratings_total'] = place.get('user_ratings_total', None)
                        adict['rating'] = place.get('rating', None)
                        adict["category"] = category
                        adict_list.append(adict)

                if 'next_page_token' not in places_result:
                    break  # No more pages available

                page_token = places_result['next_page_token']
                places_result = gmaps.places(query=category, location=location, radius=radius, region='pa', language="es", page_token=page_token)

        except googlemaps.exceptions.ApiError as e:
            print(e)
            st.write(e)

    return adict_list



def read_pdf(file_obj):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        pdf_reader = PyPDF2.PdfFileReader(file_obj)
    num_pages = pdf_reader.numPages
    text = StringIO()

    for page in range(num_pages):
        text.write(pdf_reader.getPage(page).extractText())

    return text.getvalue()

def chat_gpt_summarize(api_key, document):
    openai.api_key = api_key

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"De que trata la siguiente cotizacion: {document}",
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    summary = response.choices[0].text.strip()
    return summary


def summarize_pdf(api_key, pdf_file_obj):
    pdf_text = read_pdf(pdf_file_obj)
    summary = chat_gpt_summarize(api_key, pdf_text)
    return summary

def clean_number(x):
    return re.sub(r'\D', '', str(x))


def create_csv(numbers):
    # Convert the input list to a Pandas DataFrame
    df = pd.DataFrame(numbers, columns=['number'])

    # Remove non-numeric elements from the list and convert to int with "507" added to the beginning
    df['number'] = df['number'].apply(clean_number)
    df['number'] = df['number'].apply(lambda x: '507' + x if not x.startswith('507') else x)

    # Filter rows with exactly eleven digits
    df = df[df['number'].str.len() == 11]

    df['number'] = pd.to_numeric(df['number'], downcast='integer', errors='coerce')

    # Add empty columns for "body" and "name"
    df['body'] = ''
    df['name'] = ''

    # Rearrange the columns in the desired order
    df = df[['number', 'body', 'name']]
    return df.to_csv(index=False, encoding='utf-8').encode('utf-8')

    # Write the data to a CSV file and return as byte string
    return df.to_csv(index=False, encoding='utf-8').encode('utf-8')
