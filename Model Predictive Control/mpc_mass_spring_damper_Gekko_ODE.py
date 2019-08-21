#! /usr/bin/env python

###############################################################################
# mpc_mass_spring_damper_Gekko_ODE.py
#
# A mass-spring-damper example of Model Predictive Control using the Gekko 
# interface to APMonitor. This version uses Gekko to calculate the MPC 
# solution, but solve_ivp to simulate the system. This allows analysis of the
# effects of modeling error on the MPC solution. At each timestep, the "real" 
# system solution from the ODE solver is passed back to Gekko for use in the 
# MPC solution over the next time interval.
#
# Nominal model is:
#          +---> x              +---> y
#          |                    |
#      +--------+     k     +--------+
#      |        |---/\/\/---|        |
# u -->|   m1   |           |   m2   |
#      |        |-----]-----|        |
#      +--------+     c     +--------+
#
# Gekko - https://gekko.readthedocs.io/
# APMonitor - https://apmonitor.com/wiki/index.php
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 08/21/19
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
from scipy.integrate import solve_ivp
from tqdm import tqdm
import time

from gekko import GEKKO

DEBUGGING = False  # Set true to print out monitoring/debugging info


def eq_of_motion_nonlinear(t, w, p):
    """
    Defines the differential equations for the  spring-mass system.
    We can vary parameters from what the MPC solver is using or
    introduce noise and other disturbances to test the MPC solution's
    robustness.

    Arguments:
        w :  vector of the state variables:
        t :  time
        p : array-like parameter list
    """
    
    x = w[0]
    x_dot = w[1]
    y = w[2]
    y_dot = w[3]
    
    m1, m2, k, c, u = p
    
    # Introduce some error in the system parameters from those being used by 
    # the MPC solution
    # k = 0.8 * k         # Change the spring constant
    # c = 2.0 * c       # Change the damping ratio
    # m2 = 0.5 * m      # Change mass of m2
    
    # Add some friction on m2, which is not in the MPC solution
    mu = 0.1            # Coefficient of friction
    g = 9.81            # Acceleration due to gravity (m/s^2)
    friction = mu * m2 * g * np.sign(y_dot)

    # Create sysODE = (x', x_dot', y', y_dot')
    sysODE = np.array([x_dot,
                       k/m1 * (y - x) + c/m1 * (y_dot - x_dot) + u/m1,
                       y_dot,
                       -k/m2 * (y - x) - c/m2 * (y_dot - x_dot) - friction/m2])
    
    return sysODE


m = GEKKO(remote=False)

# In this setup, this time becomes the prediction horizon for the MPC solution
m.time = np.arange(0, 0.51, 0.01) 

# Parameters and Constants
#  https://gekko.readthedocs.io/en/latest/quick_start.html#parameters
#  https://gekko.readthedocs.io/en/latest/quick_start.html#constants

# Define the model parameters
mass_1 = 1.0                        # (kg)
mass_2 = 1.0                        # (kg)
SPRING_CONSTANT = (2*2*np.pi)**2    # Spring constant (N/m)
DAMPING_COEFF = 1.0                 # Damping coefficient (N/m/s)
MAX_FORCE = 50.0                    # maximum force from actuator (N)
MIN_FORCE = -50.0                   # minimum force from actuator (N)

#Make the damping coefficient and spring constant parameters
# https://gekko.readthedocs.io/en/latest/quick_start.html#parameters
c = m.Const(value=DAMPING_COEFF)
k = m.Const(value=SPRING_CONSTANT)

# Manipulated variables - Here, it's just the force acting on the mass
#  https://gekko.readthedocs.io/en/latest/quick_start.html#manipulated-variable
u = m.MV(value=0, lb=MIN_FORCE, ub=MAX_FORCE)
u.STATUS = 1             # allow optimizer to change this variable
u.FSTATUS = 0

# Weight on control input 
#  https://gekko.readthedocs.io/en/latest/tuning_params.html#cost
u.COST = 1e-9

# In general, we'll need to set the _.COST value. 
# The others below are optional

# Weight on rate-of-change of control input 
#  https://gekko.readthedocs.io/en/latest/tuning_params.html#dcost
# u.DCOST = 1e-1

# Explicit limit on how much the control effort can change for each iteration 
#  https://gekko.readthedocs.io/en/latest/tuning_params.html#dmax
#u.DMAX = 2

# Explicit limit on how much the control effort can change positively 
#  for each iteration. Overrides _.DMAX setting.
#  https://gekko.readthedocs.io/en/latest/tuning_params.html#dmaxhi
# u.DMAXHI = 1

# Explicit limit on how much the control effort can change negatively 
#  for each iteration. It will generally be negative to allow control effort
#  to decrease. Overrides _.DMAX setting.
#  https://gekko.readthedocs.io/en/latest/tuning_params.html#dmaxlo
# u.DMAXLO = -50

# Explicit limit on how much the control effort can change for each iteration - https://gekko.readthedocs.io/en/latest/tuning_params.html#dmax# Only let the control effort change every MV_STEP_HOR steps, 0=use global setting 
#  https://gekko.readthedocs.io/en/latest/tuning_params.html#mv-step-hor
u.MV_STEP_HOR = 10


# Controlled Variables 
# https://gekko.readthedocs.io/en/latest/quick_start.html#controlled-variable
#
# Here they are just the state of the system, because all states are involved
# in the formation of the objective function

# Define initial conditions for the system, staring from rest.
x_init = 0.0 
x_dot_init = 0.0
y_init = 0.0
y_dot_init = 0.0

# Save the initial conditions for the ODE solver
x0 = [x_init, x_dot_init, y_init, y_dot_init]

x = m.CV(value=x_init)
x.STATUS = 1            # add the SP to the objective function
x.FSTATUS = 1           # Use the measured value of the state not the estimate

x_dot = m.CV(value=x_dot_init)
x_dot.STATUS = 1        # add the SP to the objective function
x_dot.FSTATUS = 1       # Use the measured value of the state not the estimate

y = m.CV(value=y_init)
y.STATUS = 1            # add the SP to the objective function
y.FSTATUS = 1           # Use the measured value of the state not the estimate

y_dot = m.CV(value=y_dot_init)
y_dot.STATUS = 1        # add the SP to the objective function
y_dot.FSTATUS = 1       # Use the measured value of the state not the estimate

# Define the setpoint/desired target value for each each state
# https://gekko.readthedocs.io/en/latest/tuning_params.html#sp
x.SP = 1.0              # x position set point (desired final state)
x_dot.SP = 0.0          # x velocity set point (desired final state)
y.SP = 1.0              # y position set point (desired final state)
y_dot.SP = 0.0          # y velocity set point (desired final state)

# We can also manipulate the rate of change of those setpoints. Generally, it
#  will probably be preferable to control the setpoint manually instead of 
#  relying on these, especially for our research purposes.
#  https://gekko.readthedocs.io/en/latest/tuning_params.html#tau
# x.TAU = 0.01            # time constant of trajectory
# y.TAU = 0.01            # time constant of trajectory

# Set the costs for each state 
# https://gekko.readthedocs.io/en/latest/tuning_params.html#wsp
x.WSP = 1.0             # Cost on x state
x_dot.WSP = 1.0e-3      # Cost on x_dot state
y.WSP = 1.0             # Cost on y state
y_dot.WSP = 1.0e-1      # Cost on y_dot state

m.options.CV_TYPE = 2   # Used a "normal" squared error objective function

# We can also explicitly define (or add components to) the objective function
#  Here, we add a objective to penalize deflection, with a weight defined by
#  DEFLECTION_COST
#  https://gekko.readthedocs.io/en/latest/quick_start.html#objectives
DEFLECTION_COST = 1e-2
m.Obj(DEFLECTION_COST * (y - x)**2)

# Define the differential equations that define the system dynamics
m.Equation(x.dt() == x_dot)
m.Equation(mass_1 * x_dot.dt() == k * (y - x) + c * (y_dot - x_dot) + u)
m.Equation(y.dt() == y_dot)
m.Equation(mass_2 * y_dot.dt() == -k * (y - x) - c * (y_dot - x_dot))


m.options.IMODE = 6 # MPC control
m.options.SOLVER = 3
# m.options.COLDSTART = 2
# m.solve(disp=False)

# We can get additional solution information
# import json
# with open(m.path+'//results.json') as f:
#     results = json.load(f)


# Set up NumPy arrays to allow us to plot the state and control history
sim_time = np.linspace(0, 2.5, 251)
control = np.zeros_like(sim_time)
response = np.zeros((len(sim_time), 4))

dt = sim_time[1] - sim_time[0]

# Simulate the nonlinear sytem over one time interval, using the MPC solution
# from the linear system
for index in tqdm(range(len(sim_time))):
    # Now, run the nonlinear simulation. We'll use the resulting final
    # states as the initial states in the next iteration of the MPC 
    # solution.
    # Pack the parameters into arrays 
    ode_params = [mass_1, mass_2, SPRING_CONSTANT, DAMPING_COEFF, control[index]]
    
    start_time = time.time()
    nonlinear_solution = solve_ivp(fun=lambda t, w: eq_of_motion_nonlinear(t, w, ode_params), 
                                   t_span=[0, dt], 
                                   y0=x0, 
                                   # t_eval=np.linspace(0, dx.dt, 11),
                                   # dense_output=False,
                                   # max_step=max_step, 
                                   # atol=abserr, 
                                   # rtol=relerr
                                   )
    
    if DEBUGGING:
        print('Index: {}'.format(index))                                   
        print('ODE solution time: {:8.4f}s'.format(time.time() - start_time))
    
    if not nonlinear_solution.success: 
        # The ODE solver failed. Notify the user and print the error message
        print('ODE solution terminated before desired final time.')
        print('Be *very* careful trusting the results.')
        print('Message: {}'.format(nonlinear_solution.message))

    # Parse the time and response arrays from the OdeResult object
    nonlinear_sim_time = nonlinear_solution.t
    response[index,:] = nonlinear_solution.y[:,-1]
    x0 = nonlinear_solution.y[:,-1]
    
    # retrieve measurements
    x.MEAS = nonlinear_solution.y[0][-1]
    x_dot.MEAS = nonlinear_solution.y[1][-1]
    y.MEAS = nonlinear_solution.y[2][-1]
    y_dot.MEAS = nonlinear_solution.y[3][-1]

    # solve MPC
    start_time = time.time()
    m.solve(disp=False)
    
    if DEBUGGING:
        print('MPC solution time: {:8.4f}s'.format(time.time() - start_time))
          
    if index < len(sim_time)-1:
        if DEBUGGING:
            print('Control Input:     {:8.4f}N\r\n'.format(u.NEWVAL))
    
        control[index+1] = u.NEWVAL




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
 
plt.plot(sim_time, control, linewidth=2, linestyle='-', label=r'$u$')

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
#plt.savefig('MPC_massSpringDamper_Gekko_input.pdf')


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
 
plt.plot(sim_time, response[:,0], linewidth=2, linestyle='-', label=r'$m_1$')
plt.plot(sim_time, response[:,2], linewidth=2, linestyle='--', label=r'$m_2$')

# uncomment below and set limits if needed
# plt.xlim(0,5)
if np.max((response[:,0], response[:,2])) < 1.25:
    plt.ylim(0, 1.25)

# Create the legend, then fix the fontsize
leg = plt.legend(loc='upper right', ncol=2, fancybox=True)
ltext  = leg.get_texts()
plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
# plt.savefig('MPC_massSpringDamper_Gekko_response.pdf')

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
plt.ylabel('Deflection (m)', fontsize=22, weight='bold', labelpad=10)
 
plt.plot(sim_time, response[:,2] - response[:,0], linewidth=2, linestyle='-', label=r'$y - x$')

# uncomment below and set limits if needed
# plt.xlim(0,5)
# plt.ylim(0, 1.25)

## Create the legend, then fix the fontsize
# leg = plt.legend(loc='upper right', ncol=2, fancybox=True)
# ltext  = leg.get_texts()
# plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
# plt.savefig('MPC_massSpringDamper_Gekko_deflection.pdf')

# show the figure
plt.show()
# plt.close()