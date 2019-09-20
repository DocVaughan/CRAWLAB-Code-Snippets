###############################################################################
# trajecotry_interpolation.py
#
# Script exploring using the SciPy interolation routines to generate functional
# representations of array-based trajectories. We'll test how well they work
# as functions in ODE solvers using the simple model below:
#
# Simple mass-spring-damper system
#
#    +---> y        +---> X
#    |              |
#    |     k     +-----+
#    +---/\/\/---|     |
#    |           |  M  |<--- Fd
#    +-----]-----|     |
#          c     +-----+
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 09/19/19
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - @doc_vaughan
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
from scipy import interpolate
from scipy.misc import derivative
from scipy.integrate import solve_ivp

PLOT_INTERP = True  # Set true to plot a comparison of the array and interpolation

time = np.linspace(0, 5, 501)

# Define a bang-bang command using an array
y_ddot = np.zeros_like(time)
y_ddot[50:100] = 1
y_ddot[101:151] = -1

# Then create a function that represents that array using the SciPy 
# interpolation methods
y_ddot_func = interpolate.interp1d(time, y_ddot)


# Do the same for the force disturbance (but not necessarily a bang-bang)
# force_time = time
# force = np.zeros_like(force_time)
# force[301:] = 1
# Fd = interpolate.interp1d(force_time, force)

force_time = [0, 1, 2, 3, 4, 5]
force      = [0, 0, 0, 1, 1, 1]
Fd = interpolate.interp1d(force_time, 
                          force, 
                          kind='linear',
                          fill_value='extrapolate')


# We can also generate functional forms of the derivatives. We can calculate
# the derivative at each point in the time array to generate an array 
# repreenting the derivative. We then use that data to generate a function 
# using the SciPy interp1d method.
deriv_data = derivative(Fd, time, dx=1e-6)
deriv_func = interpolate.interp1d(time, 
                                  deriv_data, 
                                  kind='linear',
                                  fill_value='extrapolate')

# Do the same for the 2nd deriv
# double_deriv_data = derivative(deriv_func, time, dx=1e-6)
# double_deriv_func = interpolate.interp1d(time, 
#                                          double_deriv_data, 
#                                          kind='linear',
#                                          fill_value='extrapolate')

# An alternate way to do this would be to use one of the Numpy.diff methods
# then use the interpolation methods. This is probably worse on sparse arrays
# like the force one here. It may be better on denser ones like y_ddot above. 
# Here, we'll do it for the second derivative of Fd
double_deriv_data = np.diff(deriv_data) / (time[1] - time[0])
double_deriv_func = interpolate.interp1d(time[:-1], 
                                         double_deriv_data, 
                                         kind='linear',
                                         fill_value='extrapolate')


if PLOT_INTERP:
    # Plot the interpolation for the acceleration input
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
    plt.ylabel('Acceleration (m/s$^2$)', fontsize=22, weight='bold', labelpad=10)
    
    plt.plot(time, y_ddot, linewidth=2, linestyle='-', label=r'Array')
    plt.plot(time, y_ddot_func(time), linewidth=2, linestyle='--', label=r'Interp.')

    # uncomment below and set limits if needed
    # plt.xlim(0,5)
    # plt.ylim(0,10)

    # Create the legend, then fix the fontsize
    leg = plt.legend(loc='upper right', ncol = 1, fancybox=True)
    ltext  = leg.get_texts()
    plt.setp(ltext,fontsize=18)

    # Adjust the page layout filling the page using the new tight_layout command
    plt.tight_layout(pad=0.5)

    # save the figure as a high-res pdf in the current folder
    #plt.savefig('accel_interpolation_restuls.pdf')


    # Now, plot the interpolation for the force input
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
    
    plt.plot(force_time, force, linewidth=2, linestyle='-', label=r'Array')
    plt.plot(time, Fd(time), linewidth=2, linestyle='--', label=r'Interp.')

    # uncomment below and set limits if needed
    # plt.xlim(0,5)
    # plt.ylim(0,10)

    # Create the legend, then fix the fontsize
    leg = plt.legend(loc='upper right', ncol = 1, fancybox=True)
    ltext  = leg.get_texts()
    plt.setp(ltext,fontsize=18)

    # Adjust the page layout filling the page using the new tight_layout command
    plt.tight_layout(pad=0.5)

    # save the figure as a high-res pdf in the current folder
    #plt.savefig('force_interpolation_restuls.pdf')

    plt.show()


def eq_of_motion(w, t, p):
    """
    Defines the differential equations for the coupled spring-mass system.

    Arguments:
        w :  vector of the state variables:
        t :  time
    """
    
    x = w[0]
    x_dot = w[1]
    y = w[2]
    y_dot = w[3]
    
    m, k, c = p

    # Create sysODE = (x', x_dot', y', y_dot')
    sysODE = np.array([x_dot,
                       k/m * (y - x) + c/m * (y_dot - x_dot) - Fd(t) / m,
                       y_dot,
                       y_ddot_func(t)])

    return sysODE


# Define the parameters for simluation
m = 1.0                     # mass (kg)
k = (1.0 * 2 * np.pi)**2    # spring constant (N/m)

wn = np.sqrt(k / m)         # natural frequency (rad/s)

# Select damping ratio and use it to choose an appropriate c
zeta = 0.05                 # damping ratio
c = 2 * zeta * wn * m       # damping coeff.

# Initial conditions
x_init = 0.0                        # initial position
x_dot_init = 0.0                    # initial velocity
y_init = 0.0
y_dot_init = 0.0

# Pack the parameters and initial conditions into arrays 
p = [m, k, c]
x0 = [x_init, x_dot_init, y_init, y_dot_init]

# Call the ODE solver. 
solution = solve_ivp(fun=lambda t, w: eq_of_motion(w, t, p), 
                    t_span=[0, time[-1]], 
                    y0=x0, 
                    t_eval=time,
                    # method='LSODA',
                    # jac=lambda t, w: jacobian(w, t, p),
                    # dense_output=True,
                    # max_step=0.1, 
                    # atol=abserr, 
                    # rtol=relerr
                    )

if not solution.success: 
    # The ODE solver failed. Notify the user and print the error message
    print('ODE solution terminated before desired final time.')
    print('Be *very* careful trusting the results.')
    print('Message: {}'.format(solution.message))

# Parse the time and response arrays from the OdeResult object
sim_time = solution.t
resp = solution.y

#----- Plot the response
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
# ylim(-1.,1.)

# plot the response
plt.plot(sim_time, resp[0,:], linewidth=2, linestyle = '-', label=r'$x$')
plt.plot(sim_time, resp[2,:], linewidth=2, linestyle = '--', label=r'$y$')
    
leg = plt.legend(loc='upper right', fancybox=True)
ltext  = leg.get_texts() 
plt.setp(ltext,family='Serif',fontsize=16)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

plt.show()
