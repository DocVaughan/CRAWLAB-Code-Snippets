#! /usr/bin/env python

##########################################################################################
# PID.py
#
# general PID module - suitable for "real-time" use
#   Adapted from PID controller used on the Anaconda
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 10/30/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
##########################################################################################

import numpy as np
import time, logging

logger = logging.getLogger(__name__)



class PID(object):
    ''' Class to implement a basic PID controller for use on the Anaconda'''
    
    def __init__(self, kp, ki, kd, dt, max_out, min_out, start_time = None):
        ''' Initializing
        
        Arguments:
            kp = proportional gain, float > 0
            kd = derivative gain, float >= 0
            ki = integral gain, float >= 0
            dt = sample time (ms)
            max_out = the maximum output of the controller
            min_out = the minimum output of the controller
        '''
        logging.debug('Creating PID controller...')
        self.kp = kp
        self.kd = kd / dt
        self.ki = ki * dt
        self.dt = dt
        
        self.max_output = max_out
        self.min_output = min_out
        
        if start_time is None:
            self.current_time = time.time()
            self.previous_time = self.current_time
        else:
            self.current_time = 0.0
            self.previous_time = 0.0
        
        self.last_Error = 0.0
        self.last_state = 0.0
        self.integral_term = 0.0
        
        self.output = 0.0


    def change_gains(self, kp, kd, ki):
        self.kp = kp
        self.kd = kd / self.dt
        self.ki = ki * self.dt


    def change_sample_time(self, dt):
        self.sample_time_ratio = dt / self.dt
        
        # update gain terms to reflect new sample time
        self.ki *= self.sample_time_ratio
        self.kd /= self.sample_time_ratio
        
        # update sample time
        self.dt = dt


    def compute_output(self, desired_state, current_state, current_time = None, previous_time = None):
        if current_time is None:
            logging.debug('Current Time is None')
            self.current_time = time.time()
        else:
            self.current_time = current_time
        
        if previous_time is not None:
            self.previous_time = previous_time
            
        logging.debug('Current State: {:.4f}\t Desired State: {:.4f}'.format(current_state, desired_state))    
        logging.debug('Current Time: {:.4f}\t Previous Time: {:.4f}'.format(self.current_time, self.previous_time))    
        
        if (self.current_time - self.previous_time >= self.dt):
            self.error = desired_state - current_state
            
            self.integral_term += self.ki * self.error
            
            self.state_change = current_state - self.last_state
            self.last_state = current_state
            
            logging.debug('Error: {:.4f}\t Error_dot: {:.4f}'.format(self.error, self.state_change))
            logging.debug('Integral term: {:.4f}'.format(self.integral_term))
            
            self.output = self.kp * self.error + self.integral_term - self.kd * self.state_change
            
            # TODO: 01/24/18 - JEV - Add integral windup check
            
            # limit the output to within the range of possible values
            if self.output > self.max_output:
                self.output = self.max_output
            elif self.output < self.min_output:
                self.output = self.min_output
            
            self.previous_time = self.current_time
                
        logging.debug('PID output: {:.4f}\n'.format(self.output))

        return self.output

# Example use
if __name__ == '__main__':
    """ Example use of the PID controller
    
    This is just the PID control of a mass to a desired setpoint. 
    A constant disturbance force can be included for testing the integral term.
    
    """
    
    import matplotlib.pyplot as plt
    from scipy.integrate import odeint
    
    
    # Debug level logging
    logging.basicConfig(level=logging.DEBUG,
                        format='From %(threadName)-10s: %(message)s',
                        )

    # logging.basicConfig(level=logging.CRITICAL,
    #                     format='From %(threadName)-10s: %(message)s',
    #                     )

    # Create the PID controller
    kp = (2*np.pi)**2 # proportional gain
    ki = 50.0            # integral gain
    kd = 3.5            # derivative gain
    deltaT = 0.01       # sampling time
    u_max = 100.0       # maximum actuator effort
    pid = PID(kp, ki, kd, deltaT, u_max, -u_max, 0.0)
    
    def eq_of_motion(w, t, p):
        """
        Defines the differential equations for the coupled spring-mass system.

        Arguments:
            w :  vector of the state variables:
            t :  time
            p :  vector of the parameters:
        """
        x, x_dot = w
        m, desired, PID_force, F_disturb = p
        
        # logging.debug('PID_force = {:.4f}'.format(PID_force))
        
        # Create sysODE = (x',y_dot')
        #  We ignore the xd_dot term, as it is only an impulse as the start of the step
        sysODE = [x_dot,
                  1.0/m * (PID_force -  F_disturb)]
        return sysODE
    
    # ODE solver parameters
    abserr = 1.0e-12
    relerr = 1.0e-12
    max_step = 0.1
    stoptime = 10.0

    # Create the time samples for the output of the ODE solver.
    t = np.arange(0, stoptime, deltaT)


    # Define and pack up the parameters and initial conditions:
    m = 1.0         # system mass
    desired = 1.0   # desired setpoint - constant
    
    # Constant disturbance force (N) - can be 0, use to test integral control
    F_disturb = 15.0     

    x_init = 0.0
    x_dot_init = 0.0
    x0 = [x_init, x_dot_init]

    # Define an empty response array to fill in the for loop below
    resp = np.zeros((len(t)-1,2))

    pid_output = np.zeros_like(t)
    # Call the ODE solver one step at a time to simulate a "real time" loop
    for ii in range(len(t)-1):    
        PID_force = pid.compute_output(desired, x0[0], t[ii+1], t[ii])
        pid_output[ii] = PID_force # save current value for later plotting
        logging.debug('PID Force in Time loop: {:.4f}'.format(PID_force))
        logging.debug('Current resp: {:.4f}'.format(x0[0]))
        logging.debug('Times {:.4f}, {:.4f}'.format(t[ii], t[ii+1]))
        
        # pack the parameters and call the ode solver
        p = [m, desired, PID_force, F_disturb]
        _, resp[ii,:] = odeint(eq_of_motion, x0, (t[ii], t[ii+1]), args=(p,), atol = abserr, rtol = relerr, hmax=max_step)  
         
        # Update the initial guess for the next time through this loop 
        x0 = resp[ii,:]



    # Plot the results
    # Set the plot size - 3x2 aspect ratio is best
    fig = plt.figure(figsize=(6,4))
    ax = plt.gca()
    plt.subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)

    # Change the axis units to CMUSerif-Roman
    plt.setp(ax.get_ymajorticklabels(),family='CMUSerif-Roman',fontsize=18)
    plt.setp(ax.get_xmajorticklabels(),family='CMUSerif-Roman',fontsize=18)

    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Turn on the plot grid and set appropriate linestyle and color
    ax.grid(True,linestyle=':',color='0.75')
    ax.set_axisbelow(True)

    # Define the X and Y axis labels
    plt.xlabel('Time (s)',family='CMUSerif-Roman',fontsize=22,weight='bold',labelpad=5)
    plt.ylabel('Position (m)',family='CMUSerif-Roman',fontsize=22,weight='bold',labelpad=10)

    plt.plot(t,desired * np.ones_like(t), linewidth=2, linestyle = '--', label=r'Setpoint')
    plt.plot(t[0:-1], resp[:,0], linewidth=2, linestyle='-', label=r'Response')

    # uncomment below and set limits if needed
    # plt.xlim(0,5)
    # plt.ylim(0,10)

    # Create the legend, then fix the fontsize
    leg = plt.legend(loc='upper right', fancybox=True)
    ltext  = leg.get_texts()
    plt.setp(ltext,family='CMUSerif-Roman',fontsize=16)

    # Adjust the page layout filling the page using the new tight_layout command
    plt.tight_layout(pad=0.5)


    # plot the force resulting from the PID controller
    # Set the plot size - 3x2 aspect ratio is best
    fig = plt.figure(figsize=(6,4))
    ax = plt.gca()
    plt.subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)

    # Change the axis units to CMUSerif-Roman
    plt.setp(ax.get_ymajorticklabels(),family='CMUSerif-Roman',fontsize=18)
    plt.setp(ax.get_xmajorticklabels(),family='CMUSerif-Roman',fontsize=18)

    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Turn on the plot grid and set appropriate linestyle and color
    ax.grid(True,linestyle=':',color='0.75')
    ax.set_axisbelow(True)

    # Define the X and Y axis labels
    plt.xlabel('Time (s)',family='CMUSerif-Roman',fontsize=22,weight='bold',labelpad=5)
    plt.ylabel('PID output',family='CMUSerif-Roman',fontsize=22,weight='bold',labelpad=10)

    plt.plot(t, desired * np.ones_like(t), linewidth=2, linestyle = '--', label=r'Setpoint')
    plt.plot(t, pid_output, linewidth=2, linestyle='-', label=r'PID output')

    # uncomment below and set limits if needed
    # plt.xlim(0,5)
    # plt.ylim(0,10)

    # Create the legend, then fix the fontsize
    leg = plt.legend(loc='upper right', fancybox=True)
    ltext  = leg.get_texts()
    plt.setp(ltext,family='CMUSerif-Roman',fontsize=16)

    # Adjust the page layout filling the page using the new tight_layout command
    plt.tight_layout(pad=0.5)

    # save the figure as a high-res pdf in the current folder
#     plt.savefig('plot_filename.pdf')


    # show the figure
    plt.show()