import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt
import functions as functions

st.cache_data.clear() # Si tienes problemas con la cache, descomenta esta linea


# # Define el estilo CSS para el fondo verde
# page_bg_color = """
# <style>
# [data-testid="stAppViewContainer"] {
#     background-color: #90EE90;  /* Verde claro */
# }
# </style>
# """

# # Aplica el estilo
# st.markdown(page_bg_color, unsafe_allow_html=True)



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
        "Quiero compartir los resultados de mi análisis de datos de las 1573 entidades que han obtenido el sello RSA 2025 en Aragón en [la página web](https://www.aragonempresa.com/empresas-sello-rsa/) centrado en determinar un nicho de entidades potenciales clientes de nuestros servicios medioambientales."
        "Es interesante ver el mapa de las entidades y conocer sus perfiles respecto a la prioridad que otorgan al medioambiente, para ello accede a mapa."
        "No menos interesante, disponer de un listado de resultados de las entidades seleccionadas con las variables mas determinantes para una prospección comercial exitosa basándonos en nuestro objetivo, para ello accede a resultados."
        "Finalmente, basándonos en nuestro modelo te propongo un juego, dime los datos de tu entidad y te puedo predecir tu prioridad medioambiental." 
        "Si te interesa la parte técnica del análisis de datos te recomiendo des un vistazo a mis artículos relacionados [aquí](https://www.linkedin.com/pulse/proyecto-eda-exploratory-data-analysis-jose-luis-padilla-villanova-eccbf/?trackingId=bFOeHOQNmhyQpXCRYKoagA%3D%3D)"
        "Espero disfrutes y si tienes alguna duda o sugerencia no dudes en [contactarme](https://www.linkedin.com/in/joseluispadillavillanova/)."/
        "Gracias por tu atención 😊"
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
    ("Datos iniciales", "Mapa", "Resultados", "Predicción"))

# Lógica para navegar entre las páginas
if option == "Datos iniciales":
    functions.home(df_clasificado)
elif option=="Mapa":
    functions.map(df_clasificado)
elif option=="Resultadoss":
    functions.charts(df)
elif option=="Predicción":
    functions.prediccion(df)