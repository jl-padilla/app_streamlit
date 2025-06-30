import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk

def home(df):
    st.image("img/rsa.jpg",
         caption= "Follow the  https://www.linkedin.com/pulse/proyecto-eda-exploratory-data-analysis-jose-luis-padilla-villanova-eccbf/?trackingId=bFOeHOQNmhyQpXCRYKoagA%3D%3D",
         width= 500)
    
    with st.expander("Datos iniciales(1570):"):
        # with st.echo(code_location='below'):
        #     st.write("Welcome to app RSA2025. \
        #         This is an app to visualize the annual call for applications for the 2025 Aragon Social Responsibility Seal")
        st.dataframe(df)



def map(df):
    # Mostrar el slider de seleccion **antes de filtrar los datos**
    prioridad_minima = st.slider(
    "🔍 Filtro de prioridad ambiental mínima (1 = 🟩 Alta prioridad, 10 = 🟥 Baja prioridad)",
    min_value=1, max_value=10, value=10
)


    selec_tipo_organizacion = st.multiselect("Selecciona tipo de organización", 
                                            options = sorted(df["tipo_organizacion"].dropna().unique()),
                                            default = sorted(df["tipo_organizacion"].dropna().unique()))
    # antiguedad = st.slider("Seleccionar antiguedad de la entidad",
    #                             min_value= 1542,
    #                             max_value= 2024,
    #                             value = 2024
    #                             )
    # selec_impacto = st.slider("Seleccionar escala de impacto de la actividad en el medioambiente",
    #                                min_value = 6,
    #                                max_value = 1896,
    #                                value = 1896
    #                                )
    # selec_mejora = st.slider("Seleccionar escala de mejora de la entidad", 
    #                               min_value = 1,
    #                               max_value = 122,
    #                               value = 122
    #                               )


    # Filtrar el dataframe con las condiciones seleccionadas
    df_filtrado = df[
        (df["prioridad_medioambiental"] <= prioridad_minima) &
        (df["tipo_organizacion"].isin(selec_tipo_organizacion))
    ]
    
    # Mostrar el número de entidades y la suma de empleados
    num_entidades = df_filtrado.shape[0]
    # Mostrar en un cuadro destacado
    st.metric(label="🔹 Número total de entidades", value=num_entidades)
    num_empleados = df_filtrado["empleados_2"].sum()
    # Mostrar en un cuadro destacado
    st.metric(label="🔹 Número total de empleados", value=num_empleados)



    # Si el dataframe filtrado está vacío, evitar errores
    if df_filtrado.empty:
        st.warning("No hay datos con la seleccion.")
        return

    # Definir tooltip con información clave
    tooltip = {
        "html": """
        <div style='background-color:rgba(50,50,50,0.8); color:white; padding:10px; border-radius:5px;'>
            <b>Ubicación:</b> {nombre_organizacion}<br>
            <b>Dirección:</b> {direccion_completa}<br>
            <b>Tipo de organización:</b> {tipo_organizacion}<br>
            <b>Prioridad ambiental:</b> {prioridad_medioambiental}<br>
            <b>Antigüedad:</b> {year_3}<br>
            <b>Empleados:</b> {empleados_2}<br>
            <b>Impacto de la actividad (recuento):</b> {impacto_recuento}<br>
            <b>Mejora (recuento):</b> {mejora_recuento}<br>
            <b>Operador:</b> 'https://www.aragonempresa.com/empresas-sello-rsa/imprimir.php?idusuario={id_cliente}&idencuesta={id_formulario}' <br>
        </div>
        """,}
    
    def get_color(prioridad):
        """
        Mapea la prioridad (1=verde, 10=rojo) a colores RGB.
        """
        red = int((prioridad - 1) / 9 * 255)  # Más prioridad → más rojo
        green = int((10 - prioridad) / 9 * 255)  # Menos prioridad → más verde
        return [red, green, 0, 200]  # RGB con opacidad

    df_filtrado["color"] = df_filtrado["prioridad_medioambiental"].apply(get_color)


    # Crear capa del mapa con puntos filtrados
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_filtrado,
        get_position=["long_num", "latitud_num"],
        pickable=True,
        opacity=0.8,
        filled=True,
        get_fill_color="color",  # Colores dinámicos
        radius_min_pixels=5)
    

    # Definir estado de la vista
    view_state = pdk.ViewState(
        longitude=df_filtrado["long_num"].mean(),
        latitude=df_filtrado["latitud_num"].mean(),
        zoom=10,
        pitch=0
    )

    # Renderizar el mapa con pydeck
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="mapbox://styles/mapbox/light-v9"
    )

    # Mostrar el mapa en Streamlit correctamente
    st.pydeck_chart(deck)



import streamlit as st

def resultados(df):
    # Verificar si hay datos
    if df.empty:
        st.warning("⚠️ El DataFrame está vacío.")
        return

    # Asegurarse de que las columnas necesarias existen
    columnas_necesarias = [
        "id_cliente", "id_formulario", "tipo_organizacion", "nombre_organizacion",
        "direccion_completa", "persona_contacto", "email_contacto", "pagina-web",
        "prioridad_medioambiental", "impacto_actividad", "impacto_recuento",
        "mejora", "mejora_recuento", "clasificacion", "Empleados", "Ubicación"
    ]
    columnas_disponibles = [col for col in columnas_necesarias if col in df.columns]
    df_objetivo = df[columnas_disponibles]

    # Ordenar por prioridad y mejora
    df_objetivo = df_objetivo.sort_values(
        by=["prioridad_medioambiental", "mejora_recuento"],
        ascending=[True, True]
    )

    # Selector de entidad
    seleccion = st.selectbox("Selecciona una entidad", df_objetivo["nombre_organizacion"].dropna().unique())

    # Filtrar datos de la entidad seleccionada
    entity_data = df_objetivo[df_objetivo["nombre_organizacion"] == seleccion].iloc[0]

    # Mostrar datos visualmente
    st.subheader(f"📌 Información de {seleccion}")
    st.write(f"**Nombre:** {entity_data.get('nombre_organizacion', 'No disponible')}")
    st.write(f"**Dirección:** {entity_data.get('direccion_completa', 'No disponible')}")
    st.write(f"**Persona de contacto:** {entity_data.get('persona_contacto', 'No disponible')}")
    st.write(f"**Email de contacto:** {entity_data.get('email_contacto', 'No disponible')}")
    st.write(f"**Página web:** {entity_data.get('pagina-web', 'No disponible')}")
    st.write(f"**Prioridad ambiental:** {entity_data.get('prioridad_medioambiental', 'No disponible')}")
    st.write(f"**Impacto de la actividad:** {entity_data.get('impacto_actividad', 'No disponible')}")
    st.write(f"**Impacto de la actividad (recuento):** {entity_data.get('impacto_recuento', 'No disponible')}")
    st.write(f"**Mejora:** {entity_data.get('mejora', 'No disponible')}")
    st.write(f"**Mejora (recuento):** {entity_data.get('mejora_recuento', 'No disponible')}")
    st.write(f"**Clasificación:** {entity_data.get('clasificacion', 'No disponible')}")
    st.write(f"**Número de empleados:** {entity_data.get('Empleados', 'No disponible')}")
    st.write(f"**Ubicación:** {entity_data.get('Ubicación', 'No disponible')}")




 