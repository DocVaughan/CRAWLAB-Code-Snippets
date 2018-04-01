#! /usr/bin/env python

###############################################################################
# mpc_mass_spring_damper_UnconstrainedStateSpace.py
#
# This is a constrained Model Predictive Controller for a simple 
# mass-spring-damper system. Constraints are placed on the magnitude of the 
# control input
#
# Code largely implemented while following the notes at:
#  http://engineering.utsa.edu/ataha/wp-content/uploads/sites/38/2017/07/EE5143_Module9.pdf
# 
# So, the notation there is used for most of the matrix operations
#
# Created: 03/31/18
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

from numpy.linalg import inv, matrix_power
import control

# Define the sampling rate and number of samples to look ahead
Np = 50        # Set the prediction horizon
dt = 0.01       # The sampling time of the system (s)

# Define the stop time for the simulation
stop_time = 5

# Then, create a time array using those parameters.
# One extra sample because arange doesn't include upper bound in the array
time = np.arange(0.0, stop_time+dt, dt)

num_samples = stop_time / dt
num_cycles = num_samples / Np

# Define the parameters for simluation
m = 1.0                      # mass (kg)
k = (2.0*2*np.pi)**2         # spring constant (N/m)

wn = np.sqrt(k/m)            # natural frequency (rad/s)

# Select damping ratio and use it to choose an appropriate c
zeta = 0.00                   # damping ratio
c = 2*zeta*wn*m               # damping coeff.

# Define the minimum and maximum actuator effort
U_max = 10                    # N
U_min = -U_max                # N


# Form the continuous time version of the system
A_cont = np.array([[0,       1],
                   [-wn**2, -2*zeta*wn]])

B_cont = np.array([[0],
                   [1/m]])
                   
C_cont = np.array([[1, 0]]) #np.eye(2)

D_cont = np.zeros((np.shape(C_cont)[0],np.shape(B_cont)[1]))

sys = control.ss(A_cont, B_cont, C_cont, D_cont)

# Now, digitize it
digital_sys = control.sample_system(sys, dt)

# And extract the state space components
A = digital_sys.A
B = digital_sys.B
C = digital_sys.C
D = digital_sys.D

# Example arrays from the link in the preamble. Were used to check this code.
# A = np.array([[1, 1],[0, 1]])
# B = np.array([[0.5],[1]])
# C = np.array([[1, 0]])
# D = np.zeros((np.shape(C)[0],np.shape(B)[1]))

# Determine the number of states and inputs from the matrix shapes
num_states = len(A)
num_inputs = np.shape(B)[1]
num_outputs = np.shape(C)[0]

# Now, set up the augmented matrices for the linear programming solution
Phi = np.block([[A,      np.zeros((num_states, num_outputs))],
                [C@A,    np.eye(num_outputs)]])

Gamma = np.block([[B],
                  [C@B]])

Ca = np.block([[np.zeros((1, num_states)), np.ones((1, num_outputs))]])


# Now, we can use those augmented dynamics to generate the matrices needed 
# for the predicted output
#
# See slide number 18/32 at: 
#    http://engineering.utsa.edu/ataha/wp-content/uploads/sites/38/2017/07/EE5143_Module9.pdf
# for the full explanation of these matrices W and Z
# They basically include the prediction part of the model predictive controller
W = np.zeros((Np, num_states+num_outputs))
for index in range(Np):
    W[index, :] = Ca @ matrix_power(Phi, index+1)


Z = np.zeros((Np,Np))
offset = 0
for column in range(Np):
    for row in range(Np):
        if row + offset < Np:
            Z[row + offset, column] = Ca @ matrix_power(Phi, row) @ Gamma

    offset = offset + 1



# TODO: 03/30/18 - JEV - These should be block diagonal, not strictly diagonal, I think.
Q = 10*np.eye(Np)
# Q = np.kron(np.eye(Np//2), Q)

R = 0.01 * np.eye(Np)
# R = np.kron(np.eye(Np), R)

# See page 11 of the pdf below for reasoning for these E and H matrices:
#   https://engineering.purdue.edu/~zak/ECE680/MPC_handout.pdf
E = np.ones((Np, num_inputs))

#
H = np.zeros((Np, Np))
row, col = np.indices(H.shape)

for index in range(np.shape(H)[1]):
    H[row == col + index*2] = 1.0

# This matrix will be used for the case where we only want to limit the first
# output value of the calculated horizon. We call it Input_A because it will
# become part of Ax<=b type constraint
Input_A_I = np.block([[-np.eye(num_inputs), np.zeros((num_inputs, Np-num_inputs))],
                      [np.eye(num_inputs), np.zeros((num_inputs, Np-num_inputs))]])




# Define the initial state of the system
x1_init = 0.0
x1_dot_init = 0.0

# Define arrays to fill with the simulation data
x1_total = np.zeros_like(time)
x2_total = np.zeros_like(time)
y_total = np.zeros_like(time)
u_total = np.zeros_like(time)

# Define the "current" states and output
x0 = np.array([[x1_init],[x1_dot_init]])
y0 = np.array([[x1_init]])

# Pack them into the augmented state vector
xa_kp1 = np.block([[x0], 
                   [y0]])

# Define the desired setpoint
XD = 1.0 * np.ones((Np, 1))

# Loop over the full time range, one sample at a time. At each sample time, 
# calculate the optimal input and use it
for sample in range(int(num_samples)):
    # Update the current state using the prediction
    xa = xa_kp1 

    # Now, compute the optimal series of inputs
    deltaU = inv(R + Z.T @ Q @ Z) @ Z.T @ Q @ (XD - W @ xa)
    
    Input_b = np.array([[-U_min + E * u_total[sample]],
                        [U_max - E * u_total[sample]]])

    Input_A = Input_A_I @ deltaU
    
    


#     # TODO - 03/30/18 - JEV - Do we need to calculate these gains for anything?
#     #Compute the gain matrices Kr and Kmpc
#     K_r = np.block([[np.ones(num_inputs), np.zeros(Np - num_inputs)]]) * inv(R + Z.T @ Q @ Z) @ Z.T @ Q
# 
#     K_mpc = K_r @ W @ np.block([[np.ones((num_states,num_states))],[np.zeros((num_outputs,num_states))]])
# 
#     K_y = K_r @ W @ np.block([[np.zeros((num_states,1))],[np.ones(num_outputs)]])
# 
#     delta_u = K_r @ XD - K_y @ y0 - K_mpc @ x0

    delta_u = np.block([np.ones(num_inputs), np.zeros(Np - num_inputs)]) @ deltaU
    
    # TODO: 03/30/18 - JEV - Do we need the calculate delta_x separately?
    # delta_x_kp1 = A @ x0 + B * delta_u
    
    # Get the augmented state vector for the next step
    # TODO: 03/30/18 - JEV - That last multiply should be an @, I think
    xa_kp1 = Phi @ xa + Gamma * delta_u
    
    # Save the running totals of the states, input, and output
    u_total[sample+1] = u_total[sample] + deltaU[0]
    x1_total[sample+1] = x1_total[sample] + xa_kp1[0,:]
    x2_total[sample+1] = x2_total[sample] + xa_kp1[1,:]
    y_total[sample+1] = xa_kp1[2,:]
    
    # TODO: 03/30/18 - JEV - Clean this up.
    DEBUG = False
    if (DEBUG):
        print('DeltaU = {}'.format(deltaU))
        print('delta_u = {}'.format(delta_u))
        print('delta_x = {}'.format(delta_x_kp1))
        print('xa_kp1 = {}'.format(xa_kp1))
        input()


# Now, plot the output and control input

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
 
plt.plot(time, y_total[:len(time)], linewidth=2, linestyle='-', label=r'Data 1')

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
# plt.savefig('mpc_output.pdf')

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
 
plt.plot(time, u_total[:len(time)], linewidth=2, linestyle='-', label=r'Data 1')

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
# plt.savefig('mpc_command.pdf')

# show the figure
plt.show()


# Now, let's verify the results using a full simulation of the model 
x0 = np.array([[x1_init],[x1_dot_init]])
time_out, y_out, x_out = control.forced_response(sys, time, u_total, x0)


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
 
plt.plot(time_out, y_out, linewidth=2, linestyle='-', label=r'Data 1')

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
# plt.savefig('mpc_output_fullSimluation.pdf')

# show the figure
plt.show()
