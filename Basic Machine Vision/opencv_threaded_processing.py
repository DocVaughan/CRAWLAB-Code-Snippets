#! /usr/bin/env python

###############################################################################
# opencv_threaded_processing.py
#
# Demonstrating using threading to speed up an opencv pipeline. 
# Rates will still be limited by hardware. Here, an fps improvements beyond
# the hardware limit of the camera will be somewhat misleading. The script is
# simply processing the same frame multiple times.
#
# Uses opencv 3 and the imutils library
# 
# OpenCV was installed from:
#  - https://anaconda.org/anaconda/opencv

# imutils installed using instructions at:
#  - https://github.com/jrosebr1/imutils
#
# Adapted from code at:
#  https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
#  
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 03/23/18
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

# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2

import numpy as np
import time
import matplotlib.pyplot as plt

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=150,
    help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
    help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

# Video codec to use in writing 
# avc1 is h264, which we should use, if at all possible
FOURCC = cv2.VideoWriter_fourcc('a','v','c','1')

# Set the camera number to use (zero indexed)
CAMERA_SOURCE = 1

# define the lower and upper boundaries of the desired color in the HSV 
# Tennis-ball green
colorLower = (29, 86, 6)
colorUpper = (64, 255, 255)


# Set up arrays to store the time and centroid location of the blob
data = np.zeros((args["num_frames"], 3))  # TODO: Make this more robust to indefinite capture


# We'll process THREADED_MULT x the number of frames we processed unthreaded
THREADED_MULT = 10
data_threaded = np.zeros((args["num_frames"] * THREADED_MULT, 3))  # TODO: Make this more robust to indefinite capture



try:
    # grab a pointer to the video stream and initialize the FPS counter
    print("[INFO] sampling frames from webcam...")
    stream = cv2.VideoCapture(CAMERA_SOURCE)
    fps = FPS().start()
    
    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    # We convert the resolutions from float to integer.
    frame_width = int(stream.get(3))
    frame_height = int(stream.get(4))

    out = cv2.VideoWriter('output.mp4', FOURCC, 30.0, (frame_width,frame_height))


    # Start a counter variable and save the start times for use in time tracking
    # of live processing
    count = 0
    last_time = time.time()
    start_time = last_time
    total_elapsed_time = 0.0

    # loop over some frames
    while fps._numFrames < args["num_frames"]:
        # grab the frame from the stream and resize it to have a maximum
        # width of 400 pixels
        (grabbed, frame) = stream.read()

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
            
                data[count] = np.hstack((total_elapsed_time, np.asarray(center))).reshape(1,3)
                
                # Write to a file
                out.write(frame)

        # check to see if the frame should be displayed to our screen
        if args["display"] > 0:
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
        
        # Calculate the time elapsed and estimate current fps from it
        count = count + 1
        current_time = time.time()
        elapsed_time = current_time - last_time
    
        total_elapsed_time = current_time - start_time
    
        last_time = current_time # save current time for next loop
        fps_estimate = 1 / elapsed_time
        
        # update the FPS counter
        fps.update()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

except (KeyboardInterrupt):
    print("\n\nClosing...")
    
    # Uncomment below to re-raise the exception
    # raise
    
finally:
    # Now, we can create a mask matching any rows that are all zeros
    mask = np.all(np.isnan(data), axis=1) | np.all(data == 0, axis=1)
    
    # Then, trim the data based on that mask. This way, the data array will 
    # only have rows that have data in them.
    data= data[~mask]
    
    # do a bit of cleanup
    stream.release()
    out.release()
    cv2.destroyAllWindows()




try:
    # created a *threaded *video stream, allow the camera senor to warmup,
    # and start the FPS counter
    print("[INFO] sampling THREADED frames from webcam...")
    vs = WebcamVideoStream(src=CAMERA_SOURCE).start()
    fps = FPS().start()

    out_threaded = cv2.VideoWriter('output_threaded.mp4', FOURCC, 90.0, (frame_width,frame_height))

    # Start a counter variable and save the start times for use in time tracking
    # of live processing
    count = 0
    last_time = time.time()
    start_time = last_time
    total_elapsed_time = 0.0

    # loop over some frames...this time using the threaded stream
    while fps._numFrames < args["num_frames"] * THREADED_MULT:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()

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

                data_threaded[count] = np.hstack((total_elapsed_time, np.asarray(center))).reshape(1,3)

                # Write to a file
                out_threaded.write(frame)

        # check to see if the frame should be displayed to our screen
        if args["display"] > 0:
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
    
        # Calculate the time elapsed and estimate current fps from it
        count = count + 1
        current_time = time.time()
        elapsed_time = current_time - last_time
    
        total_elapsed_time = current_time - start_time
    
        last_time = current_time # save current time for next loop
        fps_estimate = 1 / elapsed_time
        


        # update the FPS counter
        fps.update()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

except (KeyboardInterrupt):
    print("\n\nClosing...")
    
    # Uncomment below to re-raise the exception
    # raise
    
finally:
    # Now, we can create a mask matching any rows that are all zeros
    mask = np.all(np.isnan(data_threaded), axis=1) | np.all(data_threaded == 0, axis=1)
    
    # Then, trim the data based on that mask. This way, the data array will 
    # only have rows that have data in them.
    data_threaded = data_threaded[~mask]

    # do a bit of cleanup
    out_threaded.release()
    cv2.destroyAllWindows()
    vs.stop()





# Set the plot size - 3x2 aspect ratio is best
fig = plt.figure(figsize=(6,4))
ax = plt.gca()
plt.subplots_adjust(bottom=0.17, left=0.17, top=0.96, right=0.96)

# Change the axis units font
plt.setp(ax.get_ymajorticklabels(),fontsize=18)
plt.setp(ax.get_xmajorticklabels(),fontsize=18)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Turn on the plot grid and set appropriate linestyle and color
ax.grid(True,linestyle=':', color='0.75')
ax.set_axisbelow(True)

# Define the X and Y axis labels
plt.xlabel('Time (s)', fontsize=22, weight='bold', labelpad=5)
plt.ylabel('Horiz. Location (pixels)', fontsize=22, weight='bold', labelpad=10)
 
plt.plot(data[:,0], data[:,1], linewidth=2, linestyle='--', label=r'Baseline')
plt.plot(data_threaded[:,0], data_threaded[:,1], linewidth=2, linestyle='-', label=r'Threaded')

# uncomment below and set limits if needed
# plt.xlim(0,5)
# plt.ylim(0,10)

# Create the legend, then fix the fontsize
leg = plt.legend(loc='upper right', ncol = 1, fancybox=True)
ltext  = leg.get_texts()
plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
# plt.savefig('plot_filename.pdf')



# Set the plot size - 3x2 aspect ratio is best
fig = plt.figure(figsize=(6,4))
ax = plt.gca()
plt.subplots_adjust(bottom=0.17, left=0.17, top=0.96, right=0.96)

# Change the axis units font
plt.setp(ax.get_ymajorticklabels(),fontsize=18)
plt.setp(ax.get_xmajorticklabels(),fontsize=18)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Turn on the plot grid and set appropriate linestyle and color
ax.grid(True,linestyle=':', color='0.75')
ax.set_axisbelow(True)

# Define the X and Y axis labels
plt.xlabel('Time (s)', fontsize=22, weight='bold', labelpad=5)
plt.ylabel('Vertical Location (pixels)', fontsize=22, weight='bold', labelpad=10)
 
plt.plot(data[:,0], data[:,2], linewidth=2, linestyle='--', label=r'Baseline')
plt.plot(data_threaded[:,0], data_threaded[:,2], linewidth=2, linestyle='-', label=r'Threaded')

# uncomment below and set limits if needed
# plt.xlim(0,5)
# plt.ylim(0,10)

# Create the legend, then fix the fontsize
leg = plt.legend(loc='upper right', ncol = 1, fancybox=True)
ltext  = leg.get_texts()
plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
# plt.savefig('plot_filename.pdf')


# Set the plot size - 3x2 aspect ratio is best
fig = plt.figure(figsize=(6,4))
ax = plt.gca()
plt.subplots_adjust(bottom=0.17, left=0.17, top=0.96, right=0.96)

# Change the axis units font
plt.setp(ax.get_ymajorticklabels(),fontsize=18)
plt.setp(ax.get_xmajorticklabels(),fontsize=18)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Turn on the plot grid and set appropriate linestyle and color
ax.grid(True,linestyle=':', color='0.75')
ax.set_axisbelow(True)

# Define the X and Y axis labels
plt.xlabel('Horizontal Location (pixels)', fontsize=22, weight='bold', labelpad=5)
plt.ylabel('Vertical Location (pixels)', fontsize=22, weight='bold', labelpad=10)
 
plt.plot(data[:,1], data[:,2], linewidth=2, linestyle='--', label=r'Baseline')
plt.plot(data_threaded[:,1], data_threaded[:,2], linewidth=2, linestyle='-', label=r'Threaded')

# uncomment below and set limits if needed
# plt.xlim(0,5)
# plt.ylim(0,10)
plt.axis('equal')

# Create the legend, then fix the fontsize
leg = plt.legend(loc='upper right', ncol = 1, fancybox=True)
ltext  = leg.get_texts()
plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
# plt.savefig('plot_filename.pdf')

# show the figure
plt.show()