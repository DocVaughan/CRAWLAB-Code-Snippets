#! /usr/bin/env python

###############################################################################
# openCV_videoStream.py
#
# This script finds all of the .mp4
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 12/18/18
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
import glob
import os
from multiprocessing import Pool

# The full path to the folder of images to do inference on
# video_path = video_path = "/Volumes/1TB SSD/RobotX2018_Videos_test"
video_path = video_path = "/home/ubuntu/Documents/RobotX/2018Videos"
image_output_path = video_path + "/images/"


if not os.path.exists(image_output_path):
        os.makedirs(image_output_path)


def process_video_to_jpgs(video_file):
    video_capture = cv2.VideoCapture(video_file)
    
    image_file_basename = image_output_path + os.path.basename(video_file).split('.')[0]
    
    success = True # To force first loop on while
    
    # Set/reset the frame counter
    frame_counter = 0
    
    while(success):
        success, image = video_capture.read()
        
        if frame_counter % 30 == 0:
            image_filename = image_file_basename + "_frame{:04d}.jpg".format(frame_counter)
            cv2.imwrite(image_filename, image)
            print('Writing {}'.format(image_filename))
        
        frame_counter = frame_counter + 1
        

    # When everything done, release the capture
    video_capture.release()
    
    # Close any remaining openCV windows
    # cv2.destroyAllWindows()

# We use glob to iterate through al the jpgs in that folder. This pattern will
# match that.
video_glob_pattern = video_path + "/*.MOV"


# for video_file in glob.glob(video_glob_pattern):
#     p = multiprocessing.Process(target=process_video_to_jpgs, args=video_file)
#     p.start()

# p.join()
with Pool(12) as p:
    p.map(process_video_to_jpgs, glob.glob(video_glob_pattern))

