#! /usr/bin/env python

###############################################################################
# aruco_camera_calibration.py
#
# Script to calibrate a camera using an ArUco grid (ChArUco). Code adapted from
# that at:
#  * https://github.com/CRAWlab/camera_calibration
#  * https://docs.opencv.org/3.4/da/d13/tutorial_aruco_calibration.html
#  * https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/sandbox/ludovic/aruco_calibration_rotation.html
#  * https://answers.opencv.org/question/98447/camera-calibration-using-charuco-and-python/
#
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
import glob
import tqdm
import yaml

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

arucoParams = aruco.DetectorParameters_create()

CALIBRATION_IMAGE_PATH = '/Users/localadmin/Desktop/untitled folder/'
calibration_image_glob_pattern = CALIBRATION_IMAGE_PATH + '*.jpg'

img_list = []
calib_filenames = glob.glob(calibration_image_glob_pattern)

print('Using ...', end='')

for index, filename in enumerate(calib_filenames):
    print(index, '', end='')
    img = cv2.imread(filename)
    img_list.append(img)
    h, w, c = img.shape

print('Calibration images')

counter, corners_list, id_list = [], [], []
first = True

for im in img_list:
    img_gray = cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(img_gray, aruco_dict, parameters=arucoParams)
    
    if first == True:
        corners_list = corners
        id_list = ids
        first = False
    else:
        corners_list = np.vstack((corners_list, corners))
        id_list = np.vstack((id_list, ids))
    
    counter.append(len(ids))

print('Found {} unique markers'.format(np.unique(ids)))

counter = np.array(counter)
print ("Calibrating camera .... Please wait...")

#mat = np.zeros((3,3), float)
ret, mtx, dist, rvecs, tvecs = aruco.calibrateCameraAruco(corners_list, id_list, counter, board, img_gray.shape, None, None )

print("Camera matrix is \n", mtx, "\n And is stored in calibration.yaml file along with distortion coefficients : \n", dist)
data = {'camera_matrix': np.asarray(mtx).tolist(), 'dist_coeff': np.asarray(dist).tolist()}

with open("calibration.yaml", "w") as f:
    yaml.dump(data, f)