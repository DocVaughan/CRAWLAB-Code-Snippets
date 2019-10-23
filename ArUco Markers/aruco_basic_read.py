#! /usr/bin/env python

###############################################################################
# aruco_basic_read.py
#
# script testing basic reading of Aruco markers. Just puts a point at the corner
#
# Code modified from that at:
#  http://www.philipzucker.com/aruco-in-opencv/
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 10/21/19
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

import cv2
import cv2.aruco as aruco

import os

# Define the filename containing the markers
FILENAME = 'marker_0000.jpg'

# Get the base of the filenmae. We'll use it to save the processed image with
# a similar name later
base_filename = os.path.basename(FILENAME)
base_filename = base_filename.split('.')[0]

# Load the image 
img = cv2.imread(FILENAME)

# Covert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Define the type of marker to look for and any parameters in processing
aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
parameters =  aruco.DetectorParameters_create()

# Get the list of ids detected and their corners
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, 
                                                      aruco_dict, 
                                                      parameters=parameters)

# Draw the corners and ids on the original, color image
img = aruco.drawDetectedMarkers(img, corners, ids, borderColor=(0, 0, 255, 255))


# This calibration is for the monocular camera used in the rotors_simulator
#  ROS package - https://github.com/CRAWlab/rotors_simulator
# TODO: 10/21/19 - JEV - Provide instructions for generating calibration
# NOTE; See https://github.com/CRAWlab/camera_calibration for one way to generate
camera_matrix = np.array([[218.02853116,   0.        , 320.6379542 ],
                          [  0.        , 217.78473815, 240.27390847],
                          [  0.        ,   0.        ,   1.        ]])

dist_coeffs = np.array([[-0.00894801, 0.00303889, 0.00012614, 0.00035685, -0.00083798]])

markerLength = 0.1778  # m?? TODO: 10/21/19 - JEV - correct for actual markers

# Estimate the pose of the markers in the frame
rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 
                                                markerLength, 
                                                camera_matrix, 
                                                dist_coeffs)

# Loop through all the markers found and draw the axes on them
for index, ID in enumerate(ids):
    aruco.drawAxis(img, camera_matrix, dist_coeffs, rvec[index], tvec[index], 0.5)

# Write the generated image to a file
ouptut_filename = base_filename + "_ArUco_processed.jpg"
cv2.imwrite(ouptut_filename, img)

# 