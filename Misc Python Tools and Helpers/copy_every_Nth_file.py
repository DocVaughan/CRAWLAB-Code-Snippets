#! /usr/bin/env python

###############################################################################
# copy_every_Nth_file.py
#
# Grab every N-th file from a folder and copy it to another
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 07/02/19
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

import glob
import os
import shutil
from random import shuffle

file_path = '/Volumes/1TB SSD/RoboBoat Images'
desired_path = '/Volumes/1TB SSD/RoboBoat Images/sample'

# This will create desired path if it does not already exist
if not os.path.exists(desired_path):
    os.makedirs(desired_path)

files = glob.glob(file_path + '/*ZED*.jpg')    # Get a list of files in the directory, then
# shuffle(files)          # randomize the order of the files

EVERY_NTH = 7  # Get every Nth file

# Now work through the list of files
for index, file in enumerate(files):
    file_basename = os.path.basename(file)
    new_filename_with_path = os.path.join(desired_path, file_basename)
    
    # If evenly divisible by EVERY_NTH, then copy it to the destination directory
    if index % EVERY_NTH == 0:
        print('Copying: {}'.format(file_basename))
        shutil.copy2(file, new_filename_with_path)
        
print("Sampled {} files".format(index))