import streamlit as st
# import folium
from streamlit_folium import folium_static
from dynamics import Grid
from dynamics import token, points1, points2, points3

G = Grid(token)
m = G.heat_map(id_field='423168', points=[points1, points2, points3], colors=['green', 'blue', 'red'])

st.title("My Folium Map")
folium_static(m)
