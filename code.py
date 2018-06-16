import folium
import pandas as pd

# Loading data for volcanoes
data = pd.read_csv("volcanoes.txt")

# Creating lists of latitude, longitude, elevation
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"]) # For pop-up information

# Creating a function for colors of elevation
def colors(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 2000:
        return 'red'
    else:
        return 'blue'

# Creating a map object
map = folium.Map(location = [38.58, -99.09], zoom_start = 6, tiles = "Mapbox Bright")

# Adding feature groups for volanoes and population
fgv = folium.FeatureGroup(name = "Volcanoes")
fgp = folium.FeatureGroup(name = "Population")

# Iterating through the coordinates list and making markers for volcanoes
for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location = [lt, ln], popup = str(el) + " m", radius = 6, fill_color = colors(el), color = 'grey', fill_opacity = 0.65, fill = True))

# Adding child to the feature group for population
fgp.add_child(folium.GeoJson(data = open('world.json', 'r', encoding = 'utf-8-sig').read(),
style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 # Population distribution by colors
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)

# Adding a layer control
map.add_child(folium.LayerControl())

map.save("Map1.html")
