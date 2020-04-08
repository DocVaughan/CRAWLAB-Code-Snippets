#! /usr/bin/env python

###############################################################################
# aruco_threaded_tracking.py
#
# script testing basic tracking of Aruco markers, but splitting reading the
# image from the camera into a separate thread
#
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 04/03/20
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

import cv2
import cv2.aruco as aruco
import numpy as np
import matplotlib.pyplot as plt
import threading



# Define constants for this script
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_6X6_250)
MARKERLENGTH = 0.1778  # m?? TODO: 10/21/19 - JEV - correct for actual markers

# This calibration is for the monocular camera used in the rotors_simulator
#  ROS package - https://github.com/CRAWlab/rotors_simulator
# TODO: 10/21/19 - JEV - Provide instructions for generating calibration
# NOTE; See https://github.com/CRAWlab/camera_calibration for one way to generate
# CAMERA_MATRIX = np.array([[218.02853116,   0.        , 320.6379542 ],
#                           [  0.        , 217.78473815, 240.27390847],
#                           [  0.        ,   0.        ,   1.        ]])
# 
# DIST_COEFFS = np.array([[-0.00894801, 0.00303889, 0.00012614, 0.00035685, -0.00083798]])

# These matrices are for the camera on my iMac
CAMERA_MATRIX = np.array([[5.06968479e+03, 0.00000000e+00, 5.19942085e+02],
                          [0.00000000e+00, 5.21560115e+03, 9.10942632e+02],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
                          
DIST_COEFFS = np.array([[-2.34400379e-01,  3.00945461e+01, -2.53342956e-02, 
                         -9.27051884e-02, -3.25346306e+02]])




class VideoCaptureTreading:
    def __init__(self, src=0, width=640, height=480):
        self.src = src
        self.capture = cv2.VideoCapture(self.src)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.grabbed, self.frame = self.capture.read()
        self.started = False
        self.read_lock = threading.Lock()

    def set(self, var1, var2):
        self.capture.set(var1, var2)

    def start(self):
        if self.started:
            print('[!] Threaded video capturing has already been started.')
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.capture.read()
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
            grabbed = self.grabbed
        return grabbed, frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.capture.release()


# We'll do video capture on the webcam
capture = VideoCaptureTreading(0)
capture.start()

parameters =  aruco.DetectorParameters_create()

try:
    while (True):
        # Capture frame-by-frame
        ret, frame = capture.read()
    
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
        # lists of ids and the corners beloning to each id
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, 
                                                              ARUCO_DICT, 
                                                              parameters=parameters)
    
        # corners is [] if no markers are found
        if corners != []:
            # Draw the corners and ids on the original, color image
            img = aruco.drawDetectedMarkers(frame, 
                                            corners, 
                                            ids, 
                                            borderColor=(0, 0, 255, 255))



            # Estimate the pose of the markers in the frame
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 
                                                            MARKERLENGTH, 
                                                            CAMERA_MATRIX, 
                                                            DIST_COEFFS)
            # Loop through all the markers found and draw the axes on them
            for index, ID in enumerate(ids):
                aruco.drawAxis(frame, CAMERA_MATRIX, DIST_COEFFS, 
                               rvec[index], tvec[index], 0.5)
    
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # When everything done, release the capture
    capture.stop()
    cv2.destroyAllWindows()