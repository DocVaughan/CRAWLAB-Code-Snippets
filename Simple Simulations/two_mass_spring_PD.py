#! /usr/bin/env python

##########################################################################################
# two_mass_spring_PID.py
#
# Simulation of a simple two-mass-spring system 
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 01/17/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

import numpy as np
import matplotlib.pyplot as plt
import control

m1 = 1.0
m2 = 1.0
kp = 10.0
kd =0.5
k = 1.0
c = 0.5


A = np.array([[0, 1, 0, 0],
              [-(kp + k)/m1, -(kd + c)/m1, k/m1, c/m1],
              [0, 0, 0, 1],
              [k/m2, c/m2, -k/m2, -c/m2]])
B = np.array([[0, 0],
             [kp/m1, kd/m1],
             [0, 0],
             [0, 0]])

C = np.array([[1,0,0,0],[0,0,1,0]])

D = np.array([[0, 0],[0, 0]])

sys = control.ss(A,B,C,D)

print '\nSystem 1'
print control.pole(sys)


# include input
A2 = np.array([[0, 1, 0, 0, 0, 0],
              [-(kp + k)/m1, -(kd + c)/m1, k/m1, c/m1, kp/m1, kd/m1],
              [0, 0, 0, 1, 0, 0],
              [k/m2, c/m2, -k/m2, -c/m2, 0, 0],
              [0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0]])
B2 = np.array([[0],
             [0],
             [0],
             [0],
             [0],
             [1]])

C2 = np.array([[1,0,0,0,0,0],[0,0,1,0,0,0],[0,0,0,0,1,0]])

D2 = np.array([[0], [0], [0]])

sys2 = control.ss(A2,B2,C2,D2)

print '\nSystem 2'
print control.pole(sys2)

