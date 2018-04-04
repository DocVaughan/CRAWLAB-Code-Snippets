#! /usr/bin/env python

###############################################################################
# gmaps_directions.py
#
# Simple script to get directions using the Google Maps API
#
# Requires
#  * Python client library for Google Maps API Web Services to be installed
#    - https://github.com/googlemaps/google-maps-services-python
#    - can be installed via: conda install -c conda-forge googlemaps
#  * API keys with Google. How to obtained these is explained in the link above
#  * gmplot for plotting the route
#   - https://github.com/vgm64/gmplot
#   - can be installed by conda install -c mlgill gmplot 
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
import matplotlib.pyplot as plt
from datetime import datetime

import googlemaps
import gmplot


gmaps = googlemaps.Client(key='AIzaSyDin8BFtWW9NxpQap17YFDp-MfL7pVJfEo')


# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Rougeou Hall, Lafayette, LA",
                                     "Martin Hall, Lafayette, LA",
                                     mode="walking",
                                     departure_time=now)


# The results are returned as a json object, so we need to parse them to get 
# the GPS coordinates of the start and end and waypoint locations
start_latLon = directions_result[0]['legs'][0]['start_location']
end_latLon = directions_result[0]['legs'][0]['end_location']

# create an array to hold the waypoints of the path
wayPoint_array = np.zeros((len(directions_result[0]['legs'][0]['steps'])+1, 2))

# Create an array to hold the distance to the next waypoint
wayPoint_distance = np.zeros((len(directions_result[0]['legs'][0]['steps']), 1)) 

# Fill the first value of the waypoint array with the start location
wayPoint_array[0,:] = [start_latLon['lat'], start_latLon['lng']]

# Now, loop through the steps of the directions to extract the necessary 
# coordinates to form the array of waypoints.
for index, step in enumerate(directions_result[0]['legs'][0]['steps']):
    # We only need to grab the end_location for each step because the start 
    # location of the next step is the same.
    next_waypoint_latLon = step['end_location']
    wayPoint_array[index + 1] = [next_waypoint_latLon['lat'], next_waypoint_latLon['lng']]

    # Get the distance to the next waypoint and add it to the array
    distance_to_next_waypoint = step['distance']['value']
    wayPoint_distance[index] = distance_to_next_waypoint

    
# Now, let's plot those waypoints on a map
# We first create the map object, passing its center lat, lon and a zoom level
# We'll just using the "middle" waypoint as the center
gmap = gmplot.GoogleMapPlotter(wayPoint_array[len(wayPoint_array)//2, :][0], 
                               wayPoint_array[len(wayPoint_array)//2, :][1], 
                               17)


wayPoint_array = np.array([[-92.022457, 30.209695],
     [-92.022628, 30.209846],
     [-92.022777, 30.209977],
     [-92.023212, 30.210361],
     [-92.022834, 30.210739],
     [-92.021956, 30.211616],
     [-92.021177, 30.212395],
     [-92.020224, 30.213348],
     [-92.01976, 30.212989],
     [-92.019425, 30.213326],
     [-92.018719, 30.214036],
     [-92.018216, 30.21454],
     [-92.017822, 30.214933],
     [-92.017768, 30.214987],
     [-92.017309, 30.215453],
     [-92.016977, 30.215789],
     [-92.017599, 30.21625],
     [-92.017892, 30.216466],
     [-92.018016, 30.216307],
     [-92.017999, 30.216217],
     [-92.017954, 30.216078],
     [-92.018007, 30.215941],
     [-92.01819, 30.215814],
     [-92.018474, 30.215793],
     [-92.018616, 30.21564],
     [-92.018742, 30.215503],
     [-92.018913, 30.215633]])
# Now, plot the path
gmap.plot(wayPoint_array[:,1], wayPoint_array[:,0], 'cornflowerblue', edge_width=10)

# And draw the map
gmap.draw("my_map.html")