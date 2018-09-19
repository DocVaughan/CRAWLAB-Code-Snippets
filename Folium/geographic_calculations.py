#! /usr/bin/env python

'''#######################################################################################
# geographic_calculations.py
#
# This file contains functions that implement calculations on geographic information.
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 04/23/14
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
#######################################################################################'''

import numpy as np

def calculate_distance(position1, position2):
    ''' Calculate the distance between two lat/long coordinates using a unit sphere
    
    Copied from: John Cook at http://www.johndcook.com/python_longitude_latitude.html
    
    Input arguments:
        position1 = lat/long pair in decimal degrees DD.dddddd
        position2 = lat/long pair in decimal degrees DD.dddddd
    
    Returns:
        distance = distance from position 1 to position 2 in meters
    
    
    Modified:
        *Joshua Vaughan - joshua.vaughan@louisiana.edu - 04/23/14
            - Additional commenting
            - Modified to match "theme" of CRAWLAB
            - Inputs change to long/lat array slices
    '''
    
    lat1, long1 = position1
    lat2, long2 = position2
    
    R = 6373000        # Radius of the earth in m
    
    # Convert latitude and longitude to spherical coordinates in radians.
    degrees_to_radians = np.pi/180.0
        
    # phi = 90 - latitude
    phi1 = np.deg2rad(90.0 - lat1)
    phi2 = np.deg2rad(90.0 - lat2)
        
    # theta = longitude
    theta1 = np.deg2rad(long1)
    theta2 = np.deg2rad(long2)
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (np.sin(phi1) * np.sin(phi2) * np.cos(theta1 - theta2) + 
           np.cos(phi1) * np.cos(phi2))
    
    arc = np.arccos( cos )

    # Multiply arc by the radius of the earth 
    distance = arc * R
    
    return distance

def calculate_simple_distance(position1, position2):
    ''' Calculate the distance between two lat/long coords using simple cartesian math
    
    Equation from: http://www.movable-type.co.uk/scripts/latlong.html
    
    Input arguments:
        position1 = lat/long pair in decimal degrees DD.dddddd
        position2 = lat/long pair in decimal degrees DD.dddddd
    
    Returns:
        distance = distance from position 1 to position 2 in meters
    
    
    Created: Joshua Vaughan - joshua.vaughan@louisiana.edu - 04/24/14
    
    Modified:
        *
    
    '''
    
    R = 6373000        # Radius of the earth in m
    
    lat1, long1 = np.deg2rad(position1)
    lat2, long2 = np.deg2rad(position2)
    
    dLat = lat2 - lat1
    dLon = long2 - long1
    
    x = dLon * np.cos((lat1+lat2)/2)
    distance = np.sqrt(x**2 + dLat**2) * R
    
    return distance
    
    

def calculate_bearing(position1, position2):
    ''' Calculate the bearing between two GPS coordinates 
    
    Equations from: http://www.movable-type.co.uk/scripts/latlong.html
    
    Input arguments:
        position1 = lat/long pair in decimal degrees DD.dddddd
        position2 = lat/long pair in decimal degrees DD.dddddd
    
    Returns:
        bearing = initial bearing from position 1 to position 2 in degrees
            
    Created: Joshua Vaughan - joshua.vaughan@louisiana.edu - 04/23/14
    
    Modified:
        *
        
    '''
    
    lat1, long1 = np.deg2rad(position1)
    lat2, long2 = np.deg2rad(position2)
    
    dLon = long2 - long1
    
    y = np.sin(dLon) * np.cos(lat2)
    x = np.cos(lat1)*np.sin(lat2) - np.sin(lat1)*np.cos(lat2)*np.cos(dLon)
    
    #bearing = np.rad2deg(np.arctan2(y, x))
    bearing = (np.rad2deg(np.arctan2(y, x)) + 360) % 360
    
    return bearing


def calculate_midpoint(position1, position2):
    ''' Calculate the midpoint between two GPS coordinates 
    
    Equations from: http://www.movable-type.co.uk/scripts/latlong.html
    
    Input arguments:
        position1 = lat/long pair in decimal degrees DD.dddddd
        position2 = lat/long pair in decimal degrees DD.dddddd
    
    Returns:
        midpoint = lat/long pair in decimal degrees DD.dddddd
    
    Created: Joshua Vaughan - joshua.vaughan@louisiana.edu - 04/23/14
    
    Modified:
        *
        
    '''
    
    lat1, long1 = np.deg2rad(position1)
    lat2, long2 = np.deg2rad(position2)
    
    dLat = lat2 - lat1
    dLon = long2 - long1
    
    Bx = np.cos(lat2) * np.cos(dLon)
    By = np.cos(lat2) * np.sin(dLon)
    
    midpoint_lat = np.arctan2(np.sin(lat1) + np.sin(lat2),
                      np.sqrt( (np.cos(lat1) + Bx) * (np.cos(lat1) +Bx ) + By*By ) )
    
    midpoint_long = long1 + np.arctan2(By, np.cos(lat1) + Bx)
    
    return np.rad2deg([midpoint_lat, midpoint_long])
    
    
    
def define_destination(start_position, bearing, distance):
    ''' Calculate the endpoint given a GPS coordinate, heading, and desired distance 
    
    Equations from: http://www.movable-type.co.uk/scripts/latlong.html
    
    Inputs arguments:
      start_position = GPS lat/long pair in decimal degrees DD.ddddddd
      bearing = start bearing (deg)
      distance = how far to go (m)
    
    Returns:
      end_position = GPS lat/long pair of endpoint in decimal degrees DD.ddddddd
    
    Created: Joshua Vaughan - joshua.vaughan@louisiana.edu - 04/23/14
    
    Modified:
        *
        
    '''
    
    R = 6373000.0        # Radius of the earth in m
    
    start_lat, start_long = np.deg2rad(start_position)
    bearing = np.deg2rad(bearing)
    
    end_lat = np.arcsin(np.sin(start_lat)*np.cos(distance/R) + 
                        np.cos(start_lat)*np.sin(distance/R)*np.cos(bearing))

    end_long = start_long + np.arctan2(np.sin(bearing)*np.sin(distance/R)*np.cos(start_lat), 
                                       np.cos(distance/R)-np.sin(start_lat)*np.sin(end_lat))
    
    return np.rad2deg([end_lat, end_long])
