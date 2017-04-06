#! /usr/bin/env python

###############################################################################
# steering_snippet.py
#
# A snippet with functions to convert vel, omega commands to skid steer 
# commands and vice-versa. In both cases, limits can be imposed on the 
# resulting output. Default limits are set at +/-100 to map to sending 
# commands as a percentage of maximum velocity.
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 04/01/17
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
import matplotlib.pyplot as plt



def bodyFixed_to_trackSpeeds(velocity, angular_velocity, track_width,
                             right_track_max=100, right_track_min=-100,
                             left_track_max=100, left_track_min=-100):
    """ 
    Function maps speeds issued in the body-fixed system frame to the
    necessary skid-steering track velocities.
    
    Arguments:
      velocity - forward velocity (m/s)
      angular_velocity - rotational velocity (rad/s)
      track_width - track width of the vehicle (distance between the two tracks) (m)
      right_track_max - maximum speed of right track, default = 100
      right_track_min - maximum speed of right track, default = -100
      left_track_max - maximum speed of right track, default = 100
      left_track_min - maximum speed of right track, default = -100
    
    Returns:
        right_track_speed (m/s), left_track_speed (m/s)
    """
    
    right_track_speed = (track_width * angular_velocity + 2 * velocity) / 2
    left_track_speed = (-track_width * angular_velocity + 2 * velocity) / 2

    # limit tracks to within their speeds. To maintain turning command, we can't
    # just scale proportionally. So, we subtract off the same velocity from all
    if right_track_speed > right_track_max:
        left_track_speed = left_track_speed + (right_track_max - right_track_speed)
        right_track_speed = right_track_max
    elif right_track_speed < right_track_min:
        left_track_speed = left_track_speed + (right_track_min - right_track_speed)
        right_track_speed = right_track_min
    
    if left_track_speed > left_track_max:
        right_track_speed = right_track_speed + (left_track_max - left_track_speed)
        left_track_speed = left_track_max
    elif left_track_speed < left_track_min:
        right_track_speed = right_track_speed + (left_track_min - left_track_speed)
        left_track_speed = left_track_min
    
    return right_track_speed, left_track_speed

def trackSpeeds_to_bodyFixed(right_track_speed, left_track_speed, track_width):
    """ 
    Function maps speeds for individual skid-steering tracks to the body-fixed
    velocity and angular velocity
    
    Arguments:
      right_track_speed - speed of the right track
      left_track_speed - speed of left track
      track_width - track width of the vehicle (distance between the two tracks)
      right_track_max - maximum speed of right track, default = 100
      right_track_min - maximum speed of right track, default = -100
      left_track_max - maximum speed of right track, default = 100
      left_track_min - maximum speed of right track, default = -100
    
    Returns:
        velocity (m)
        angular_velocity (rad/)
    """

    velocity = (right_track_speed + left_track_speed) / 2
    angular_velocity = (right_track_speed - left_track_speed) / track_width
    
    return velocity, angular_velocity
    
# def trackSpeeds_to_bodyFixed_percentage(right_track_speed, left_track_speed, track_width
#                              right_track_max = 100, right_track_min=-100,
#                              left_track_max = 100, left_track_min = -100):