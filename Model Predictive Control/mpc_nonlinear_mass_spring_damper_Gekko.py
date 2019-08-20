#! /usr/bin/env python

###############################################################################
# mpc_mass_spring_damper_Gekko.py
#
# A mass-spring-damper example of Model Predictive Control using the Gekko 
# interface to APMonitor. This version uses Gekko to both simulate the system 
# (solve the ODEs) and calculate the MPC solution.
#
# Gekko - https://gekko.readthedocs.io/
# APMonitor - https://apmonitor.com/wiki/index.php
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 08/20/19
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


def eq_of_motion_nonlinear(t, w, p):
    """
    Defines the differential equations for the nonlinear spring-mass system.
    It's has a hardening spring and hardening damper.

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
    
    #k = 1.25*k

    # Create sysODE = (x', x_dot', y', y_dot')
    sysODE = np.array([x_dot,
                       k/m1 * (y - x) + c/m1 * (y_dot - x_dot) + u/m1,
                       y_dot,
                       -k/m2 * (y - x) - c/m2 * (y_dot - x_dot)])
    
    return sysODE


m = GEKKO()
m.time = np.linspace(0, 0.5, 51)

# m.options.CTRL_HOR = 100
# m.options.PRED_HOR = 200

# Define the model parameters
mass_1 = 1.0                        # (kg)
mass_2 = 1.0                        # (kg)
SPRING_CONSTANT = (2*2*np.pi)**2    # Spring constant (N/m)
DAMPING_COEFF = 0.0                 # Damping coefficient (N/m/s)
MAX_FORCE = 50.0                    # maximum force from actuator (N)
MIN_FORCE = -50.0                   # minimum force from actuator (N)

# Make the damping coefficient and spring constant parameters
# https://gekko.readthedocs.io/en/latest/quick_start.html#parameters
c = m.Param(value=DAMPING_COEFF)
k = m.Param(value=SPRING_CONSTANT)

# Manipulated variables - Here, it's just the force acting on the mass
# https://gekko.readthedocs.io/en/latest/quick_start.html#manipulated-variable
u = m.MV(value=0, lb=MIN_FORCE, ub=MAX_FORCE)
u.STATUS = 1             # allow optimizer to change this variable
u.COST = 1e-6            # weight on control input - https://gekko.readthedocs.io/en/latest/tuning_params.html#cost
#u.DCOST = 1e-3           # weight on rate-of-change of control input - https://gekko.readthedocs.io/en/latest/tuning_params.html#dcost


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

x0 = [x_init, x_dot_init, y_init, y_dot_init]

x = m.CV(value=x_init)
x.STATUS = 1            # add the SP to the objective function

x_dot = m.CV(value=x_dot_init)
x_dot.STATUS = 1        # add the SP to the objective function

y = m.CV(value=y_init)
y.STATUS = 1            # add the SP to the objective function

y_dot = m.CV(value=y_dot_init)
y_dot.STATUS = 1        # add the SP to the objective function

m.options.CV_TYPE = 2   # Used a "normal" squared error objective function

# Define the setpoint/desired target value for each each state
# https://gekko.readthedocs.io/en/latest/tuning_params.html#sp
x.SP = 1.0              # x position set point (desired final state)
x_dot.SP = 0.0          # x velocity set point (desired final state)
y.SP = 1.0              # y position set point (desired final state)
y_dot.SP = 0.0          # y velocity set point (desired final state)

# Set the costs for each state 
# https://gekko.readthedocs.io/en/latest/tuning_params.html#wsp
x.WSP = 1.0             # Cost on x state
x_dot.WSP = 1.0e-3      # Cost on x_dot state
y.WSP = 1.0             # Cost on y state
y_dot.WSP = 1.0e-1      # Cost on y_dot state


# We can also manipulate the rate of change of those setpoints. Generally, it
# will probably be preferable to control the setpoint manually instead of 
# relying on these, especially for our research purposes.
# x.TR_INIT = 1  # set point trajectory
# x_dot.TR_INIT = 1  # set point trajectory
# y.TR_INIT = 1  # set point trajectory
# y_dot.TR_INIT = 1  # set point trajectory

# x.TAU = 0.01      # time constant of trajectory
# y.TAU = 0.01      # time constant of trajectory

# Define the differential equations that define the system dynamics
m.Equation(x.dt() == x_dot)
m.Equation(mass_1 * x_dot.dt() == k * (y - x) + c * (y_dot - x_dot) + u)
m.Equation(y.dt() == y_dot)
m.Equation(mass_2 * y_dot.dt() == -k * (y - x) - c * (y_dot - x_dot))

m.options.IMODE = 6 # MPC control
m.options.SOLVER = 3
# m.solve(disp=False)

# We can get additional solution information
# import json
# with open(m.path+'//results.json') as f:
#     results = json.load(f)


# Set up NumPy arrays to allow us to plot the state and control history
sim_time = np.linspace(0, 5, 501)
control = np.zeros_like(sim_time)
response = np.zeros((len(sim_time), 4))

dt = sim_time[1] - sim_time[0]

# Simulate the nonlinear sytem over one time interval, using the MPC solution
# from the linear system
for index in range(len(sim_time)-1):
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

    print('Index: {}'.format(index))                                   
    print('ODE solution: {}'.format(time.time() - start_time))
    
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
    m.solve(disp=False) # remote=False for local solve
    print('MPC solution: {}\r\n'.format(time.time() - start_time))

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
if np.max((x.value, y.value)) < 1.25:
    plt.ylim(0, 1.25)

# Create the legend, then fix the fontsize
leg = plt.legend(loc='upper right', ncol=2, fancybox=True)
ltext  = leg.get_texts()
plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
# plt.savefig('MPC_massSpringDamper_Gekko_response.pdf')

# show the figure
plt.show()
# plt.close()