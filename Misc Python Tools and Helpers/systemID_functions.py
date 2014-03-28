#! /usr/bin/env python

##########################################################################################
# systemID_example.py
#
# Script to demonstrate basic time-based system ID
#
# NOTE: Plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 03/28/14
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

import numpy as np
from matplotlib.pyplot import *
import control


def log_dec(peak1,peak2,num_cycles):
    '''##########################################################################################
    # log_dec.py
    #
    # Script to compute damping ratio using log dec method
    #
    # Inputs:
    #   peak1 = the amplitude of the first peak
    #   peak2 = the amplitude of the Nth peak
    #   num_cycles = the number of periods between two peaks
    # 
    # Output:
    #   zeta = the damping ratio
    #
    # NOTE: Plotting is set up for output, not viewing on screen.
    #       So, it will likely be ugly on screen. The saved PDFs should look
    #       better.
    #
    # Created: 03/28/14
    #   - Joshua Vaughan
    #   - joshua.vaughan@louisiana.edu
    #   - http://www.ucs.louisiana.edu/~jev9637
    #
    # Modified:
    #   *
    #
    ######################################################################################
    '''
    import numpy as np

    delta = 1./num_cycles*np.log(peak1 / peak2)

    zeta = 1./np.sqrt(1 + (2 * np.pi/delta)**2)
    
    return zeta
    

def get_local_Extrema(time,data):
    ''' # Function to get the local extrema for a response
    #
    # Inputs:
    #   time = time array corresponding to the data
    #   data = the response data array (only pass a single dimension/state at at time)
    #
    # Output:
    #   localMaxes = the amplitude of the local maxes
    #   localMax_Times = the times of the local maxes
    #
    # Created: 03/28/14
    #   - Joshua Vaughan
    #   - joshua.vaughan@louisiana.edu
    #   - http://www.ucs.louisiana.edu/~jev9637
    ######################################################################################
    '''
    from scipy import signal
    
    # Get local maximums
    localMax_indexes = signal.argrelextrema(data, np.greater)
    localMaxes = data[localMax_indexes]
    localMax_Times = time[localMax_indexes]

    # Get local minimums
    localMin_indexes = signal.argrelextrema(data, np.less)
    localMins = data[localMin_indexes]
    localMin_Times = time[localMin_indexes]
    
    return localMaxes, localMax_Times, localMins, localMin_Times
    

def get_zero_crossings(time,data):
    ''' Function to get the local extrema for a response
    #
    # Inputs:
    #   time = time array corresponding to the data
    #   data = the response data array (only pass a single dimension/state at at time)
    #   
    # Output:
    #   zeros = an array of the times of the zero crossings
    #
    # Created: 03/28/14
    #   - Joshua Vaughan
    #   - joshua.vaughan@louisiana.edu
    #   - http://www.ucs.louisiana.edu/~jev9637
    ######################################################################################
    '''
    
    # create an empty zeros array
    zeros = []
    
    for index in range(len(time)-1):
        if np.sign(data[index]) != np.sign(data[index + 1]):
            zeros.append(time[index])
    
    return zeros


def CRAWLAB_fft(data,time,plotflag):
    ''' Function to get the FFT for a response
    #
    # Inputs:
    #   time = time array corresponding to the data
    #   data = the response data array (only pass a single dimension/state at at time)
    #   plotflag = will plot the FFT if nonzero
    #   
    # Output:
    #   fft_freq = an array of the freqs used in the FFT
    #   fft_mag = an array of the amplitude of the FFT at each freq in fft_freq
    #
    # Created: 03/28/14
    #   - Joshua Vaughan
    #   - joshua.vaughan@louisiana.edu
    #   - http://www.ucs.louisiana.edu/~jev9637
    ######################################################################################
    '''
    
    from scipy.fftpack import fft
    
    # correct for any DC offset
    offset = np.mean(data) 

    # Get the natural frequency
    sample_time = time[1] - time[0]
    n = len(data)

    fft_mag = fft((data - offset)*np.hanning(len(data)))
    fft_freq = np.linspace(0.0, 1.0/(2.0*sample_time), n/2)
    
    if plotflag:
        # Plot the relationshiop
        #   Many of these setting could also be made default by the .matplotlibrc file
        fig = figure(figsize=(6,4))
        ax = gca()
        subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)
        setp(ax.get_ymajorticklabels(),fontsize=18)
        setp(ax.get_xmajorticklabels(),fontsize=18)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.grid(True,linestyle=':',color='0.75')
        ax.set_axisbelow(True)

        xlabel('Frequency (Hz)',fontsize=22,labelpad=8)
        ylabel('FFT magnitude',fontsize=22,labelpad=10)
    
        plot(fft_freq, 2.0/n * np.abs(fft_mag[0:n/2]), linewidth=2, linestyle='-')
        
        # Adjust the page layout filling the page using the new tight_layout command
        tight_layout(pad=0.5)
        show()
    
    # Uncomment below to find and print the frequency at which the highest peak occurs
    freq_index = np.argmax(2.0/n * np.abs(fft_mag[0:n/2]))
    print '\nHighest magnitude peak occurs at: ' + str(fft_freq[freq_index]) + ' Hz.'
    return fft_freq, fft_mag



# ----- Below demonstrates the use of the functions above -------------------------------

# We'll first create a response to look at
m = 1.0                 # kg
k = (2.*np.pi)**2.      # N/m (Selected to give an undamped wn of 1Hz)
wn = np.sqrt(k/m)       # Natural Frequency (rad/s)

z = 0.1                 # Define a desired damping ratio
c = 2*z*wn*m            # calculate the damping coeff. to create it (N/(m/s))


# Define the system to use in simulation - in transfer function form here
num = [1/m]
den = [1,2.*z*wn,wn**2]

sys = control.tf(num,den)


# Set up simulation parameters
t = np.linspace(0,5,500)            # time for simulation, 0-5s with 500 points in-between

F = np.zeros_like(t)

# Define the initial conditions x_dot(0) = 10, x(0) = 0
x0 = [10.,0.]

# run the simulation - utilize the built-in initial condition response function
[T,yout] = control.initial_response(sys,t,x0)


# Should return the zero crossings
zeros = get_zero_crossings(T,yout)

# Get the peaks of the response
localMaxes, localMax_Times, localMins, localMin_Times = get_local_Extrema(T,yout)

# Calculate the damping ratio from both the local maxes and the local minimums
zeta_maxes = log_dec(localMaxes[0],localMaxes[-1],len(localMaxes)-1)
zeta_mins = log_dec(localMins[0],localMins[-1],len(localMins)-1)



# Let's plot our results
# Set the plot size - 3x2 aspect ratio is best
fig = figure(figsize=(6,4))
ax = gca()
subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)

# Change the axis units to CMU Serif
setp(ax.get_ymajorticklabels(),family='CMU Serif',fontsize=18)
setp(ax.get_xmajorticklabels(),family='CMU Serif',fontsize=18)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Turn on the plot grid and set appropriate linestyle and color
ax.grid(True,linestyle=':',color='0.75')
ax.set_axisbelow(True)

# Define the X and Y axis labels
xlabel('Time (s)',family='CMU Serif',fontsize=22,weight='bold',labelpad=5)
ylabel('Position (m)',family='CMU Serif',fontsize=22,weight='bold',labelpad=10)

plot(T, yout , linewidth=2,linestyle="-",label=r'Response')
plot(zeros,np.zeros_like(zeros),'o', markersize = 8, label=r'Zero Crossings')
plot(localMax_Times, localMaxes, 'v', markersize = 8, label=r'Local Maxes')
plot(localMin_Times, localMins, '^', markersize = 8, label=r'Local Mins')

# uncomment below and set limits if needed
# xlim(0,5)
ylim(-1.5,2)

# # Create the legend, then fix the fontsize
leg = legend(loc='upper right', ncol = 1, fancybox=True)
ltext  = leg.get_texts()
setp(ltext,family='CMU Serif',fontsize=16)

# Adjust the page layout filling the page using the new tight_layout command
tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
#savefig('plot_filename.pdf',dpi=600)

# show the figure
show()



#-----  We can also use the FFT to get the frequency ------------------------------------
freq, mag = CRAWLAB_fft(yout,T,True)
    

