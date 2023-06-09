from fastapi import FastAPI
from auravant_api import Auravant_API
import requests
import json
import pandas as pd

# Iniciar FastAPI. 
app = FastAPI(title= 'Estimación biomasa disponible.', 
              description= 'Con las imágenes satelitales para obtener el NDVI de un campo, saber cuánto forraje se dispone y por cuánto tiempo, para razas Británicas entre los 450 y 500 kg, en un lote determinado.')

# Leer el csv que se tiene en la carpeta dataset.
df = pd.read_csv('./dataset/All_Harvest.csv').set_index('Fecha')
df.dropna(how='all', inplace=True)
df = pd.DataFrame(df)

# Variables para consumir la API de auravant. 
url = 'https://api.auravant.com/api/'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzcmMiOiJ3IiwidWlkIjoiVUlELTc2MmYzOTBmYTExYmIwYTlkYmI1OWRhZjJmMDUyNTU3IiwiZXhwIjoxNjgzODgzMDk2LCJ2IjoxNTQ2LCJsb2NhbGUiOiJlbl9VUyIsImRldiI6MjA4fQ.uBjwDPApnEimVmgpa3Ky0BlhYK7BaOgqurqTpUV4cSA'
A = Auravant_API(token)

# Definir la función para obtener los tipos de cultivos.
@app.get('/Cultivos', description= 'A continuación se va a desplegar una lista de tipos de cultivos, para poder determinar la cantidad de biomasa y días de pastoreo de su lote. Por favor, verifique el número al que corresponde su tipo de cultivo.')
async def tipos_de_cultivo():
    cultivos = sorted(df.columns.to_list())
    tipos_cultivos = [cultivo for cultivo in cultivos if len(cultivo) >4]
    cultivos_dicc = [] 
    for i, e in enumerate(tipos_cultivos, 1):
        salida = {i: e}
        cultivos_dicc.append(salida)
    return cultivos_dicc

# Definir la función para obtener los lotes que dispone el usuario.
@app.get('/Lotes', description= "A continuación se va a desplegar una lista de todos los lotes que usted dispone. Por favor, verifique el número 'id_field' del lote para el análisis.")
async def Lotes_disponibles():

    df_field = A.get_all_fields()
    df_field = pd.DataFrame(df_field)
    
    dicc = df_field.to_dict(orient= 'index')

    return dicc

# Definir la función para obtener los datos del lote y la biomasa del mismo.
@app.get('/Biomasa y Pastoreo', description= 'Introduzca los valores solicitados como números enteros, sin comas, puntos ni espacios.')
async def Biomasa_y_Pastoreo_por_campo(Id_lote: str, Cow_number: int, Type_cultivo: int):

    types = await tipos_de_cultivo()

    for ind, cultivos in enumerate(types, 1):
        if Type_cultivo == ind:
            cultivo = cultivos[ind]

    df_field = A.get_all_fields()
    df_farm = A.get_farms()
    df_ndvi = A.get_NDVI(Id_lote)

    name_field = df_field[df_field['id_field'] == Id_lote]['name'].values[0]
    name_farm = df_farm[df_farm['id_farm'] == df_field[df_field['id_field'] == str(Id_lote)]['id_farm'].values[0]]['name'].values[0]
    area = df_field.loc[df_field['id_field'] == str(Id_lote)]['area'].values[0]
    Biomasa_max = df[cultivo].max()

    total_ration = Cow_number * 15 
    df_ndvi['biomass_mean'] = round((df_ndvi['ndvi_mean'] * Biomasa_max) * area, 1)
    biomass = df_ndvi['biomass_mean'].values[0]
    ndvi = round(df_ndvi['ndvi_mean'][0], 2)
    
    time = round(biomass / total_ration)

    biomass_80 = biomass * .20
    time_80 = round( biomass_80 / total_ration)

    biomass_50 = biomass * .50
    time_50 = round( biomass_50 / total_ration)

    biomass_20 = biomass * .80
    time_20 = round(biomass_20 / total_ration)

    water = Cow_number * 100
    total_water = water * round(time)

    ans = {'Id_lote': Id_lote,
           'Nombre del lote': name_field, 
           'Campo al que pertenece': name_farm,
           'Área en hectáreas': round(area, 3), 
           'Tipo de cultivo': cultivo,
           'Total animales': Cow_number,
           'Total de agua por día en litros': water,
           'Total de agua para los días de pastoreo estimados': total_water,
           'Biomasa del lote en kg': biomass,
           'NDVI': ndvi, 
           'Días de pastoreo estimados': time,
           f'Días de pastoreo estimados con el 20% de forraje consumido': time_80,
           f'Días de pastoreo estimados con el 50% de forraje consumido': time_50,
           f'Días de pastoreo estimados con el 80% de forraje consumido': time_20}
    
    global biomasa_lote, id_lote, name_lote, name_campo, area_lote, name_cultivo, indice_green # Permitir usar las variables de la función, en otra función.
    biomasa_lote = biomass
    id_lote = Id_lote
    name_lote = name_field
    name_campo = name_farm 
    area_lote = round(area, 3)
    name_cultivo = cultivo
    indice_green = ndvi



    return {"Información del lote": ans}

# Definir la función para que el usuario ingrese la cantidad de días en los que decida rotar el ganado.
@app.get('/Cantidad de animales ideales', description= 'Ingrese por favor la cantidad de días en los que pretende dejar el ganado en el lote anteriormente consultado.')
async def Ideal_de_animales(dias: int):

    global biomasa_lote, id_lote, name_lote, name_campo, area_lote, name_cultivo, indice_green # Llamar las variables de funciones anteriores. 

    time_per_ration = dias * 15 

    animals = round(biomasa_lote / time_per_ration)
    total_ration = 15 * animals

    animals_80 = round(animals * .20) 
    animals_50 = round(animals * .50)
    animals_20 = round(animals * .80)

    water = animals * 100

    ans = { 'Id_lote': id_lote,
            'Nombre del lote': name_lote, 
            'Campo al que pertenece': name_campo,
            'Área en hectáreas': area_lote, 
            'Tipo de cultivo': name_cultivo,
            'NDVI': indice_green, 
            'Biomasa del lote en kg': biomasa_lote,
            f'Cantidad de animales ideales': animals,
            'Total de agua por día en litros': water,
            f'Cantidad de animales ideales con el 20% consumido': animals_80,
            f'Cantidad de animales ideales con el 50% consumido': animals_50,
            f'Cantidad de animales ideales con el 80% consumido': animals_20} 

    return ans