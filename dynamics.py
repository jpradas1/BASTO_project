from shapely.geometry import Polygon, Point, MultiPolygon
import folium
import pyproj
import json, os
import pandas as pd

class HeatMap(object):
    plots, heads = 0, 0
    gps_path, plot_path = 0, 0

    def __init__(self, farm: str):
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
        square_size = 0.001
        # Divide the square into smaller squares
        minx, miny, maxx, maxy = square.bounds

        # Create a list to store the smaller squares
        small_squares = []

        x = minx
        while x < maxx:
            y = miny
            while y < maxy:
                small_square_coords = [(x, y),
                                    (x + square_size, y),
                                    (x + square_size, y + square_size),
                                    (x, y + square_size),
                                    (x, y)]
                small_square = Polygon(small_square_coords)
                if small_square.intersects(square):
                    small_squares.append(small_square_coords)
                y += square_size
            x += square_size

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
    
    def repoint(self, date: str):
        position = []
        for points in self.heads:
            this_point = []
            df = points.loc[points['timestamp'].dt.date == pd.to_datetime(date).date()]
            for lat, lng in zip(df['lat'].values, df['lng'].values):
                this_point.append(Point(lat, lng))
            position.append(this_point)
        position = [p for pp in position for p in pp]
        return position
    
    # def cmap(self, intersection: list, points: list):
    #     this_cmap, this_cmap2 = {}, {}
    #     for ii, inter in enumerate(intersection):
    #         inter = Polygon(inter)
    #         this_cmap[ii] = 0
    #         for dot in points:
    #             if inter.contains(dot):
    #                 this_cmap[ii] += 1

    #     suma = sum([x for x in this_cmap.values()])

    #     for k, v in this_cmap.items():
    #         this_cmap2[k] = round(v / suma, 3) * 100

    #     cmin = min(this_cmap.values())
    #     cmax = max(this_cmap.values())

    #     for k, v in this_cmap.items():
    #         this_cmap[k] = round((v - cmin) / (cmax - cmin), 2)

    #     return this_cmap, this_cmap2
    
    def heat_map(self, from_date: str, to_date: str):
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

        points = self.repoint(from_date)
        ver_point = [list(pp.coords) for pp in points]

        for inter in intersection:
            folium.Polygon(locations=inter, color='black', fill=True, fill_color='green', opacity=0.4, fill_opacity=0.5).add_to(map)

        for pp in ver_point:
            # for p in pp:
            folium.Polygon(locations=pp, color='red', fill=True, fill_color='red', opacity=1, fill_opacity=1).add_to(map)
        # folium.Polygon(locations=vertices, color='black', fill=False, opacity=0.6).add_to(map)
        
        # for dots, color in zip(points, colors):
        #     dots = self.repoint(dots)
        #     cmap, cmap2 = self.cmap(intersection, dots)
        #     self.paint(intersection, cmap, cmap2, color, map)

        return map.show_in_browser()
    
    # def paint(self, intersection: list, cmap: dict, cmap2: dict, color: str, m: folium.Map):
    #     utm_proj = pyproj.Proj(proj='utm', zone=20, south=False)

    #     for ii, domain in enumerate(intersection):
    #         if cmap[ii] > 0.0:
    #             coords_m = [utm_proj(long, lat) for lat, long in domain]
    #             coords_m = Polygon(coords_m)
    #             area = round(coords_m.area / 10000, 3)

    #             polygon = folium.Polygon(locations=domain, color='white', fill=True, fill_color=color, opacity=0.4, fill_opacity=cmap[ii])
    #             popup = folium.Popup(f'Area: {area} ha <br> Time: {cmap2[ii]}%', max_width=400)
    #             polygon.add_child(popup)
    #             m.add_child(polygon)

farm = 'MACSA'
HM = HeatMap(farm)
# print(HM.grid(key='0'))
# HM.heat_map(date='2022-08-17')
# print(HM.heat_map(from_date='2023-03-29', to_date='2023-04-02'))
# print(HM.minimum_regions())