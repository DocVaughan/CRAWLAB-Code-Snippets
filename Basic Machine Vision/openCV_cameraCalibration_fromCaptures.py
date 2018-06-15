#! /usr/bin/env python

###############################################################################
# openCV_cameraCalibration_fromCaptures.py
#
# Script to do basic camera calibration in OpenCV using a checkerboard and 
# a series of captures from the camera. As written, this code uses the 10x8 
# (9x7 internal) grid found at:
#  https://www.mrpt.org/downloads/camera-calibration-checker-board_9x7.pdf
# a copy of which is found in this repository.
#
# Code adapted from that at:
#  * http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html
#
# For more information, see:
#  * http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html
#  * https://github.com/opencv/opencv/blob/master/samples/python/calibrate.py
#  * https://longervision.github.io/2017/03/19/opencv-internal-calibration-chessboard/
#  
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 06/15/18
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

# For saving calibration data, you may need to install via 'conda install pyyaml'
import yaml  

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:7].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


# Define the camera capture instance
cap = cv2.VideoCapture(0)

# number of images in which we've found the corners of the checkerboard
num_found = 0 

NUM_IMAGES = 10 # The number of images we want to use for calibration

while num_found < NUM_IMAGES:
    ret, img = cap.read() # Capture a frame
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (9,7), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners on the original image
        img = cv2.drawChessboardCorners(img, (9,7), corners2,ret)
        cv2.imshow('img',img)
        cv2.waitKey(1000) # Display until a key is pressed or 1s passes
        
        num_found = num_found + 1 # We found a checkerboard, increment the counter
        
# Now, we'll calculate the camera distortion based on the images we found above
rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(objpoints, 
                                                                  imgpoints, 
                                                                  gray.shape[::-1], 
                                                                  None, 
                                                                  None)
                                                                  
# We can save that calibration information to be used later for other images
# or processing from this camera. We'll save it to a yaml file
data = {'camera_matrix': np.asarray(camera_matrix).tolist(), 'dist_coeff': np.asarray(dist_coefs).tolist()}

with open('calibration.yaml', 'w') as f:
    yaml.dump(data, f)
    
# To load that calibration file, we would need to have the calibration.yaml
# file for the camera being used and pass its location below
CALIBRATION_FILENAME = 'calibration.yaml'
with open(CALIBRATION_FILENAME) as f:
    loadeddict = yaml.load(f)

mtxloaded = np.asarray(loadeddict.get('camera_matrix'))
distloaded = np.asarray(loadeddict.get('dist_coeff'))


# We could then use that information to correct for distortion in the
# images from that camera
ret, img = cap.read() # capture another imaage
h,  w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtxloaded, 
                                                  distloaded,
                                                  (w,h),1,(w,h))

# We could not operate on the corrected image
corrected_img = cv2.undistort(img, mtxloaded, distloaded, None, newcameramtx)

# Or rop the image based on the corrections, then operate on it
x,y,w,h = roi
corrected_img = corrected_img[y:y+h, x:x+w]

# Uncomment the line below to save the corrected image
# cv2.imwrite('calibrated_result.png', corrected_img)

# Now, show the original and corrected images
cv2.imshow('Original', img)
cv2.imshow('Corrected', corrected_img)
cv2.waitKey() # Display until a key is pressed

cap.release()
cv2.destroyAllWindows()
