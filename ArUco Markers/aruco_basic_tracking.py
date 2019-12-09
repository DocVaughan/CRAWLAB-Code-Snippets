#! /usr/bin/env python

###############################################################################
# aruco_basic_tracking.py
#
# script testing basic tracking of Aruco markers
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
 
# We'll do video capture on the webcam
cap = cv2.VideoCapture(0)
 
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
 
    # lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, 
                                                          aruco_dict, 
                                                          parameters=parameters)

    # Draw the corners and ids on the original, color image
    img = aruco.drawDetectedMarkers(frame, 
                                    corners, 
                                    ids, 
                                    borderColor=(0, 0, 255, 255))


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
        aruco.drawAxis(frame, camera_matrix, dist_coeffs, 
                       rvec[index], tvec[index], 0.5)
    
    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()