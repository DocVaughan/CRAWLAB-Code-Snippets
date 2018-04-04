#! /usr/bin/env python

###############################################################################
# mpc_planarCrane_nonlinear.py
#
# Solving a Model Predictive Controller for a simple planar crane system
# using the cvxpy module. The solution has a constraint on maximum
# velocity and maximum payload deflection. 
# 
# We'll use a course sample time and the linearized model 
# during the solution procedure then simulate the full nonlinear crane 
# system using odeint with the solution result.
#
# Note: This isn't quite how this would really work with a nonlinear system.
#       We'd be predicting using the linear model at each step, but using
#       measurements of the current state of nonlinear system. As implemented 
#       here, the model used to generate the "measurements" for the MPC 
#       solution is the linear one.
#
# cvxpy - https://cvxgrp.github.io/cvxpy/index.html
# 
# This full optimal control tutorial for cvxpy was used as the basis for this script:
#  http://nbviewer.jupyter.org/github/cvxgrp/cvx_short_course/blob/master/intro/control.ipynb
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 04/04/18
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

import control
import cvxpy as cvx

# We need to import the ode solver for the nonlinear simulation
from scipy.integrate import odeint

# Define the time oriented parameters for the problem
prediction_horizon = 20     # Number of samples to use in prediction
dt = 0.1                    # Sampling time (s) to use in prediction

stop_time = 10.0             # Time to end the simulation

# One extra sample because arange doesn't include upper bound in the array
time = np.arange(0, stop_time + dt, dt)

num_samples = stop_time / dt # Determine the number of samples in the sim time

# Define the system parameters
l = 1.0                     # cable length (m)
g = 9.81                    # gravity (m/s)

# Limits on system
U_max = 10                  # Maximum trolley acceleration (m/s)
V_max = 1.25                # Maximum velocity (m/s)
theta_max = np.deg2rad(5)  # maximum deflection (rad.)

# Now, define the state-space form of the equations of motion
# For derivation of these, you can see the Jupyter notebook at: 
#   https://git.io/vxDsz
A = np.array([[0,    1, 0, 0], 
              [-g/l, 0, 0, 0],
              [0,    0, 0, 1],
              [0,    0, 0, 0]])
B = np.array([[0], [1/l], [0], [1]])
C = np.eye(4)               # Output all states
D = np.zeros((4, 1))

sys = control.ss(A, B, C, D)

# Convert the system to digital. We need to use the discrete version of the 
# system for the MPC solution
digital_sys = control.sample_system(sys, dt)

# Get the number of states and inputs - for use in setting up the optimization
# problem
num_states = np.shape(A)[0] # Number of states
num_inputs = np.shape(B)[1] # Number of inputs

# Define the desired states to track. Here, it's just a desired final value
# in the each of the states
XD = 1.0            # desired position (m)
XD_dot = 0.0        # desired velocity (m/s)
thetaD = 0.0        # desired cable angle (rad)
thetaD_dot = 0.0    # desired cable angular velocity (rad/s)

# Define the weights on the system states and input
q11 = 100   # The weight on error in angle from desired
q22 = 10    # The weight on error in angular velocity from desired
q33 = 10    # The weight on error in position from desired
q44 = 0     # The weight on error in velocity from desired

# We only have 1 element of u, so this is the weighting of the input
r11 = 0.0001 # The 1,1 element of R


# Define the initial conditions
theta_init = 0.0       # Initial Angle (rad)
theta_dot_init = 0.0   # Initial Angular velocity (rad/s)
x_init = 0.0           # Initial position (m)
x_dot_init = 0.0       # Initial velocity (m/s)

# form array of initial conditions for solver
x_0 = np.array([theta_init, theta_dot_init, x_init, x_dot_init]) 

# Store the initial conditions as the first element of arrays to be appended
# to in the solution process
theta_total = np.array([theta_init])
theta_dot_total = np.array([theta_dot_init])
x_total = np.array([x_init])
x_dot_total = np.array([x_dot_init])

# Initialize arrays to hold the full input sequences. It's first element is 0.
u_total = np.zeros(1,)


# Form the variables needed for the cvxpy solver
x = cvx.Variable(int(num_states), int(prediction_horizon + 1))
u = cvx.Variable(int(num_inputs), int(prediction_horizon))

# Now, we work through the range of the simulation time. At each step, we
# look prediction_horizon samples into the future and optimize the input over
# that range of time. We then take only the first element of that sequence
# as the current input, then repeat.
for _ in range(int(num_samples)):

    states = []
    for t in range(prediction_horizon):
        cost = (q11 * cvx.sum_squares(thetaD - x[0, t+1]) + 
                q22 * cvx.sum_squares(thetaD_dot - x[1, t+1]) + 
                q33 * cvx.sum_squares(XD - x[2, t+1]) + 
                q44 * cvx.sum_squares(XD_dot - x[3, t+1]) + 
                r11 * cvx.sum_squares(u[:,t]))

        constr = [x[:, t+1] == digital_sys.A * x[:, t] + digital_sys.B * u[:, t],
                  cvx.norm(u[:,t], 'inf') <= U_max,
                  cvx.norm(x[0,t], 'inf') <= theta_max,
                  cvx.norm(x[3,t], 'inf') <= V_max]
              
        states.append(cvx.Problem(cvx.Minimize(cost), constr))

    # sums problem objectives and concatenates constraints.
    prob = sum(states)
    prob.constraints += [x[:,0] == x_0]
    prob.solve()

    u_total = np.append(u_total, u[0].value)
    theta_total = np.append(theta_total, x[0,1].value)
    theta_dot_total = np.append(theta_dot_total, x[1,1].value)
    x_total = np.append(x_total, x[2,1].value)
    x_dot_total = np.append(x_dot_total, x[3,1].value)

    # Finally, save the current state as the initial condition for the next
    x_0 = np.array(x[:,1].value.A.flatten())


# Now, we'll use the command we generated with MPC in the full nonlinear simulation

def eq_of_motion(w, t, p):
    """
    Defines the differential equations for the coupled spring-mass system.

    Arguments:
        w :  vector of the state variables:
        t :  time
        p :  vector of the parameters:
    """
    theta, theta_dot, x, x_dot = w
    l, g, u_mpc, time = p

    # Create sysODE = (theta', theta_dot')
    sysODE = [theta_dot,
             -g/l * theta + 1.0/l * x_ddot(t, p),
             x_dot,
             x_ddot(t, p)]
    
    return sysODE

def x_ddot(t, p):
    """
    Defines the accel input to the system.
    
    We'll pick the value of the array corresponding to the latest sample whose 
    time is not greater than the time of the solver.
    
    Arguments:
        t : current time step 
        p : vector of parameters
    """
    l, g, u_mpc, time = p
    
    # Get the last value not greater than the time the solveer wants. This is
    # basically a zero-order hold
    x_ddot = u_mpc[np.max(np.argwhere(t >= time))] 
    
    return x_ddot


# Define the parameter and initial condition arrays for the ode solver
p = [l, g, u_total, time]
x0 = [theta_init, theta_dot_init, x_init, x_dot_init]

# ODE solver parameters
abserr = 1.0e-9
relerr = 1.0e-9
max_step = 0.01

# Define a time array for the simulation
sim_time = np.arange(0, stop_time + 0.01, 0.01)

# Now, run the simulation
response = odeint(eq_of_motion, x0, sim_time, args=(p,) , atol=abserr, rtol=relerr,  hmax=max_step)

# parse the response for easier plotting
theta_resp = response[:,0]
theta_dot_resp = response[:,1]
x_resp = response[:,2]
x_dot_resp = response[:,3]

payload_position = x_resp + l * np.sin(theta_resp)

# I'm including a message here, so that I can tell from the terminal when it's
# done running. Otherwise, the plot windows tend to end up hidden behind others
# and I have to dig around to get them.
input("\nDone solving... press enter to plot the results.")



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

plt.plot(sim_time, x_resp, linewidth=2, linestyle='--', label=r'Trolley') 
plt.plot(sim_time, payload_position, linewidth=2, linestyle='-', label=r'Payload')

# uncomment below and set limits if needed
# plt.xlim(0,5)
plt.ylim(0, np.ceil(1.25*np.max(payload_position)))

# Create the legend, then fix the fontsize
leg = plt.legend(loc='upper right', ncol = 2, fancybox=True)
ltext  = leg.get_texts()
plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
# plt.savefig('mpc_cvxpy_position_response.pdf')


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
plt.ylabel('Angle (deg)', fontsize=22, weight='bold', labelpad=10)

plt.plot(sim_time, np.rad2deg(theta_resp), linewidth=2, linestyle='-', label=r'Angle') 

# Also plot lines to show the limit being enforced on angle
plt.plot(sim_time, np.rad2deg(theta_max)*np.ones_like(sim_time), linewidth = 1.5, linestyle = ':', color = "#333333", zorder=1)
plt.plot(sim_time, -np.rad2deg(theta_max)*np.ones_like(sim_time), linewidth = 1.5, linestyle = ':', color = "#333333", zorder=1)

props = dict(boxstyle='round', edgecolor='white', facecolor='white', alpha=0.95)

# place a text box to label the two limit lines
textstr = "Angle Limit"
ax.text(sim_time[-1], np.rad2deg(theta_max), 
        textstr, 
        fontsize=14,
        verticalalignment='center', 
        horizontalalignment='right',
        bbox=props)
        
ax.text(sim_time[-1], np.rad2deg(-theta_max), 
        textstr, 
        fontsize=14,
        verticalalignment='center', 
        horizontalalignment='right',
        bbox=props)

# uncomment below and set limits if needed
# plt.xlim(0,5)
plt.ylim(np.floor(1.25*np.rad2deg(-theta_max)), np.ceil(1.25*np.rad2deg(theta_max)))

# Create the legend, then fix the fontsize
# leg = plt.legend(loc='upper right', ncol = 2, fancybox=True)
# ltext  = leg.get_texts()
# plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
# plt.savefig('mpc_cvxpy_angle_response.pdf')


accel = np.zeros_like(sim_time)
for index, t in enumerate(sim_time):
    accel[index] = x_ddot(t, p)

     
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
plt.ylabel('Accel. (m/$s^2$)', fontsize=22, weight='bold', labelpad=10)
 
plt.plot(time, u_total, linewidth=2, linestyle='-', label=r'MPC Input')
plt.plot(sim_time, accel, linewidth=2, linestyle='--', label=r'ODE Solver')

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
# plt.savefig('mpc_cvxpy_input.pdf')

# show the figure
plt.show()
