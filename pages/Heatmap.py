import streamlit as st
from streamlit_folium import folium_static
from dynamics import HeatMap
from datetime import datetime, timedelta

st.title("Dinámicas de Pastoreo: Mapa de Calor")
st.info("Esta sección ofrece información esencial sobre el movimiento de los animales, así como \
        de las zonas de mayor pastoreo. Es decir, se brinda un mapa de calor donde las regiones \
        con más color representan zonas donde los animales pasaron mas tiempo. Contrariamente a \
        esto, las zonas más claras son aquellas donde ha ocurrido bajo transito de animales, o \
        directamente ninguno.")

farm = st.radio(
    "Campo:",
    ('MACSA', 'La Florida'))

default = 30

max_date = datetime.now()
delta = timedelta(days=7)
min_date = max_date - delta

start_date = st.date_input("Fecha Inicial", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.date_input("Fecha Final", value=max_date, min_value=min_date, max_value=max_date)

density = st.slider("Densidad de la cuadrícula", min_value=1, max_value=50, value=default)
d = density/(10**4)
HHM = HeatMap(farm, d)
m = HHM.heat_map(from_date=start_date, to_date=end_date)

folium_static(m)
