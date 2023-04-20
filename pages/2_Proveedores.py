import streamlit as st
import funciones as func
import streamlit as st



st.title(":mag: Proveedores")


# Google api
google_api = func.credenciales_google()
# Categorías:

categorias = ['Electricista','Plomero','Pintura','Iluminación','Gypsero','Ebanista','Mobiliario','Aires Acondicionados','Decoradores',
              'Co-workings','Papel de pared','Cerrajero','Pintura Industrial','Instalador','Sistema de Bombeo','Albañil','Cielo Rasos','Soldadura',
              'Techos','Ventanas','Vidrio','Tapicería','Fumigación','Pulido de pisos','Limpieza interna','Lavandería','Limpieza de ventanas',
              'Limpieza de alfombras','Recolección de Basura','Recolección de Reciclaje','Guindolas','Andamios','Plataformas Elevadas','Vigilancia',
              'Cámaras de seguridad','Control de acceso','Background Checks','Ciberseguridad','Sistemas de alarmas','Logística terreste',
              'Logistica maritima','Talleres','Servicios de mensajeria','Repuestos para autos','Sensores de incendio','Fugas de gas','Estudios de impacto ambiental',
              'Estudio de suelo','Event Planners','Entretenimiento','Reservaciones','Almuerzos ejecutivos','Catering','Eventos deportivos','Floristería',
              'Proveedor de Wifi','Red telefonica','Agencias de viaje','Planes de turismo','Alquiler de yates','Seguro de responsabilidad civil',
              'Seguros de vida','Seguros de salud privado','Seguros de vehiculos','Seguros contra robos','Servicios de traducción','Call Centers',
              'Staff On Demand','Head Hunters','Digitalización de documentos','Auditoría','Servicio de impresión','Servicio de notaría','Contabilidad',
              'Servicios legales','Laboratorios médicos','Campañas de mercadeo','Membresías de gimnasio/ Reservaciones de canchas',
              'Autolavados','Clases particulares para niños','Guarderias','Recursos Humanos','Pasarelas de pago',
              'Consultores de nube','Soporte técnico','Útiles de oficina','Articulos de limpieza','Snacks','Bebidas alcoholicas',
              'Desechables','Dispensadores de agua',
              'Tanques de gas','Linea Blanca','Uniformes','Bordados','Frutas y Verduras', "fontanero"]

categorias = categorias.sort()

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