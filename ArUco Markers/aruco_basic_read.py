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
FILENAME = 'left0000.jpg'

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


# We'll use a "fake" camera calibration matrix for now. It might mess up the results.
# TODO: 10/21/19 - JEV - provide instructions for generating calibration
# NOTE; See https://github.com/CRAWlab/camera_calibration for one way to generate
camera_matrix = np.array([[813.18292644,   0.        , 318.76403921],
                          [  0.        , 812.39009204, 239.16050615],
                          [  0.        ,   0.        ,   1.        ]])

dist_coeffs = np.array([[-1.01845774e-01, 3.58089018e-01, -1.67284171e-04,  
                          2.08061053e-03, 7.48716318e-02]])

markerLength = 3.75  # TODO: 10/21/19 - JEV - correct for actual markers

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