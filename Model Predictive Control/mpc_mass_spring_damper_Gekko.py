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

from gekko import GEKKO

# Create an instance of GEKKO. By default, this points to a server at
#  http://byu.apmonitor.com, where the solution is actually done. That means
#  that you'll need to be connected to the Internet for it to work.
m = GEKKO()

# Optionally, you can instantiate with remote=False to solve locally. The major
#  downside of this for most of what we do is that the local implementation 
#  does not include IPOPT solver, which is generally significantly better than 
#  APOPT for the types of problems we solve.
# m = GEKKO(remote=False)

m.time = np.linspace(0, 5, 501)

# m.options.SOLVER = 3      # Choose the solver, 1: APOPT, 2: BPOPT, 3: IPOPT (default)
# m.options.MAX_ITER = 250  # Set the maximum number of solver iterations. Default is 250.
# m.options.COLDSTART = 2
# m.options.AUTO_COLD = 5
# m.options.REDUCE = 10

# Parameters and Constants
#  https://gekko.readthedocs.io/en/latest/quick_start.html#parameters
#  https://gekko.readthedocs.io/en/latest/quick_start.html#constants
mass_1 = 1.0                        # (kg)
mass_2 = 1.0                        # (kg)
c = m.Const(value=0.0)              # Spring constant (N/m/s)
k = m.Const(value=(2*2*np.pi)**2)   # Spring constant (N/m)
MAX_FORCE = 50.0                    # maximum force from actuator (N)
MIN_FORCE = -50.0                   # minimum force from actuator (N)

# Manipulated variables - Here, it's just the force acting on the mass
#  https://gekko.readthedocs.io/en/latest/quick_start.html#manipulated-variable
u = m.MV(value=0, lb=MIN_FORCE, ub=MAX_FORCE)
u.STATUS = 1             # allow optimizer to change this variable

# Weight on control input 
#  https://gekko.readthedocs.io/en/latest/tuning_params.html#cost
u.COST = 1e-6            

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
# u.MV_STEP_HOR = 10



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

# We can also manipulate the rate of change of those setpoints. Generally, it
#  will probably be preferable to control the setpoint manually instead of 
#  relying on these, especially for our research purposes.
#  https://gekko.readthedocs.io/en/latest/tuning_params.html#tau
# x.TAU = 0.01      # time constant of trajectory
# y.TAU = 0.01      # time constant of trajectory

# Set the costs for each state 
# https://gekko.readthedocs.io/en/latest/tuning_params.html#wsp
x.WSP = 1.0             # Cost on x state
x_dot.WSP = 1.0e-3      # Cost on x_dot state
y.WSP = 1.0             # Cost on y state
y_dot.WSP = 1.0e-1      # Cost on y_dot state


# Define the differential equations that define the system dynamics
m.Equation(x.dt() == x_dot)
m.Equation(mass_1 * x_dot.dt() == k * (y - x) + c * (y_dot - x_dot) + u)
m.Equation(y.dt() == y_dot)
m.Equation(mass_2 * y_dot.dt() == -k * (y - x) - c * (y_dot - x_dot))

m.options.IMODE = 6 # MPC control
#m.solve(disp=False, GUI=False)  # Cold start
m.solve(disp=True)              # Now full solution

# We can get additional solution information
# import json
# with open(m.path+'//results.json') as f:
#     results = json.load(f)


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
 
plt.plot(m.time, u.value, linewidth=2, linestyle='-', label=r'$u$')

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
 
plt.plot(m.time, x.value, linewidth=2, linestyle='-', label=r'$m_1$')
plt.plot(m.time, y.value, linewidth=2, linestyle='--', label=r'$m_2$')

# uncomment below and set limits if needed
# plt.xlim(0,5)
if np.max((x.value, y.value)) < 1.25:
    plt.ylim(0, 1.25)

# Create the legend, then fix the fontsize
leg = plt.legend(loc='upper right', ncol = 2, fancybox=True)
ltext  = leg.get_texts()
plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
# plt.savefig('MPC_massSpringDamper_Gekko_response.pdf')

# show the figure
plt.show()
# plt.close()