#! /usr/bin/env python

###############################################################################
# mapbox_directions.py
#
# Script demonstrating getting walking directions using the MapBox API
# 
# We'll use the folium to draw the map
# To install: conda install folium
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 04/03/18
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
# TODO:
#   * 
###############################################################################

import numpy as np

from mapbox import Directions, Static
import folium

direction_service = Directions(access_token='pk.eyJ1IjoiZG9jdmF1Z2hhbiIsImEiOiI1NXdlS184In0.xkx1iJIxebVhEXFS8cadrg')
static_service = Static(access_token='pk.eyJ1IjoiZG9jdmF1Z2hhbiIsImEiOiI1NXdlS184In0.xkx1iJIxebVhEXFS8cadrg')

origin = {'type': 'Feature',
          'properties': {'name': 'Rougeou Hall'},
          'geometry': {
          'type': 'Point',
          'coordinates': [-92.0224611, 30.2096914]}}
          
destination = {'type': 'Feature',
               'properties': {'name': 'Martin Hall'},
                'geometry': {
                'type': 'Point',
                'coordinates': [-92.0189939, 30.215553]}}
                
response = direction_service.directions([origin, destination], 'mapbox.walking')

path =  response.geojson()['features'][0]['geometry']['coordinates']


# Get the start and end locations from the 
start = [origin['geometry']['coordinates'][1], origin['geometry']['coordinates'][0]]
end = [destination['geometry']['coordinates'][1], destination['geometry']['coordinates'][0]]

# Set up base map
mymap = folium.Map(location = start, tiles= 'MapBox', 
                   API_key='docvaughan.iia856df', 
                   zoom_start=16, 
                   height=1200, 
                   width = 1800)

# We could also add clickable lat/long popup
# mymap.add_child(folium.LatLngPopup()) 

# Add circle markers for the start and end points
folium.GeoJson(origin, name="Start").add_to(mymap)
folium.GeoJson(destination, name="End").add_to(mymap)

# We could also add those as colored circle markers
folium.features.CircleMarker(location = [start[0], start[1]], 
                              radius = 10, 
                              popup = 'Start -- Lat, Lon: {:4.4f}, {:4.4f}'.format(start[0], start[1]), 
                              color = '#00FF00', 
                              fill=True, 
                              fill_color = '#00FF00').add_to(mymap)
                              
folium.features.CircleMarker(location = [end[0], end[1]], 
                             radius = 10, 
                             popup = 'End -- Lat, Lon: {:4.4f}, {:4.4f}'.format(end[0], end[1]), 
                             color = '#FF0000', 
                             fill=True, 
                             fill_color = '#FF0000').add_to(mymap)


for index, waypoint in enumerate(path):
    folium.features.CircleMarker(location = [waypoint[1], waypoint[0]], 
                                 radius = 5, 
                                 popup='Waypoint Num: {:.0f} -- Lat, Lon: {:4.4f}, {:4.4f}'.format(index+1, waypoint[1], waypoint[0]), 
                                 color = '#0000FF', 
                                 fill=True, 
                                 fill_color = '#0000FF').add_to(mymap)

# We can add the paths direction from the geojson data returned from MapBox API
folium.GeoJson(response.geojson()['features'][0], name="Path 1").add_to(mymap)
folium.GeoJson(response.geojson()['features'][1], name="Path 2").add_to(mymap)

# We can also add a layer control button to allow hiding layers
folium.LayerControl().add_to(mymap)

# Define a name for the map file (be more unique than this in real use)
# and save the file
map_filename = 'map.html'
mymap.save(map_filename)