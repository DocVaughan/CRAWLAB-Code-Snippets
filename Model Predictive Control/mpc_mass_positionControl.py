#! /usr/bin/env python

###############################################################################
# mpc_mass_positionControl.py
#
# Solving a Model Predictive Controller for a simple mass system with viscous
# friction using the cvxpy module. We'll use a course sample time during the
# solution procedure then simulate the system with a finer time.
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
# Created: 03/29/18
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 04/04/18 - JEV - joshua.vaughan@louisiana.edu
#       - General cleanup
#       - Simplification of program logic around looping over full duration
#       - 
#
# TODO:
#   * 
###############################################################################

import numpy as np
import matplotlib.pyplot as plt

import control
import cvxpy as cvx


# Define the time oriented parameters for the problem
prediction_horizon = 10     # Number of samples to use in prediction
dt = 0.1                    # Sampling time (s) to use in prediction

stop_time = 5.0             # Time to end the simulation

# One extra sample because arange doesn't include upper bound in the array
time = np.arange(0, stop_time + dt, dt)

num_samples = stop_time / dt # Determine the number of samples in the sim time

# Define the system parameters
m = 1.0                     # mass (kg)
c = 1                       # oefficient to represent the viscous friction
U_max = 50                  # Maximum actuator effort (N)

A = np.array([[0, 1], [0, -c/m]])
B = np.array([[0], [1/m]])
C = np.eye(2)               # Output both position and velocity
D = np.zeros((2, 1))

sys = control.ss(A, B, C, D)

# Convert the system to digital. We need to use the discrete version of the 
# system for the MPC solution
digital_sys = control.sample_system(sys, dt)

# Get the number of states and inputs - for use in setting up the optimization
# problem
num_states = np.shape(A)[0] # Number of states
num_inputs = np.shape(B)[1] # Number of inputs

# Define the desired trajectory to track. Here, it's just a desired final position
XD = 1.0
XD_dot = 0.0

# Define the weights on the system states and input
q11 = 100   # The weight on error in position from desired
q22 = 0     # The weight on error in velocity from desired

# We only have 1 element of u, so this is the weighting of the input
r11 = 0.0001 # The 1,1 element of R - 


# Define the initial conditions
x1_init = 0.0           # Initial position (m)
x1_dot_init = 0.0       # Initial velocity (m/s)

# form array of initial conditions for solver
x_0 = np.array([x1_init, x1_dot_init]) 

# Store the initial conditions as the first element of arrays to be appended
# to in the solution process
x1_total = np.array([x1_init])
x2_total = np.array([x1_dot_init])

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
        cost = (q11 * cvx.sum_squares(XD - x[0, t+1]) + 
                q22 * cvx.sum_squares(XD_dot - x[1, t+1]) + 
                r11 * cvx.sum_squares(u[:,t]))

        constr = [x[:, t+1] == digital_sys.A * x[:, t] + digital_sys.B * u[:, t],
                  cvx.norm(u[:,t], 'inf') <= U_max]
              
        states.append(cvx.Problem(cvx.Minimize(cost), constr))

    # sums problem objectives and concatenates constraints.
    prob = sum(states)
    prob.constraints += [x[:,0] == x_0]
    prob.solve(solver=cvx.ECOS)

    u_total = np.append(u_total, u[0].value)
    x1_total = np.append(x1_total, x[0,1].value)
    x2_total = np.append(x2_total, x[1,1].value)

    # Finally, save the current state as the initial condition for the next
    x_0 = np.array(x[:,1].value.A.flatten())


# ----- Simulation using this command ----
# Now, let's use a zero order hold on the  u_total vector to generate a higher
# sample rate command

new_dt = 0.01                   # Sampling time (s) to use in prediction
sampling_multiple = dt / new_dt 

# Define the new time vector
time = np.arange(0, stop_time, new_dt)

sampling_offset = np.ones(int(sampling_multiple),)

u_newDt = np.kron(u_total, sampling_offset)
u_newDt = u_newDt[int(sampling_multiple):]


t_out, y_out, x_out = control.forced_response(sys, time, u_newDt)



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
 
plt.plot(t_out, y_out[0,:], linewidth=2, linestyle='-', label=r'Position')

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
plt.ylabel('Force (N)', fontsize=22, weight='bold', labelpad=10)
 
plt.plot(time, u_newDt, linewidth=2, linestyle='-', label=r'Input')

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
