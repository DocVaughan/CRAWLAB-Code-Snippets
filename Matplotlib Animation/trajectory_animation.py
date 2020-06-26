#! /usr/bin/env python 

##########################################################################################
# trajectory_animation.py
#
# Script to a demonstrate a simple animation of a trajectory showing a vector
# force field 
#
# NOTE: Plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
# 
# Created: 12/6/13 
#   - Joshua Vaughan 
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 06/26/20 - JEV 
#       - updated for new animation API
#       - styling updated to match CRAWLAB norms
#
##########################################################################################


import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def eq_of_motion(states, t, p):
    """
    Defines the differential equations for the coupled spring-mass system.

    Arguments:
        states :  vector of the state variables:
        t :  time
        p :  vector of the parameters:
    """
    x, x_dot, y, y_dot = states
    m, kp, kd, L, StartTime, Fmax, FcurAmp, FcurAngle = p

    # Create system diff eq
    sysODE = [x_dot,
              1/m * (np.dot(F(t, states, p),  [1, 0]) + np.dot(Fcur(t, p), [1, 0])),
              y_dot,
              1/m * (np.dot(F(t, states, p), [0, 1]) + np.dot(Fcur(t, p), [0, 1]))]
    
    return sysODE
    
    
def F(t, states, p):
    """ 
    Defines the force/control input to the system. Is limited by Fmax
    
    Note: This is not tuned for best performance. It's effectively placeholder.
    """
    x, x_dot, y, y_dot = states
    m, kp, kd, L, StartTime, Fmax, FcurAmp, FcurAngle = p

    Lx, Ly = L
    endpoint = des_pos(t,L,StartTime)
    xd = endpoint[0]
    yd = endpoint[1]
    
    # We're using the non-derivative kick version of the PD controller
    Fx = kp * (xd - x) + kd * (-x_dot)
    Fy = kp * (yd - y) + kd * (-y_dot)
    
    # Limit the force to within symmetric limits defined by Umax
    #   There are more clever/faster ways to do this, but this is most easiest 
    #   to understand.
    F_amp = np.sqrt(Fx**2 + Fy**2)
    F_ang = np.arctan2(Fy, Fx)
    
    if F_amp > Fmax:
        F_amp = Fmax
    
    Fx = F_amp * np.cos(F_ang)
    Fy = F_amp * np.sin(F_ang)
    
    F = np.array([Fx, Fy])
    
    return F
        

def Fcur(t,p):
    """
    Defines the current disturbance input to the system
    """
    
    # Unpack variables
    m, kp, kd, L, StartTime, Fmax, FcurAmp, FcurAngle = p
    
    Current_Amplitude = FcurAmp
    cur_angle = FcurAngle
    
    Fcur = Current_Amplitude * np.asarray([np.cos(cur_angle), np.sin(cur_angle)])
    
    return Fcur
    

def des_pos(t, L, StartTime):
    """
    defines the desired trajectory
    """
    
    Lx, Ly = L   # unpack the two desired end coords
    
    xd = 5 * np.cos(0.1 * 2 * np.pi * t)
    yd = 5 * np.sin(0.1 * 2 * np.pi * t)
    
    des_pos = np.array([xd, yd])
    
    return des_pos


#---- Main script -----------------------------------------------------------------------

# System Parameters
m = 1.0             # mass
kp = 40.0
kd = 35.0
Fmax = 100

# Water current parameters
FcurAmp = 25.0                   # amplitude of the effective current force
FcurAngle = np.deg2rad(30.0)     # angle of the effective current force


# Input Parameters
Lx = 100.0                # Desired X position
Ly = 100.0                # Desired Y position
StartTime = 0.0           # Time of command start

# ODE solver parameters
abserr = 1.0e-8
relerr = 1.0e-6
stoptime = 15.0
numpoints = 1501
stepmax = 0.01

# Create the time samples for the output of the ODE solver.
# create a time array from 0..100 sampled at 0.1 second steps
dt = 0.05
t = np.arange(0.0, stoptime + dt, dt)


# Pack up the parameters and initial conditions:
L = [Lx, Ly]
p = [m, kp, kd, L, StartTime, Fmax, FcurAmp, FcurAngle]

# Initial conditions
x_init, y_init = des_pos(0,L,StartTime)
x_dot_init = 0.0
y_dot_init = 0.0
# Pack them into a vector
x0 = [x_init, x_dot_init, y_init, y_dot_init]


# Call the ODE solver.
resp = odeint(eq_of_motion, x0, t, args=(p,), atol=abserr, rtol=relerr)

# get the x and y position responses for plotting
x_resp = resp[:,0]
y_resp = resp[:,2]

# Save the desired trajectory for plotting too
desired_traj = des_pos(t, L, StartTime)
x_desired = desired_traj[0]
y_desired = desired_traj[1]

# Get current for plotting
Fcurrent = np.zeros((len(t), 2))

# Set up vector field of current
for ii in np.arange(len(t)):
    Fcurrent[ii,:] = Fcur(t[ii], p)
    
# Define the range of x and y coordinates to draw the current quivers over
xrange = np.linspace(-20, 20, 8) 
yrange = np.linspace(-10, 10, 8)
    
curX, curY = np.meshgrid(xrange, yrange)


# Set the plot size - 16x9 aspect ratio is best for videos
# We are mostly setting up the size and overall plot formatting here.
# The data here is just a placeholder, it will be filled during the animation
fig = plt.figure(figsize=(8, 4.5))
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
ax.grid(True, linestyle=':', color='0.75')
ax.set_axisbelow(True)

# Define the X and Y axis labels
plt.xlabel('X Position (m)', fontsize=22, weight='bold', labelpad=5)
plt.ylabel('Y Position (m)', fontsize=22, weight='bold', labelpad=10)
 
 
#  , '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628'
 
# define items to animate
time_template = 'Time = {:5.2f} s'
time_text = ax.text(0.05, 0.95, '', 
                    transform=ax.transAxes, 
                    fontsize=18, 
                    bbox=dict(facecolor='white', edgecolor='white', alpha=0.75))

plt.plot(x_desired, y_desired, linewidth=2, color='#4daf4a', linestyle='-.', label=r'Desired')

# This marker will serve as the vehicle
marker = ax.annotate('',xy=(x_resp[0], y_resp[0]),
                    xytext=(x_resp[1], y_resp[1]),
                    xycoords='data',
                    arrowprops=dict(width=2, headlength=16, facecolor='#e41a1c', edgecolor='#e41a1c'),
                    animated=True)

# We'll trail the past behind the marker
ghost, = ax.plot([],[], '#e41a1c', linewidth=2, linestyle='-', alpha=1, label=r'Actual')

# And use a quiver plot to represent the wind/current/etc
Q = ax.quiver(curX, curY, 
              Fcurrent[:,0], Fcurrent[:,1], 
              color='#377eb8', 
              edgecolors=('#377eb8'), 
              alpha = 0.5,
              width=0.0025, 
              animated=True)

# uncomment below and set limits if needed
plt.axis('equal')
plt.xlim(-15, 15)
plt.ylim(-10, 10)

# Create the legend, then fix the fontsize
leg = plt.legend(loc='upper right', ncol = 1, fancybox=True)
ltext  = leg.get_texts()
plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)




def init():
    '''
    Define the items to animate
    '''
    
    marker.xytext = ([], [])
    marker.xy = ([], [])
    
    ghost.set_data([], [])
    time_text.set_text('')
    
    ax.set_xlim(-15, 15)
    ax.set_ylim(-10, 10)
    
    return marker, ghost, Q,
    
    
def animate(i):
    ''' 
    Do the actual animation by updating values at each time step
    '''
    ax.set_xlim(-15, 15)
    ax.set_ylim(-10, 10)
    
    Q.set_UVC(Fcurrent[i,0], Fcurrent[i,1])
    
    x = x_resp[i]
    y = y_resp[i]
    
    
    # Here, I just use the difference between the last position and the current
    # one to get the angle. You can also use a heading response to determine
    # this angle.
    if i == 0:
        last_x, last_y = 0, 0
    else:
        last_x, last_y = x_resp[i - 1], y_resp[i - 1]
        
    angle = np.arctan2((y - last_y), (x - last_x))
    
    x_base = x - 1.0/2 * np.cos(angle)
    y_base = y - 1.0/2 * np.sin(angle)

    marker.set_position((x_base, y_base))
    marker.xytext = (x_base, y_base)
    marker.xy = (x, y)
        
    # Leave a "trail" behind the boat to show the path it took
    # You can leave the full trail
    x_ghost = x_resp[:i]
    y_ghost = y_resp[:i]
    
    # Or just a portion of it.
    # Here, we have it hard coded to be a two second trail (2/dt steps)
    # x_ghost = x_resp[np.max((0, i-int(2/dt))):i]
    # y_ghost = y_resp[np.max((0, i-int(2/dt))):i]
    
    ghost.set_data(x_ghost, y_ghost)
    
    time_text.set_text(time_template.format(i * dt))
    
    return marker, ghost, Q,
    

# Call the matplotlib animation function
anim = animation.FuncAnimation(fig, 
                               animate, 
                               np.arange(1, len(resp)), 
                               init_func=init,
                               interval=20, 
                               blit=True)


# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
anim.save('trajectory_animation.mp4', fps=30, dpi=300, bitrate = 2500, extra_args=['-vcodec', 'libx264'])

# close "Figure" - actually just removes from queue to show at next show() command
plt.close(fig)