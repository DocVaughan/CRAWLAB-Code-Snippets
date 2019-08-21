#! /usr/bin/env python 

##########################################################################################
# mass_spring_damper_nonlinear.py
#
# Script to a simulate a spring-mass-damper system with a hardening spring and nonlinear
# damping. We'll later use this model as simple example for several nonlinear control
# methods.
#
# NOTE: Plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
# 
# Created: 08/15/19
#   - Joshua Vaughan 
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
# TODO:
#   * 08/15/19 - JEV
#        - Add hard limits on deflection
#
##########################################################################################

# Simple two-mass-spring-damper system
#
#          +---> x              +---> y
#          |                    |
#      +--------+     k     +--------+
#      |        |---/\/\/---|        |
# f -->|   m1   |           |   m2   |
#      |        |-----]-----|        |
#      +--------+     c     +--------+


import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def eq_of_motion_nonlinear(t, w, p):
    """
    Defines the differential equations for the nonlinear spring-mass system.
    It's has a hardening spring and hardening damper.

    Arguments:
        w :  vector of the state variables:
        t :  time
    """
    
    x = w[0]
    x_dot = w[1]
    y = w[2]
    y_dot = w[3]
    
    m1, m2, k, c, Distance, StartTime, Amax, Vmax, F_amp = p
    
    # Create sysODE = (x', x_dot', y', y_dot')
    sysODE = np.array([x_dot,
                       k/m1 * (y - x)**3 + c/m1 * (y_dot - x_dot)**3 + f(t, p)/m1,
                       y_dot,
                       -k/m2 * (y - x)**3 - c/m2 * (y_dot - x_dot)**3])

    return sysODE

def eq_of_motion_linear(t, w, p):
    """
    Defines the differential equations for the nonlinear spring-mass system.
    It's has a hardening spring and hardening damper.

    Arguments:
        w :  vector of the state variables:
        t :  time
    """
    
    x = w[0]
    x_dot = w[1]
    y = w[2]
    y_dot = w[3]
    
    m1, m2, k, c, Distance, StartTime, Amax, Vmax, F_amp = p

    # Create sysODE = (x', x_dot', y', y_dot')
    sysODE = np.array([x_dot,
                       k/m1 * (y - x) + c/m1 * (y_dot - x_dot) + f(t, p)/m1,
                       y_dot,
                       -k/m2 * (y - x) - c/m2 * (y_dot - x_dot)])

    return sysODE


def f(t, p):
    """
    defines the disturbance force input to the system
    """
    m1, m2, k, c, Distance, StartTime, Amax, Vmax, F_amp = p
    

    # A simple bang-bang command in force beginning at t=StartTime
    f = F_amp * (t >= StartTime) * (t <= StartTime + 0.25) - F_amp * (t > StartTime + 0.25) * (t <= StartTime + 0.5)
    
    return f


# Note: For some problems you should define the Jacobian of the equations of
# motion and pass it to the ODE solver. This is especially true if the system
# is stiff - https://en.wikipedia.org/wiki/Stiff_equation


#---- Main script -----------------------------------------------------------------------

# Define the parameters for simluation
m1 = 1.0                     # mass (kg)
m2 = 1.0                     # mass (kg)
k = (1.0 * 2 * np.pi)**2     # spring constant (N/m)

# Select damping ratio and use it to choose an appropriate c
c = 1.0                      # damping coeff. (N/m/s)

# ODE solver parameters
abserr = 1.0e-9
relerr = 1.0e-9
max_step = 0.1
stoptime = 5.0
numpoints = 501

# Create the time samples for the output of the ODE solver
t = np.linspace(0.0, stoptime, numpoints)

# Initial conditions
x_init = 0.0                        # initial position
x_dot_init = 0.0                    # initial velocity
y_init = 0.0                        # initial position
y_dot_init = 0.0                    # initial velocity

# Set up the parameters for the input function
Distance = 1.0               # Desired move distance (m)
Amax = 20.0                  # acceleration limit (m/s^2)
Vmax = 2.0                   # velocity limit (m/s)
StartTime = 0.5              # Time the y(t) input will begin
F_amp = 100.0                # Amplitude of Disturbance force (N)

# Pack the parameters and initial conditions into arrays 
p = [m1, m2, k, c, Distance, StartTime, Amax, Vmax, F_amp]
x0 = [x_init, x_dot_init, y_init, y_dot_init]


linear_solution = solve_ivp(fun=lambda t, w: eq_of_motion_linear(t, w, p), 
                            t_span=[0, stoptime], 
                            y0=x0, 
                            dense_output=True,
                            #t_eval=t, 
                            max_step=max_step, 
                            atol=abserr, 
                            rtol=relerr
                            )

if not linear_solution.success: 
    # The ODE solver failed. Notify the user and print the error message
    print('ODE solution terminated before desired final time.')
    print('Be *very* careful trusting the results.')
    print('Message: {}'.format(solution.message))

# Parse the time and response arrays from the OdeResult object
linear_sim_time = linear_solution.t
linear_resp = linear_solution.y

# Call the ODE solver using the nonlinear equations of motion
nonlinear_solution = solve_ivp(fun=lambda t, w: eq_of_motion_nonlinear(t, w, p), 
                               t_span=[0, stoptime], 
                               y0=x0, 
                               dense_output=True,
                               #t_eval=t, 
                               max_step=max_step, 
                               atol=abserr, 
                               rtol=relerr
                               )

if not nonlinear_solution.success: 
    # The ODE solver failed. Notify the user and print the error message
    print('ODE solution terminated before desired final time.')
    print('Be *very* careful trusting the results.')
    print('Message: {}'.format(solution.message))

# Parse the time and response arrays from the OdeResult object
nonlinear_sim_time = nonlinear_solution.t
nonlinear_resp = nonlinear_solution.y


#----- Plot the responses
# Make the figure pretty, then plot the results
#   "pretty" parameters selected based on pdf output, not screen output
#   Many of these setting could also be made default by the .matplotlibrc file
fig = plt.figure(figsize=(6,4))
ax = plt.gca()
plt.subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)
plt.setp(ax.get_ymajorticklabels(),family='serif',fontsize=18)
plt.setp(ax.get_xmajorticklabels(),family='serif',fontsize=18)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.grid(True,linestyle=':',color='0.75')
ax.set_axisbelow(True)

plt.xlabel('Time (s)',family='serif',fontsize=22,weight='bold',labelpad=5)
plt.ylabel('Position (m)',family='serif',fontsize=22,weight='bold',labelpad=10)

# plot the linear response
plt.plot(linear_sim_time, linear_resp[0,:], linewidth=2, linestyle = '-', label=r'$x$ -- Lin')
plt.plot(linear_sim_time, linear_resp[2,:], linewidth=2, linestyle = '--', label=r'$y$ -- Lin.')

# Plot the nonlinear response, matching the colors
#plt.plot(nonlinear_sim_time, nonlinear_resp[0,:], linewidth=2, linestyle = '-.', color = '#e41a1c', label=r'$x$ -- Nonlin')
#plt.plot(nonlinear_sim_time, nonlinear_resp[2,:], linewidth=2, linestyle = ':', color = '#377eb8', label=r'$y$ -- Nonlin.')

plt.plot(nonlinear_sim_time, nonlinear_resp[0,:], linewidth=2, linestyle = '-.', label=r'$x$ -- Nonlin')
plt.plot(nonlinear_sim_time, nonlinear_resp[2,:], linewidth=2, linestyle = ':', label=r'$y$ -- Nonlin.')


leg = plt.legend(loc='lower right', ncol=2, fancybox=True)
ltext  = leg.get_texts() 
plt.setp(ltext,family='Serif',fontsize=16)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# If you want to save the figure, uncomment the commands below. 
# The figure will be saved in the same directory as your IPython notebook.
# Save the figure as a high-res pdf in the current folder
# plt.savefig('MassSpringDamper_Disturbance_Resp.pdf')

# Show the figures
plt.show()
