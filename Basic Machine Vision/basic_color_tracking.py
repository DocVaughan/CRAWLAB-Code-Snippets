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
#   * 03/23/18 - JEV - joshua.vaughan@louisiana.edu
#       - Improved the time tracking for the webcam version
#       - Improved data handling for webcam version
#       - Better commenting and formatting throughout
#       - 
#
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
import time
import cv2


FILENAME = '/Users/josh/Desktop/jump_freq.m4v'
WEBCAM = True # Set false to use the file at the path specified above

# define the lower and upper boundaries of the desired color in the HSV 
# Tennis-ball green
colorLower = (29, 86, 6)
colorUpper = (64, 255, 255)



# if a video path was not supplied, grab the reference
# to the webcam
if WEBCAM:
    camera = cv2.VideoCapture(0)

    # Create an array to hold the data. We don't know how long the capture will
    # last, so we create a "large" array. At 30fps, which is easily achievable
    # if we aren't displaying the image at every step, the array below would
    # provide enough storage for just over 30s of capture.
    data = np.zeros((1000, 3))  # TODO: Make this more robust to indefinite capture
 
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(FILENAME)
    fps = camera.get(cv2.CAP_PROP_FPS) 
    num_frames = int(camera.get(cv2.CAP_PROP_FRAME_COUNT))

    # Initialize the array list of tracked points. If we are using a video file
    # then we know the length and can be more precise in sizing the data array
    data = np.zeros((num_frames, 3))


# Start a counter variable and save the start times for use in time tracking
# of live processing
count = 0
last_time = time.time()
start_time = last_time
total_elapsed_time = 0.0


try:
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

        # Uncomment below to show the masked image
        # NOTE: This will *dramatically* slow down the processing
        # cv2.imshow("Frame", mask)
    
        # find contours in the mask and initialize the current
        # (x, y) center of the object
        cnts = cv2.findContours(mask.copy(),
                                cv2.RETR_EXTERNAL,
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

            if WEBCAM:
                data[count] = np.hstack((total_elapsed_time, np.asarray(center))).reshape(1,3)
            else:
                data[count] = np.hstack((count * 1/fps, np.asarray(center))).reshape(1,3)
                

        # Uncomment below to show the frame at each iteration
        # NOTE: This will *dramatically* slow down the processing
        # cv2.imshow("Frame", frame)
        
        # Calculate the time elapsed and estimate current fps from it
        current_time = time.time()
        elapsed_time = current_time - last_time
        
        total_elapsed_time = current_time - start_time
        
        last_time = current_time # save current time for next loop
        fps_estimate = 1 / elapsed_time
        # Print out the status and estimate of current FPS
        print('Center: {} \t FPS: {:5.2f}'.format(center, fps_estimate))

except (KeyboardInterrupt):
    print("\n\nClosing...")
    
    # Uncomment below to re-raise the exception
    # raise
    
finally:
    # Now, we can create a mask matching any rows that are all zeros
    mask = np.all(np.isnan(data), axis=1) | np.all(data == 0, axis=1)
    
    # Then, trim the data based on that mask. This way, the data array will 
    # only have rows that have data in them.
    data = data[~mask]

    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()