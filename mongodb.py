from pymongo import MongoClient
import pandas as pd
import os, json

client = MongoClient('localhost', 27017)
basto_db = client.basto

def pathing(paths: list):
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)

def aggregate(farm: str, device: str):
    print('Extracting from Mongodb', end='\r')
    pipeline = [
        {
            "$match":{
                "dataRowType": "{}".format(device)
            }
        },
        {
            "$lookup": 
                {
                    "from": "devices",
                    "localField": "UUID",
                    "foreignField": "deviceMACAddress",
                    "as": "devices"
                }
        },
        {
            "$lookup":
                {
                    "from": "animals",
                    "localField": "devices.deviceAnimalID",
                    "foreignField": "_id",
                    "as": "animals"
                }
        },
        {
            "$lookup":
                {
                    "from": "settlements",
                    "localField": "animals.animalSettlement",
                    "foreignField": "_id",
                    "as": "settlements"
                }
        },
        {
            "$match": {
                "settlements.name": "{}".format(farm)
            }
        },
        {
            "$unwind": "$devices"
        },
        {
            "$project":
                {
                    "_id": 0,
                    "dataRowData": 1,
                    "UUID": 1,
                    "createdAt": 1    
                }
        }
    ]

    datarows = basto_db.datarows
    this_aggregate = datarows.aggregate(pipeline)

    return this_aggregate

def GPS(farm: str, device: str, path: str):
    this_aggregate = [x for x in aggregate(farm, device)]

    uuid = []
    for doc in this_aggregate:
        u = doc['UUID']
        if u not in uuid:
            uuid.append(u)

    time_position = {uu: {'timestamp': [], 'lat': [], 'lng': []} for uu in uuid}

    for doc in this_aggregate:
        dataRowData = doc['dataRowData']
        time_position[doc['UUID']]['timestamp'].append(doc['createdAt'])
        for keys in list(dataRowData.keys())[1:3]:
            time_position[doc['UUID']][keys].append(dataRowData[keys])

    ii = 1
    for k, v in time_position.items():
        df = pd.DataFrame(v).dropna()
        df.to_csv(path + str(k) + '.csv', index=False)
        print(f'Creating csv {ii} of {len(uuid)}', end='\r')
        ii += 1

def plots(farm: str, plot_path: str):
    settlements = basto_db.settlements
    settlements = [x for x in settlements.find({'name': '{}'.format(farm)})]

    settlements_plots = []
    for doc in settlements:
        for plot in doc['plots']:
            settlements_plots.append(plot)

    plots = basto_db.plots
    plots = [x for x in plots.find({'_id': {"$in": settlements_plots}})]

    virtualFenceGeoPoints = {ii: {'lat': [], 'lng': []} for ii in settlements_plots}
    geoPoints = {ii: {'lat': [], 'lng': []} for ii in settlements_plots}

    for plot in plots:
        vFG = plot['virtualFenceGeoPoints']
        gP = plot['geoPoints']
        if vFG:
            for x in vFG[0]:
                virtualFenceGeoPoints[plot['_id']]['lat'].append(x['lat'])
                virtualFenceGeoPoints[plot['_id']]['lng'].append(x['lng'])
        if gP:
            for x in gP:
                geoPoints[plot['_id']]['lat'].append(x['lat'])
                geoPoints[plot['_id']]['lng'].append(x['lng'])

    geoPoints = {ii: geoPoints[key] for ii, key in zip(range(len(geoPoints)), list(geoPoints.keys()))}

    plots_json = json.dumps(geoPoints)

    with open(plot_path + farm.replace(' ', '_') + '.json', 'w') as f:
        print('Saving plots json', end='\r')
        f.write(plots_json)

if __name__ == "__main__":
    farm = 'MACSA'
    device = 'GPS'

    gps_path = './basto_dataset/gps_{}/'.format(farm.replace(' ', '_'))
    plot_path = './basto_dataset/plots/'

    pathing([gps_path, plot_path])
    GPS(farm, device, gps_path)
    plots(farm, plot_path)