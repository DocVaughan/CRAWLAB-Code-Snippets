#! /usr/bin/env python 

##########################################################################################
# mass_spring_InitCond.py
#
# Script to analyze a mass-spring system
# Uses state-space form of the equations of motion and the control systems module:
#   https://www.cds.caltech.edu/~murray/wiki/Control_Systems_Library_for_Python
# 
# Created: 2/2/13 
#   - Joshua Vaughan 
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 2/4/13 - commenting and cleanup - JEV - joshua.vaughan@louisiana.edu
#   * 2/13/13 - Added damped initial condition response - JEV
#   * 1/27/14 - Updated numpy import to name np - JEV
#
##########################################################################################

# A simple mass-spring system
#                  +---> X
#                  |
#   /|          +-----+
#   /|     k    |     |
#   /|---/\/\---|  M  |
#   /|          |     |
#   /|          +-----+

import numpy as np              # Grab all of the NumPy functions
from matplotlib.pyplot import * # Grab MATLAB plotting functionsm
import control                  # import the control system functions


# Define system parameters
k = (2*np.pi)**2       # Spring constant (N/m) - selected to give 1 Hz natural freq.
m = 1               # Mass (kg) 

wn = np.sqrt(k/m)      # natural frequency (rad/s)

# Define the system to use in simulation - in state space form here
A = [[0,1], [-k/m, 0]]

B = [[0],[1]]

C = [[1,0],[0,1]]

D = [[0],[0]]

sys = control.ss(A,B,C,D)


# Set up simulation parameters
t = np.linspace(0,5,500)            # time for simulation, 0-5s with 500 points in between
x0 = [[1],[0]]                      # initial condition, x=1, x_dot=0

# run the simulation - utilize the built-in initial condition response function
[T,yout] = control.initial_response(sys,t,x0)

# Make the figure pretty, then plot the results
fig = figure(figsize=(6,4))
ylim(-1.5,1.5)
ax = gca()
subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.98)
setp(ax.get_ymajorticklabels(),family='CMU Serif',fontsize=18)
setp(ax.get_xmajorticklabels(),family='CMU Serif',fontsize=18)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

xlabel('Time (s)',family='CMU Serif',fontsize=22,weight='bold')
ylabel('Position (m)',family='CMU Serif',fontsize=22,weight='bold')
plot(T,yout,color="blue",linewidth=2)

# save the figure as a high-res pdf in the current folder
savefig('Initial_Cond_Resp_Undamped.pdf')



# A simple mass-spring-damper system
#                  +---> X
#                  |
#   /|    k     +-----+
#   /|---/\/\---|     |
#   /|          |  M  |
#   /|----]-----|     |
#   /|    c     +-----+

# Set the damping ratio and use it do define c
z = 0.05
c = 2*z*wn*m

# Define the system to use in simulation - in state space form here
A = [[0,1], [-k/m, -c/m]]

B = [[0],[1]]

C = [[1,0],[0,1]]

D = [[0],[0]]

sys_damp = control.ss(A,B,C,D)


# Set up simulation parameters
t = np.linspace(0,5,500)            # time for simulation, 0-5s with 500 points in between
x0 = [[1],[0]]                      # initial condition, x=1, x_dot=0

# run the simulation - utilize the built-in initial condition response function
[T,yout_damp] = control.initial_response(sys_damp,t,x0)

# Make the figure pretty, then plot the results
fig = figure(figsize=(6,4))
ylim(-1.5,1.5)
ax = gca()
subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.98)
setp(ax.get_ymajorticklabels(),family='CMU Serif',fontsize=18)
setp(ax.get_xmajorticklabels(),family='CMU Serif',fontsize=18)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

xlabel('Time (s)',family='CMU Serif',fontsize=22,weight='bold')
ylabel('Position (m)',family='CMU Serif',fontsize=22,weight='bold')
plot(T,yout_damp,color="blue",linewidth=2)

# save the figure as a high-res pdf in the current folder
savefig('Initial_Cond_Resp_Damped.pdf')

# show the figures
show()
