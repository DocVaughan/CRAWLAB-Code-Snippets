#! /usr/bin/env python 

################################################################################
# tracking_error.py
#
# Script to a demonstrate calculating the various measures of error between two 
# curves. Foreach element in one (response) array we calculate various error
# metrics from another array (representing the desired trajctory). Some of these
# could also be used to calculate the difference between curves, even if that
# difference doesn't truly represent an error.
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
#   * 10/10/19 - JEV - Added spatial error calculations
#
# TODO:
#   * 10/01/19 - JEV - Implement a sliding window version for spatial error 
#
################################################################################

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# Define an array representing the time 
DURATION = 5        # seconds of data to use
SAMPLE_TIME = 0.1   # Sampling time
time = np.linspace(0, DURATION, int(DURATION/SAMPLE_TIME) + 1)

# Define the desired trajetory in 2D. This should be a circle of radius 1
x_desired = 2 * time #np.sin(2 * np.pi * time)
y_desired = np.cos(0.2 * np.pi * time)

# Define arrays such that each row represents an (x,y) position at time N*dt
# where N is the array index and dt was the sample time used. Here, we'll use
# the desired trajectory with a phase shift and a higher frequency sinusoided 
# added to it
x_actual = 2 * time + 0.25 * np.sin(1 *  2 * np.pi * time) # np.sin(2 * np.pi * time + np.pi / 4) +
y_actual = np.cos(0.2 * np.pi * time) + 0.1 * np.sin(1 * 2 * np.pi * time)

# Now, we can calculate various error metrics between two two trajectories

# ----- Temporal Tracking Error -----
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
# using the temporal error measurement
rms = np.sqrt(np.mean(temporal_error**2))


# ----- Spatial Tracking Error -----
# Calculating the spatial tracking error is more complex. We need to find the 
# closest point on the desired trajectory for each point on the actual 
# trajectory. This means that we are basically taking a point (a single sample 
# of the actual trajecotry) and finding the closest point on the line 
# that defines the desired trajecory. A naive way to do this is to cacluate the 
# distance from the actual trajectory point to every point in the desired 
# trajectory. 

# Let's first implement the naive version. It can be a decent approximation if 
# the spacing between the points is fine enough and the trajectories are "simple"
# NOTE: This for loop implementation will not scale up well
spatial_naive = np.zeros_like(x_actual)
error_index_naive = np.zeros_like(x_actual)

for index, _ in enumerate(x_actual):
    spatial_naive[index] = np.min(np.sqrt((x_desired - x_actual[index])**2 +
                                          (y_desired - y_actual[index])**2))
    
    # We'll also save the index of the point in desired trajetory that was the
    # minimum error
    error_index_naive[index] = np.argmin(np.sqrt((x_desired - x_actual[index])**2 +
                                                 (y_desired - y_actual[index])**2))


# A slightly more sophistaiced way is to generate a higher density array  
# approximating desired trajectory using interpolation. This may even be 
# necessary depending on the spacing of the arrays. Note, if we have a 
# functionally-defined desired trajectory, we could use it to define this finer
# mesh directly. Here, I'm using interpolation to show what we'd need to do if
# we only had course data for both the desired and actual. 

# We'll first define a finer mesh for the time array to caclulate points at
INTERP_SCALE = 100           # Factor by which ot increase the number of points
INTERP_SAMPLE_TIME = SAMPLE_TIME / INTERP_SCALE
time_interp = np.linspace(0, DURATION, int(DURATION/INTERP_SAMPLE_TIME) + 1)

# We can choose to do simple linear interpolation between the points
# x_desired_interp = np.interp(time_interp, time, x_desired)
# y_desired_interp = np.interp(time_interp, time, y_desired)

# Or more complex, using the scipy interp1d and cubic interpolation
# We first generate the functions 
x_desired_func = interpolate.interp1d(time, 
                                      x_desired, 
                                      kind='cubic',
                                      fill_value='extrapolate')

y_desired_func = interpolate.interp1d(time, 
                                      y_desired, 
                                      kind='cubic',
                                      fill_value='extrapolate')

# Then, calculate the values at the higher resolution array of the desired 
# trajectory
x_desired_interp = x_desired_func(time_interp)
y_desired_interp = y_desired_func(time_interp)

# Let's first implement the version using the interpolated desired trajectory. 
# We'll use the same algorithm as the naive version. 
# NOTE: As with the naive version, this for loop implementation will not scale up well
spatial_interp = np.zeros_like(x_actual)
error_index_interp = np.zeros_like(x_actual)

for index, _ in enumerate(x_actual):
    spatial_interp[index] = np.min(np.sqrt((x_desired_interp - x_actual[index])**2 +
                                          (y_desired_interp - y_actual[index])**2))
    
    # We'll also save the index of the point in desired trajetory that was the
    # minimum error
    error_index_interp[index] = np.argmin(np.sqrt((x_desired_interp - x_actual[index])**2 +
                                                 (y_desired_interp - y_actual[index])**2))



# A more sophisticated (and perhaps necessary, depending on the spacing of the
# data) way is to generate line segments representing lines connecting each
# successive pairs on points on the desired trajectory. Then, we'll look for the
# closest point on each of those lines to the current point in the actual 
# trajectory. We'll have to be careful, because the lines we define will extend
# beyond the two poitns on the desired trajectory used to define them.
# TODO: 10/01/19 - JEV - Implement this fix
#
# The wikipedia entry on this actually does a 
# pretty good job of summarizing the various ways to do this:
#
#   https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
#
# We will implement this version:
#
#   https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points
#
# using every pair of two points on the desired trajectory and calculating the 
# distance to every one of those segments from the current point on the actual
# trajectory. We'll select the minimum value.
#
# In general, we would want to be be more careful than I am here about "where" 
# we connect to the desired path. For example, we are not taking any precautions
# against connecting to some point that the actual trajectory should have already
# passed.
#
# For example, you'll notice that the error reported by this method is much 
# lower than that calculated by the methods above. We're matching *any* point 
# on the lines defined by the pairs of points of the desired trajectory, which
# extend beyond the poitns themselves.
#
# TODO: 10/01/19 - JEV - Add an example using a sliding window on the desired 
# trajectory to demonstrate one way to address this issue.

# We'll have 1 less point than array length because we need two points to define
# each line segment
spatial_error = np.zeros(len(x_actual)-1)
spatial_error_index = np.zeros(len(x_actual)-1)
error_array = np.zeros_like(spatial_error)

# NOTE: This for loop implementation will not scale up well
for act_index, _ in enumerate(spatial_error):
    # Zero the error array for the current acutal trajetory part
    error_array = np.zeros_like(spatial_error)

    for index, _ in enumerate(spatial_error):
        x_diff = x_desired[index + 1] - x_desired[index]
        y_diff = y_desired[index + 1] - y_desired[index]
        den = np.sqrt(x_diff**2 + y_diff**2)
        
        num = np.abs(y_diff * x_actual[act_index] - 
                     x_diff * y_actual[act_index] +
                     x_desired[index + 1] * y_desired[index] -
                     y_desired[index + 1] * x_desired[index])
        
        error_array[index] = num / den

    spatial_error[act_index] = np.min(error_array)
    spatial_error_index[act_index] = np.argmin(error_array)

