#! /usr/bin/env python

###############################################################################
# track_via_mouse_click.py.py
#
# Creates an array of positions within the frame based on the point
# clicked on in each frame. Essentially, we are doing manual feature tracking.
#
# OpenCV 
#    - http://opencv.org
#   - Install with conda by - 
#        $ conda install -c https://conda.binstar.org/menpo opencv3
# 
# Code modified from:
#   - http://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 11/18/16
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


FILENAME = 'Tipover_Unsecure_CWs_CloseUp_trimmed.mov'
WEBCAM = True

# global that gets changed to false after we click the mouse button on each 
# frame of the video
waiting_for_click = True

# global counter for frame number
count = 0


def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    # TODO: Try to eliminate global variables - 11/18/16 - JEV
    global data, count
    global waiting_for_click
 
    # if the left mouse button was clicked, record the (x, y) coordinates 
    if event == cv2.EVENT_LBUTTONUP:
        t = count * 1/fps
        data[count, :] = (t, x, y)
        
        print('t = {}, x = {}, y = {}'.format(t, x, y))
        
        waiting_for_click = False
        count = count + 1
        

# if using the webcamgrab the reference to the webcam
if WEBCAM:
    camera = cv2.VideoCapture(0)
else: # otherwise, grab a reference to the video file
    camera = cv2.VideoCapture(FILENAME)
    
    # NOTE: Be careful with fps, openCV sometimes gets this one wrong.
    # It seems to depend on the type of encoding used to generate the video.
    fps = camera.get(cv2.CAP_PROP_FPS) 
    
    num_frames = int(camera.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # create an array of zeros to fill with tracking data
    data = np.zeros((num_frames, 3))

try:
    # Loop through the video
    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()
 
        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if not WEBCAM and not grabbed:
            break

        # show the frame to our screen
        cv2.imshow("Frame", frame)
        # Define the callback function for mouse action
        cv2.setMouseCallback("Frame", click_and_crop)
        waiting_for_click = True


        while True:
            if waiting_for_click:    
                key = cv2.waitKey(10) & 0xFF
            
                # if the 'q' key is pressed, stop the loop
                if key == ord("q"):
                    break
            else:
                break

        # if the 'q' key is pressed, now break this loop
        if key == ord("q"):
            break

except (KeyboardInterrupt, SystemExit):
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
    data_filename = FILENAME + '_data.csv'
    
    np.savetxt(data_filename, data, delimiter=',') 
    

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
data_filename = FILENAME + '_data.csv'
np.savetxt(data_filename, data, delimiter=',') 