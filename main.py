from fastapi import FastAPI
from auravant_api import Auravant_API
import requests
import json
import pandas as pd

app = FastAPI()

df = pd.read_csv('./dataset/All_Harvest.csv').set_index('Fecha')
df.dropna(how='all', inplace=True)
df = pd.DataFrame(df)

url = 'https://api.auravant.com/api/'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzcmMiOiJ3IiwidWlkIjoiVUlELTc2MmYzOTBmYTExYmIwYTlkYmI1OWRhZjJmMDUyNTU3IiwiZXhwIjoxNjgzODgzMDk2LCJ2IjoxNTQ2LCJsb2NhbGUiOiJlbl9VUyIsImRldiI6MjA4fQ.uBjwDPApnEimVmgpa3Ky0BlhYK7BaOgqurqTpUV4cSA'
A = Auravant_API(token)

@app.get('/Cultivos')
async def Cultivos(respuesta: str):
    if respuesta == 'no' or respuesta == 'No':
        return 'Puede seguir con la otra consulta.'
    else:
        columnas = df.columns.to_list()
        return columnas

@app.get('/Campos')
async def Campos(respuesta: str):
        if respuesta == 'no' or respuesta == 'No':
            return 'Puede seguir con la otra consulta.'
        else:
            df_field = A.get_all_fields()
            df_field = pd.DataFrame(df_field)

            return df_field.to_dict(orient= 'records')

@app.get('/Biomasa y Pastoreo')
async def BiomasayPastoreo(id_lote: int, cow_number: int, cultivo: str):

    df_field = A.get_all_fields()
    df_ndvi = A.get_NDVI(id_lote)
    Biomasa_max = df[cultivo].max()
    total_ration = cow_number * 15 

    area = df_field.loc[df_field['id_field'] == str(id_lote)]['area'].values[0]
    
    df_ndvi['biomass_mean'] = round((df_ndvi['ndvi_mean'] * Biomasa_max) * area, 1)
    
    biomass01 = df_ndvi['biomass_mean'].values[0]

    time = biomass01 / total_ration

    return f'La cantidad de biomasa actual del campo numero {id_lote} con un área total de {round(area, 3)} ha es de {biomass01} kg. Con estos valores se estiman {round(time)} días de pastoreo.'