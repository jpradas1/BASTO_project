from fastapi import FastAPI
from auravant_api import Auravant_API
import requests
import json
import pandas as pd

app = FastAPI(title= 'Estimación biomasa disponible.', 
              description= 'Con el mapa de dinámica de pastoreo y las imágenes satelitales con NDVI, calcular las superficies consumidas vs la remanente. Objetivo, saber cuánto forraje se dispone y por cuánto tiempo.')

df = pd.read_csv('./dataset/All_Harvest.csv').set_index('Fecha')
df.dropna(how='all', inplace=True)
df = pd.DataFrame(df)

url = 'https://api.auravant.com/api/'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzcmMiOiJ3IiwidWlkIjoiVUlELTc2MmYzOTBmYTExYmIwYTlkYmI1OWRhZjJmMDUyNTU3IiwiZXhwIjoxNjgzODgzMDk2LCJ2IjoxNTQ2LCJsb2NhbGUiOiJlbl9VUyIsImRldiI6MjA4fQ.uBjwDPApnEimVmgpa3Ky0BlhYK7BaOgqurqTpUV4cSA'
A = Auravant_API(token)


@app.get('/Cultivos', description= 'A continuación se va a desplegar una lista de tipos de cultivos, para poder determinar la cantidad de biomasa y días de pastoreo de su lote. Por favor, verifique el número al que corresponde su tipo de cultivo.')
async def tipos_de_cultivo():
    cultivos = sorted(df.columns.to_list())
    tipos_cultivos = []
    for i, e in enumerate(cultivos, 1):
        salida = f'El cultivo número {i} es {e}'
        tipos_cultivos.append(salida)
    return tipos_cultivos


@app.get('/Lotes', description= "A continuación se va a desplegar una lista de todos los lotes que usted dispone. Por favor, verifique el número 'id_field' del lote para el análisis.")
async def Lotes_disponibles():
    df_field = A.get_all_fields()
    df_field = pd.DataFrame(df_field)
    total_fields = []
    fields = [f for f in df_field.to_dict(orient= 'records')]
    for ind, ele in enumerate(fields, 1):
        salida = f'''El lote numero {ind} es 
        {ele} 
        '''
        total_fields.append(salida)
    return total_fields


@app.get('/Biomasa y Pastoreo', description= 'Introduzca los valores solicitados como números enteros, sin comas, puntos ni espacios.')
async def Biomasa_y_Pastoreo_por_campo(Id_lote: int, Cow_number: int, Type_cultivo: int):

    tipos = await tipos_de_cultivo()
    for i, e in enumerate(tipos, 1):
        if i == Type_cultivo:
            contador = 0
            for char in e[:20]:
                if char.isalnum():
                    contador += 1
            if contador == 16:
                cultivo = e[23:] 
            elif contador == 17:
                cultivo = e[24:]

    df_field = A.get_all_fields()
    df_farm = A.get_farms()
    df_ndvi = A.get_NDVI(Id_lote)

    name_field = df_field[df_field['id_field'] == str(Id_lote)]['name'].values[0]
    name_farm = df_farm[df_farm['id_farm'] == df_field[df_field['id_field'] == '417283']['id_farm'].values[0]]['name'].values[0]
    area = df_field.loc[df_field['id_field'] == str(Id_lote)]['area'].values[0]
    Biomasa_max = df[cultivo].max()

    total_ration = Cow_number * 15 
    df_ndvi['biomass_mean'] = round((df_ndvi['ndvi_mean'] * Biomasa_max) * area, 1)
    biomass = df_ndvi['biomass_mean'].values[0]
    
    time = biomass / total_ration

    return f'''Información del lote {Id_lote}: 

    Nombre del lote: {name_field} 
    Campo al que pertenece: {name_farm} 
    Área: {round(area, 3)} ha 
    Tipo de cultivo: {cultivo} 
    Total animales: {Cow_number} 

    La biomasa es de {biomass} kg para todo el campo. Con estos valores se estiman {round(time)} días de pastoreo.'''
    