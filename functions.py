import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk

def home(df):
    st.image("img/madrid_skyline.jpg",
         caption= "Best tap water in the world, now with more Cargatron",
         width= 1000)
    
    with st.expander("Description:"):
        with st.echo(code_location='below'):
            st.write("Welcome to the Project Cargatron. \
                This is an app to visualize charging points in Madrid")
            st.dataframe(df)

def map(df):
    tooltip = {
        "html": "<b>Ubicación:</b> {UBICACION}<br><b>Operador:</b> {OPERADOR}",
        "style": {
            "backgroundColor": "salmon",
            "color": "white"
        }
    }

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["LONGITUD", "LATITUD"],
        pickable=True,
        opacity=0.8,
        filled=True,
        get_fill_color=[255, 0, 0, 200],  # Add a visible color (red)
        radius_min_pixels=5,  # Ensure minimum size for visibility
    )

    # Set the view state
    view_state = pdk.ViewState(
        longitude=df["LONGITUD"].mean(),
        latitude=df["LATITUD"].mean(),
        zoom=10,  # Slightly reduced zoom to see more area
        pitch=0
    )

    # Create the deck
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="mapbox://styles/mapbox/light-v9"  # Add a map style
    )

    # Display the map in Streamlit
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