import streamlit as st
from streamlit_folium import folium_static
from dynamics import HeatMap

farm = 'MACSA'

from_date = '2023-03-29'
to_date = '2023-03-30'

HHM = HeatMap(farm)
m = HHM.heat_map(from_date, to_date)

st.title("Dinámicas de Pastoreo: Mapa de Calor")
folium_static(m)
