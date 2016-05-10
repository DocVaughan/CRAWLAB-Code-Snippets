#! /usr/bin/env python

###############################################################################
# basic_color_tracking.py
#
# Basic color tracking with OpenCV3 and Python
#
# OpenCV 
#    - http://opencv.org
#   - Install with conda by - 
#        $ conda install -c https://conda.binstar.org/menpo opencv3
# 
# Code modified from:
#   - http://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 05/09/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
import cv2


FILENAME = '/Users/josh/Desktop/jump_freq.m4v'
WEBCAM = False

# define the lower and upper boundaries of the desired color in the HSV 
colorLower = (100, 124, 92)
colorUpper = (120, 172, 218)

# Initialize the array list of tracked points
 
 
# if a video path was not supplied, grab the reference
# to the webcam
if WEBCAM:
    camera = cv2.VideoCapture(0)
 
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(FILENAME)
    fps = camera.get(cv2.CAP_PROP_FPS) 
    num_frames = int(camera.get(cv2.CAP_PROP_FRAME_COUNT))
    data = np.zeros((num_frames, 3))

count = 0
# Loop through the video
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
 
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if not WEBCAM and not grabbed:
        break
 
    # convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    # construct a mask for the desired color, then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # cv2.imshow("Frame", mask)
    
        # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
 
    
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
        
        data[count] = np.hstack((count * 1/fps, np.asarray(center))).reshape(1,3)


    # show the frame to our screen
#     cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    count = count + 1
 
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()