from shapely.geometry import Polygon, Point, MultiPolygon
import folium
import pyproj
import json, os, random
import pandas as pd
import numpy as np
from datetime import datetime

class HeatMap(object):
    plots, heads = 0, 0
    gps_path, plot_path = 0, 0

    def __init__(self, farm: str, density: float):
        self.square_size = density

        self.farm = farm.replace(' ', '_')
        self.gps_path = './basto_dataset/gps_' + self.farm + '/'
        self.plot_path = './basto_dataset/plots/'
        try:
            files = os.listdir(self.gps_path)
            self.heads = [pd.read_csv(self.gps_path + name) for name in files]
            for df in self.heads:
                df['timestamp'] = pd.to_datetime(df['timestamp'])

            with open(self.plot_path + self.farm + '.json', 'r') as f:
                self.plots = json.load(f)
        except:
            print('Get dataset by running: \n \
                  \t python3 mongodb.py')
    
    def vertex(self, polygon: str):
        this_vertex = []
        polygon = polygon.strip("POLYGON()").split(',')
        for p in polygon:
            p = p.split(' ')
            v = (float(p[1]), float(p[0]))
            this_vertex.append(v)
        return this_vertex
    
    def minimum_regions(self):
        polygons = []
        for key in self.plots.keys():
            polygons.append(self.vertex_format(self.plots[key]))
        
        polygons = [Polygon(vertex) for vertex in polygons]
        union = polygons[0]
        for pp in polygons[1:]:
            try:
                union = union.union(pp)
            except:
                continue
        minimum = []
        for geom in union.geoms:
            minimum.append(list(geom.exterior.coords))

        return minimum
    
    def vertex_format(self, coords: dict):
        this_vertex = [(lat, lng) for lat, lng in zip(coords['lat'], coords['lng'])]
        return this_vertex
    
    def grid(self, polygon: list):
        # Define polygons
        field = Polygon(polygon)
        square = field.envelope
        # Define the size of the smaller squares
        # self.square_size = 0.003
        # Divide the square into smaller squares
        minx, miny, maxx, maxy = square.bounds

        # Create a list to store the smaller squares
        small_squares = []

        x = minx
        while x < maxx:
            y = miny
            while y < maxy:
                small_square_coords = [(x, y),
                                    (x + self.square_size, y),
                                    (x + self.square_size, y + self.square_size),
                                    (x, y + self.square_size),
                                    (x, y)]
                small_square = Polygon(small_square_coords)
                if small_square.intersects(square):
                    small_squares.append(small_square_coords)
                y += self.square_size
            x += self.square_size

        intersection = []
        for sq in small_squares:
            solid = Polygon(sq)
            if solid.intersects(field):
                try:
                    inter = solid.intersection(field)
                    intersection.append(list(inter.exterior.coords))
                except:
                    for geom in inter.geoms:
                        intersection.append(list(geom.exterior.coords))

        return intersection
    
    def repoint(self, from_date: str, to_date: str):
        position = []
        for points in self.heads:
            this_point = []
            df = points.loc[(points['timestamp'].dt.date >= pd.to_datetime(from_date).date()) & \
                            (points['timestamp'].dt.date <= pd.to_datetime(to_date).date())]
            for lat, lng in zip(df['lat'].values, df['lng'].values):
                this_point.append(Point(lat, lng))
            position.append(this_point)
        position = [p for pp in position for p in pp]
        return position
    
    def cmap(self, intersection: list, points: list):
        this_cmap, this_cmap2 = {}, {}
        for ii, inter in enumerate(intersection):
            inter = Polygon(inter)
            this_cmap[ii] = 0
            for dot in points:
                if inter.contains(dot):
                    this_cmap[ii] += 1

        suma = sum([x for x in this_cmap.values()])

        for k, v in this_cmap.items():
            this_cmap2[k] = round(v / suma * 100, 1)

        cmin = min(this_cmap.values())
        cmax = max(this_cmap.values())

        for k, v in this_cmap.items():
            this_cmap[k] = round((v - cmin) / (cmax - cmin), 2)

        return this_cmap, this_cmap2
    
    def heat_map(self, from_date: datetime, to_date: datetime):
        vertices = self.minimum_regions()
        intersection = []
        for minn in vertices:
            inter = self.grid(minn)
            for ii in inter:
                intersection.append(ii)

        polygon = [Polygon(vertex) for vertex in vertices]
        multipolygon = MultiPolygon(polygon)

        centroid = multipolygon.centroid
        lat_center = centroid.coords[0][0]
        lon_center = centroid.coords[0][1]
        
        map = folium.Map(location=[lat_center, lon_center], zoom_start=13)

        # points = self.repoint(from_date, to_date)
        # date1 = datetime.strptime(from_date, '%Y-%m-%d')
        # date2 = datetime.strptime(to_date, '%Y-%m-%d')
        delta = to_date - from_date
        num_days = delta.days

        points = self.test_points(multipolygon, num_days)
        
        for vertex in vertices:
            folium.Polygon(locations=vertex, color='green', fill=False, opacity=1).add_to(map)

        for kk, dots in enumerate(points):
            cmap, cmap2 = self.cmap(intersection, dots)
            self.paint(intersection, cmap, cmap2, map, kk)

        return map
    
    def paint(self, intersection: list, cmap: dict, cmap2: dict, m: folium.Map, id: int):
        utm_proj = pyproj.Proj(proj='utm', zone=20, south=False)

        for ii, domain in enumerate(intersection):
            if cmap[ii] > 0.0:
                coords_m = [utm_proj(long, lat) for lat, long in domain]
                coords_m = Polygon(coords_m)
                area = round(coords_m.area / 10000, 3)

                polygon = folium.Polygon(locations=domain, color='white', fill=True, fill_color='red', opacity=0.4, fill_opacity=cmap[ii])
                popup = folium.Popup(f' _id: {id} <br> Area: {area} ha <br> Time: {cmap2[ii]}%', max_width=400)
                polygon.add_child(popup)
                m.add_child(polygon)

    def test_points(self, multipolygon: MultiPolygon, days: int):
        minx, miny, maxx, maxy = multipolygon.bounds
        cenx, ceny = 0.001, 0.001
        varx, vary = days * cenx, days * ceny
        X, Y = [], []
        points = []
        n = 10
        while len(points) != n:
            x = random.uniform(minx, maxx)
            y = random.uniform(miny, maxy)
            point = Point(x, y)
            if multipolygon.contains(point):
                points.append(point)
                X.append(x)
                Y.append(y)

        points = []
        m = n * 6
        for x, y in zip(X, Y):
            new_points = []
            while len(new_points) != m:
                x_ = x + random.normalvariate(cenx, varx)
                y_ = y + random.normalvariate(ceny, vary)
                point = Point(x_, y_)
                if multipolygon.contains(point):
                    new_points.append(point)
            points.append(new_points)
        
        return points