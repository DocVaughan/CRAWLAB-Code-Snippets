#! /usr/bin/env python 

##########################################################################################
# mass_spring_damper_odeint.py
#
# Script to a simulate a spring-mass-damper system with an ode solver
#
# NOTE: Plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should ` look
#       better.
# 
# Created: 11/27/13 
#   - Joshua Vaughan 
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 12/4/13 - Joshua Vaughan - joshua.vaughan@louisiana.edu
#       - Better commenting
#       - Renaming functions to make their purpose more obvious
#   * 01/30/17 - Joshua Vaughan - joshua.vaughan@louisiana.edu
#       - added debugger examples, currently commented out
#
##########################################################################################

# Simple mass-spring-damper system
#
#    +---> Xd       +---> X
#    |              |
#    |     k     +-----+
#    +---/\/\/---|     |
#    |           |  M  |
#    +-----]-----|     |
#          c     +-----+


import numpy as np
import matplotlib.pyplot as plt 
from scipy.integrate import odeint

# from IPython.core.debugger import Tracer
# debug_here = Tracer()
# or
# import ipbd  # may need to install
# or
# import pdb


def eq_of_motion(w, t, p):
    """
    Defines the differential equations for the coupled spring-mass system.

    Arguments:
        w :  vector of the state variables:
        t :  time
        p :  vector of the parameters:
    """
    x, x_dot = w
    m, k, c, L, StartTime = p
    
#     ipdb.set_trace()
#
#   or
#   
#    debug_here() # import of Tracer needed
#    
#   or 
#
#     pdb.set_trace()
    
    # Create sysODE = (x',y_dot')
    #  We ignore the xd_dot term, as it is only an impulse as the start of the step
    sysODE = [x_dot,
              c/m * (-x_dot) + k/m * (xd(t,L,StartTime) - x)]
    return sysODE


def xd(t, L, StartTime):
    """
    defines the input to the system
    """
    
    # Pick your input as one of the xd definitions below
    
    # For an unshaped input
    xd = L * (t >= StartTime)
    
    # For a ZV shaped input, designed for 1HZ and no damping 
    # xd = 0.5 * L * (t >= StartTime) + 0.5 * L * (t >= StartTime+0.5)
    
    return xd
    



#---- Main script -----------------------------------------------------------------------

# System Parameters
m = 1.0                 # mass
k = (2*np.pi)**2        # Spring constants
c = 0.0                 # damping coefficient
wn = np.sqrt(k / m)     # natural frequency

# Initial conditions
x_init = 0.0
x_dot_init = 0.0

# Input Parameters
L = 1.0                 # Step size
StartTime = 0.5         # Time of step input


# ODE solver parameters
abserr = 1.0e-8
relerr = 1.0e-6
stoptime = 5.0
numpoints = 501

# Create the time samples for the output of the ODE solver.
t = np.linspace(0, stoptime, numpoints)

# Pack up the parameters and initial conditions:
p = [m, k, c, L, StartTime]
x0 = [x_init, x_dot_init]

# Call the ODE solver.
resp = odeint(eq_of_motion, x0, t, args=(p,), atol = abserr, rtol = relerr)
              

# Plot the response
#   Many of these setting could also be made default by the .matplotlibrc file
fig = plt.figure(figsize=(6,4))
ax = plt.gca()
plt.subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)
plt.setp(ax.get_ymajorticklabels(),fontsize=18)
plt.setp(ax.get_xmajorticklabels(),fontsize=18)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.grid(True,linestyle=':',color='0.75')
ax.set_axisbelow(True)

plt.xlabel('Time (s)',fontsize=22,labelpad=8)
plt.ylabel('Position (m)',fontsize=22,labelpad=10)

plt.plot(t,xd(t, L, StartTime),'--',linewidth=2,label=r'$x_d$')
plt.plot(t,resp[:,0],linewidth=2,label=r'$x$')

plt.ylim(0,2.5)

leg = plt.legend(loc='upper right', ncol = 2, fancybox=True)
ltext  = leg.get_texts() 
plt.setp(ltext,fontsize=16)

# save the figure as a high-res pdf in the current folder
plt.savefig('mass_spring_damper.pdf',dpi=300)

plt.show()