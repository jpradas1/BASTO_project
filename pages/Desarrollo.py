import streamlit as st
import requests
from datetime import datetime, timedelta
import time
import plotly.graph_objects as go

st.header("Estimación biomasa disponible")
st.info("Utilizamos imágenes satelitales para obtener el NDVI de un lote, saber cuánto forraje se dispone y por cuánto tiempo, para razas Británicas entre los 450 y 500 kg")

# TRABAJO CON API:
#Obtener la información de todos los cultivos
url_cultivos = 'https://fastapi-basto-project.onrender.com/Cultivos'
response_cultivos = requests.get(url_cultivos)
data_cultivos = response_cultivos.json()
cultivos = [data_cultivos[indice-1][str(indice)] for indice, elemento in enumerate(data_cultivos, 1)]

#Obtener informacion de todos los lotes
url_lotes = 'https://fastapi-basto-project.onrender.com/Lotes'
response_lotes = requests.get(url_lotes)
data_lotes = response_lotes.json()
lotes = [data_lotes[lote] for lote in data_lotes]
ids_lotes = [lote['id_field'] for lote in lotes]

#Crear una función para guardar las respuestas de arriba
def get_app_state():
    return {'cultivo seleccionado': id_lote_sel,
            'lote seleccionado': cultivo_sel,
            'cantidad animales': cantidad_vacas}

#Selección de cada cultivo, id de lote y se introduce la cantidad de animales.
id_lote_sel = st.selectbox('Seleccione el ID de lote:', ids_lotes) #Selección de id de lote
cultivo_sel = st.selectbox('Seleccione el cultivo del lote:', cultivos) #Selección de cultipo
cantidad_vacas = st.text_input("Ingrese la cantidad de vacas: ") #Ingreso de la cantidad de animales

#Llamar a las respuestas antes seleccionadas
app_state = get_app_state() 

#Establecer el id de lote del cultivo para consumir la api... (La consulta de id_lote_sel daba el nombre, pero para el link de fastapi se necesita el id o número de cultivo)
for pos, cultivo in enumerate(cultivos, 1):
    if cultivo_sel in cultivo:
        place = pos


#Para obtener los datos de la api, se necesitaba crear una función de manera que fuera global. Con esto es más fácil para trabajar las gráficas.
 
def obtener_datos_biomasa():

    params = {"Id_lote": id_lote_sel, "Cantidad_vacas": cantidad_vacas, "Forraje": place}

    response_biomasa = requests.get("https://fastapi-basto-project.onrender.com/Biomasa y Pastoreo?Id_lote=" + id_lote_sel + "&Cow_number=" + cantidad_vacas + "&Type_cultivo=" + str(place))

    info_biomasa = response_biomasa.json()
    diccionario = info_biomasa['Información del lote']
    return diccionario

#Ahora activo el boton de calcular para realizar los filtros de la información de 'obtener_datos_biomasa()' y que sea visiblemente mejor.  
if st.button("Calcular"):

    info_lotes = obtener_datos_biomasa()

    st.header("Información")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.title(info_lotes['Nombre del lote'])
        st.write("Nombre del lote")

    with col2:
        st.title(info_lotes['Área en hectáreas'])
        st.write("Área (ha)")

    with col3:
        st.title(info_lotes['Total de agua por día en litros'])
        st.write("Agua necesaria por día (litros)")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.title(info_lotes['Tipo de cultivo'])
        st.write("Tipo de cultivo")

    with col5:
        st.title(info_lotes['Biomasa del lote en kg'])
        st.write("Biomasa total (kg)")

    with col6:
        st.title(info_lotes['NDVI'])
        st.write("NDVI")

    col7, col8, col9 = st.columns(3)

    with col7:
        st.title(info_lotes['Días de pastoreo estimados con el 20% de forraje consumido'])
        st.write("Días de pastoreo (al 20%)")

    with col8:
        st.title(info_lotes['Días de pastoreo estimados con el 50% de forraje consumido'])
        st.write("Días de pastoreo (al 50%)")

    with col9:
        st.title(info_lotes['Días de pastoreo estimados con el 80% de forraje consumido'])
        st.write("Días de pastoreo (al 80%)")


# ESTILO TÍTULOS (INFO)
st.markdown("""
<style>
h1 {
    color: #6f7dbc;
    background-color: #fff;
    
}
</style>
""", unsafe_allow_html=True)



st.markdown("***")


#GRÁFICOS: 
#Gráfico NDVI.

st.header("Gráficas NDVI y Biomasa disponible")

checkbox = st.checkbox("NDVI")
if checkbox:
    info_lotes = obtener_datos_biomasa()
    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = info_lotes['NDVI'],
        gauge = dict(
            shape = 'bullet',
            axis = dict(range=[0,1], tickwidth=1, tickcolor="black"),
            bar = dict(color="#1f77b4", thickness = 0),
            bgcolor = "white",
            borderwidth = 2,
            bordercolor = "gray",
            steps = [
                dict(range=[0, .33], color='rgba(255, 0, 0, 0.6)'),
                dict(range=[.33, .60], color='rgba(255, 250, 75, 0.8)'),
                dict(range=[.60, 1], color='rgba(0, 255, 0, 0.6)') 
            ],
            threshold = dict(line = dict(color = "black", width = 4), thickness = 0.75, value = info_lotes['NDVI'])
        ),
        number = dict(
            font = dict(size=30, color = 'black'),
            suffix = "",
            valueformat = ".2f"
        )
        ))
        
        fig.update_layout(
            height=300,
            width=350,
            title={'text':"NDVI",
                'font': {'color':'black'}},
            title_font_size=30,
            title_x=0.5
            )

        st.plotly_chart(fig)
    
    with col2:
        st.error("Rojo: Biomasa nula o no apta para el consumo")
        st.warning("Amarillo: Biomasa apta para el consumo de baja calidad o poca biomasa en el lote")
        st.success("Verde: Biomasa apta para el consumo de alta calidad")
    

#Gráfico biomasa por día
checkbox = st.checkbox("Biomasa por día")
if checkbox:
    info_lotes = obtener_datos_biomasa()

    col1, col2 = st.columns(2)

    with col1:
        st.title(int(info_lotes['Biomasa del lote en kg'] * 0.2))
        st.write("Biomasa disponible (pastoreo al 20%)")

        st.title(int(info_lotes['Biomasa del lote en kg'] * 0.5))
        st.write("Biomasa disponible (pastoreo al 50%)")

        st.title(int(info_lotes['Biomasa del lote en kg'] * 0.8))
        st.write("Biomasa disponible (pastoreo al 80%)")

    with col2:
        info_lotes = obtener_datos_biomasa()
        max = int(info_lotes['Biomasa del lote en kg'])
        dias = int(info_lotes['Días de pastoreo estimados'])
        vacas = int(info_lotes['Total animales'])
        ration_day = (info_lotes['Biomasa del lote en kg']/dias)

        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            title = {'text': "Biomasa por día"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                    'axis': {'range': [0, max]},  
                    }))

        #Agrega un slider de Streamlit
        valor_slider = st.slider("Selecciona la cantidad de días", min_value=0, max_value=dias)

        # Actualiza el valor del indicador en función del valor seleccionado en el slider
        fig.update_traces(value= valor_slider * ration_day)

        # Actualiza el color de la barra cada vez que se cambie el valor del slider
        st.session_state.valor_actual = valor_slider * vacas * 15
        if st.session_state.valor_actual != valor_slider * vacas * 15:
            st.session_state.valor_actual = valor_slider * vacas * 15
            actualizar_color(st.session_state.valor_actual)

        fig.update_layout(width=400, height=400)
        st.plotly_chart(fig)

 

st.markdown("***")


# CANTIDAD ÓPTIMA DE ANIMALES
st.header("Cantidad óptima de animales por lote")
cantidad_dias = st.text_input("Ingrese la cantidad de días de pastoreo: ") #Ingreso de la cantidad de días

def obtener_datos_animales():

    params = {"total_dias": cantidad_dias}

    response_animales = requests.get('https://fastapi-basto-project.onrender.com/Cantidad de animales ideales?dias=' + str(cantidad_dias))
    info_animales = response_animales.json()
    
    return info_animales


if st.button("Calcular cantidad de animales"):
    info_dias = (obtener_datos_animales())

    st.header("Información")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.title(info_dias['Cantidad de animales ideales con el 20% consumido'])
        st.write("Cantidad animales óptima (20% consumido)")

    with col2:
        st.title(info_dias['Cantidad de animales ideales con el 50% consumido'])
        st.write("Cantidad animales óptima (50% consumido)")

    with col3:
        st.title(info_dias['Cantidad de animales ideales con el 80% consumido'])
        st.write("Cantidad animales óptima (80% consumido)")


    col4, col5, col6 = st.columns(3)

    with col4:
        st.title(str(int(info_dias['Cantidad de animales ideales con el 20% consumido']) * 100) + " " + "L")
        st.write("Cantidad agua necesaria (20% consumido)")


    with col5:
        st.title(str(int(info_dias['Cantidad de animales ideales con el 50% consumido']) * 100) + " " + "L")
        st.write("Cantidad agua necesaria (50% consumido)")

    with col6:
        st.title(str(int(info_dias['Cantidad de animales ideales con el 80% consumido']) * 100) + " " + "L")
        st.write("Cantidad agua necesaria (80% consumido)")


# CRONÓMETRO
def countdown2(t):
    # Crear un cuadro vacío para mostrar el cronómetro
    timer_box = st.empty()

    while t:
        # Calcular los días, horas, minutos y segundos restantes
        dias, segundos = divmod(t, 86400)
        horas, segundos = divmod(segundos, 3600)
        minutos, segundos = divmod(segundos, 60)

        # Crear una cadena con el tiempo restante formateado
        timer = '{:02d}d {:02d}h {:02d}m {:02d}s'.format(dias, horas, minutos, segundos)

        # Mostrar el cronómetro en el cuadro vacío
        timer_box.text(timer)

        # Esperar un segundo y actualizar el tiempo restante
        time.sleep(1)
        t -= 1

    # Mostrar un mensaje cuando el tiempo se agote
    timer_box.text('¡Es necesario rotar los animales!')

# Esta función crea un cronómetro que cuenta el tiempo que falta para rotar los animales


st.markdown("***")

# ALARMA:
st.header("Alarma")

cb = st.checkbox('Pastoreo con 20% consumido')
if cb:
#     st.write(
    info_dias = obtener_datos_biomasa()
    # Se toman los días de pastoreo al 20%
    days = info_dias['Días de pastoreo estimados con el 20% de forraje consumido']

    # Calcula la fecha de la alarma
    alarm_time = datetime.now() + timedelta(days=days)

    # Muestra la fecha y hora de la alarma
    st.error(f"Habrá que rotar los animales el {alarm_time.strftime('%d/%m/%Y')}")

    # Verifica si la alarma debe sonar
    if alarm_time - timedelta(days=2) <= datetime.now() < alarm_time - timedelta(days=1):
        st.write("¡Dentro de 2 días será necesario rotar los animales!")
    elif alarm_time - timedelta(days=1) <= datetime.now() < alarm_time:
        st.write("¡Mañana será necesario rotar los animales!")

    # Llamo cronómetro
    t = info_dias['Días de pastoreo estimados con el 20% de forraje consumido'] * 86400
    st.text("Aún restan:") 
    countdown2(t)


cb = st.checkbox('Pastoreo con 50% consumido')
if cb:
#     st.write(
    info_dias = obtener_datos_biomasa()
    # Se toman los días de pastoreo al 50%
    days = info_dias['Días de pastoreo estimados con el 50% de forraje consumido']

    # Calcula la fecha de la alarma
    alarm_time = datetime.now() + timedelta(days=days)

    # Muestra la fecha y hora de la alarma
    st.error(f"Habrá que rotar los animales el {alarm_time.strftime('%d/%m/%Y')}")

    # Verifica si la alarma debe sonar
    if alarm_time - timedelta(days=2) <= datetime.now() < alarm_time - timedelta(days=1):
        st.write("¡Dentro de 2 días será necesario rotar los animales!")
    elif alarm_time - timedelta(days=1) <= datetime.now() < alarm_time:
        st.write("¡Mañana será necesario rotar los animales!")

    # Llamo cronómetro
    t = info_dias['Días de pastoreo estimados con el 50% de forraje consumido'] * 86400
    st.text("Aún restan:") 
    countdown2(t)


cb = st.checkbox('Pastoreo con 80% consumido')
if cb:
#     st.write(
    info_dias = obtener_datos_biomasa()
    # Se toman los días de pastoreo al 80%
    days = info_dias['Días de pastoreo estimados con el 80% de forraje consumido']

    # Calcula la fecha de la alarma
    alarm_time = datetime.now() + timedelta(days=days)

    # Muestra la fecha y hora de la alarma
    st.error(f"Habrá que rotar los animales el {alarm_time.strftime('%d/%m/%Y')}")

    # Verifica si la alarma debe sonar
    if alarm_time - timedelta(days=2) <= datetime.now() < alarm_time - timedelta(days=1):
        st.write("¡Dentro de 2 días será necesario rotar los animales!")
    elif alarm_time - timedelta(days=1) <= datetime.now() < alarm_time:
        st.write("¡Mañana será necesario rotar los animales!")

    # Llamo cronómetro
    t = info_dias['Días de pastoreo estimados con el 80% de forraje consumido'] * 86400
    st.text("Aún restan:") 
    countdown2(t)



st.markdown("***")



# LINK A LA API:
st.header("Link a la API de Bastó - Team Data #3")
link = '[API_Basto](https://fastapi-basto-project.onrender.com/docs#/)'
st.markdown(link, unsafe_allow_html=True)

