#! /usr/bin/env python

###############################################################################
# basicPID_wrapping.py
#
# Python code to wrap a very simple PID controller shared library
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 06/20/16
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

# Import the ctypes module. Importing all for now.
import ctypes

# From PID.h
# typedef struct {
#     double Kp;                  // Proportional Gain
#     double Kd;                  // Derivative Gain
#     double Ki;                  // Derivative Gain
#     double lastMeasurement;     // Measurement input remembered from last loop
#     double integralTerm;       // Running total for integral term
#     double outMax;              // Maximum value of output
#     double outMin;              // Minimum value of output
#     int controlON;              // 1 if controller is active, allows us to still keep track of controller even if not acting
#     double sampleTime;          // the sample time being used in the interrupt
# } PID;

class PID(ctypes.Structure):
         _fields_ = [('Kp', ctypes.c_double),
                     ('Kd', ctypes.c_double),
                     ('Ki', ctypes.c_double),
                     ('lastMeasurement', ctypes.c_double),
                     ('integralTerm', ctypes.c_double),
                     ('outMax', ctypes.c_double),
                     ('outMin', ctypes.c_double),
                     ('controlON', ctypes.c_int),
                     ('sampleTime', ctypes.c_double)]



# Load the libhello_world c code, built as a shared-library
# Give it a name to make it callable
# Currently, requires the file to be in the path/folder this script is run from
pid = ctypes.CDLL('libPID.dylib')

# define the argument and return types (not always necessary, it seems)
pid.set_up_PID.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, 
                           ctypes.c_double, ctypes.c_double, ctypes.c_double]
pid.set_up_PID.restypes = [ctypes.POINTER(ctypes.c_int)]

pid.compute_PID.argtypes = [ctypes.c_double, ctypes.c_double, PID]
pid.compute_PID.restypes = [ctypes.c_double]

pid.change_PID_limits.argtypes = [ctypes.c_double, ctypes.c_double, PID]
# pid.change_PID_limits.restypes = ctypes.v

test = PID(1,1,1,10,0,100,-100,1,0.01)

# pid.change_PID_limits(-50, 75, ctypes.byref(test))