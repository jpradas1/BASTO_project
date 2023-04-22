from fastapi import FastAPI
from auravant_api import Auravant_API
import requests
import json
import pandas as pd

app = FastAPI(title= 'Estimación biomasa disponible.', 
              description= 'Con las imágenes satelitales para obtener el NDVI de un campo, saber cuánto forraje se dispone y por cuánto tiempo, para razas Británicas entre los 450 y 500 kg, en un lote determinado.')

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
        salida = {f'El lote numero {ind} es: {ele}'}
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
    
    time = round(biomass / total_ration)

    biomass_20 = biomass * .80
    time_20 = round(biomass_20 / total_ration)

    biomass_50 = biomass * .50
    time_50 = round( biomass_50 / total_ration)

    biomass_80 = biomass * .20
    time_80 = round( biomass_80 / total_ration)

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
           'Días de pastoreo estimados': time,
           f'Días de pastoreo estimados con el 20% ({round(biomass_20, 1)} kg) de forraje consumido': time_20,
           f'Días de pastoreo estimados con el 50% ({round(biomass_50, 1)} kg) de forraje consumido': time_50,
           f'Días de pastoreo estimados con el 80% ({round(biomass_80, 1)} kg) de forraje consumido': time_80}
    
    global biomasa_lote
    biomasa_lote = biomass 

    return {"Información del lote": ans}


@app.get('/Cantidad de animales ideales', description= 'Ingrese por favor la cantidad de días en los que pretende dejar el ganado en .')
async def Ideal_de_animales(dias: int):

    global biomasa_lote

    time_per_ration = dias * 15 

    animals = round(biomasa_lote / time_per_ration)
    total_ration = 15 * animals

    biomasa_lote_20 = biomasa_lote * .80 
    time_20 = round( biomasa_lote_20 / total_ration)

    biomasa_lote_50 = biomasa_lote * .50
    time_50 = round( biomasa_lote_50 / total_ration)

    biomasa_lote_80 = biomasa_lote * .20 
    time_80 = round( biomasa_lote_80 / total_ration)

    water = animals * 100

    ans = { 'Biomasa del lote en kg': biomasa_lote,
            f'Cantidad de animales ideales para {dias} días de pastoreo': animals,
            'Total de agua por día en litros': water,
            f'Días de pastoreo estimados con el 20% ({round(biomasa_lote_20, 1)} kg) de forraje consumido': time_20,
            f'Días de pastoreo estimados con el 50% ({round(biomasa_lote_50, 1)} kg) de forraje consumido': time_50,
            f'Días de pastoreo estimados con el 80% ({round(biomasa_lote_80, 1)} kg) de forraje consumido': time_80} 

    return ans