#! /usr/bin/env python 

##########################################################################################
# mass_PD_ForceLimited.py
#
# Script to a simulate a force-limited PD position control of a mass system with an ode solver
#
# NOTE: Plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
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
#
##########################################################################################

# PD control of a mass system
#
#    +---> Xd       +---> X
#    |              |
#    |     kp    +-----+
#    +---/\/\/---|     |
#    |           |  M  |
#    +-----]-----|     |
#          kd    +-----+


import numpy as np
from matplotlib.pyplot import * # Grab plotting functions
from scipy.integrate import odeint


def eq_of_motion(states, t, p):
    """
    Defines the differential equations for the coupled spring-mass system.

    Arguments:
        w :  vector of the state variables:
        t :  time
        p :  vector of the parameters:
    """
    x, x_dot = states
    m, kp, kd, L, StartTime, Umax = p

    # Create f = (x1',y1',x2',y2'):
    sysODE = [x_dot,
         U(t,states,p)]
    return sysODE
    
    
def U(t,states,p):
    """ 
        Defines the force input to the system. Is limited by Umax
    """
    x, x_dot = states
    m, kp, c, L, StartTime, Umax = p
    
    # We're using the non-derivative kick version of the PD controller
    U = kd/m*(-x_dot) + kp/m*(xd(t,L,StartTime)-x)
    
    # Limit the force to within symmetric limits defined by Umax
    #   There are more clever/faster ways to do this, but this is most easiest 
    #   to understand.
    if U > Umax:
        U = Umax
    elif U < -Umax:
        U = -Umax
        
    return U
        

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
m = 1.0             # mass
kp = (2*np.pi)**2       # Spring constants
kd = 0.0             # damping coefficient

# Initial conditions
# x1 and x2 are the initial displacements; y1 and y2 are the initial velocities
x_init = 0.0
x_dot_init = 0.0

# Input Parameters
L = 1.0             # Step size
StartTime = 0.5     # Time of step input
Umax = 5.


# ODE solver parameters
abserr = 1.0e-8
relerr = 1.0e-6
stoptime = 10.0
numpoints = 1001

# Create the time samples for the output of the ODE solver.
t = np.linspace(0,stoptime,numpoints)

# Pack up the parameters and initial conditions:
p = [m, kp, kd, L, StartTime, Umax]
x0 = [x_init, x_dot_init]


# Call the ODE solver.
resp = odeint(eq_of_motion, x0, t, args=(p,), atol=abserr, rtol=relerr)




#-----  Plot the response
#   Many of these setting could also be made default by the .matplotlibrc file
fig = figure(figsize=(6,4))
ax = gca()
subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)
setp(ax.get_ymajorticklabels(),fontsize=18)
setp(ax.get_xmajorticklabels(),fontsize=18)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.grid(True,linestyle=':',color='0.75')
ax.set_axisbelow(True)

xlabel('Time (s)',fontsize=22,labelpad=8)
ylabel('Position (m)',fontsize=22,labelpad=10)

plot(t,xd(t, L, StartTime),'--',linewidth=2,label=r'$x_d$')
plot(t,resp[:,0],linewidth=2,label=r'$x$')

ylim(0,2.5)

leg = legend(loc='upper right', ncol = 2, fancybox=True)
ltext  = leg.get_texts() 
setp(ltext,fontsize=16)

# save the figure as a high-res pdf in the current folder
savefig('mass_spring_damper_RespNonlinForce.pdf',dpi=300)


#----- Now, let's plot the force
# first fill the arrays with zeros
force = np.zeros(len(t))
des_force = np.zeros(len(t))

# Now, loop over the time vector and fill the desired and actual forces
for ii in range(len(t)):
    force[ii] = U(t[ii],resp[ii,:],p)
    des_force[ii] = kd/m*(-resp[ii,1]) + kp/m*(xd(t[ii],L,StartTime)-resp[ii,0])


#   Many of these setting could also be made default by the .matplotlibrc file
fig = figure(figsize=(6,4))
ax = gca()
subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)
setp(ax.get_ymajorticklabels(),fontsize=18)
setp(ax.get_xmajorticklabels(),fontsize=18)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.grid(True,linestyle=':',color='0.75')
ax.set_axisbelow(True)

xlabel('Time (s)',fontsize=22,labelpad=8)
ylabel('Position (m)',fontsize=22,labelpad=10)

plot(t,xd(t, L, StartTime),'--',linewidth=2,label=r'$x_d$')
plot(t,des_force,':',linewidth=2,label=r'$U_d$')
plot(t,force,linewidth=2,label=r'$U$')

ylim(-40,60)

leg = legend(loc='upper right', ncol = 3, fancybox=True)
ltext  = leg.get_texts() 
setp(ltext,fontsize=16)

# save the figure as a high-res pdf in the current folder
savefig('mass_spring_damper_Nonlinforce.pdf',dpi=300)

show()