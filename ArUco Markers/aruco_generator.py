#! /usr/bin/env python

###############################################################################
# aruco_generator.py
#
# script testing basic generation of Aruco markers
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
 
MARKER_ID = 2           # ID for generated maker
MARKER_SIZE = 640       # Pixel size of (square) marker
 
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

img = aruco.drawMarker(aruco_dict, MARKER_ID, MARKER_SIZE)

# Write the generated image to a file
cv2.imwrite(f"test_marker_{MARKER_ID}.jpg", img)
 
# Then, show is
cv2.imshow('frame', img)
cv2.waitKey(0)
cv2.destroyAllWindows()