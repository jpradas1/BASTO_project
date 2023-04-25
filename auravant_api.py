import requests
import json
import pandas as pd
import os

class Auravant_API(object):
    url = 'https://api.auravant.com/api/'

    def __init__(self, token: str):
         self.token = token
    
    def _headers(self):
        head = {
            'Authorization': f'Bearer {self.token}'
        }
        return head
    
    def _get_info(self):
        request = requests.get(self.url + 'getfields', headers=self._headers())
        response = json.loads(request.text)
        return response['user']
    
    def get_farms(self):
        farms = self._get_info()['farms']
        id_farms = [x for x in farms.keys()]
        names = [farms[x]['name'] for x in id_farms]
        bbox = [farms[x]['bbox'] for x in id_farms]
        L = lambda x: len([x for x in farms[x]['fields']])
        number = [L(x) for x in id_farms]

        df = pd.DataFrame({'id_farm': id_farms, 'name': names,
                            'polygon': bbox, 'N_fields': number})

        return df
    
    def get_fields(self, id_farm: str):
        fields = self._get_info()['farms'][id_farm]['fields']
        id_fields = [x for x in fields.keys()]
        names = [fields[x]['name'] for x in id_fields]
        bbox = [fields[x]['shapes']['current']['polygon'] for x in id_fields]
        areas = [fields[x]['shapes']['current']['area'] for x in id_fields]

        df = pd.DataFrame({'id_field': id_fields, 'name': names, 'area': areas,
                            'polygon': bbox})
        return df
    
    def get_all_fields(self):
        farms = self._get_info()['farms']
        id_fields = [y for x in farms.keys() for y in farms[x]['fields'].keys()]
        names = [farms[x]['fields'][y]['name'] for x in farms.keys() \
                 for y in farms[x]['fields'].keys()]
        polygon = [farms[x]['fields'][y]['shapes']['current']['polygon'] for x in farms.keys() \
                 for y in farms[x]['fields'].keys()]
        bbox = [farms[x]['fields'][y]['shapes']['current']['bbox'] for x in farms.keys() \
                 for y in farms[x]['fields'].keys()]
        id_farms = [x for x in farms.keys() for y in farms[x]['fields'].keys()]
        areas = [farms[x]['fields'][y]['shapes']['current']['area'] for x in farms.keys() \
                 for y in farms[x]['fields'].keys()]

        df =  pd.DataFrame({'id_field': id_fields, 'name': names, 'id_farm': id_farms,
                            'area': areas, 'polygon': polygon, 'bbox': bbox})
        return df
    
    def get_max_vegetation(self):
        file = './dataset/All_Harvest.csv'
        if os.path.exists(file):
            df = pd.read_csv(file).set_index('Fecha')
            crops = df.columns
            maxx = [df[c].max() for c in crops]
            df_max = pd.DataFrame({'Vegetation': crops, 'Max_Biomass': maxx})
            return df_max
        
        print("There's no file './dataset/All_Harvest.csv'. \n \
                In order to build this file, please run\n \
                python3 tcf_scraping.py")


    def get_NDVI(self, id_field: str, date_from = None, date_to = None, latest = False):

        id_field = int(id_field)
        ndvi = {"field_id": id_field}

        response_ndvi = requests.get(self.url+'fields/ndvi', headers=self._headers(),
                                     params=ndvi)
        records_ndvi = json.loads(response_ndvi.text)

        dates = [pd.to_datetime(x['date']).date() for x in records_ndvi['ndvi']]
        values = [x['ndvi_mean'] for x in records_ndvi['ndvi']]

        if date_from == None:
            date_from = min(dates)
        if date_to == None:
            date_to = max(dates)

        date_from = pd.to_datetime(date_from).date()
        date_to = pd.to_datetime(date_to).date()

        df = pd.DataFrame({'date': dates, 'ndvi_mean': values})
        df = df.loc[(df['date'] >= date_from) & (df['date'] <= date_to)]

        if latest:
            return df.iloc[0,:].values

        return df
    
    def create_farm(self, name_farm: str, name_field: str, polygon: str):
        data = {
            'nombre': name_field,
            'shape': polygon,
            'nombrecampo': name_farm
            }
        
        post = requests.post(self.url+'agregarlote', headers=self._headers(), data=data)
        response = json.loads(post.text)
        return response
    
    def add_field(self, id_farm: str, name_field: str, polygon: str):
        id_farm = int(id_farm)
        data = {
            'nombre': name_field,
            'shape': polygon,
            'idcampo': id_farm
        }

        add = requests.post(self.url+'agregarlote', headers=self._headers(), data=data)
        response = json.loads(add.text)
        return response
    
    def delete_field(self, id_field: str):
        delete = requests.get(self.url+'borrarlotes?lote='+id_field, headers=self._headers())
        return delete.text