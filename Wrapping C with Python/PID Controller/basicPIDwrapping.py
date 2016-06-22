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
from scipy.integrate import ode

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
# 
#
# PID set_up_PID(double Kp, double Ki, double Kd, 
#                double outMax, double outMin, double sampleTime);
# double compute_PID(double measurement, double desired, PID *pid);
# void change_PID_limits(double min, double max, PID *pid);

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
pid.set_up_PID.restype = PID

pid.compute_PID.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.POINTER(PID)]
pid.compute_PID.restype = ctypes.c_double

pid.change_PID_limits.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.POINTER(PID)]
pid.change_PID_limits.restypes = None


# Define some parameters for our PID controller
kp = 6.28
kd = 0.0
ki = 0.0
outMax = 100
outMin = -100
sampleTime = 0.01

# Define the PID controller
controller = pid.set_up_PID(kp, ki, kd, outMax, outMin, sampleTime)

# We can change the max and min of the output
# pid.change_PID_limits(-50, 50, controller)


# Now, let's do a simple digital simulation of a mass 

def eq_of_motion(t, w, p):
    """ A simple mass with a force input 
    
    Arguments:
      w : the states, [x, x_dot]
      t : the current timestep
      p : the parameters
        p = [m, curr_force]
    
    Returns:
      sysODE : 1st order differential equations
    """
    
    m, curr_force = p
    
    sysODE = [w[1],
              1.0 / m * curr_force]
    
    return sysODE
    

# System parameters 
m = 1.0                     # mass (kg)
Distance = 1.0              # Desired move distance (m)

# ODE solver parameters
stoptime = 5.0
numpoints = stoptime / sampleTime + 1

# Create the time samples for the output of the ODE solver
t = np.linspace(0.0, stoptime, numpoints)

# Define the input - a step input at t = StartTime
StartTime = 0.5
x_d = np.ones_like(t) * Distance * (t > StartTime)
# x_d[0:np.round(StartTime/sampleTime)] = 0

# Initial conditions
x_init = 0.0                # initial position
x_dot_init = 0.0            # initial velocity

# Pack the initial conditions
x0 = [x_init, x_dot_init]

# Set up the ODE solver

# Set up the initial point for the ode solver
curr_force = 0
r = ode(eq_of_motion).set_initial_value(x0, t[0]).set_f_params((m, curr_force))
 
# define the sample time
dt = sampleTime   

# pre-populate the response and force arrays with zeros
response = np.zeros((len(t), len(x0)))
force = np.zeros(len(t))

# Set the initial index to 0
index = 0

# Now, numerically integrate the ODE while:
#   1. the last step was successful
#   2. the current time is less than the desired simluation end time
# We're using this method, so that we can enforce the PID output being 
# calculated only once per time step, attempting to replicate how it would
# perform on an embedded, real-time system.
#
# Also note: In this method the integration can fail before the final time
while r.successful() and r.t < t[-1]:
    response[index, :] = r.y
    
    # compute the force output of this timestep
    curr_force = pid.compute_PID(response[index, 0], 
                                 x_d[index], 
                                 ctypes.byref(controller))
    
    force[index] = curr_force # save the current force for plotting
    
    # update the force applied to the system by curr_force
    r.set_f_params((m, curr_force))
    
    # do the integration
    r.integrate(r.t + dt)
    index += 1


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
plt.ylabel('Position (m)', fontsize=22, weight='bold', labelpad=10)
 
plt.plot(t, response[:,0], linewidth=2, linestyle='-', label=r'$x$')

# uncomment below and set limits if needed
# plt.xlim(0,5)
# plt.ylim(0,10)

# Create the legend, then fix the fontsize
# leg = plt.legend(loc='upper right', ncol = 1, fancybox=True)
# ltext  = leg.get_texts()
# plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
# plt.savefig('Wrapped_C_PID_control_response.pdf')


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
plt.ylabel('Force (N)', fontsize=22, weight='bold', labelpad=10)
 
plt.plot(t, force, linewidth=2, linestyle='-', label=r'Force')

# uncomment below and set limits if needed
# plt.xlim(0,5)
# plt.ylim(0,10)

# Create the legend, then fix the fontsize
# leg = plt.legend(loc='upper right', ncol = 1, fancybox=True)
# ltext  = leg.get_texts()
# plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
# plt.savefig('Wrapped_C_PID_control_force.pdf')

# show the figure
plt.show()