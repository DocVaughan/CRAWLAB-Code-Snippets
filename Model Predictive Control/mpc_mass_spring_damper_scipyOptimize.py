#! /usr/bin/env python

###############################################################################
# mpc_mass_spring_damper_scipyOptimize.py
#
# Solving a Model Predictive Controller for a simple mass-spring-damper 
# system using the optimization packages of scipy
# 
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 04/20/18
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

# import minimize from scipy
from scipy.optimize import minimize

# We'll use the control system toolbox to create and simulate the system
import control


# Define the time oriented parameters for the problem
prediction_horizon = 10     # Number of samples to use in prediction
dt = 0.1                    # Sampling time (s)

stop_time = 5.0             # Time to end the simulation

# One extra sample because arange doesn't include upper bound in the array
time = np.arange(0, stop_time + dt, dt)

num_samples = stop_time / dt # Determine the number of samples in the sim time

# Define the parameters for simluation
m = 1.0                     # mass (kg)
k = (1.0*2*np.pi)**2        # spring constant (N/m)

wn = np.sqrt(k/m)           # natural frequency (rad/s)

# Select damping ratio and use it to choose an appropriate c
zeta = 0.1                  # damping ratio
c = 2*zeta*wn*m             # damping coeff.

U_max = 50                  # Maximum actuator effort (N)

A = np.array([[0, 1], [-wn**2, -2*zeta*wn]])
B = np.array([[0], [1/m]])
C = np.eye(2)
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
q11 = 100    # The weight on error in position from desired
q22 = 1      # The weight on error in velocity from desired

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


# Form the variables needed for solver. x will hold the states during the
# horizon and u contains the variables that we are solving for. 
#
# Both are set to zero here, but a smarter initial guess, particular with the 
# u array is *strongly* advised
x = np.zeros(num_states * (int(prediction_horizon + 1)))
u = np.zeros(num_inputs * (int(prediction_horizon + 1),))

# We will pass the states to the optimizer too. This allows us to define the 
# constraints in a way that is more easily integrated with the minimize method
initial_guess = np.hstack((x, u))



def cost_function(optim_states, *args):
    """ 
    Cost function to minimize during the optimization. Here, we are using a 
    quadratic cost on state error and actuator effor
    
    Arguments:
      inputs : the input to solve for
      states : the states
      Q : An array weighting the states error xT * Q * x
      R : An array weighting the input uT * R * u
      
    Returns:
      float representing the cost
    """
    
    prediction_horizon, desired_states, x0, Q, R = args
    
    # parse the states in the optimization to system states and inputs
    states = optim_states[:num_states * (int(prediction_horizon + 1))].reshape(prediction_horizon+1, num_states)
    inputs = optim_states[num_states * (int(prediction_horizon + 1)):].reshape(prediction_horizon+1, num_inputs)
    
    # initialize the costs
    state_cost = 0
    input_cost = 0
    
    # calculate the state error
    states_error = desired_states - states
    
    for state_error in states_error:
        state_cost = state_cost + state_error.T @ Q @ state_error
        
    for input in inputs:
        try:
            input_cost = input_cost + input.T @ R @ input
        except ValueError:    
            input_cost = input_cost + input * R * input
            
    return 0.5 * state_cost + 0.5 * input_cost
   
def calculate_next_step(optim_states, t, args):
    # parse the states in the optimization to system states and inputs
    x = optim_states[:num_states * (int(prediction_horizon + 1))].reshape(prediction_horizon+1, num_states)
    u = optim_states[num_states * (int(prediction_horizon + 1)):].reshape(prediction_horizon+1, num_inputs)
    
#     import pdb
#     pdb.set_trace()
    ineq_constraint = -x[t+1, :].reshape(2,1) + digital_sys.A * x[t, :].reshape(2,1) + digital_sys.B * u[t, :]
    print(ineq_constraint.reshape(1,2))
    return ineq_constraint

    
def generate_constraints(optim_states, args):

    prediction_horizon, desired_states, x0, Q, R = args
        
    # parse the states in the optimization to system states and inputs
    x = optim_states[:num_states * (int(prediction_horizon + 1))].reshape(prediction_horizon+1, num_states)
    u = optim_states[num_states * (int(prediction_horizon + 1)):].reshape(prediction_horizon+1, num_inputs)
    
    for t in range(prediction_horizon):
        constraints = ({'type': 'eq',
                        'fun': lambda x: calculate_next_step(x, t, args)})
    
#     contraints += ({'type': 'ineq',
#                     'fun': lambda u: u_max - u})
#                     
#     contraints += ({'type': 'ineq',
#                     'fun': lambda u: u - u_min})
                    
    return constraints

Q = 100*np.eye(num_states)
R = np.eye(num_inputs)
desired_states = np.hstack((np.ones((prediction_horizon+1,1)), np.zeros((prediction_horizon+1,1))))

x_init = 0.0
x_dot_init = 0.0
x0 = [x_init, x_dot_init]

args = prediction_horizon, desired_states, x0, Q, R

# Now, form the contraints
constraints = generate_constraints(initial_guess, args)

# And generate bounds
# bounds = []
# x_max = 10
# x_min = -x_max
# x_dot_max = 100
# x_dot_min = -x_dot_max
# u_max = 100
# u_min = -100
# 
# for _ in range(prediction_horizon):
#     bounds.append((x_min, x_max), (x_dot_min, x_dot_max), (u_min, u_max))


u_total = np.zeros((int(num_samples), num_inputs))
# Now, we work through the range of the simulation time. At each step, we
# look prediction_horizon samples into the future and optimize the input over
# that range of time. We then take only the first element of that sequence
# as the current input, then repeat.
for index in range(int(num_samples)):

    res = minimize(cost_function, initial_guess, args, #bounds=bnds,
                   constraints=constraints, method='SLSQP', 
                   options={'maxiter':1e3, 'eps':1e-9, 'disp':True})
    
    # Finally, save the current state as the initial condition for the next
    initial_guess = res.x
    
    x = res.x[:num_states * (int(prediction_horizon + 1))].reshape(prediction_horizon+1, num_states)
    x0 = x[0, :]
    
    u = res.x[num_states * (int(prediction_horizon + 1)):].reshape(prediction_horizon+1, num_inputs)
    u_total[index, :] = u[0,:]
    
    args = prediction_horizon, desired_states, x0, Q, R


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


# Convert the system to digital using the faster sampling rate.
new_digital_sys = control.sample_system(sys, new_dt)

# Now, simulate the systema at the new higher sampling rate
t_out, y_out, x_out = control.forced_response(new_digital_sys, time, u_newDt)


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
 
plt.plot(t_out, y_out[:,0], linewidth=2, linestyle='-', label=r'Position')

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