import streamlit as st
import pandas as pd

# Configuración inicial del proyecto
st.set_page_config(
    page_title="Project Cargatron",
    page_icon=":zap:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Proyecto Cargatron")

df= pd.read_csv("data/red_recarga_acceso_publico_2024.csv", sep=";")
st.dataframe(df)

uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

if uploaded_file is not None:
    # Leer el archivo CSV subido
    df = pd.read_csv(uploaded_file, sep=";")
    
    # Mostrar el DataFrame en Streamlit
    st.write("Contenido del archivo CSV:")
    st.dataframe(df)

with st.expander("Descripción del proyecto"):
    st.write(
        """
        Este proyecto tiene como objetivo analizar y visualizar datos de carga de vehículos eléctricos en España. 
        Se utilizarán técnicas de análisis de datos y visualización para extraer información útil y relevante.
        """
    )