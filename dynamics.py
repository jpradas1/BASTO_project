from shapely.geometry import Polygon, Point
import folium
# import pyproj
# import pandas as pd


from auravant_api import Auravant_API

class Grid(object):
    A = 0
    map = 0

    def __init__(self, token):
        self.token = token
        self.A = Auravant_API(token)
    
    def vertex(self, polygon: str):
        this_vertex = []
        polygon = polygon.strip("POLYGON()").split(',')
        for p in polygon:
            p = p.split(' ')
            v = (float(p[1]), float(p[0]))
            this_vertex.append(v)
        return this_vertex
    
    def polygon_format(self, domain: list):
        string = 'POLYGON(('
        for point in domain:
            string += str(point[1]) + ' ' + str(point[0]) + ','

        string = string[:-1] + '))'
        return string
    
    def grid(self, id_field: str):
        df = self.A.get_all_fields()
        polygon = self.vertex(df.loc[df['id_field'] == id_field]['polygon'].values[0])
        bbox = self.vertex(df.loc[df['id_field'] == id_field]['bbox'].values[0])

        # Define polygons
        field = Polygon(polygon)
        square = Polygon(bbox)
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

        return intersection, polygon
    
    def repoint(self, points: dict):
        this_points = []
        for lat, lng in zip(points['lat'], points['long']):
            this_points.append(Point(lat, lng))
        return this_points
    
    def heat_map(self, id_field: str, points: dict, color: str):
        points = self.repoint(points)
        intersection, vertices = self.grid(id_field)
        polygon = Polygon(vertices)

        cmap = {}
        for ii, inter in enumerate(intersection):
            inter = Polygon(inter)
            cmap[ii] = 0
            for dot in points:
                if inter.contains(dot):
                    cmap[ii] += 1

        cmin = min(cmap.values())
        cmax = max(cmap.values())

        for k, v in cmap.items():
            cmap[k] = round((v - cmin) / (cmax - cmin), 2)
        
        centroid = polygon.centroid
        lat_center = centroid.coords[0][0]
        lon_center = centroid.coords[0][1]
        self.map = folium.Map(location=[lat_center, lon_center], zoom_start=13)

        folium.Polygon(locations=vertices, color='black', fill=False, opacity=0.4).add_to(self.map)

        for ii, domain in enumerate(intersection):
            if cmap[ii] == 0.0:
                folium.Polygon(locations=domain, color='black', fill=False, opacity=0.4).add_to(self.map)
            else:
                folium.Polygon(locations=domain, color='black', fill=True, fill_color=color, opacity=0.4, fill_opacity=cmap[ii]).add_to(self.map)

        return self.map.show_in_browser()
    
    def merge_map(self, id_field: str, points: list, colors: list):
        
        for po, co in zip(points, colors):
            self.heat_map(id_field, po, colors)

        return self.map.show_in_browser()
    
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzcmMiOiJ3IiwidWlkIjoiVUlELWIyMWIzMzhhOTkxNmY4YzJlMjI5Y2UxZTdmNjE0ZTE5IiwiZXhwIjoxNjg0Njk4ODQ4LCJ2IjoxNTY1LCJsb2NhbGUiOiJlbl9VUyIsImRldiI6MjEyfQ.l2VXXMo94tKOsq195agpqUPwrq724kYn82AHvM-g2cE'
G = Grid(token)
# print(G.grid(id_field='423174'))

points1 = {'lat': [-31.248425966096146,
  -31.24793592873743,
  -31.249189840663067,
  -31.247847725530516,
  -31.24929705033053,
  -31.250325087960928,
  -31.250624578397797,
  -31.24909940606454,
  -31.248346638579285,
  -31.251140782929944,
  -31.248774629329095,
  -31.249463356731844,
  -31.249141169368805,
  -31.24805983366443,
  -31.249374310930587,
  -31.247640003732286,
  -31.24952821539418,
  -31.24948874592328,
  -31.24930752963639,
  -31.24824462621217,
  -31.24761267460425,
  -31.247872887009354,
  -31.249781751425875,
  -31.24904529469351,
  -31.249279396527687],
 'long': [-59.5078530495098,
  -59.505259836656265,
  -59.507482491448705,
  -59.508075149039534,
  -59.51065446408019,
  -59.50903600670224,
  -59.50901268404446,
  -59.506731336833404,
  -59.50514206617215,
  -59.509906084167746,
  -59.50645976801043,
  -59.50764382279321,
  -59.507819715046104,
  -59.50793470024395,
  -59.5079498786426,
  -59.50766407026134,
  -59.50802528892576,
  -59.50774536748798,
  -59.51007922673252,
  -59.507896665200526,
  -59.50909210896383,
  -59.50848406042576,
  -59.50705250472574,
  -59.50775245117131,
  -59.507915601116835]}

points2 = {'lat': [-31.244103842890247,
  -31.245145131475514,
  -31.245133779117765,
  -31.245052663114535,
  -31.244940558837925,
  -31.243994805270802,
  -31.245635095821147,
  -31.245720952274908,
  -31.24511733221453,
  -31.245919205806644,
  -31.246351671851986,
  -31.245408709040046,
  -31.245347542649874,
  -31.247299022594476,
  -31.24523484104706,
  -31.24538929074371,
  -31.24663621201656,
  -31.246043158138903,
  -31.24533593288329,
  -31.24545708044251,
  -31.24596831536856,
  -31.24553832686717,
  -31.24603076187365,
  -31.245351369276516,
  -31.245464063685148],
 'long': [-59.50111195130349,
  -59.50101105267428,
  -59.50027594610544,
  -59.49863246320712,
  -59.50112384842769,
  -59.49909200449747,
  -59.50244212331597,
  -59.49953020651772,
  -59.50129682015405,
  -59.503575453191694,
  -59.50072158648346,
  -59.501504765138165,
  -59.501600258892495,
  -59.502278840415336,
  -59.501668464813434,
  -59.50159768682544,
  -59.50407521698913,
  -59.501643705543955,
  -59.501598695232474,
  -59.50209503679791,
  -59.50144331159055,
  -59.499702257113775,
  -59.500163062417656,
  -59.50158382860524,
  -59.502230363163775]}

# G.merge_map(id_field='423174', points=[points1, points2], colors=['blue', 'green'])
G.heat_map(id_field='423174', points=points1, color='green')