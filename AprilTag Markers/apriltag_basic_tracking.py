#! /usr/bin/env python

###############################################################################
# apriltag_basic_tracking.py
#
# script testing basic tracking of AprilTag markers
#
# Code modified from that at:
#  https://github.com/AprilRobotics/apriltag/wiki/AprilTag-User-Guide 
# and
#  https://www.pyimagesearch.com/2020/11/02/apriltag-with-python/
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 10/20/21
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
import numpy as np
import apriltag

 
# We'll do video capture on the webcam
cap = cv2.VideoCapture(0)

# This calibration is for the monocular camera used in the rotors_simulator
#  ROS package - https://github.com/CRAWlab/rotors_simulator
# TODO: 10/21/19 - JEV - Provide instructions for generating calibration
# NOTE; See https://github.com/CRAWlab/camera_calibration for one way to generate
# camera_matrix = np.array([[218.02853116,   0.        , 320.6379542 ],
#                           [  0.        , 217.78473815, 240.27390847],
#                           [  0.        ,   0.        ,   1.        ]])
# 
# dist_coeffs = np.array([[-0.00894801, 0.00303889, 0.00012614, 0.00035685, -0.00083798]])

# These matrices are for the camera on my iMac
CAMERA_MATRIX = np.array([[5.06968479e+03, 0.00000000e+00, 5.19942085e+02],
                          [0.00000000e+00, 5.21560115e+03, 9.10942632e+02],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
                          
DIST_COEFFS = np.array([[-2.34400379e-01,  3.00945461e+01, -2.53342956e-02, 
                         -9.27051884e-02, -3.25346306e+02]])
                         
markerLength = 0.1524  # m - markers are 6in 

try:
    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()
    
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        detector = apriltag("tagStandard36h11")
        detections = detector.detect(gray)
        
        # loop over the AprilTag detection results
        for r in detections:
            # extract the bounding box (x, y)-coordinates for the AprilTag
            # and convert each of the (x, y)-coordinate pairs to integers
            (ptA, ptB, ptC, ptD) = r.corners
            ptB = (int(ptB[0]), int(ptB[1]))
            ptC = (int(ptC[0]), int(ptC[1]))
            ptD = (int(ptD[0]), int(ptD[1]))
            ptA = (int(ptA[0]), int(ptA[1]))
           
            # draw the bounding box of the AprilTag detection
            cv2.line(frame, ptA, ptB, (0, 255, 0), 2)
            cv2.line(frame, ptB, ptC, (0, 255, 0), 2)
            cv2.line(frame, ptC, ptD, (0, 255, 0), 2)
            cv2.line(frame, ptD, ptA, (0, 255, 0), 2)
           
            # draw the center (x, y)-coordinates of the AprilTag
            (cX, cY) = (int(r.center[0]), int(r.center[1]))
            cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
           
            # draw the tag family on the image
            tagFamily = r.tag_family.decode("utf-8")
            cv2.putText(frame, tagFamily, (ptA[0], ptA[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
           
            print("[INFO] tag family: {}".format(tagFamily))
        
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()