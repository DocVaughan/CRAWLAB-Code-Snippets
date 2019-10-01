#! /usr/bin/env python 

################################################################################
# spatial_tracking_error.py
#
# Script to a demonstrate calculating the spatial error between two curves. For
# each element in one (response) array we find the distance to closest point on
# another array (representing the desired trajctory)
#
# NOTE: Plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
# 
# Created: 09/25/19
#   - Joshua Vaughan 
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
# TODO:
#   * 
#
################################################################################

import numpy as np
import matplotlib.pyplot as plt

# Define an array representing the time 
DURATION = 5        # seconds of data to use
SAMPLE_TIME = 0.01   # Sampling time
time = np.linspace(0, DURATION, int(DURATION/SAMPLE_TIME) + 1)

# Define the desired trajetory in 2D. This should be a circle of radius 1
x_desired = np.sin(2 * np.pi * time)
y_desired = np.cos(2 * np.pi * time)

# Define arrays such that each row represents an (x,y) position at time N*dt
# where N is the array index and dt was the sample time used. Here, we'll use
# the desired trajectory with a phase shift and a higher frequency sinusoided 
# added to it
x_actual = np.sin(2 * np.pi * time + np.pi / 4) + 0.25 * np.sin(10 * 2 * np.pi * time)
y_actual = np.cos(2 * np.pi * time + np.pi / 4) + 0.25 * np.cos(10 * 2 * np.pi * time)

# Now, we can calculate various error metrics between two two trajectories

# The easiest to implement is the temporal error. We just get the Euclidian 
# distance between the desired coordinates and actual coordinates at each 
# point in time. Since the array indices correspond to sample times, we can 
# just do this at every index of the two arrays
temporal_error = np.sqrt((x_desired - x_actual)**2 + (y_desired - y_actual)**2)

# Now, calculate the integral square error (ISE). We'll calculate the total over 
# the entire time interval and the running total.
integral_square_error_overTime = np.cumsum(temporal_error**2) * SAMPLE_TIME
integral_square_error_total = np.trapz(temporal_error**2, dx=SAMPLE_TIME)

# Now, calculate the integral absolute error (IAE). We'll calculate the total 
# over the entire time interval and the running total.
integral_absolute_error_overTime = np.cumsum(temporal_error) * SAMPLE_TIME
integral_absolute_error_total = np.trapz(temporal_error, dx=SAMPLE_TIME)

# Now, calculate the integral time squared (ITSE) error. We'll calculate the 
# total over the entire time interval and the running total.
integral_time_sqaured_overTime = np.cumsum(time * temporal_error**2) * SAMPLE_TIME
integral_time_sqaured_total = np.trapz(time * temporal_error**2, dx=SAMPLE_TIME)

# Now, calculate the integral time absolute (ITAE) error. We'll calculate the 
# total over the entire time interval and the running total.
integral_time_absolute_overTime = np.cumsum(time * temporal_error) * SAMPLE_TIME
integral_time_absolute_total = np.trapz(time * temporal_error, dx=SAMPLE_TIME)

# We can also calculate root-mean-square (RMS) error over the full trajectory
rms = np.sqrt(np.mean(temporal_error**2))