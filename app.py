import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt
import functions as functions

st.cache_data.clear() # Si tienes problemas con la cache, descomenta esta linea


# Configuración inicial del proyecto
st.set_page_config(
    page_title="Exploratory Data Analysis: Analisis medioambiental RSA2025",
    page_icon=":zap:",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Carga y procesamiento de datos
df = pd.read_csv("data/datos_rsa_limpio_final_2.csv")
df_clasificado = df[["id_cliente",
                     "id_formulario",
                      "tipo_organizacion",
                      "nombre_organizacion",
                      "direccion_completa",
                      "year_3", 
                      "empleados_2", 
                      "prioridad_medioambiental", 
                      "latitud_num", 
                      "long_num",
                      "impacto_actividad",
                      "impacto_recuento", 
                      "mejora",
                      "mejora_recuento", 
                      "clasificacion" ]]


# Título de la aplicación
st.header(f"My Streamlit APP - Project RSA2025")

# st.image("img/rsa.jpg", width=700)



with st.expander("About the proyect", expanded=True):
    st.write(
        "A company specializing in environmental business consulting wants to compile a list of potential clients for its marketing department at its headquarters in Aragon."
        "The annual call for applications for the 2025 Aragon Social Responsibility Seal is a recognition for companies in Aragon. " \
        "It publishes details of the entities that have earned it on its freely accessible website. "
        "In addition, a form is available, filled out by the company, which includes both its contact information and relevant data to determine if the entity could be a future client of our services. " \
        "Based on these 1,573 entities and the information provided, we propose identifying a group of entities that fit the profile of an entity interested in the environment and with improvement needs that we can cover with our services. "
    )
# uploaded_file = st.sidebar.file_uploader(
#     "Choose a file (must be ';' separated)", type=["csv"]
#     )

# if uploaded_file is not None:
#     try:
#         df = pd.read_csv(uploaded_file, sep=";")
#         st.balloons()
#     except:
#         st.write("File format not recognized.")

# st.dataframe(df)

# Sistema de navegación
option = st.sidebar.selectbox(
    "Page:",
    ("Home", "Map", "Results"),
    "Pagina:",
    ("Casa", "Mapa", "Resltados")
)

# Lógica para navegar entre las páginas
if option == "Home":
    functions.home(df_clasificado)
elif option=="Map":
    functions.map(df_clasificado)
elif option=="Charts":
    functions.charts(df)