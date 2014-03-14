#! /usr/bin/env python 

##########################################################################################
# mass_spring_damper_ForceDist_odeint.py
#
# Script to a simulate a spring-mass-damper system with a force disturbance 
#   using an ode solver
#
# NOTE: Plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
# 
# Created: 3/14/14 
#   - Joshua Vaughan 
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
##########################################################################################

# Simple mass-spring-damper system
#
#    +---> Xd       +---> X
#    |              |
#    |     k     +-----+
#    +---/\/\/---|     |
#    |           |  M  |<--- Fd
#    +-----]-----|     |
#          c     +-----+


import numpy as np
from matplotlib.pyplot import * 
from scipy.integrate import odeint


def eq_of_motion(w, t, p):
    """
    Defines the differential equations for the coupled spring-mass system.

    Arguments:
        w :  vector of the state variables:
        t :  time
        p :  vector of the parameters:
    """
    x, x_dot, y, y_dot = w
    m, k, c, Distance, StartTime, Amax, Vmax, DistStart, F_amp = p

    # Create sysODE = (x', x_dot', y', y_dot')
    sysODE = [x_dot,
             k/m * (y - x) + c/m * (y_dot - x_dot) - f(t, p)/m,
             y_dot,
             y_ddot(t, p)]
    return sysODE


def f(t, p):
    """
    defines the disturbance force input to the system
    """
    m, k, c, Distance, StartTime, Amax, Vmax, DistStart, F_amp = p
    
    # Select one of the two inputs below
    # Be sure to comment out the one you're not using
    
    # Input Option 1: 
    #    Just a step in force beginning at t=DistStart
    # f = F_amp * (t >= DistStart)
    
    # Input Option 2:
    #    A pulse in force beginning at t=DistStart and ending at t=(DistStart+0.1)
    f = F_amp * (t >= DistStart) * (t <= DistStart + 0.1)
    
    return f


def y_ddot(t, p):
    """
    Defines the accel input to the system.
    
    Depending on the desired move distance, max accel, and max velocity, the input is either
    bang-bang or bang-coast-bang
    """
    m, k, c, Distance, StartTime, Amax, Vmax, DistStart, F_amp = p
    
    # These are the times for a bang-coast-bang input 
    t1 = StartTime
    t2 = (Vmax/Amax) + t1
    t3 = (Distance/Vmax) + t1
    t4 = (t2 + t3) - t1
    
    if t3 <= t2: # command should be bang-bang, not bang-coast-bang
        t2 = np.sqrt(Distance/Amax)+t1
        t3 = 2*np.sqrt(Distance/Amax)+t1
        
        accel = Amax*(t > t1) - 2*Amax*(t > t2) + Amax*(t > t3)
    
    else: # command is bang-coast-bang
        accel = Amax*(t > t1) - Amax*(t > t2) - Amax*(t > t3) + Amax*(t > t4)

    return accel
    



#---- Main script -----------------------------------------------------------------------

# Define the parameters for simluation
m = 1.0                      # mass (kg)
k = (1.0*2*np.pi)**2             # spring constant (N/m)

wn = np.sqrt(k/m)            # natural frequency (rad/s)

# Select damping ratio and use it to choose an appropriate c
zeta = 0.05                   # damping ratio
c = 2*zeta*wn*m              # damping coeff.

# ODE solver parameters
abserr = 1.0e-9
relerr = 1.0e-9
max_step = 0.01
stoptime = 10.0
numpoints = 10001

# Create the time samples for the output of the ODE solver
t = np.linspace(0.,stoptime,numpoints)

# Initial conditions
x_init = 0.0                        # initial position
x_dot_init = 0.0                    # initial velocity
y_init = 0.0
y_dot_init = 0.0

# Set up the parameters for the input function
Distance = 1.0               # Desired move distance (m)
Amax = 20.0                   # acceleration limit (m/s^2)
Vmax = 2.0                   # velocity limit (m/s)
StartTime = 0.5              # Time the y(t) input will begin
DistStart = 4.5              # Time the disturbance input will begin
F_amp = 100.0                 # Amplitude of Disturbance force (N)

# Pack the parameters and initial conditions into arrays 
p = [m, k, c, Distance, StartTime, Amax, Vmax, DistStart, F_amp]
x0 = [x_init, x_dot_init, y_init, y_dot_init]

# Call the ODE solver.
resp = odeint(eq_of_motion, x0, t, args=(p,), atol=abserr, rtol=relerr,  hmax=max_step)
              

#----- Plot the response
# Make the figure pretty, then plot the results
#   "pretty" parameters selected based on pdf output, not screen output
#   Many of these setting could also be made default by the .matplotlibrc file
fig = figure(figsize=(6,4))
ax = gca()
subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)
setp(ax.get_ymajorticklabels(),family='serif',fontsize=18)
setp(ax.get_xmajorticklabels(),family='serif',fontsize=18)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.grid(True,linestyle=':',color='0.75')
ax.set_axisbelow(True)

xlabel('Time (s)',family='serif',fontsize=22,weight='bold',labelpad=5)
ylabel('Position (m)',family='serif',fontsize=22,weight='bold',labelpad=10)
# ylim(-1.,1.)

# plot the response
plot(t,resp[:,0], linewidth=2, linestyle = '-', label=r'$x$')
plot(t,resp[:,2], linewidth=2, linestyle = '--', label=r'$y$')

# If there is a non-zero force disturbance show where it began via an annotation
if F_amp > 0:
    annotate(r'Force Disturbance Begins',
         xy=(DistStart,resp[-1,2]), xycoords='data',
         ha='center',
         xytext=(DistStart, 1.05*np.max(resp[:,0])), textcoords='data', fontsize=16,
         arrowprops=dict(arrowstyle="simple, head_width = 0.35, tail_width=0.05", connectionstyle="arc3", color="black"),color = "black")
    
leg = legend(loc='upper right', fancybox=True)
ltext  = leg.get_texts() 
setp(ltext,family='Serif',fontsize=16)

# Adjust the page layout filling the page using the new tight_layout command
tight_layout(pad=0.5)

# If you want to save the figure, uncomment the commands below. 
# The figure will be saved in the same directory as your IPython notebook.
# Save the figure as a high-res pdf in the current folder
# savefig('MassSpringDamper_Disturbance_Resp.pdf')


#----- Let's look at the forces acting on the mass
Fsp = k * (resp[:,2] - resp[:,0])       # Spring Force (N)
Fd =  c * (resp[:,3] - resp[:,1])       # Damping Force (N)
F_pos = Fsp + Fd                        # Total force from position input

# Calculate the disturbance force over time by calling the disturbance force function
F_dist = np.zeros_like(t)

for ii in range(len(t)):
    F_dist[ii] = -f(t[ii],p)
    
# Now, let's plot the forces    
# Make the figure pretty, then plot the results
#   "pretty" parameters selected based on pdf output, not screen output
#   Many of these setting could also be made default by the .matplotlibrc file
fig = figure(figsize=(6,4))
ax = gca()
subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)
setp(ax.get_ymajorticklabels(),family='serif',fontsize=18)
setp(ax.get_xmajorticklabels(),family='serif',fontsize=18)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.grid(True,linestyle=':',color='0.75')
ax.set_axisbelow(True)

xlabel('Time (s)',family='serif',fontsize=22,weight='bold',labelpad=5)
ylabel('Force (N)',family='serif',fontsize=22,weight='bold',labelpad=10)

# You may need to reset these limits based on the forces in your simulation
ymax = 1.1 * np.max([np.max(np.abs(F_pos)), np.max(np.abs(F_dist))])
ylim(-ymax, ymax)

# plot the response
plot(t,F_pos, linewidth=2, linestyle = '-', label=r'Spring-Damper')
plot(t,F_dist, linewidth=2, linestyle = '--', label=r'Disturbance')

leg = legend(loc='best', fancybox=True)
ltext  = leg.get_texts() 
setp(ltext,family='Serif',fontsize=16)

# Adjust the page layout filling the page using the new tight_layout command
tight_layout(pad=0.5)

# If you want to save the figure, uncomment the commands below. 
# The figure will be saved in the same directory as your IPython notebook.
# Save the figure as a high-res pdf in the current folder
# savefig('MassSpringDamper_Disturbance_Forces.pdf')


# Show the figures
show()