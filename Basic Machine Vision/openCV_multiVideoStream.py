#! /usr/bin/env python

###############################################################################
# openCV_multiVideoStream.py
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

import numpy as np
import cv2

cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(1)
cam3 = cv2.VideoCapture(2)


try:
    while(True):
        # Capture frame-by-frame
        ret1, frame1 = cam1.read()
        ret2, frame2 = cam2.read()
        ret3, frame3 = cam3.read()

        # Display the resulting frame
        cv2.imshow('Camera 1', frame1)
        cv2.imshow('Camera 2', frame2)
        cv2.imshow('Camera 3', frame3)
    
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