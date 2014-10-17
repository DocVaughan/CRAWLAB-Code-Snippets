#! /usr/bin/env python

##########################################################################################
# basic_InputShaping.py
#
# Script to run through use of the ZV shaper on a mass-spring-damper system
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 10/17/14
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################


import numpy as np
from matplotlib.pyplot import *

# Import the ODE solver
from scipy.integrate import odeint


def eq_of_motion(w, t, p):
    """
    Defines the differential equations for the coupled spring-mass system.

    Arguments:
        w :  vector of the state variables:
        t :  time
        p :  vector of the parameters:
    """
    # Unpack the states
    x, x_dot, y, y_dot = w
    
    # Unpack the parameters
    m, k, c, Distance, StartTime, Amax, Vmax, Shaper = p

    # Create sysODE = (x', x_dot', y', y_dot')
    sysODE = [x_dot,
             k/m * (y - x) + c/m * (y_dot - x_dot),
             y_dot,
             y_ddot(t, p)]
    return sysODE


def y_ddot(t, p):
    """
    Defines the accel input to the system.
    
    We'll make a call to our lab function accel_input()
    
    Depending on the desired move distance, max accel, and max velocity, the input is either
    bang-bang or bang-coast-bang
    """
    m, k, c, Distance, StartTime, Amax, Vmax, Shaper = p
    
    y_ddot = accel_input(Amax,Vmax,Distance,StartTime,t,Shaper)
    
    return y_ddot




def accel_input(Amax,Vmax,Distance,StartTime,CurrTime,Shaper):
    """
    Original MATLAB/Octave premable
    ###########################################################################
    # function [accel] = accel_input(Amax,Vmax,Distance,CurrTime,Shaper)
    #
    # Function returns acceleration at a given timestep based on user input
    #
    # Amax = maximum accel, assumed to besymmetric +/-
    # Vmax = maximum velocity, assumed to be symmetric in +/-
    # Distance = desired travel distance 
    # StartTime = Time command should begin
    # CurrTime = current time 
    # Shaper = array of the form [Ti Ai] - matches output format of shaper functions
    #           in toolbox
    #          * If Shaper is empty, then unshaped is run
    #
    #
    # Assumptions:
    #   * +/- maximums are of same amplitude
    #   * command will begin at StartTime (default = 0)
    #   * rest-to-rest bang-coast-bang move (before shaping)
    #
    # Created: 9/23/11 - Joshua Vaughan - vaughanje@gatech.edu
    #
    # Modified: 
    #   10/11/11
    # 		* Added hard-coded shaping option - JEV (vaughanje@gatech.edu)
    # 		* embedded into shaped_jumping.m for use there
    #
    ###########################################################################
    #
    #
    # Converted to Python on 3/3/13 by Joshua Vaughan (joshua.vaughan@louisiana.edu)
    #
    # Modified:
    #   * 3/26/14 - Joshua Vaughan - joshua.vaughan@louisiana.edu
    #       - Updated some commenting, corrected typos
    #       - Updated numpy import as np
    """

    # These are the times for a bang-coast-bang input 
    t1 = StartTime
    t2 = (Vmax/Amax) + t1
    t3 = (Distance/Vmax) + t1
    t4 = (t2 + t3)-t1
    end_time = t4

    if len(Shaper) == 0:
        # If no shaper is input, create an unshaped command
        if t3 <= t2: # command should be bang-bang, not bang-coast-bang
            t2 = np.sqrt(Distance/Amax)+t1
            t3 = 2.0 * np.sqrt(Distance/Amax)+t1
            end_time = t3
        
            accel = Amax*(CurrTime > t1) - 2*Amax*(CurrTime > t2) + Amax*(CurrTime > t3)
    
        else: # command is bang-coast-bang
            accel = Amax*(CurrTime > t1) - Amax*(CurrTime > t2) - Amax*(CurrTime > t3) + Amax*(CurrTime > t4)

    else: # create a shaped command
        ts = np.zeros((9,1))
        A = np.zeros((9,1))
        # 	Parse Shaper parameters
        for ii in range(len(Shaper)):
            ts[ii] = Shaper[ii,0]  # Shaper impulse times
            A[ii] = Shaper[ii,1]  # Shaper impulse amplitudes

        # Hard-coded for now
        # TODO: be smarter about constructing the total input - JEV - 10/11/11
        accel = (A[0]*(Amax*(CurrTime > (t1+ts[0])) - Amax*(CurrTime > (t2+ts[0])) - Amax*(CurrTime > (t3+ts[0])) + Amax*(CurrTime > (t4+ts[0])))
        +	A[1]*(Amax*(CurrTime > (t1+ts[1])) - Amax*(CurrTime > (t2+ts[1])) - Amax*(CurrTime > (t3+ts[1])) + Amax*(CurrTime > (t4+ts[1])))
        +   A[2]*(Amax*(CurrTime > (t1+ts[2])) - Amax*(CurrTime > (t2+ts[2])) - Amax*(CurrTime > (t3+ts[2])) + Amax*(CurrTime > (t4+ts[2])))
        +   A[3]*(Amax*(CurrTime > (t1+ts[3])) - Amax*(CurrTime > (t2+ts[3])) - Amax*(CurrTime > (t3+ts[3])) + Amax*(CurrTime > (t4+ts[3])))
        +   A[4]*(Amax*(CurrTime > (t1+ts[4])) - Amax*(CurrTime > (t2+ts[4])) - Amax*(CurrTime > (t3+ts[4])) + Amax*(CurrTime > (t4+ts[4])))
        +   A[5]*(Amax*(CurrTime > (t1+ts[5])) - Amax*(CurrTime > (t2+ts[5])) - Amax*(CurrTime > (t3+ts[5])) + Amax*(CurrTime > (t4+ts[5])))
        +   A[6]*(Amax*(CurrTime > (t1+ts[6])) - Amax*(CurrTime > (t2+ts[6])) - Amax*(CurrTime > (t3+ts[6])) + Amax*(CurrTime > (t4+ts[6])))
        +   A[7]*(Amax*(CurrTime > (t1+ts[7])) - Amax*(CurrTime > (t2+ts[7])) - Amax*(CurrTime > (t3+ts[7])) + Amax*(CurrTime > (t4+ts[7])))
        +   A[8]*(Amax*(CurrTime > (t1+ts[8])) - Amax*(CurrTime > (t2+ts[8])) - Amax*(CurrTime > (t3+ts[8])) + Amax*(CurrTime > (t4+ts[8]))))

    return accel



def ZV(f,zeta,deltaT):
    """
    This function returns an exact and digitized version of the ZV shaper for 
    natural frequency, f Hz, and damping ratio, zeta. The exactshaper is digitize for use
    at a shaping ratio of deltaT seconds/sample.
    
    Original MATLAB preamble
        ZV(f,zeta,deltaT) -- Bill Singhose
        Generates a ZV shaper for 1 mode.
        f - frequency (Hz) of vibration being controlled.
        zeta - damping ratio of vibration being controlled.
        deltaT - time spacing at which input to system is updated.
        
        This function generates the exact sequence and then uses
        DigitizeSeq to convert the exact sequence to digital format.
    
    
    Converted to Python on 2/19/13 - Joshua Vaughan - joshua.vaughan@louisiana.edu
    
    Arguments:
      f : frequency to suppress vibraton at (Hz)
      zeta : damping ratio 
      deltaT : The sampling time used in the digial implementation of the shaper
    
    Returns:
      shaper : the digitized version of the shaper
      exactshaper : the exact shaper soltuion in. Impulse times and amplitudes are in 2x2 array
    
    """

    Wn = 2*np.pi*f
    shaperdeltaT = np.pi / (Wn * np.sqrt(1-(zeta)**2))
    K = np.exp(-zeta * np.pi / (np.sqrt(1-zeta**2)))
    shaperdenom  =  1 + K

    time2 = shaperdeltaT   
 
    amp1 = 1.0 / shaperdenom
    amp2 = K / shaperdenom

    exactshaper = np.array([[0.,amp1],[time2,amp2]])
    shaper = digseq(exactshaper,deltaT)

    return shaper, exactshaper



def digseq(seq, step):
    """
    This function digitizes an impulse sequence, seq, so that it will function properly
    for a sampling rate of step seconds/sample.
    
    Original MATLAB preamble
        digseq - Whit Rappole
        DIGITIZESEQ Map a sequence onto digital timing loop
        dseq = digseq(seq,step)
    
        Uses a linear extrapolation to split each continuous
        impulse into two digital impulses
        

    Converted to Python on 2/18/13 by Joshua Vaughan (joshua.vaughan@louisiana.edu)
    """

    dseq = np.zeros((round(seq[-1,0]/step)+2,1))

    for nn in range(len(seq)):
        index = np.floor(seq[nn,0]/step)
        woof = (seq[nn,0]-index*step)/step
        dseq[index+1] = dseq[index+1]+woof*seq[nn,1]
        dseq[index] = dseq[index]+seq[nn,1] - woof*seq[nn,1]

    while dseq[len(dseq)-1] == 0:
        dseq = dseq[0:(len(dseq)-1)]

    return dseq


# Define the parameters for simluation
m = 1.0                         # mass (kg)
k = (0.5*2*np.pi)**2            # spring constant (N/m)

wn = np.sqrt(k/m)               # natural frequency (rad/s)

# Select damping ratio and use it to choose an appropriate c
zeta = 0.0                      # damping ratio
c = 2*zeta*wn*m                 # damping coeff.

# ODE solver parameters
abserr = 1.0e-9
relerr = 1.0e-9
max_step = 0.001
stoptime = 5.0
numpoints = 50001

# Create the time samples for the output of the ODE solver
t = np.linspace(0.0, stoptime, numpoints)

# Initial conditions
x_init = 0.0                        # initial position
x_dot_init = 0.0                    # initial velocity
y_init = 0.0                        # initial "command" position
y_dot_init = 0.0                    # initial "command" velocity

# Set up the parameters for the input function
Distance = 1.5                      # Desired move distance (m)
Amax = 200.0                        # acceleration limit (m/s^2)
Vmax = 1.0                          # velocity limit (m/s)
StartTime = 0.5                     # Time the y(t) input will begin

# Design and define an input Shaper  
Shaper = [] # An empty shaper means no input shaping

# Pack the parameters and initial conditions into arrays 
p = [m, k, c, Distance, StartTime, Amax, Vmax, Shaper]
x0 = [x_init, x_dot_init, y_init, y_dot_init]

# Call the ODE solver
resp_unshaped = odeint(eq_of_motion, x0, t, args=(p,), atol=abserr, rtol=relerr,  hmax=max_step)


# No grids for these dual y plots
rcParams['axes.grid'] = False 

# Make the figure pretty, then plot the results
#   "pretty" parameters selected based on pdf output, not screen output
#   Many of these setting could also be made default by the .matplotlibrc file
fig = figure(figsize=(6,4))
ax1 = gca()
subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)
setp(ax1.get_ymajorticklabels(),family='serif',fontsize=18)
setp(ax1.get_xmajorticklabels(),family='serif',fontsize=18)
# ax1.spines['right'].set_color('none')
ax1.spines['top'].set_color('none')
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
# ax1.grid(False,linestyle=':',color='0.75')
ax1.set_axisbelow(True)

xlabel('Time (s)',family='serif',fontsize=24,weight='bold',labelpad=5)
ylabel('Velocity Command',family='serif',fontsize=24, color = '#e41a1c', weight='bold',labelpad=10)

# plot the response
ax1.plot(t,resp_unshaped[:,3], linewidth=2, 
         color = '#e41a1c', linestyle = '--', label=r'Command $(y)$')
ylim(0,1.5)
yticks([0,0.5,1,1.5],['0','0.5','1.0','1.5'])
xticks([0,1,2,3,4,5],['0','1','2','3','4','5'])

ax2 = ax1.twinx()
ax2.spines['top'].set_color('none')
ax2.plot(t,resp_unshaped[:,0], linewidth=2, color = '#377eb8', 
         linestyle = '-', label=r'Response $(x)$')
ylim(0,2)
yticks([0,0.5,1,1.5,2.0],['0','0.5','1.0','1.5','2.0'])
ylabel('Payload Response',family='serif', fontsize=24, color = '#377eb8',weight='bold',labelpad=10)


# leg = legend(loc='lower right', fancybox=True)
# ltext  = leg.get_texts() 
# setp(ltext,family='Serif',fontsize=16)

# Adjust the page layout filling the page using the new tight_layout command
# tight_layout(pad=0.5)

# If you want to save the figure, uncomment the commands below. 
# The figure will be saved in the same directory as your IPython notebook.
# Save the figure as a high-res pdf in the current folder
# savefig('MassSpringDamper_UnshapedVEL_Resp.pdf')



#----- Now let's apply some input shaping -----------------------------------------------

# Design and define an input Shaper  
[digShaper, Shaper] = ZV(wn/(2.0*np.pi), zeta, max_step)

# Pack the parameters and initial conditions into arrays 
p = [m, k, c, Distance, StartTime, Amax, Vmax, Shaper]

# Call the ODE solver to get the shaped response
resp_shaped = odeint(eq_of_motion, x0, t, args=(p,), atol=abserr, rtol=relerr,  hmax=max_step)

# No grids for these dual y plots
rcParams['axes.grid'] = False 


# Make the figure pretty, then plot the results
#   "pretty" parameters selected based on pdf output, not screen output
#   Many of these setting could also be made default by the .matplotlibrc file
fig = figure(figsize=(6,4))
ax1 = gca()
subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)
setp(ax1.get_ymajorticklabels(),family='serif',fontsize=18)
setp(ax1.get_xmajorticklabels(),family='serif',fontsize=18)
# ax1.spines['right'].set_color('none')
ax1.spines['top'].set_color('none')
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
# ax1.grid(True,linestyle=':',color='0.75')
ax1.set_axisbelow(True)

xlabel('Time (s)',family='serif',fontsize=24,weight='bold',labelpad=5)
ylabel('Input Shaped \nVelocity Command',family='serif', fontsize=24, color = '#e41a1c',weight='bold',labelpad=10)


# plot the response
ax1.plot(t,resp_shaped[:,3], linewidth=2, color = '#e41a1c', linestyle = '--', label=r'Command $(y)$')
ylim(0,1.5)
yticks([0,0.5,1,1.5],['0','0.5','1.0','1.5'])
xticks([0,1,2,3,4,5],['0','1','2','3','4','5'])

ax2 = ax1.twinx()
ax2.spines['top'].set_color('none')
ax2.plot(t,resp_shaped[:,0], linewidth=2, color = '#377eb8', linestyle = '-', label=r'Response $(x)$')
ylim(0,2)
yticks([0,0.5,1,1.5,2.0],['0','0.5','1.0','1.5','2.0'])
ylabel('Input Shaped \nPayload Response',family='serif', fontsize=24, color = '#377eb8',weight='bold',labelpad=10)

# leg = legend(loc='lower right', fancybox=True)
# ltext  = leg.get_texts() 
# setp(ltext,family='Serif',fontsize=16)

# Adjust the page layout filling the page using the new tight_layout command
# tight_layout(pad=0.5)

# If you want to save the figure, uncomment the commands below. 
# The figure will be saved in the same directory as your IPython notebook.
# Save the figure as a high-res pdf in the current folder
# savefig('MassSpringDamper_ZVshapedVEL_Resp.pdf')



#----- Now, let's compare the shaped and unshaped directly ------------------------------

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

# plot the response
plot(t,resp_unshaped[:,0], linewidth=2, linestyle = '-', label=r'Unshaped')
plot(t,resp_shaped[:,0], linewidth=2, linestyle = '--', label=r'ZV-shaped')

leg = legend(loc='lower right', fancybox=True)
ltext  = leg.get_texts() 
setp(ltext,family='Serif',fontsize=16)

# Adjust the page layout filling the page using the new tight_layout command
# tight_layout(pad=0.5)

# If you want to save the figure, uncomment the commands below. 
# The figure will be saved in the same directory as your IPython notebook.
# Save the figure as a high-res pdf in the current folder
# savefig('MassSpringDamper_Resp_Comparison.pdf')

# Now show all the plots
show()