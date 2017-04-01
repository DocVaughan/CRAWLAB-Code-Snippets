#! /usr/bin/env python

###############################################################################
# skidSteering_calculations.py
#
# quick script to check some skid-steering calculations
#
#         ^ Y
#         |
#         |
#     <--- omega (rotation)
#         v
# v_l     ^       v_r
# ^       |       ^
# |  +---------+  |
# +--|         |--+
# |  |  body   |  |  -----> X
# +--|         |--+
#    +---------+
#
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


   
v_r = 0             # right side velocity
v_l = 0             # left side velocity

track_width = 0.55  # Husky Track width

v = 0               # forward velocity
omega = 0           # rotational velocity 

omega = np.linspace(-100, 100, 201)

def brute_force_check(R, omega):
    v1 = 100 + 0.5 * R * omega  # v_l_max inequality
    v2 = 100 - 0.5 * R * omega  # v_r_max inequality
    
    v_fromMaxes = np.minimum(v1, v2)
    
    v3 = -100 + 0.5 * R * omega # v_l_min inequality
    v4 = -100 - 0.5 * R * omega # v_r_min inequality
    
    v_fromMins = np.maximum(v3, v4)
    
    return v_fromMaxes, v_fromMins
    
vel1, vel2 = brute_force_check(track_width, omega)
    

