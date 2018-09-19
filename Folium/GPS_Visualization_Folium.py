#! /usr/bin/env python

##########################################################################################
# GPS_Visualization_Folium.py
#
# Script to read control decision data collected using during single waypoint trials
#  Adapted from a similar script used to process data from the Anaconda and Husky
#
# Uses Folium to generate maps of a GPS path 
#  - https://github.com/python-visualization/folium
#  - Conda install - https://anaconda.org/conda-forge/folium
#
# NOTE: Plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 06/11/14
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 07/10/14 - Joshua Vaughan - joshua.vaughan@louisiana.edu
#       - condensed batch processing and single run into this script, choose via boolean
#       - condensed "only IMU" data and "Control" data scripts into this one
#       - general code cleanup
#   * 09/12/15 - JEV - joshua.vaughan@louisiana.edu
#       - conversion to Python 3
#       - begin conversion away from Anaconda data
#   * 09/16/15 - JEV - joshua.vaughan@louisiana.edu
#       - Update parsing for ARLISS 2015 data log order
#   * 09/13/18 - JEV - joshua.vaughan@louisiana.edu
#       - Added parsing for ARLISS 2018 data log order
#       - Updates for Folium 0.6
#
##########################################################################################

from __future__ import print_function, division

import numpy as np

import folium
import glob
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory

import geographic_calculations as geoCalc

import datetime


PRODUCE_FOLIUMMAP = True         # Produce a Folium-based map?
DRAW_WAYPOINTS = False           # Draw the waypoints?
BATCH = False                    # Batch processing?



def create_map(data_filename):
    ''' Actually creates the map '''
    waypoints = None
    target = None
    
    # TODO: be more efficient
    with open(data_filename, 'rb') as data_file:  
         data = np.genfromtxt(data_file, delimiter=',', skip_header = 1)#, dtype = 'float')

    if np.shape(data)[1] == 14: # _controlHistory... file
        data_ok = True
        time = data[:,0]
        imu_heading = data[:,1]
        latitude = data[:,2]
        longitude = data[:,3]
        gps_heading = data[:,4]
        gps_speed = data[:,5]
        waypoint_number = data[:,6]             
        waypoint_latitude = data[:,7]           
        waypoint_longitude = data[:,8]          
        distance_to_waypoint = data[:,9]        
        bearing_to_waypoint = data[:,10] 
        course_correction = data[:,11]
        turn_direction = data[:,12]
        control_from_PID = data[:,13]
    
        _, waypoint_indices = np.unique(waypoint_number, return_index = True)
    
        waypoints = np.vstack((waypoint_latitude[waypoint_indices], 
                               waypoint_longitude[waypoint_indices]))
                           
        waypoints = waypoints.T

    elif np.shape(data)[1] == 19:  # _rawIMUGPS... file
        data_ok = True
        time = data[:,0]
        quart0 = data[:,1]
        quart1 = data[:,2]
        quart2 = data[:,3]
        quart3 = data[:,4]
        x_accel = data[:,5]
        y_accel = data[:,6]
        z_accel = data[:,7]
        x_mag = data[:,8]
        y_mag = data[:,9]
        z_mag = data[:,10]
        roll = data[:,11]
        pitch = data[:,12]
        yad = data[:,13]
        imu_heading = data[:,14]
        latitude = data[:,15]
        longitude = data[:,16]
        gps_heading = data[:,17]
        gps_speed = data[:,18]
    
        waypoints = None
    
    elif np.shape(data)[1] == 11: # pyBoard... file
        # (timestamp, past point, current point, current bearing, desired bearing, angle, target distance)
        data_ok = True
        
        hours = data[:,0]
        minutes = data[:,1]
        seconds = data[:,2]
        
        time = []
        
        for index, hour in enumerate(hours):
            time_stamp = datetime.datetime(2015, 9, 16, int(hours[index]), int(minutes[index]), int(seconds[index]))
            time = np.append(time, time_stamp.strftime('%H:%M:%S'))
        
        past_latitude = data[:,3]
        past_longitude = data[:,4]
        
        # current
        latitude = data[:,5]
        longitude = data[:,6]
        
        current_bearing = data[:,7]
        desired_bearing = data[:,8]
        
        angle_to_turn = data[:,9]
        
        target_distance = data[:,10]

    elif np.shape(data)[1] == 7: # ARLISS 2018 Log file
        # Time,Latitude,Longitude,DistanceToTarget,CurrentBearing,DesiredBearing,CourseCorrection
        data_ok = True
        
        time = (data[:,0] - data[0,0])/1000
        latitude = data[0:,1]
        longitude = data[0:,2]
        target_distance = data[0:,3]
        current_bearing = data[0:,4]
        desired_bearing = data[0:,5]
        angle_to_turn = data[0:,6]
        
        target = np.array([40.8680667, -119.1216167])
        
        past_latitude = False # Used in a later check for this data
        
        waypoints = None
        
    else:
        data_ok = False
        print('\nImproper data length in file {}.'.format(data_filename))
        print('Skippping it... \n\n')

    if data_ok: # If we have meaningful data, make the map
        # Define the start, target, and midpoint locations
        if past_latitude:
            start = np.array([past_latitude[0], past_longitude[0]])
        else:
            start = np.array([latitude[0], longitude[0]])

        if target is None:
            if waypoints is not None:
                target = waypoints[-1,:]    # last waypoint is the target location
            else:
                target = np.array([latitude[-1], longitude[-1]])


        midpoint = geoCalc.calculate_midpoint(start, target)


        if PRODUCE_FOLIUMMAP:
            ''' Create a folium map'''
            # Set up base map, centered on the midpoint between start and finish
            mymap = folium.Map(location = [midpoint[0], midpoint[1]], zoom_start=14)
    
            lat_shaped = latitude.reshape(len(latitude),1)
            long_shaped = longitude.reshape(len(latitude),1)

            # Draw a green circle with popup information at the start location
#             folium.CircleMarker(location = [start[0], start[1]], radius = 10, 
#                                             popup = 'Start -- Lat, Lon: {:4.4f}, {:4.4f}'.format(start[0], start[1]), 
#                                             color = '#00FF00', 
#                                             fill_color = '#00FF00').add_to(mymap)
                                            
            folium.Marker(location = [start[0], start[1]], 
                          popup = 'Landing: {:4.4f}, {:4.4f}'.format(start[0], start[1]),
                          icon=folium.Icon(color = 'green',icon='download')).add_to(mymap)
            
            # Draw a red circle with popup information at the target location
#             folium.CircleMarker(location = [target[0], target[1]], radius = 10, 
#                                             popup = 'Target -- Lat, Lon: {:4.4f}, {:4.4f}'.format(target[0], target[1]), 
#                                             color = '#FF0000', 
#                                             fill_color = '#FF0000').add_to(mymap)
            
            folium.Marker(location = [target[0], target[1]], 
                          popup = 'Target: {:4.4f}, {:4.4f}'.format(target[0], target[1]),
                          icon=folium.Icon(color = 'red',icon='flag')).add_to(mymap)

            if DRAW_WAYPOINTS:
                for index, waypoint in enumerate(waypoints):
                    if index < len(waypoints)-1:
                        # Draw white circles with popup information at each waypoint
                        folium.CirleMarker(location = [waypoint[0],waypoint[1]], 
                                            radius = 8, 
                                            popup='Waypoint Num: {:.0f} -- Lat, Lon: {:4.4f}, {:4.4f}'.format(index+1, waypoint[0], waypoint[1]), 
                                            color = '#FFFFFF', 
                                            fill_color = '#FFFFFF').add_to(mymap)

                #----- Draw the trial on a  map ---------------------------------------------------
            path = np.hstack((lat_shaped,long_shaped))

            # if path is large, downsample for plotting, plot only ~1000 points
            if np.shape(path)[0] > 1000:
                path = path[0::np.shape(path)[0]//1000]
    
            # Uncomment below to draw the path line in addition to the data point bubbles above
            # mymap.line(path, line_color='#FF0000', line_weight=5)
    
            # for each point on the path, draw a circle that contains system information
            #  in a popup when clicked on
            for index, current_pos in enumerate(path):
                if index < 51:
                    folium.CircleMarker(location = [current_pos[0], current_pos[1]], radius = 1, 
    #                                     popup = 'Time: {} -- Lat, Lon: {:4.4f}, {:4.4f} -- Speed: {:3.2f} m/s -- Actual Heading: {:3.0f} deg -- Desired Heading: {:3.0f} deg -- Distance to Waypoint: {:.0f} m'.format(time[index], latitude[index], longitude[index], gps_speed[index], imu_heading[index], bearing_to_waypoint[index], distance_to_waypoint[index]), 
                                        popup = 'Time: {} s -- Lat, Lon: {:4.4f}, {:4.4f} -- Distance to Target: {:.0f} m -- Actual Bearing: {:3.0f} deg -- Desired Heading: {:3.0f} deg -- Course Correction: {:3.0f}'.format(time[index], latitude[index], longitude[index], target_distance[index], current_bearing[index], desired_bearing[index], angle_to_turn[index]), 
                                        color = '#0000FF', fill_color = '#0000FF').add_to(mymap)
                else:
                    folium.CircleMarker(location = [current_pos[0], current_pos[1]], radius = 1, 
    #                                     popup = 'Time: {} -- Lat, Lon: {:4.4f}, {:4.4f} -- Speed: {:3.2f} m/s -- Actual Heading: {:3.0f} deg -- Desired Heading: {:3.0f} deg -- Distance to Waypoint: {:.0f} m'.format(time[index], latitude[index], longitude[index], gps_speed[index], imu_heading[index], bearing_to_waypoint[index], distance_to_waypoint[index]), 
                                        popup = 'Time: {} s -- Lat, Lon: {:4.4f}, {:4.4f} -- Distance to Target: {:.0f} m -- Actual Bearing: {:3.0f} deg -- Desired Heading: {:3.0f} deg -- Course Correction: {:3.0f}'.format(time[index], latitude[index], longitude[index], target_distance[index], current_bearing[index], desired_bearing[index], angle_to_turn[index]), 
                                        color = '#FF0000', fill_color = '#FF0000').add_to(mymap)


            # define filename - assumes that original datafile was .csv
            #   TODO: make this more robust
            map_filename = data_filename.replace('csv', 'html')
            mymap.save(map_filename)
        


if __name__ == "__main__":
    if BATCH:
        root = tk.Tk()
        root.withdraw()
        file_path = askdirectory()
    
        filename_pattern = file_path + "/*_controlHistory.csv"

        for data_filename in glob.glob(filename_pattern):
            print(data_filename)
            create_map(data_filename)

    else:
        root = tk.Tk()
        root.withdraw()

        data_filename = askopenfilename()
        create_map(data_filename)
