import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk

def home(df):
    st.image("img/rsa.jpg",
         caption= "Follow me on LinkedIn https://www.linkedin.com/in/joseluispadillavillanova/",
         width= 1000)
    
    with st.expander("Datos iniciales(1570):"):
        # with st.echo(code_location='below'):
        #     st.write("Welcome to app RSA2025. \
        #         This is an app to visualize the annual call for applications for the 2025 Aragon Social Responsibility Seal")
        st.dataframe(df)



def map(df):
    # Mostrar el slider de seleccion **antes de filtrar los datos**
    prioridad_minima = st.slider("Filtrar por la prioridad ambiental que determina la entidad", min_value=1, max_value=10, value=1)
    selec_tipo_organizacion = st.multiselect("Seleccionar tipo de organización", 
                                            options = sorted(df["tipo_organizacion"].dropna().unique()),
                                            default = sorted(df["tipo_organizacion"].dropna().unique()))
    antiguedad = st.slider("Seleccionar antiguedad de la entidad",
                                min_value= 1542,
                                max_value= 2024,
                                value = 2024
                                )
    selec_impacto = st.slider("Seleccionar impacto de la actividad",
                                   min_value = 6,
                                   max_value = 1896,
                                   value = 1896
                                   )
    selec_mejora = st.slider("Seleccionar mejora", 
                                  min_value = 1,
                                  max_value = 122,
                                  value = 122
                                  )


    # Filtrar el dataframe con las condiciones seleccionadas
    df_filtrado = df[
        (df["prioridad_medioambiental"] >= prioridad_minima) &
        (df["tipo_organizacion"].isin(selec_tipo_organizacion)) &
        (df["year_3"] >= antiguedad) &
        (df["impacto_recuento"] >= selec_impacto) &
        (df["mejora_recuento"] >= selec_mejora)
    ]
    
    # Mostrar el número de entidades y la suma de empleados
    num_entidades = df_filtrado.shape[0]
    st.write(f"🔹 **Número total de entidades que cumplen la selección:** {num_entidades}")


    # Si el dataframe filtrado está vacío, evitar errores
    if df_filtrado.empty:
        st.warning("No hay datos con la seleccion.")
        return

    # Definir tooltip con información clave
    tooltip = {
        "html": """
        <b>Ubicación:</b> {nombre_organizacion}<br>
        <b>Dirección:</b> {direccion_completa}<br>
        <b>Operador:</b> <a href='https://www.aragonempresa.com/empresas-sello-rsa/imprimir.php?idusuario={id_cliente}&idencuesta={id_formulario}' target='_blank'>Ver detalles</a><br>
        """,
        "style": {
            "backgroundColor": "salmon",
            "color": "white"
        }
    }

    # Crear capa del mapa con puntos filtrados
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_filtrado,
        get_position=["long_num", "latitud_num"],
        get_radius=50,
        get_fill_color=[255,100,100,200],
        pickable=True
    )

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



def charts(df):
    left, right = st.columns(2)

    with left:

        df_group_carg = df.groupby("DISTRITO")["NUM_EQUIPOS"].sum().reset_index().sort_values(by="NUM_EQUIPOS", ascending=False)
        st.header("Cargadores por distrito")
        # st.bar_chart(df_group_carg, 
        #             x="DISTRITO",
        #             y="NUM_EQUIPOS",
        #             x_label="Distrito",
        #             y_label="Cargadores")

        chart_distrito = alt.Chart(df_group_carg).mark_bar().encode(
            x=alt.X('DISTRITO', sort=None, title='Distrito'),
            y=alt.Y('NUM_EQUIPOS', title='Cargadores')
        )

        st.altair_chart(chart_distrito, use_container_width=True)


    with right:

        # Visualizaciones - Cargadores por Operador
        st.header("Cargadores por Operador")
        df_group_oper = df.groupby("OPERADOR")[["NUM_EQUIPOS"]].sum().reset_index().sort_values(by="NUM_EQUIPOS", ascending=False)
        # st.bar_chart(data = df_group_oper, 
        #             x="OPERADOR", 
        #             y="NUM_EQUIPOS",
        #             x_label="Operador",
        #             y_label="Cargadores")


        chart_operador = alt.Chart(df_group_oper).mark_bar().encode(
            x=alt.X('OPERADOR', sort=None, title='Operador'),
            y=alt.Y('NUM_EQUIPOS', title='Cargadores')
        )

        st.altair_chart(chart_operador, use_container_width=True)