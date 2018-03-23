#! /usr/bin/env python

###############################################################################
# openCV_multiVideoStream_intervalSave.py
#
# Simply display the video captures by 3 USB cameras
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 07/28/17
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

from __future__ import print_function

import numpy as np
import cv2

import time
import datetime # for unique filesaves

SHOW_IMAGES = False # Set true to open windows showing the image from each cam

cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(1)
cam3 = cv2.VideoCapture(2)


# Read a few frames to force the camera to adjust to current lighting, etc
for _ in range(10):
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()
    ret3, frame3 = cam3.read()
    time.sleep(0.1)

try:
    while(True):
        # Capture frame-by-frame - end='' prevent a line return here
        print('Capturing a frame from each camera, and...', end='')
        ret1, frame1 = cam1.read()
        ret2, frame2 = cam2.read()
        ret3, frame3 = cam3.read()

        if SHOW_IMAGES: 
            # Display the resulting frame
            cv2.imshow('Camera 1', frame1)
            cv2.imshow('Camera 2', frame2)
            cv2.imshow('Camera 3', frame3)
        
        # Define the image filenames, made unique by timestamping them
        time_stamp_string = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        file_save1 = 'cam1_' + time_stamp_string + '.jpg'
        file_save2 = 'cam2_' + time_stamp_string + '.jpg'
        file_save3 = 'cam3_' + time_stamp_string + '.jpg'
        
        # Now, actually save the files
        print(' saving the images.')
        cv2.imwrite(file_save1, frame1)
        cv2.imwrite(file_save2, frame2)
        cv2.imwrite(file_save3, frame3)
        
        # Wait 10 seconds before getting the next frame
        time.sleep(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except (KeyboardInterrupt, SystemExit):
    pass

finally:
    # Do stuff no matter how you exit
    # When everything done, release the captures
    cam1.release()
    cam2.release()
    cam3.release()

    cv2.destroyAllWindows()