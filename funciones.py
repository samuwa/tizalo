import openai
import googlemaps
from googlemaps.exceptions import ApiError
import streamlit as st

# Credenciales

def gpt_answer(prompt):
    openai_key = "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"

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
    api_key = 'AIzaSyCwo3H7f87Wkks5T1-TbdGRhPt92YONRkY'
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

def sort_dicts_by_key(dicts, key, default_value=None, reverse=True):
    if default_value is None:
        default_value = -float('inf') if reverse else float('inf')

    # Custom sorting key function that handles missing keys
    def sort_key_func(item):
        return item.get(key, default_value)

    return sorted(dicts, key=sort_key_func, reverse=reverse)
# Conseguir Proveedores

def get_places(api_key, category, location, radius):
    adict_list = []
    try:
        gmaps = googlemaps.Client(api_key)
        # Use the Google Places API to search for businesses in the specified location and category
        places_result = gmaps.places(query=category, location=location, radius=radius)

        # Extract the place IDs for each result
        place_ids = [result['place_id'] for result in places_result['results']]

        # Use the Google Places API to get the details for each place, including its reviews, address, and phone number
        details_result = [gmaps.place(place_id, fields=['name', 'rating', 'user_ratings_total', 'formatted_address', 'formatted_phone_number']) for place_id in place_ids]

        # Print the details for each place
        for place in details_result: # place["result"]["parameter"]
            adict = {}
            if 'name' in place['result']:
                #print(f"Name: {place['result']['name']}")
                adict['name'] = place['result']['name']
            if 'formatted_address' in place['result']:
                #print(f"Address: {place['result']['formatted_address']}")
                adict['formatted_address'] = place['result']['formatted_address']
            if 'formatted_phone_number' in place['result']:
                #print(f"Phone number: {place['result']['formatted_phone_number']}")
                adict['formatted_phone_number'] = place['result']['formatted_phone_number']
            if 'user_ratings_total' in place['result']:
                #print(f"Number of reviews: {place['result']['user_ratings_total']}")
                adict['user_ratings_total'] = place['result']['user_ratings_total']
                adict['puntaje'] = place['result']['rating'] + puntos_extra(place['result']['user_ratings_total'])
            if 'rating' in place['result']:
                #print(f"Average rating: {place['result']['rating']}")
                adict['rating'] = place['result']['rating']
            adict["category"] = category

            # Si tiene 'user_ratings_total" --> Agregar un nuevo key "puntaje" que agregue rating in puntos_extra(user_ratings_total)



            adict_list.append(adict)
        #print()
    except ApiError as e:
        print(e)
    return sort_dicts_by_key(adict_list, key='puntaje')
