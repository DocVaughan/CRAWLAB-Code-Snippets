#! /usr/bin/env python

###############################################################################
# aruco_grid_generator.py
#
# Script to generate grids of ArUco markers, which are often used for camera 
# calibration. These are typically called ChArUco boards.
#
# Code modified from that at:
#  * https://docs.opencv.org/3.4/da/d13/tutorial_aruco_calibration.html
#  * https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/sandbox/ludovic/aruco_calibration_rotation.html
#  * https://answers.opencv.org/question/98447/camera-calibration-using-charuco-and-python/
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 10/23/19
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - @doc_vaughan
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
from cv2 import aruco

# Define the type of ArUco markers to make the board from
aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)

# Define the board's setup and create it
NUM_SQUARES_X = 7
NUM_SQUARES_Y = 5

# We're using inches to match opencv dpi saving
SQUARE_LENGTH = 3                       # absolute length of a square (inch) 
MARKER_LENGTH = 0.8 * SQUARE_LENGTH     # absolute length of a marker (inch)

# CharucoBoard_create(squaresX, squaresY, squareLength, markerLength, dictionary)
board = aruco.CharucoBoard_create(NUM_SQUARES_X, 
                                  NUM_SQUARES_Y, 
                                  SQUARE_LENGTH, 
                                  MARKER_LENGTH, 
                                  aruco_dict)

# Then draw it, specifyin the output dimensions in pixels. We're using 72 
# pixels per inch here, to match openCV saving for png images. This will create
# markers whose physicaly size, when printed at 100%, matches that which we 
# specified above.
imboard = board.draw((int(NUM_SQUARES_X * SQUARE_LENGTH * 72), 
                      int(NUM_SQUARES_Y * SQUARE_LENGTH * 72)))

# Now, save the board. Be sure to change the filename to reflect the aruco_dict
# that you used to generate it. We also include the square length and marker 
# length since those parameters are important for both calibration and pose
# estimation. We'll first save it as a .png
cv2.imwrite(f'ChArUco_orig_sq{SQUARE_LENGTH}_mark{MARKER_LENGTH:.2f}.png', 
            imboard)